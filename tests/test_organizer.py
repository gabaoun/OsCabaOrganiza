import unittest
import shutil
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

# Importa do novo pacote
from app.core import Organizer
from app.utils import load_config

class TestOrganizer(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.path = Path(self.test_dir)
        # Configuração Mockada
        self.config = {
            "extensions": {
                "Imagens": [".jpg", ".png"]
            },
            "others_folder": "Outros"
        }
        self.organizer = Organizer(self.config, dry_run=False)

    def tearDown(self):
        try:
            shutil.rmtree(self.test_dir)
        except PermissionError:
            pass # Às vezes o Windows segura o arquivo

    def test_find_folder(self):
        """Testa lógica de encontrar pasta no novo Core."""
        self.assertEqual(self.organizer._find_folder('.jpg'), 'Imagens')
        self.assertEqual(self.organizer._find_folder('.exe'), 'Outros')

    def test_dry_run_does_not_move(self):
        """Testa se Dry Run respeita os arquivos."""
        self.organizer.dry_run = True
        
        dummy = self.path / "teste.jpg"
        dummy.touch()
        
        self.organizer.organize_by_extension(self.path)
        
        # Arquivo deve continuar no mesmo lugar
        self.assertTrue(dummy.exists())
        # Pasta Imagens NÃO deve existir
        self.assertFalse((self.path / "Imagens").exists())

    def test_real_move(self):
        """Testa movimentação real."""
        dummy = self.path / "foto.jpg"
        dummy.touch()
        
        self.organizer.organize_by_extension(self.path)
        
        expected = self.path / "Imagens" / "foto.jpg"
        self.assertTrue(expected.exists())
        self.assertFalse(dummy.exists())

    def test_ignore_hidden_files(self):
        """Testa se arquivos ocultos são ignorados."""
        hidden = self.path / ".gitkeep"
        hidden.touch()
        
        self.organizer.organize_by_extension(self.path)
        
        # Arquivo deve permanecer onde está
        self.assertTrue(hidden.exists())
        self.assertFalse((self.path / "Outros" / ".gitkeep").exists())

    def test_recursive_move(self):
        """Testa se encontra arquivos em subpastas."""
        subfolder = self.path / "Downloads_Antigos"
        subfolder.mkdir()
        
        nested_file = subfolder / "foto_antiga.jpg"
        nested_file.touch()
        
        # Ativa recursividade
        self.organizer.organize_by_extension(self.path, recursive=True)
        
        expected = self.path / "Imagens" / "foto_antiga.jpg"
        
        self.assertTrue(expected.exists())
        self.assertFalse(nested_file.exists())

    def test_remove_empty_folders(self):
        """Testa se remove a pasta vazia após mover."""
        subfolder = self.path / "Para_Deletar"
        subfolder.mkdir()
        
        file_inside = subfolder / "img.jpg"
        file_inside.touch()
        
        # Move E limpa
        self.organizer.organize_by_extension(self.path, recursive=True, remove_empty=True)
        
        # Arquivo movido
        self.assertTrue((self.path / "Imagens" / "img.jpg").exists())
        # Pasta original deletada
        self.assertFalse(subfolder.exists())

if __name__ == '__main__':
    unittest.main()