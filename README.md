# OsCabaOrganiza: Concurrent File System Engine

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Code_Style-PEP_8-green.svg?style=for-the-badge" />
</p>

**OsCabaOrganiza** is a high-performance command-line application engineered to automate and optimize file system organization. Built to process massive volumes of files concurrently, it ensures transactional safety and predictable behavior during OS-level operations.

## ⚙️ Core Technical Features

- **Concurrent Batch Processing:** Leverages Python's multiprocessing and threading models to handle large-scale data ingestion and sorting in parallel.
- **Transactional State Management:** Implements a robust command system (undo/redo) that tracks file operations, allowing developers to safely revert state changes and avoid data corruption.
- **Real-time Event Hooks:** Uses `watchdog` to monitor directory events at the OS level, triggering automated workflows instantly upon file creation.
- **Data Extraction:** Automatically detects, verifies, and extracts compressed archives (`.zip`, `.tar`, `.gz`) within the pipeline.

## 🚀 Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI tool
python main.py --help
```
