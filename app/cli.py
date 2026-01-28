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
    parser.add_argument("--recursive", action="store_true", help="Organiza também subpastas (Recursivo)")
    parser.add_argument("--remove-empty", action="store_true", help="Remove pastas vazias após organizar")
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
            organizer.organize_by_extension(target_dir, recursive=args.recursive, remove_empty=args.remove_empty)
        elif args.mode == 'date':
            organizer.organize_by_date(target_dir, recursive=args.recursive, remove_empty=args.remove_empty)
            
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
            
            if choice == '3':
                break

            if choice in ['1', '2']:
                # Perguntas Interativas
                rec_input = input("Incluir subpastas (Recursivo)? [s/N]: ").strip().lower()
                is_recursive = rec_input == 's'
                
                clean_input = input("Remover pastas vazias ao final? [s/N]: ").strip().lower()
                is_remove_empty = clean_input == 's'

                sim_input = input("Apenas simular (Dry Run)? [s/N]: ").strip().lower()
                is_dry_run = sim_input == 's'
                organizer.dry_run = is_dry_run

                if choice == '1':
                    organizer.organize_by_extension(target_dir, recursive=is_recursive, remove_empty=is_remove_empty)
                elif choice == '2':
                    organizer.organize_by_date(target_dir, recursive=is_recursive, remove_empty=is_remove_empty)
                
                if is_dry_run:
                    print("\n[INFO] Isso foi apenas uma simulação.")

if __name__ == "__main__":
    main()
