import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
from .utils import setup_logger

logger = setup_logger()

class Organizer:
    def __init__(self, config: Dict, dry_run: bool = False):
        self.extensions_map = config.get("extensions", {})
        self.others_folder = config.get("others_folder", "Outros")
        self.dry_run = dry_run

    def _find_folder(self, extension: str) -> str:
        """Encontra a pasta correta baseada na extensão."""
        for folder, extensions in self.extensions_map.items():
            if extension in extensions:
                return folder
        return self.others_folder

    def _move_single_file(self, file_path: Path, folder_name: str, base_directory: Path) -> str:
        """
        Move um único arquivo. Função thread-safe (isolada).
        Retorna uma mensagem de status.
        """
        try:
            target_folder = base_directory / folder_name
            
            # Cria pasta (se não for simulação)
            if not self.dry_run:
                target_folder.mkdir(parents=True, exist_ok=True)

            destination_path = target_folder / file_path.name

            # Tratamento de duplicatas
            counter = 1
            # Nota: Em dry_run, check de existência pode falhar se a pasta não existe ainda,
            # mas assumimos o estado atual do disco.
            while destination_path.exists():
                destination_path = target_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1

            if self.dry_run:
                return f"[SIMULAÇÃO] Moveria: '{file_path.name}' -> '{folder_name}/{destination_path.name}'"
            
            shutil.move(str(file_path), str(destination_path))
            return f"Sucesso: '{file_path.name}' -> '{folder_name}/{destination_path.name}'"
            
        except Exception as e:
            return f"ERRO ao mover '{file_path.name}': {str(e)}"

    def organize_by_extension(self, directory: Path) -> None:
        """Organiza arquivos usando Threads para performance."""
        files = [f for f in directory.iterdir() if f.is_file() and f.name != "main.py"]
        
        if not files:
            logger.info("Nenhum arquivo para organizar.")
            return

        logger.info(f"Iniciando organização de {len(files)} arquivos (Por Extensão)...")
        
        # Processamento Paralelo
        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                folder = self._find_folder(file_path.suffix.lower())
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            # Coletar resultados
            for future in futures:
                logger.info(future.result())

    def organize_by_date(self, directory: Path) -> None:
        """Organiza arquivos por data de criação usando Threads."""
        files = [f for f in directory.iterdir() if f.is_file() and f.name != "main.py"]
        
        if not files:
            logger.info("Nenhum arquivo para organizar.")
            return

        logger.info(f"Iniciando organização de {len(files)} arquivos (Por Data)...")

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                created_at = datetime.fromtimestamp(file_path.stat().st_ctime)
                folder = created_at.strftime('%d-%m-%Y')
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            for future in futures:
                logger.info(future.result())
