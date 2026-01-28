import argparse
import sys
from pathlib import Path
from tkinter import Tk, filedialog
from .core import Organizer
from .utils import load_config, setup_logger

def get_directory_gui() -> Optional[Path]:
    """Abre janela para selecionar diretório."""
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory(title="Selecione o diretório para organizar")
    return Path(path) if path else None

def main():
    # Configuração de Argumentos da Linha de Comando
    parser = argparse.ArgumentParser(description="OsCabaOrganiza - Organizador de Arquivos Profissional")
    parser.add_argument("--path", type=str, help="Caminho do diretório a ser organizado")
    parser.add_argument("--mode", choices=['ext', 'date'], help="Modo de organização: 'ext' (Extensão) ou 'date' (Data)")
    parser.add_argument("--dry-run", action="store_true", help="Simula a organização sem mover arquivos")
    parser.add_argument("--verbose", action="store_true", help="Mostra logs detalhados")
    
    args = parser.parse_args()
    
    # Configuração
    logger = setup_logger(args.verbose)
    config = load_config()
    organizer = Organizer(config, dry_run=args.dry_run)
    
    target_dir = None

    # Lógica de Decisão: CLI vs Interativo
    if args.path:
        target_dir = Path(args.path)
        if not target_dir.exists():
            logger.error("Diretório especificado não existe.")
            return
            
        if not args.mode:
            logger.error("No modo CLI, você deve especificar --mode 'ext' ou 'date'.")
            return

        if args.mode == 'ext':
            organizer.organize_by_extension(target_dir)
        elif args.mode == 'date':
            organizer.organize_by_date(target_dir)
            
    else:
        # Modo Interativo (sem argumentos)
        print("--- OsCabaOrganiza (Modo Interativo) ---")
        target_dir = get_directory_gui()
        
        if not target_dir:
            logger.warning("Nenhum diretório selecionado.")
            return

        while True:
            print(f"\nDiretório: {target_dir}")
            print("1. Organizar por Extensão")
            print("2. Organizar por Data")
            print("3. Sair")
            
            choice = input("Opção: ").strip()
            
            # Pergunta de simulação no modo interativo
            is_dry = False
            if choice in ['1', '2']:
                 sim = input("Apenas simular (Dry Run)? [s/N]: ").strip().lower()
                 if sim == 's':
                     organizer.dry_run = True
                     is_dry = True
                 else:
                     organizer.dry_run = False

            if choice == '1':
                organizer.organize_by_extension(target_dir)
            elif choice == '2':
                organizer.organize_by_date(target_dir)
            elif choice == '3':
                break
            
            if is_dry:
                print("\n[INFO] Isso foi apenas uma simulação.")

if __name__ == "__main__":
    main()
