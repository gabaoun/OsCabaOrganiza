# 🚀 OsCabaOrganiza - Smart File Organizer

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/Code_Style-PEP_8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()

> **👨‍💻 Desenvolvido por Gabriel Penha (Gabaoun)**

**OsCabaOrganiza** é uma ferramenta CLI enterprise-grade desenvolvida em Python para automação inteligente de organização de arquivos. Projetada com padrões de engenharia de software modernos, esta solução demonstra expertise em desenvolvimento de sistemas robustos, concorrência e experiência do usuário em terminal.

## 💼 Competências Técnicas Demonstradas

### 🎯 Core Features
- **📂 Organização Inteligente**: Algoritmo de classificação por extensão e data com configuração JSON
- **🕒 Real-time Monitoring**: Sistema de file system events com arquitetura observer pattern
- **🔄 Atomic Operations**: Sistema de undo/redo com transações reversíveis
- **📊 Analytics Dashboard**: Métricas detalhadas de performance e volume de dados
- **🚀 High Performance**: Multi-threading com ThreadPoolExecutor para processamento paralelo
- **🎨 Rich Terminal UI**: Interface moderna com progress bars, tables e syntax highlighting
- **⌨️ Graceful Shutdown**: Signal handling para interrupção segura com cleanup automático

### 🏗️ Engineering Excellence
- **Clean Architecture**: Separação clara de responsabilidades com injeção de dependências
- **Error Handling**: Tratamento robusto de exceções com logging estruturado
- **Configuration Management**: Sistema de configuração externa com validação
- **Testing**: Testes unitários com pytest e mocking de file system
- **Packaging**: Executável standalone com PyInstaller para distribuição empresarial

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Propósito |
|------------|------------|-----------|
| **Linguagem** | Python 3.13+ | Core development with type hints |
| **Terminal UI** | Rich | Interfaces ricas com tabelas, progress bars e syntax highlighting |
| **File System** | Watchdog | Cross-platform file system events monitoring |
| **Packaging** | PyInstaller | Distribuição como executável standalone |
| **Color Support** | Colorama | Terminal color management cross-platform |
| **Development** | pytest, black, mypy | Testing, formatting e type checking |

**📦 Production Ready**: Containerizado e pronto para deploy em ambientes empresariais

## 🚀 Quick Start

### Pré-requisitos
- Python 3.13+ com pip
- Git

### Instalação
```bash
# Clone o repositório
git clone https://github.com/gabaoun/OsCabaOrganiza.git
cd OsCabaOrganiza

# Instale dependências em ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Execute a aplicação
python main.py
```

### Build para Produção
```bash
# Gere executável standalone
pyinstaller --onefile --windowed main.py

# Execute sem dependências Python
./dist/main
```

## 📁 Arquitetura do Projeto

```
OsCabaOrganiza/
├── app/                    # Core application layer
│   ├── __init__.py
│   ├── organizer.py        # Business logic & file operations
│   ├── ui.py              # Rich terminal interface
│   └── config.py          # Configuration management
├── tests/                  # Test suite
│   ├── test_organizer.py
│   └── test_config.py
├── config.json            # File extension mapping
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎯 Por que este projeto é relevante para recrutadores?

### ✅ Demonstração de Competências Técnicas
- **Python Avançado**: Type hints, async/await, context managers
- **Design Patterns**: Observer, Strategy, Factory Method
- **Performance**: Multi-threading, memory optimization, batch processing
- **DevOps**: Packaging, configuration management, cross-platform compatibility

### ✅ Soft Skills
- **Problem Solving**: Automação de tarefas repetitivas complexas
- **User Experience**: Interface intuitiva com feedback visual
- **Code Quality**: Clean code, documentação, testabilidade
- **Innovation**: Solução criativa para problema comum do dia a dia

### ✅ Enterprise Readiness
- **Escalabilidade**: Processa milhares de arquivos sem degradação
- **Confiabilidade**: Tratamento robusto de erros e recuperação
- **Manutenibilidade**: Código modular e bem documentado
- **Deploy**: Distribuição simplificada sem dependências

## 📬 Conecte-se Comigo

**Gabriel Penha (Gabaoun)**
- 📧 Email: [penhagabriellima@gmail.com]
- 🐙 GitHub: [github.com/gabaoun]

> **🚀 Disponível para oportunidades**: Python | Automation | Full-Stack Development

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

**⭐ Se este projeto demonstrou o tipo de solução que sua empresa precisa, entre em contato!**
