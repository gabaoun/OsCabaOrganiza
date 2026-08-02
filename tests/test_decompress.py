import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from app.core import Organizer


class TestDecompression(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.path = Path(self.test_dir)
        self.config = {
            "extensions": {},
            "others_folder": "Others"
        }
        self.organizer = Organizer(self.config, dry_run=False)

    def tearDown(self):
        try:
            shutil.rmtree(self.test_dir)
        except PermissionError:
            pass

    def test_decompress_zip(self):
        # Create a dummy zip file
        zip_path = self.path / "archive.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('file.txt', 'content')
            zf.writestr('inner/file2.txt', 'content2')

        self.organizer.decompress_files(self.path)

        expected_dir = self.path / "archive"
        self.assertTrue(expected_dir.exists())
        self.assertTrue((expected_dir / "file.txt").exists())
        self.assertTrue((expected_dir / "inner/file2.txt").exists())
        
        # Verify stats
        self.assertEqual(self.organizer.stats["extracted"], 1)

    def test_dry_run_decompress(self):
        self.organizer.dry_run = True
        zip_path = self.path / "archive_dry.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr('file.txt', 'content')

        self.organizer.decompress_files(self.path)
        
        expected_dir = self.path / "archive_dry"
        self.assertFalse(expected_dir.exists())
        self.assertEqual(self.organizer.stats["extracted"], 0)

    def test_ignore_non_archives(self):
        text_file = self.path / "text.txt"
        text_file.write_text("hello")
        
        self.organizer.decompress_files(self.path)
        
        # Should not create folder text
        self.assertFalse((self.path / "text").exists())
        self.assertEqual(self.organizer.stats["extracted"], 0)

if __name__ == '__main__':
    unittest.main()