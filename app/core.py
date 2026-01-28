import shutil
import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from .utils import setup_logger, check_esc_pressed, flush_input

logger = setup_logger()

# Tenta importar watchdog, mas não falha se não estiver disponível
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

class UndoManager:
    """Gerencia o histórico de operações para permitir desfazer."""
    def __init__(self, history_file: Path):
        self.history_file = history_file
        self.history: List[Dict] = []
        self._load_history()

    def _load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def register_move(self, src: str, dst: str):
        """Registra uma movimentação."""
        self.history.append({
            "action": "move",
            "src": src,
            "dst": dst,
            "timestamp": datetime.now().isoformat()
        })
        self._save_history()

    def _save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass

    def undo_last_session(self) -> List[str]:
        """Desfaz as operações registradas e limpa o histórico."""
        results = []
        # Processa do último para o primeiro (LIFO)
        for entry in reversed(self.history):
            if entry["action"] == "move":
                src = Path(entry["src"]) # Onde estava originalmente
                dst = Path(entry["dst"]) # Onde está agora

                if dst.exists():
                    try:
                        # Garante que a pasta original exista
                        src.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Evita sobrescrever se algo foi criado no lugar do original
                        target = src
                        counter = 1
                        while target.exists():
                            target = src.parent / f"{src.stem}_restored_{counter}{src.suffix}"
                            counter += 1
                        
                        shutil.move(str(dst), str(target))
                        results.append(f"Restaurado: {dst.name} -> {target}")
                        
                        # Remove pasta de destino se ficou vazia
                        try:
                            dst.parent.rmdir()
                        except OSError:
                            pass
                    except Exception as e:
                        results.append(f"Erro ao restaurar {dst.name}: {e}")
                else:
                    results.append(f"Arquivo não encontrado para restaurar: {dst}")
        
        # Limpa o histórico após desfazer
        self.history = []
        if self.history_file.exists():
            os.remove(self.history_file)
            
        return results

class SentinelHandler(FileSystemEventHandler):
    """Manipulador de eventos do Watchdog."""
    def __init__(self, organizer_instance, directory: Path):
        self.organizer = organizer_instance
        self.directory = directory

    def on_created(self, event):
        if event.is_directory:
            return
        
        # Aguarda um pouco para garantir que o arquivo foi escrito
        time.sleep(1)
        
        file_path = Path(event.src_path)
        # Ignora arquivos temporários ou do próprio sistema
        if file_path.name == "undo_log.json" or file_path.name.startswith('.'):
            return

        # Chama a organização para este arquivo específico
        # Nota: Chamamos direto, sem thread pool aqui para simplificar
        # em um cenário real, poderia ser enfileirado.
        self.organizer.process_single_file_event(file_path, self.directory)

