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
    path = filedialog.askdirectory(title="Select directory to organize")
    root.destroy()
    return Path(path) if path else None

def show_report(organizer: Organizer, duration: float):
    """Displays colored final report."""
    table = Table(title="Organization Report")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Files Moved", str(organizer.stats["moved"]))
    table.add_row("Files Decompressed", str(organizer.stats.get("extracted", 0)))
    table.add_row("Errors", str(organizer.stats["errors"]))
    
    # Byte formatting
    bytes_val = organizer.stats["bytes"]
    if bytes_val > 1024 * 1024:
        size_str = f"{bytes_val / (1024*1024):.2f} MB"
    else:
        size_str = f"{bytes_val / 1024:.2f} KB"
        
    table.add_row("Processed Volume", size_str)
    table.add_row("Time Elapsed", f"{duration:.2f}s")
    
    console.print(table)

def run_organization_with_progress(organizer: Organizer, directory: Path, mode: str, recursive: bool, remove_empty: bool):
    """Executes organization with progress bar."""
    
    # Pre-count (fast) to define bar total
    with console.status("[bold green]Analyzing files..."):
        all_files = list(organizer._get_files(directory, recursive))
        if mode == 'decompress':
            # Filter only compatible archive files
            exts = set(organizer._get_archive_extensions())
            total_files = sum(1 for f in all_files if f.suffix in exts or ''.join(f.suffixes) in exts)
        else:
            total_files = len(all_files)
    
    if total_files == 0:
        msg = "No compressed files found." if mode == 'decompress' else "No files to organize."
        console.print(f"[yellow]{msg}[/yellow]")
        return

    start_time = time.time()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        action_text = "Decompressing..." if mode == 'decompress' else "Organizing..."
        task = progress.add_task(f"[green]{action_text}", total=total_files)
        
        # Simple callback to advance bar
        def update_bar():
            progress.advance(task)

        if mode == 'ext':
            organizer.organize_by_extension(directory, recursive, remove_empty, progress_callback=update_bar)
        elif mode == 'date':
            organizer.organize_by_date(directory, recursive, remove_empty, progress_callback=update_bar)
        elif mode == 'decompress':
            organizer.decompress_files(directory, recursive, progress_callback=update_bar)

    end_time = time.time()
    show_report(organizer, end_time - start_time)

def main():
    parser = argparse.ArgumentParser(description="OsCabaOrganiza - Professional Organizer")
    parser.add_argument("--path", type=str, help="Directory path")
    args = parser.parse_args()
    
    # Setup
    logger = setup_logger(verbose=False)
    config = load_config()
    organizer = Organizer(config)
    
    if args.path:
        # Simple CLI mode
        target = Path(args.path)
        organizer.organize_by_extension(target)
        return

    # Rich Interactive Mode
    print_banner()
    
    target_dir = get_directory_gui()
    if not target_dir:
        console.print("[red]No directory selected.[/red]")
        return

    while True:
        console.print(Panel.fit(f"[bold blue]Target:[/bold blue] {target_dir}", border_style="blue"))
        
        console.print("\n[bold]Main Menu[/bold]")
        console.print("1. [cyan]Organize by Extension[/cyan]")
        console.print("2. [cyan]Organize by Date[/cyan]")
        console.print("3. [cyan]Batch Decompress[/cyan]")
        console.print("4. [yellow]Sentinel Mode (Monitoring)[/yellow]")
        console.print("5. [magenta]Undo[/magenta]")
        console.print("6. [red]Exit[/red]")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == '6':
            console.print("[green]See you later![/green]")
            break
            
        elif choice in ['1', '2', '3']:
            recursive = Confirm.ask("Include subfolders (Recursive)?")
            
            remove_empty = False
            if choice != '3':
                remove_empty = Confirm.ask("Remove empty folders at the end?")
                
            dry_run = Confirm.ask("Simulate only (Dry Run)?")
            
            organizer.dry_run = dry_run
            
            mode = 'ext'
            if choice == '2': mode = 'date'
            elif choice == '3': mode = 'decompress'
            
            run_organization_with_progress(organizer, target_dir, mode, recursive, remove_empty)
            
        elif choice == '4':
            console.print("[bold yellow]Starting Sentinel Mode...[/bold yellow]")
            console.print("Monitoring directory. Press [bold red]ESC[/bold red] to stop.")
            organizer.start_sentinel(target_dir)
            console.print("[yellow]Sentinel stopped.[/yellow]")
            
        elif choice == '5':
            if Confirm.ask("Undo last organization in this folder?"):
                with console.status("[bold red]Reverting changes..."):
                    results = organizer.undo_operation(target_dir)
                
                if not results:
                    console.print("[yellow]Nothing to undo or history not found.[/yellow]")
                else:
                    console.print(f"[green]Reverted {len(results)} files.[/green]")

if __name__ == "__main__":
    main()