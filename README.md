# OsCabaOrganiza

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

High-performance file-system organization engine for Windows. OsCabaOrganiza classifies and relocates files at scale — by extension category or creation date — with **parallel execution**, **real-time directory watching**, **archive batch extraction**, and **transactional undo**.

Built for automated housekeeping of unstructured directories, it combines a streaming CLI with an interactive console interface and a silent automation mode for scripting.

---

## Key Capabilities

- **Extension-Based Organization:** Classifies files into 13 category folders (Images, Audio, Video, Documents, Data, Archives, Executables, Code, Web, Database, Config, Ebooks, Misc) via an O(1) extension→folder lookup map.
- **Date-Based Organization:** Groups files into `%d-%m-%Y` folders using filesystem creation timestamps.
- **Parallel Batch Processing:** File moves run through a `ThreadPoolExecutor` with lock-protected statistics for high-throughput directories.
- **Real-Time Monitoring (Sentinel):** A `watchdog` `Observer` watches a directory and auto-organizes new files as they arrive — with ESC-key abort support.
- **Transactional Undo:** Every move is journaled to `undo_log.json`; `undo_last_session()` restores files LIFO with collision-safe naming (`_restored_N`) and prunes emptied folders.
- **Archive Extraction:** Batch decompression of `.zip`, `.tar`, `.gz`, `.bz2`, `.xz`, and more, with correct handling of double extensions (`.tar.gz`).
- **Operator Safety:** ESC-key interrupt cancels in-flight futures and aborts the current operation cleanly.
- **Recursive & Cleanup Modes:** Optional recursive traversal and removal of emptied folders.

---

## Tech Stack

| Layer          | Technology                  |
| :------------- | :-------------------------- |
| Language       | Python >= 3.14              |
| Concurrency    | `concurrent.futures` (thread pool) |
| CLI / UI       | Rich (panels, tables, live progress) |
| File Watching  | watchdog (`Observer`)       |
| GUI Prompt     | tkinter (folder picker)     |
| Packaging      | PyInstaller (single-binary) |
| Testing        | unittest                   |

---

## Architecture

```text
┌──────────────────────────────────────────────────────┐
│                      CLI Layer                        │
│  app/cli.py — argparse (--path) + Rich interactive    │
│              menu (organize / decompress / watch /    │
│              undo / exit)                             │
└──────────────────────────┬───────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────┐
│                   Core Engine                         │
│  app/core.py                                          │
│  ├── Organizer                                       │
│  │     ├── organize_by_extension()  (ThreadPool)      │
│  │     ├── organize_by_date()       (ThreadPool)      │
│  │     ├── decompress_files()                         │
│  │     └── start_sentinel()         (watchdog)        │
│  └── UndoManager                                      │
│        └── undo_last_session()  (JSON journal)        │
└──────────────────────────┬───────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────┐
│                Configuration & Helpers                │
│  config.json (extension rules)                        │
│  app/utils.py (logging, input, app path resolution)   │
└──────────────────────────────────────────────────────┘
```

### Project Structure

```text
OsCabaOrganiza/
├── main.py                # Entry point
├── config.json            # Extension classification rules
├── app/
│   ├── core.py            # Organizer, UndoManager, SentinelHandler
│   ├── cli.py             # Argument parsing + interactive menu
│   └── utils.py           # Logging, input handling, path resolution
├── tests/                 # Unit test suite
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python >= 3.14
- Git

### Installation

```bash
git clone https://github.com/gabaoun/OsCabaOrganiza.git
cd OsCabaOrganiza

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Usage

**Automation mode** — organize a directory silently by extension:

```bash
python main.py --path "C:\Users\you\Downloads"
```

**Interactive mode** — launch the menu-driven console (folder picker + operation selection):

```bash
python main.py
```

The interactive menu supports: organize by extension, organize by date, batch decompress, sentinel watch mode, and undo last session. ESC aborts any running operation.

### Building a Standalone Binary

Package the application into a single executable (no Python runtime required on the target machine):

```bash
python -m PyInstaller --onefile --name OsCabaOrganiza main.py

# Run the generated executable
./dist/OsCabaOrganiza.exe
```

Prebuilt binaries are published on the [releases page](https://github.com/gabaoun/OsCabaOrganiza/releases).

---

## Configuration

Classification rules are driven by `config.json`. Place a custom file alongside the executable or in the project root to override defaults.

| Key              | Type     | Description                                                        |
| :--------------- | :------- | :----------------------------------------------------------------- |
| `extensions`     | object   | Maps category folder names to arrays of lowercase file extensions. |
| `others_folder`  | string   | Destination folder name for unclassified extensions.               |

Example:

```json
{
    "extensions": {
        "Images": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"],
        "Audio":  ["mp3", "wav", "aac", "flac", "ogg"]
    },
    "others_folder": "Others"
}
```

---

## CLI Reference

| Argument | Description                                                        |
| :------- | :----------------------------------------------------------------- |
| `--path` | Target directory. When provided, runs a one-shot extension-based organization and exits. |

---

## Testing

```bash
python -m unittest discover tests
```

---

## License

Distributed under the **MIT** License. See `LICENSE` for details.
