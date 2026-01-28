import unittest
import shutil
import tempfile
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
        shutil.rmtree(self.test_dir)

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

if __name__ == '__main__':
    unittest.main()