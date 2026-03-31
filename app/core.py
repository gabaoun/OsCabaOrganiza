import shutil
import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from .utils import setup_logger, check_esc_pressed, flush_input

logger = setup_logger()

# Try to import watchdog, but don't fail if not available
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

class UndoManager:
    """Manages operation history to allow undo."""
    def __init__(self, history_file: Path):
        self.history_file = history_file
        self.history: List[Dict] = []
        self._load_history()

    def _load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def register_move(self, src: str, dst: str):
        """Registers a file move."""
        self.history.append({
            "action": "move",
            "src": src,
            "dst": dst,
            "timestamp": datetime.now().isoformat()
        })
        self._save_history()

    def _save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass

    def undo_last_session(self) -> List[str]:
        """Undoes registered operations and clears history."""
        results = []
        # Process from last to first (LIFO)
        for entry in reversed(self.history):
            if entry["action"] == "move":
                src = Path(entry["src"]) # Original location
                dst = Path(entry["dst"]) # Current location

                if dst.exists():
                    try:
                        # Ensure original folder exists
                        src.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Avoid overwriting if something was created in the original's place
                        target = src
                        counter = 1
                        while target.exists():
                            target = src.parent / f"{src.stem}_restored_{counter}{src.suffix}"
                            counter += 1
                        
                        shutil.move(str(dst), str(target))
                        results.append(f"Restored: {dst.name} -> {target}")
                        
                        # Remove destination folder if it became empty
                        try:
                            dst.parent.rmdir()
                        except OSError:
                            pass
                    except Exception as e:
                        results.append(f"Error restoring {dst.name}: {e}")
                else:
                    results.append(f"File not found to restore: {dst}")
        
        # Clear history after undo
        self.history = []
        if self.history_file.exists():
            os.remove(self.history_file)
            
        return results

class SentinelHandler(FileSystemEventHandler):
    """Watchdog event handler."""
    def __init__(self, organizer_instance, directory: Path):
        self.organizer = organizer_instance
        self.directory = directory

    def on_created(self, event):
        if event.is_directory:
            return
        
        # Wait a bit to ensure the file was written
        time.sleep(1)
        
        file_path = Path(event.src_path)
        # Ignore temporary or system files
        if file_path.name == "undo_log.json" or file_path.name.startswith('.'):
            return

        # Process this specific file
        self.organizer.process_single_file_event(file_path, self.directory)

