# 🚀 OsCabaOrganiza - Enterprise-Grade File Automation CLI

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/Code_Style-PEP_8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()

> **👨‍💻 Developed by Gabriel Penha (Gabaoun)**

**OsCabaOrganiza** is a high-performance CLI tool engineered to automate file system organization. Built with Python, it leverages modern software engineering principles—including concurrency, design patterns, and atomic transactions—to deliver a robust, user-friendly experience.

This project serves as a comprehensive portfolio piece demonstrating proficiency in **system programming**, **architecture design**, and **Python best practices**.

---

## 💼 Why This Matters (For Recruiters)

This project is not just a script; it is a full-fledged application that demonstrates ready-to-hire skills:

### 🛠 Technical Proficiency
- **Advanced Python**: Utilizes type hinting (`typing`), context managers, and decorators for clean, maintainable code.
- **Concurrency & Performance**: Implements `ThreadPoolExecutor` for non-blocking, parallel file processing, significantly speeding up large batch operations.
- **System Programming**: Direct interaction with OS file systems, signal handling (graceful shutdowns), and cross-platform compatibility.
- **Design Patterns**:
  - **Observer Pattern**: Used in the "Sentinel" mode to monitor real-time file system events.
  - **Strategy Pattern**: Decouples organization logic (by extension vs. by date).
  - **Transactional Safety**: Implements an Undo/Redo system using JSON-based transaction logs to ensure data integrity.

### 🎨 Product Engineering
- **User Experience (UX)**: Features a polished CLI with `rich` for progress bars, colored output, and interactive tables.
- **Reliability**: Comprehensive error handling and logging ensure the application doesn't crash unexpectedly during batch operations.
- **Maintainability**: Follows **Clean Architecture** principles, separating core logic (`app/core.py`) from the presentation layer (`app/cli.py`, `app/ui.py`).

---

## 🎯 Key Features

- **📂 Intelligent Sorting**: Automatically organizes files into folders based on extensions or creation dates (fully configurable via `config.json`).
- **👀 Sentinel Mode (Real-time)**: Watches directories in the background and organizes files the moment they are created (using `watchdog`).
- **↩️ Atomic Undo/Redo**: Safely reverts operations. If a batch move fails or you change your mind, you can restore the previous state instantly.
- **📦 Bulk Decompression**: Automatically detects and extracts supported archives (`.zip`, `.tar`, `.gz`, etc.) into dedicated folders.
- **📊 Analytics Dashboard**: Provides real-time statistics on processed files, volume moved, and execution time.
- **🚀 High Performance**: Thread-safe operations allow processing thousands of files in seconds without UI freezing.

---

## 🛠️ Tech Stack

| Component | Technology | Reasoning |
|-----------|------------|-----------|
| **Core Language** | Python 3.13+ | Leverages modern syntax and robust standard library (`pathlib`, `shutil`, `concurrent.futures`). |
| **CLI / UI** | Rich | Delivers a modern, readable terminal interface with minimal overhead. |
| **File Monitoring** | Watchdog | Efficient, cross-platform file system event handling. |
| **Configuration** | JSON | Standard, human-readable format for portable configuration. |
| **Distribution** | PyInstaller | Compiles the app into a standalone binary for easy distribution. |
| **Testing** | Pytest | Ensures reliability through unit and integration tests. |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/gabaoun/OsCabaOrganiza.git
cd OsCabaOrganiza

# 2. Create a virtual environment (Recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

### Building for Production
To create a standalone executable (no Python installation required for the end-user):

```bash
# Build the binary using PyInstaller
pyinstaller --onefile --windowed main.py

# Run the generated executable
./dist/main
```

---

## 📁 Project Architecture

The codebase follows a modular structure to ensure scalability and ease of testing.

```plaintext
OsCabaOrganiza/
├── app/
│   ├── __init__.py
│   ├── core.py            # Business logic (Organizer, UndoManager, Sentinel)
│   ├── cli.py             # Command-line entry point and argument parsing
│   ├── ui.py              # UI rendering logic (Rich integration)
│   ├── utils.py           # Helper functions (Logging, Input handling)
│   └── config.py          # Configuration loader and validator
├── tests/                 # Unit and integration tests
├── config.json            # User configuration (Mappings, settings)
├── main.py                # Application bootstrapper
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## 📬 Connect With Me

I am a software engineer passionate about building efficient tools and solving real-world problems.

**Gabriel Penha (Gabaoun)**
- 📧 Email: [penhagabriellima@gmail.com]
- 🐙 GitHub: [github.com/gabaoun]

> **🚀 Open to Work**: Python Backend | System Automation | Full-Stack Development

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.