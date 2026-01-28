# 🚀 OsCabaOrganiza - Organizador de Arquivos Supremo

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

O **OsCabaOrganiza** é uma ferramenta de linha de comando (CLI) profissional desenvolvida em Python para automatizar a organização de arquivos em diretórios bagunçados. Ideal para manter sua pasta de Downloads ou Desktop sempre limpa.

![Banner](https://img.shields.io/badge/UI-Rich_Terminal-cyan)

## ✨ Funcionalidades

- **📂 Organização Inteligente**: Organize arquivos por extensão ou por data de criação.
- **🕒 Modo Sentinel (Monitoramento)**: O programa monitora sua pasta em tempo real e organiza novos arquivos instantaneamente.
- **🔄 Sistema de Desfazer (Undo)**: Cometeu um erro? Desfaça a última organização com um clique.
- **📊 Relatórios Detalhados**: Veja estatísticas de quantos arquivos foram movidos e o volume de dados processado.
- **🚀 Performance**: Utiliza Multi-threading para processar milhares de arquivos em segundos.
- **🎨 UI Moderna**: Interface rica no terminal com barras de progresso e cores vibrantes.
- **⌨️ Aborto Seguro**: Pressione `ESC` a qualquer momento para interromper a operação com segurança.

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/) - Linguagem base.
- [Rich](https://github.com/Textualize/rich) - Interface gráfica no terminal.
- [Watchdog](https://github.com/gorakhargosh/watchdog) - Monitoramento de eventos do sistema de arquivos.
- [PyInstaller](https://pyinstaller.org/) - Criação do executável standalone.

## 📦 Como Instalar e Rodar

### Pré-requisitos
- Python 3.13 ou superior instalado.

### Passos
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/OsCabaOrganiza.git
   cd OsCabaOrganiza
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o programa:**
   ```bash
   python main.py
   ```

## 🏗️ Estrutura do Projeto

```text
OsCabaOrganiza/
├── app/                # Lógica central e interface
├── tests/              # Testes automatizados (Unit Testing)
├── config.json         # Mapeamento de extensões configurável
├── main.py             # Ponto de entrada
└── requirements.txt    # Dependências
```

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---
Desenvolvido com ☕ por [Seu Nome/Github]