class Organizer:
    def __init__(self, config: Dict, dry_run: bool = False):
        self.config = config
        self.others_folder = config.get("others_folder", "Outros")
        self.dry_run = dry_run
        self.lock = Lock()
        
        # Lookup O(1)
        self.extension_lookup: Dict[str, str] = {}
        for folder, extensions in config.get("extensions", {}).items():
            for ext in extensions:
                self.extension_lookup[ext.lower()] = folder

        # Undo Manager será inicializado quando soubermos o diretório alvo
        self.undo_manager: Optional[UndoManager] = None
        
        # Estatísticas para relatório
        self.stats = {"moved": 0, "errors": 0, "bytes": 0}

    def _find_folder(self, extension: str) -> str:
        return self.extension_lookup.get(extension.lower(), self.others_folder)

    def _move_single_file(self, file_path: Path, folder_name: str, base_directory: Path) -> str:
        """Move arquivo, atualiza stats e registra undo."""
        if file_path.name.startswith('.') or file_path.name == "undo_log.json":
            return f"Ignorado: {file_path.name}"

        try:
            target_folder = base_directory / folder_name
            file_size = file_path.stat().st_size

            if not self.dry_run:
                target_folder.mkdir(parents=True, exist_ok=True)

            with self.lock:
                destination_path = target_folder / file_path.name
                counter = 1
                while destination_path.exists():
                    destination_path = target_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
                    counter += 1

            if self.dry_run:
                return f"[SIMULAÇÃO] Moveria: '{file_path.name}'"
            
            # Executa Mover
            src_str = str(file_path.resolve())
            dst_str = str(destination_path.resolve())
            
            shutil.move(src_str, dst_str)
            
            # Registra no Undo e Stats
            if self.undo_manager:
                self.undo_manager.register_move(src_str, dst_str)
            
            with self.lock:
                self.stats["moved"] += 1
                self.stats["bytes"] += file_size
                
            return f"Sucesso: {file_path.name}"
            
        except Exception as e:
            with self.lock:
                self.stats["errors"] += 1
            return f"ERRO: {str(e)}"

    def process_single_file_event(self, file_path: Path, base_directory: Path):
        """Processa um único arquivo (usado pelo Sentinel)."""
        if not file_path.exists():
            return
            
        folder = self._find_folder(file_path.suffix)
        res = self._move_single_file(file_path, folder, base_directory)
        # Em modo Sentinel, imprimimos direto no log ou console se possível
        if "Sucesso" in res:
            logger.info(f"[Sentinel] {res}")

    def _get_files(self, directory: Path, recursive: bool):
        iterator = directory.rglob('*') if recursive else directory.iterdir()
        for f in iterator:
            if f.is_file() and f.name != "main.py" and f.name != "undo_log.json":
                yield f

    def organize_by_extension(self, directory: Path, recursive: bool = False, remove_empty: bool = False, progress_callback: Callable = None) -> None:
        self.undo_manager = UndoManager(directory / "undo_log.json")
        self.stats = {"moved": 0, "errors": 0, "bytes": 0} # Reset stats
        
        files = list(self._get_files(directory, recursive))
        if not files:
            return

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                folder = self._find_folder(file_path.suffix)
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            for future in futures:
                if check_esc_pressed():
                    executor.shutdown(wait=False, cancel_futures=True)
                    return

                res = future.result()
                if progress_callback:
                    progress_callback()

        if remove_empty:
            self._remove_empty_folders(directory)

    def organize_by_date(self, directory: Path, recursive: bool = False, remove_empty: bool = False, progress_callback: Callable = None) -> None:
        self.undo_manager = UndoManager(directory / "undo_log.json")
        self.stats = {"moved": 0, "errors": 0, "bytes": 0}

        files = list(self._get_files(directory, recursive))
        if not files:
            return

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                created_at = datetime.fromtimestamp(file_path.stat().st_ctime)
                folder = created_at.strftime('%d-%m-%Y')
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            for future in futures:
                if check_esc_pressed():
                    executor.shutdown(wait=False, cancel_futures=True)
                    return

                res = future.result()
                if progress_callback:
                    progress_callback()

        if remove_empty:
            self._remove_empty_folders(directory)

    def _remove_empty_folders(self, directory: Path):
        if self.dry_run:
            return
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in dirs:
                path = Path(root) / name
                try:
                    path.rmdir()
                except OSError:
                    pass

    def start_sentinel(self, directory: Path):
        """Inicia o modo de monitoramento contínuo."""
        if not HAS_WATCHDOG:
            logger.error("Biblioteca 'watchdog' não instalada.")
            return

        self.undo_manager = UndoManager(directory / "undo_log.json")
        event_handler = SentinelHandler(self, directory)
        observer = Observer()
        observer.schedule(event_handler, str(directory), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
                if check_esc_pressed():
                    break
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()

    def undo_operation(self, directory: Path) -> List[str]:
        """Wrapper para o undo manager."""
        mgr = UndoManager(directory / "undo_log.json")
        return mgr.undo_last_session()