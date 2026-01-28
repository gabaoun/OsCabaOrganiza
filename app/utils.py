import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console

# Instância global do Console do Rich para UI avançada
console = Console()

# Dependências de UI/Sistema
try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    from colorama import init
    init(autoreset=True)
except ImportError:
    init = lambda **kwargs: None

def check_esc_pressed() -> bool:
    """Verifica se ESC foi pressionado (Apenas Windows)."""
    if msvcrt and msvcrt.kbhit():
        ch = msvcrt.getch()
        if ch == b'\x1b':
            return True
    return False

def flush_input():
    """Limpa o buffer de entrada (Apenas Windows)."""
    if msvcrt:
        while msvcrt.kbhit():
            msvcrt.getch()

def setup_logger(verbose: bool = False) -> logging.Logger:
    logger = logging.getLogger("OsCabaOrganiza")
    if logger.hasHandlers():
        logger.handlers.clear()

    # Em produção com Rich, preferimos não sujar o terminal com logs crus,
    # a menos que seja verbose.
    if verbose:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL) # Silencia logs normais para dar lugar à UI
    
    return logger

def get_app_path() -> Path:
    """Retorna o diretório base da aplicação (compatível com PyInstaller)."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent

def load_config(config_name: str = "config.json") -> Dict[str, Any]:
    """Carrega as configurações."""
    base_path = get_app_path()
    path = base_path / config_name

    default_config = {
        "extensions": {},
        "others_folder": "Outros"
    }
    
    if not path.exists():
        cwd_path = Path.cwd() / config_name
        if cwd_path.exists():
            path = cwd_path
        else:
            return default_config
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        if "extensions" in config:
            normalized_extensions = {}
            for folder, exts in config["extensions"].items():
                normalized_extensions[folder] = [ext.lower() for ext in exts]
            config["extensions"] = normalized_extensions
            
        return config
    except Exception as e:
        console.print(f"[red]Erro ao ler {config_name}: {e}[/red]")
        return default_config

from rich.panel import Panel

def print_banner():
    """Imprime o banner ASCII art estilizado."""
    banner_text = r"""
   ____       ____      _            
  / __ \___  / __/__ __| |_  ___     
 / /_/ (_-< / _// _ `/ _ \/ _ `/     
 \____/___/_\__/\_,_/_.__/\_,_/      
      Organiza v2.0 - Profissional
    """
    console.print(Panel(banner_text, style="cyan", expand=False))
    console.print("[bold green]Bem-vindo ao Organizador de Arquivos Supremo![/bold green]", justify="left")
