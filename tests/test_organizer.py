import unittest
import shutil
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import from package
from app.core import Organizer
from app.utils import load_config

class TestOrganizer(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.path = Path(self.test_dir)
        # Mock Config
        self.config = {
            "extensions": {
                "Images": [".jpg", ".png"]
            },
            "others_folder": "Others"
        }
        self.organizer = Organizer(self.config, dry_run=False)

    def tearDown(self):
        try:
            shutil.rmtree(self.test_dir)
        except PermissionError:
            pass # Windows sometimes holds the file

    def test_find_folder(self):
        """Tests folder lookup logic."""
        self.assertEqual(self.organizer._find_folder('.jpg'), 'Images')
        self.assertEqual(self.organizer._find_folder('.exe'), 'Others')

    def test_dry_run_does_not_move(self):
        """Tests if Dry Run respects files."""
        self.organizer.dry_run = True
        
        dummy = self.path / "test.jpg"
        dummy.touch()
        
        self.organizer.organize_by_extension(self.path)
        
        # File should remain in place
        self.assertTrue(dummy.exists())
        # Images folder should NOT exist
        self.assertFalse((self.path / "Images").exists())

    def test_real_move(self):
        """Tests real file move."""
        dummy = self.path / "photo.jpg"
        dummy.touch()
        
        self.organizer.organize_by_extension(self.path)
        
        expected = self.path / "Images" / "photo.jpg"
        self.assertTrue(expected.exists())
        self.assertFalse(dummy.exists())

    def test_ignore_hidden_files(self):
        """Tests if hidden files are ignored."""
        hidden = self.path / ".gitkeep"
        hidden.touch()
        
        self.organizer.organize_by_extension(self.path)
        
        # File should remain where it is
        self.assertTrue(hidden.exists())
        self.assertFalse((self.path / "Others" / ".gitkeep").exists())

    def test_recursive_move(self):
        """Tests if it finds files in subfolders."""
        subfolder = self.path / "Old_Downloads"
        subfolder.mkdir()
        
        nested_file = subfolder / "old_photo.jpg"
        nested_file.touch()
        
        # Activate recursion
        self.organizer.organize_by_extension(self.path, recursive=True)
        
        expected = self.path / "Images" / "old_photo.jpg"
        
        self.assertTrue(expected.exists())
        self.assertFalse(nested_file.exists())

    def test_remove_empty_folders(self):
        """Tests if empty folders are removed after moving."""
        subfolder = self.path / "To_Delete"
        subfolder.mkdir()
        
        file_inside = subfolder / "img.jpg"
        file_inside.touch()
        
        # Move AND clean
        self.organizer.organize_by_extension(self.path, recursive=True, remove_empty=True)
        
        # File moved
        self.assertTrue((self.path / "Images" / "img.jpg").exists())
        # Original folder deleted
        self.assertFalse(subfolder.exists())

    @patch('app.core.check_esc_pressed', return_value=True)
    @patch('app.core.flush_input')
    @patch('app.core.logger')
    def test_abort_immediate(self, mock_logger, mock_flush, mock_check_esc):
        """Tests if ESC press aborts the operation."""
        # Create mocks to simulate files
        dummy_files = []
        for i in range(10):
            p = MagicMock(spec=Path)
            p.name = f'file_{i}.txt'
            p.suffix = '.txt'
            p.is_file.return_value = True
            p.stat.return_value.st_ctime = 1000000 
            dummy_files.append(p)
        
        # Mock _get_files to return our fake files
        with patch.object(self.organizer, '_get_files', return_value=dummy_files):
            # Mock _move_single_file to avoid real IO
            with patch.object(self.organizer, '_move_single_file', return_value="Success") as mock_move:
                
                self.organizer.organize_by_extension(Path('.'))
                
                # Check if abort message was logged
                mock_logger.warning.assert_called_with("Operation aborted by user (ESC pressed).")

if __name__ == '__main__':
    unittest.main()