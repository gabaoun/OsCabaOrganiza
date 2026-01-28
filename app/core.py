import shutil
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from .utils import setup_logger

logger = setup_logger()

class Organizer:
    def __init__(self, config: Dict, dry_run: bool = False):
        self.extensions_map = config.get("extensions", {})
        self.others_folder = config.get("others_folder", "Outros")
        self.dry_run = dry_run
        self.lock = Lock()  # Previne colisão de nomes entre threads

    def _find_folder(self, extension: str) -> str:
        """Encontra a pasta correta baseada na extensão."""
        for folder, extensions in self.extensions_map.items():
            if extension in extensions:
                return folder
        return self.others_folder

    def _move_single_file(self, file_path: Path, folder_name: str, base_directory: Path) -> str:
        """
        Move um único arquivo. Thread-safe.
        """
        # Ignora arquivos ocultos/sistema
        if file_path.name.startswith('.'):
            return f"Ignorado (Oculto): '{file_path.name}'"

        try:
            target_folder = base_directory / folder_name
            
            if not self.dry_run:
                target_folder.mkdir(parents=True, exist_ok=True)

            # --- SEÇÃO CRÍTICA (Thread Safe) ---
            # Usamos Lock aqui para garantir que duas threads não gerem o mesmo nome
            # de arquivo simultaneamente (ex: foto_1.jpg)
            with self.lock:
                destination_path = target_folder / file_path.name
                counter = 1
                while destination_path.exists():
                    destination_path = target_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
                    counter += 1
            # --- FIM DA SEÇÃO CRÍTICA ---

            if self.dry_run:
                return f"[SIMULAÇÃO] Moveria: '{file_path.name}' -> '{folder_name}/{destination_path.name}'"
            
            shutil.move(str(file_path), str(destination_path))
            return f"Sucesso: '{file_path.name}' -> '{folder_name}/{destination_path.name}'"
            
        except Exception as e:
            return f"ERRO ao mover '{file_path.name}': {str(e)}"

    def _remove_empty_folders(self, directory: Path):
        """Remove pastas vazias recursivamente."""
        if self.dry_run:
            return

        # Caminha de baixo para cima (bottom-up) para remover subpastas aninhadas
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in dirs:
                path = Path(root) / name
                try:
                    # rmdir só funciona se a pasta estiver vazia
                    path.rmdir()
                    logger.info(f"Pasta vazia removida: {path}")
                except OSError:
                    pass # Pasta não estava vazia

    def _get_files(self, directory: Path, recursive: bool):
        """Gerador de arquivos (iterdir ou rglob)."""
        if recursive:
            return directory.rglob('*')
        return directory.iterdir()

    def organize_by_extension(self, directory: Path, recursive: bool = False, remove_empty: bool = False) -> None:
        """Organiza arquivos por extensão."""
        # Filtra apenas arquivos e ignora o próprio script main.py se estiver lá
        files = [f for f in self._get_files(directory, recursive) 
                 if f.is_file() and f.name != "main.py"]
        
        if not files:
            logger.info("Nenhum arquivo para organizar.")
            return

        logger.info(f"Iniciando organização de {len(files)} arquivos (Recursivo: {recursive})...")
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                folder = self._find_folder(file_path.suffix.lower())
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            for future in futures:
                res = future.result()
                if "ERRO" in res:
                    logger.error(res)
                elif "Ignorado" not in res: # Reduz verbosidade de arquivos ocultos
                    logger.info(res)

        if remove_empty:
            logger.info("Limpando pastas vazias...")
            self._remove_empty_folders(directory)

    def organize_by_date(self, directory: Path, recursive: bool = False, remove_empty: bool = False) -> None:
        """Organiza arquivos por data."""
        files = [f for f in self._get_files(directory, recursive) 
                 if f.is_file() and f.name != "main.py"]
        
        if not files:
            logger.info("Nenhum arquivo para organizar.")
            return

        logger.info(f"Iniciando organização de {len(files)} arquivos (Recursivo: {recursive})...")

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                created_at = datetime.fromtimestamp(file_path.stat().st_ctime)
                folder = created_at.strftime('%d-%m-%Y')
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            for future in futures:
                res = future.result()
                if "ERRO" in res:
                    logger.error(res)
                else:
                    logger.info(res)

        if remove_empty:
            logger.info("Limpando pastas vazias...")
            self._remove_empty_folders(directory)
