import shutil
import logging
from pathlib import Path
from datetime import datetime
from tkinter import Tk, filedialog
from typing import Dict, List

# Configuração de Logging
# Isso permite que vejamos o que está acontecendo com timestamps e níveis de severidade
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def create_default_extensions_map() -> Dict[str, List[str]]:
    """Retorna o mapa padrão de extensões para pastas."""
    return {
        'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
        'Documentos': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.csv', '.md'],
        'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'],
        'Musicas': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
        'Arquivos Compactados': ['.zip', '.rar', '.7z', '.tar.gz', '.iso'],
        'Scripts': ['.py', '.js', '.html', '.css', '.json', '.java', '.cpp'],
        'Aplicativos': ['.exe', '.msi', '.dmg', '.sh', '.bat'],
        'Fontes': ['.ttf', '.otf'],
    }

def find_folder_by_extension(extension: str, extensions_map: Dict[str, List[str]]) -> str:
    """
    Encontra o nome da pasta com base na extensão do arquivo.
    Retorna 'Others' se não encontrar correspondência.
    """
    for folder, extensions in extensions_map.items():
        if extension in extensions:
            return folder
    return 'Others'

def move_file(file_path: Path, folder_name: str, base_directory: Path, dry_run: bool = False) -> None:
    """
    Move um arquivo para a pasta especificada.
    
    Args:
        file_path (Path): O caminho do arquivo original.
        folder_name (str): O nome da pasta de destino.
        base_directory (Path): O diretório base onde a pasta será criada.
        dry_run (bool): Se True, apenas simula a ação (log) sem mover de fato.
    """
    target_folder = base_directory / folder_name
    
    # Lógica de Simulação (Dry Run)
    if not dry_run:
        try:
            target_folder.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.error(f"Erro ao criar pasta {target_folder}: {e}")
            return

    destination_path = target_folder / file_path.name

    # Trata duplicatas adicionando um contador (ex: arquivo_1.txt)
    # Nota: Em dry_run, a verificação de existência é baseada no estado atual do disco.
    counter = 1
    while destination_path.exists():
        destination_path = target_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1

    try:
        if dry_run:
            logger.info(f"[SIMULAÇÃO] Moveria: '{file_path.name}' -> '{folder_name}/{destination_path.name}'")
        else:
            shutil.move(str(file_path), str(destination_path))
            logger.info(f"Sucesso: '{file_path.name}' -> '{folder_name}/{destination_path.name}'")
    except Exception as e:
        logger.error(f"Erro ao mover '{file_path.name}': {e}")

def organize_files_by_extension(directory: Path, dry_run: bool = False) -> None:
    """Organiza os arquivos no diretório agrupando por extensão."""
    extensions_map = create_default_extensions_map()
    
    logger.info(f"Iniciando organização por extensão... (Modo: {'SIMULAÇÃO' if dry_run else 'REAL'})")
    
    for item_path in directory.iterdir():
        # Ignora diretórios e o próprio script
        if item_path.is_file() and item_path.name != Path(__file__).name:
            extension = item_path.suffix.lower()
            folder_name = find_folder_by_extension(extension, extensions_map)
            move_file(item_path, folder_name, directory, dry_run=dry_run)

def organize_files_by_creation_date(directory: Path, dry_run: bool = False) -> None:
    """Organiza os arquivos no diretório agrupando por data de criação."""
    
    logger.info(f"Iniciando organização por data... (Modo: {'SIMULAÇÃO' if dry_run else 'REAL'})")

    for item_path in directory.iterdir():
        if item_path.is_file() and item_path.name != Path(__file__).name:
            # Obtém a data de criação
            created_at = datetime.fromtimestamp(item_path.stat().st_ctime)
            folder_name = created_at.strftime('%d-%m-%Y')
            move_file(item_path, folder_name, directory, dry_run=dry_run)

def main():
    root = Tk()
    root.withdraw() # Oculta a janela principal do Tkinter
    
    print("--- OsCabaOrganiza: Organizador de Arquivos Profissional ---")
    print("Selecione o diretório na janela que irá abrir...")
    
    selected_dir = filedialog.askdirectory(title="Selecione o diretório para organizar")
    
    if not selected_dir:
        logger.warning("Nenhum diretório selecionado. Encerrando.")
        return

    directory_path = Path(selected_dir)
    logger.info(f"Diretório selecionado: {directory_path}")

    while True:
        print("\nEscolha uma opção:")
        print("1. Organizar por Extensão")
        print("2. Organizar por Data de Criação")
        print("3. Sair")
        
        choice = input("Digite o número da opção: ").strip()
        
        if choice == '3':
            logger.info("Encerrando o programa.")
            break
            
        if choice in ['1', '2']:
            # Pergunta sobre o modo Dry Run
            sim_input = input("Deseja apenas SIMULAR (sem mover arquivos)? (s/n) [s]: ").strip().lower()
            is_dry_run = sim_input != 'n'  # Default é Sim (segurança primeiro)
            
            if choice == '1':
                organize_files_by_extension(directory_path, dry_run=is_dry_run)
            elif choice == '2':
                organize_files_by_creation_date(directory_path, dry_run=is_dry_run)
                
            if is_dry_run:
                print("\n--- Fim da Simulação. Nenhum arquivo foi movido. ---")
            else:
                print("\n--- Organização Concluída! ---")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()