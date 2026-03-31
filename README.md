# 🚀 OsCabaOrganiza

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/Code_Style-PEP_8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()

> **👨‍💻 Developed by Gabriel Penha (Gabaoun)**

---

> ## 🧩 Overview

**OsCabaOrganiza** is a command-line application built to simplify file system organization.  
It focuses on handling large volumes of files efficiently while maintaining predictable behavior and data safety.

This project was built to explore concurrency, modular design, and practical system-level programming in Python.

---

## ⚙️ Features

- **File Organization**
  - Sort files by extension or creation date
  - Configurable rules via `config.json`

- **Batch Processing**
  - Handles large volumes of files using parallel execution

- **Real-time Monitoring**
  - Watches directories and processes new files automatically

- **Undo Support**
  - Tracks operations and allows reverting changes safely

- **Archive Handling**
  - Detects and extracts compressed files (`.zip`, `.tar`, `.gz`)

- **CLI Interface**
  - Structured output with progress feedback

---

## 🛠️ Tech Stack

- **Python 3.14**
- **Rich** (CLI output)
- **Watchdog** (file system events)
- **Unittest** (testing)

---

## 📥 Download

You can download the latest version of **OsCabaOrganiza** directly from our [releases page](https://github.com/gabaoun/OsCabaOrganiza/releases).

### How to use the Executable:
1. Download the `OsCabaOrganiza.exe` file.
2. Ensure that the `config.json` file is in the same folder as the executable (optional, but recommended for customizing rules).
3. Run the file by double-clicking or via terminal:
   ```bash
   ./OsCabaOrganiza.exe
   ```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.14 or higher
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
python -m PyInstaller --onefile --name OsCabaOrganiza main.py

# Run the generated executable
./dist/OsCabaOrganiza.exe
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
│   └── utils.py           # Helper functions (Logging, Input handling)
├── tests/                 # Unit and integration tests
├── config.json            # User configuration (Mappings, settings)
├── main.py                # Application bootstrapper
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## 📬 Contact:
**Gabriel Penha (Gabaoun)**
- 📧 Email: [penhagabriellima@gmail.com]
- 🐙 GitHub: [github.com/gabaoun]
  
---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