class Organizer:
    def __init__(self, config: Dict, dry_run: bool = False):
        self.config = config
        self.others_folder = config.get("others_folder", "Others")
        self.dry_run = dry_run
        self.lock = Lock()
        
        # Lookup O(1)
        self.extension_lookup: Dict[str, str] = {}
        for folder, extensions in config.get("extensions", {}).items():
            for ext in extensions:
                self.extension_lookup[ext.lower()] = folder

        # Undo Manager will be initialized when we know the target directory
        self.undo_manager: Optional[UndoManager] = None
        
        # Statistics for report
        self.stats = {"moved": 0, "errors": 0, "bytes": 0, "extracted": 0}

    def _find_folder(self, extension: str) -> str:
        return self.extension_lookup.get(extension.lower(), self.others_folder)

    def _get_archive_extensions(self) -> List[str]:
        """Returns list of extensions supported by shutil."""
        extensions = []
        for format_name, exts, description in shutil.get_unpack_formats():
            extensions.extend(exts)
        return extensions

    def _decompress_single_file(self, file_path: Path, base_directory: Path) -> str:
        """Decompresses a file into a folder with its name."""
        try:
            # Handle double extensions like .tar.gz
            folder_name = file_path.stem
            if file_path.suffix.lower() == '.gz' and Path(folder_name).suffix.lower() == '.tar':
                folder_name = Path(folder_name).stem
            elif file_path.suffix.lower() == '.bz2' and Path(folder_name).suffix.lower() == '.tar':
                folder_name = Path(folder_name).stem
            elif file_path.suffix.lower() == '.xz' and Path(folder_name).suffix.lower() == '.tar':
                folder_name = Path(folder_name).stem

            output_folder = base_directory / folder_name
            
            if self.dry_run:
                return f"[SIMULATION] Would decompress: '{file_path.name}' to '{folder_name}/'"

            # Create destination folder
            output_folder.mkdir(parents=True, exist_ok=True)

            # Decompress
            shutil.unpack_archive(str(file_path), str(output_folder))

            with self.lock:
                self.stats["extracted"] += 1
                self.stats["bytes"] += file_path.stat().st_size
            
            return f"Decompressed: {file_path.name} -> {folder_name}/"
            
        except Exception as e:
            with self.lock:
                self.stats["errors"] += 1
            return f"ERROR decompressing {file_path.name}: {str(e)}"

    def _move_single_file(self, file_path: Path, folder_name: str, base_directory: Path) -> str:
        """Moves file, updates stats and registers undo."""
        if file_path.name.startswith('.') or file_path.name == "undo_log.json":
            return f"Ignored: {file_path.name}"

        try:
            target_folder = base_directory / folder_name
            file_size = file_path.stat().st_size

            if not self.dry_run:
                target_folder.mkdir(parents=True, exist_ok=True)

            with self.lock:
                destination_path = target_folder / file_path.name
                counter = 1
                while destination_path.exists():
                    destination_path = target_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
                    counter += 1

            if self.dry_run:
                return f"[SIMULATION] Would move: '{file_path.name}'"
            
            # Execute Move
            src_str = str(file_path.resolve())
            dst_str = str(destination_path.resolve())
            
            shutil.move(src_str, dst_str)
            
            # Register Undo and Stats
            if self.undo_manager:
                self.undo_manager.register_move(src_str, dst_str)
            
            with self.lock:
                self.stats["moved"] += 1
                self.stats["bytes"] += file_size
                
            return f"Success: {file_path.name}"
            
        except Exception as e:
            with self.lock:
                self.stats["errors"] += 1
            return f"ERROR: {str(e)}"

    def process_single_file_event(self, file_path: Path, base_directory: Path):
        """Processes a single file (used by Sentinel)."""
        if not file_path.exists():
            return
            
        folder = self._find_folder(file_path.suffix)
        res = self._move_single_file(file_path, folder, base_directory)
        if "Success" in res:
            logger.info(f"[Sentinel] {res}")

    def _get_files(self, directory: Path, recursive: bool):
        iterator = directory.rglob('*') if recursive else directory.iterdir()
        for f in iterator:
            if f.is_file() and f.name != "main.py" and f.name != "undo_log.json":
                yield f

    def organize_by_extension(self, directory: Path, recursive: bool = False, remove_empty: bool = False, progress_callback: Callable = None) -> None:
        self.undo_manager = UndoManager(directory / "undo_log.json")
        self.stats = {"moved": 0, "errors": 0, "bytes": 0, "extracted": 0} # Reset stats
        
        files = list(self._get_files(directory, recursive))
        if not files:
            return

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                folder = self._find_folder(file_path.suffix)
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            for future in futures:
                if check_esc_pressed():
                    logger.warning("Operation aborted by user (ESC pressed).")
                    executor.shutdown(wait=False, cancel_futures=True)
                    return

                res = future.result()
                if progress_callback:
                    progress_callback()

        if remove_empty:
            self._remove_empty_folders(directory)

    def organize_by_date(self, directory: Path, recursive: bool = False, remove_empty: bool = False, progress_callback: Callable = None) -> None:
        self.undo_manager = UndoManager(directory / "undo_log.json")
        self.stats = {"moved": 0, "errors": 0, "bytes": 0, "extracted": 0}

        files = list(self._get_files(directory, recursive))
        if not files:
            return

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in files:
                created_at = datetime.fromtimestamp(file_path.stat().st_ctime)
                folder = created_at.strftime('%d-%m-%Y')
                futures.append(executor.submit(self._move_single_file, file_path, folder, directory))
            
            for future in futures:
                if check_esc_pressed():
                    logger.warning("Operation aborted by user (ESC pressed).")
                    executor.shutdown(wait=False, cancel_futures=True)
                    return

                res = future.result()
                if progress_callback:
                    progress_callback()

        if remove_empty:
            self._remove_empty_folders(directory)

    def decompress_files(self, directory: Path, recursive: bool = False, progress_callback: Callable = None) -> None:
        """Batch decompresses files."""
        self.stats = {"moved": 0, "errors": 0, "bytes": 0, "extracted": 0}
        
        # Identify supported extensions
        supported_exts = set(self._get_archive_extensions())
        
        # Filter only supported archive files
        all_files = list(self._get_files(directory, recursive))
        archive_files = [f for f in all_files if ''.join(f.suffixes) in supported_exts or f.suffix in supported_exts]
        
        if not archive_files:
             archive_files = [f for f in all_files if f.suffix in supported_exts]

        if not archive_files:
            return

        with ThreadPoolExecutor() as executor:
            futures = []
            for file_path in archive_files:
                futures.append(executor.submit(self._decompress_single_file, file_path, directory))
            
            for future in futures:
                if check_esc_pressed():
                    logger.warning("Operation aborted by user (ESC pressed).")
                    executor.shutdown(wait=False, cancel_futures=True)
                    return

                res = future.result()
                if progress_callback:
                    progress_callback()

    def _remove_empty_folders(self, directory: Path):
        if self.dry_run:
            return
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in dirs:
                path = Path(root) / name
                try:
                    path.rmdir()
                except OSError:
                    pass

    def start_sentinel(self, directory: Path):
        """Starts continuous monitoring mode."""
        if not HAS_WATCHDOG:
            logger.error("'watchdog' library not installed.")
            return

        self.undo_manager = UndoManager(directory / "undo_log.json")
        event_handler = SentinelHandler(self, directory)
        observer = Observer()
        observer.schedule(event_handler, str(directory), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
                if check_esc_pressed():
                    break
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()

    def undo_operation(self, directory: Path) -> List[str]:
        """Wrapper for undo manager."""
        mgr = UndoManager(directory / "undo_log.json")
        return mgr.undo_last_session()
