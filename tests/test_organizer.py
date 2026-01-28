import unittest
import sys
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adiciona o diretório pai ao path para importar o main.py
sys.path.insert(0, str(Path(__file__).parent.parent))

import main

class TestOrganizer(unittest.TestCase):

    def setUp(self):
        # Cria um diretório temporário para os testes
        self.test_dir = tempfile.mkdtemp()
        self.path = Path(self.test_dir)
        self.extensions_map = main.create_default_extensions_map()

    def tearDown(self):
        # Remove o diretório temporário após os testes
        shutil.rmtree(self.test_dir)

    def test_find_folder_by_extension(self):
        """Testa se a extensão correta retorna a pasta correta."""
        self.assertEqual(main.find_folder_by_extension('.jpg', self.extensions_map), 'Imagens')
        self.assertEqual(main.find_folder_by_extension('.pdf', self.extensions_map), 'Documentos')
        self.assertEqual(main.find_folder_by_extension('.py', self.extensions_map), 'Scripts')
        self.assertEqual(main.find_folder_by_extension('.xyz', self.extensions_map), 'Others')

    def test_move_file_dry_run(self):
        """Testa se o modo Dry Run NÃO move arquivos."""
        # Cria um arquivo dummy
        dummy_file = self.path / "test_file.txt"
        dummy_file.touch()
        
        target_folder = "Documentos"
        
        with patch('main.logger') as mock_logger, \
             patch('shutil.move') as mock_move:
            
            main.move_file(dummy_file, target_folder, self.path, dry_run=True)
            
            # Verifica se shutil.move NÃO foi chamado
            mock_move.assert_not_called()
            # Verifica se o log foi chamado
            self.assertTrue(mock_logger.info.called)
            # Verifica se a pasta NÃO foi criada
            self.assertFalse((self.path / target_folder).exists())

    def test_move_file_real(self):
        """Testa a movimentação real de arquivos."""
        dummy_file = self.path / "real_file.txt"
        dummy_file.write_text("conteudo")
        
        target_folder = "Documentos"
        
        main.move_file(dummy_file, target_folder, self.path, dry_run=False)
        
        expected_path = self.path / target_folder / "real_file.txt"
        
        # Verifica se o arquivo existe no novo local
        self.assertTrue(expected_path.exists())
        # Verifica se o arquivo sumiu do local antigo
        self.assertFalse(dummy_file.exists())

    def test_duplicate_rename(self):
        """Testa se arquivos duplicados são renomeados corretamente."""
        target_folder_name = "Documentos"
        target_folder = self.path / target_folder_name
        target_folder.mkdir()
        
        # Cria arquivo JÁ existente no destino
        existing_file = target_folder / "teste.txt"
        existing_file.write_text("existente")
        
        # Cria arquivo novo na origem com MESMO nome
        new_file = self.path / "teste.txt"
        new_file.write_text("novo")
        
        main.move_file(new_file, target_folder_name, self.path, dry_run=False)
        
        # Esperamos que tenha sido criado como teste_1.txt
        expected_renamed = target_folder / "teste_1.txt"
        
        self.assertTrue(expected_renamed.exists())
        self.assertEqual(expected_renamed.read_text(), "novo")
        self.assertEqual(existing_file.read_text(), "existente")

if __name__ == '__main__':
    unittest.main()
