# 📂 OsCabaOrganiza

> **Automação de arquivos profissional, paralela e segura.**

O **OsCabaOrganiza** é uma ferramenta de engenharia de software projetada para transformar o caos de diretórios em ordem estruturada. Diferente de scripts simples, esta aplicação utiliza **concorrência (Threads)**, **configuração externa** e **arquitetura modular** para lidar com milhares de arquivos de forma eficiente.

---

## 🚀 Funcionalidades Avançadas

- **⚡ Alta Performance:** Utiliza `ThreadPoolExecutor` para mover arquivos em paralelo, maximizando o uso de I/O.
- **🛡️ Thread Safety:** Implementação de `Lock` para evitar condições de corrida (Race Conditions) ao renomear arquivos duplicados.
- **🔄 Recursividade:** Capacidade de vasculhar subpastas (`--recursive`) e trazer arquivos para a raiz organizada.
- **🧹 Limpeza Automática:** Opcionalmente remove pastas vazias (`--remove-empty`) após a organização.
- **🙈 Ignora Ocultos:** Protege arquivos de sistema e configurações (como `.git`, `.DS_Store`) por padrão.
- **🧪 Modo Dry-Run:** Simula toda a operação mostrando logs do que seria feito, sem risco de perda de dados.

## 🛠️ Tecnologias e Padrões

Este projeto demonstra práticas de **Engenharia de Software Sênior**:

- **Arquitetura Modular:** Separação clara entre Core (`app/core.py`), Interface (`app/cli.py`) e Configuração.
- **Type Hinting:** Código 100% tipado para robustez e clareza.
- **Testes Automatizados:** Suíte de testes unitários (`unittest`) cobrindo cenários de borda e mocks.
- **Configuração Externa:** Regras de extensão carregadas de `config.json` (Princípio Open/Closed).

## 📦 Instalação e Uso

### Pré-requisitos
- Python 3.8+

### Clonar o repositório
```bash
git clone https://github.com/gabaoun/OsCabaOrganiza.git
cd OsCabaOrganiza
```

### Modo Interativo (GUI/Menu)
Basta rodar o script e seguir as instruções na tela:
```bash
python main.py
```

### Modo CLI (Power User)
Ideal para scripts de servidor ou automação via CRON.

**Exemplo 1: Simular organização recursiva**
```bash
python main.py --path "C:/Downloads" --mode ext --recursive --dry-run
```

**Exemplo 2: Organizar por data e limpar pastas vazias**
```bash
python main.py --path "C:/Fotos" --mode date --remove-empty --verbose
```

---

## 🧪 Rodando os Testes

Para verificar a integridade da aplicação:
```bash
python -m unittest discover tests
```

---

## 📄 Estrutura do Projeto

```text
OsCabaOrganiza/
├── app/
│   ├── core.py         # Lógica de negócio (Threads, Locks, File Ops)
│   ├── cli.py          # Interface CLI e Tratamento de Argumentos
│   └── utils.py        # Logging e Carregamento de JSON
├── config.json         # Mapeamento de extensões editável
├── tests/              # Testes unitários
└── main.py             # Entry point
```

---
*Desenvolvido com foco em Clean Code e Scalability.*