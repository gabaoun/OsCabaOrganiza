import argparse
import sys
import time
from pathlib import Path
from typing import Optional
from tkinter import Tk, filedialog

from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.live import Live

from .core import Organizer
from .utils import load_config, setup_logger, console, print_banner, get_app_path

def get_directory_gui() -> Optional[Path]:
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory(title="Selecione o diretório para organizar")
    root.destroy()
    return Path(path) if path else None

def show_report(organizer: Organizer, duration: float):
    """Exibe relatório final colorido."""
    table = Table(title="Relatório de Organização")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="magenta")
    
    table.add_row("Arquivos Movidos", str(organizer.stats["moved"]))
    table.add_row("Erros", str(organizer.stats["errors"]))
    
    # Formatação de bytes
    bytes_val = organizer.stats["bytes"]
    if bytes_val > 1024 * 1024:
        size_str = f"{bytes_val / (1024*1024):.2f} MB"
    else:
        size_str = f"{bytes_val / 1024:.2f} KB"
        
    table.add_row("Volume Processado", size_str)
    table.add_row("Tempo Decorrido", f"{duration:.2f}s")
    
    console.print(table)

def run_organization_with_progress(organizer: Organizer, directory: Path, mode: str, recursive: bool, remove_empty: bool):
    """Executa a organização com barra de progresso."""
    
    # Contagem prévia (rápida) para definir o total da barra
    with console.status("[bold green]Analisando arquivos..."):
        total_files = len(list(organizer._get_files(directory, recursive)))
    
    if total_files == 0:
        console.print("[yellow]Nenhum arquivo para organizar.[/yellow]")
        return

    start_time = time.time()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("[green]Organizando...", total=total_files)
        
        # Callback simples para avançar a barra
        def update_bar():
            progress.advance(task)

        if mode == 'ext':
            organizer.organize_by_extension(directory, recursive, remove_empty, progress_callback=update_bar)
        elif mode == 'date':
            organizer.organize_by_date(directory, recursive, remove_empty, progress_callback=update_bar)

    end_time = time.time()
    show_report(organizer, end_time - start_time)

def main():
    parser = argparse.ArgumentParser(description="OsCabaOrganiza - Organizador Profissional")
    parser.add_argument("--path", type=str, help="Caminho do diretório")
    args = parser.parse_args()
    
    # Setup
    # No modo interativo, o logger do utils já silencia o output padrão para não quebrar a UI
    logger = setup_logger(verbose=False)
    config = load_config()
    organizer = Organizer(config)
    
    if args.path:
        # Modo CLI simples (sem UI rica por enquanto, mantendo compatibilidade básica)
        target = Path(args.path)
        organizer.organize_by_extension(target)
        return

    # Modo Interativo Rico
    print_banner()
    
    target_dir = get_directory_gui()
    if not target_dir:
        console.print("[red]Nenhum diretório selecionado.[/red]")
        return

    while True:
        console.print(Panel.fit(f"[bold blue]Alvo:[/bold blue] {target_dir}", border_style="blue"))
        
        console.print("\n[bold]Menu Principal[/bold]")
        console.print("1. [cyan]Organizar por Extensão[/cyan]")
        console.print("2. [cyan]Organizar por Data[/cyan]")
        console.print("3. [yellow]Modo Sentinel (Monitoramento)[/yellow]")
        console.print("4. [magenta]Desfazer (Undo)[/magenta]")
        console.print("5. [red]Sair[/red]")
        
        choice = Prompt.ask("Escolha uma opção", choices=["1", "2", "3", "4", "5"])
        
        if choice == '5':
            console.print("[green]Até logo![/green]")
            break
            
        elif choice in ['1', '2']:
            recursive = Confirm.ask("Incluir subpastas (Recursivo)?")
            remove_empty = Confirm.ask("Remover pastas vazias ao final?")
            dry_run = Confirm.ask("Apenas simular (Dry Run)?")
            
            organizer.dry_run = dry_run
            mode = 'ext' if choice == '1' else 'date'
            
            run_organization_with_progress(organizer, target_dir, mode, recursive, remove_empty)
            
        elif choice == '3':
            console.print("[bold yellow]Iniciando Modo Sentinel...[/bold yellow]")
            console.print("O programa ficará monitorando a pasta. Pressione [bold red]ESC[/bold red] para parar.")
            organizer.start_sentinel(target_dir)
            console.print("[yellow]Sentinel encerrado.[/yellow]")
            
        elif choice == '4':
            if Confirm.ask("Deseja desfazer a última organização nesta pasta?"):
                with console.status("[bold red]Revertendo alterações..."):
                    results = organizer.undo_operation(target_dir)
                
                if not results:
                    console.print("[yellow]Nada para desfazer ou histórico não encontrado.[/yellow]")
                else:
                    console.print(f"[green]Revertidos {len(results)} arquivos.[/green]")

if __name__ == "__main__":
    main()