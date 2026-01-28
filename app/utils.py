import json
import logging
from pathlib import Path
from typing import Dict, List, Any

# Configuração de Logging Centralizada
def setup_logger(verbose: bool = False) -> logging.Logger:
    logger = logging.getLogger("OsCabaOrganiza")
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Carrega as configurações do arquivo JSON. Se falhar, retorna padrão."""
    path = Path(config_path)
    default_config = {
        "extensions": {},
        "others_folder": "Outros"
    }
    
    if not path.exists():
        logging.warning(f"Arquivo de configuração '{config_path}' não encontrado. Usando padrões vazios.")
        return default_config
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao ler config.json: {e}")
        return default_config
