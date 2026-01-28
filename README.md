# 📂 OsCabaOrganiza

> **Uma ferramenta simples e eficiente para automação de organização de arquivos.**

Bem-vindo ao **OsCabaOrganiza**! Este projeto nasceu de uma necessidade comum: lidar com pastas de downloads caóticas e diretórios desorganizados. É um script Python projetado para automatizar a triagem de arquivos, movendo-os para pastas categorizadas com base em seu tipo ou data de criação.

Este projeto reflete meu interesse em **automação**, **manipulação de sistemas de arquivos** e criação de ferramentas que resolvem problemas reais do dia a dia.

---

## 🚀 Funcionalidades

O script oferece uma interface interativa via terminal, com seleção de pastas via interface gráfica nativa do sistema (Tkinter), permitindo:

- **Organização por Extensão**: Agrupa arquivos em pastas semânticas como `Imagens`, `Documentos`, `Videos`, `Scripts`, entre outros.
- **Organização por Data**: Cria pastas baseadas na data de criação dos arquivos (formato `DD-MM-YYYY`), ideal para backup de fotos ou logs.
- **Tratamento de Conflitos**: Renomeia automaticamente arquivos duplicados para evitar sobrescrita acidental.
- **Segurança**: Ignora o próprio arquivo do script e pastas já existentes para evitar recursão indesejada.

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando apenas a **Biblioteca Padrão do Python**, demonstrando como é possível criar soluções robustas sem dependências externas pesadas.

- **Python 3+**
- `os` e `shutil`: Para navegação no sistema de arquivos e movimentação de dados.
- `tkinter`: Para fornecer uma interface gráfica simples de seleção de diretório.
- `datetime`: Para manipulação de metadados temporais dos arquivos.

## 📦 Como Usar

1. Certifique-se de ter o Python instalado.
2. Clone este repositório:
   ```bash
   git clone https://github.com/gabaoun/OsCabaOrganiza.git
   ```
3. Navegue até a pasta do projeto:
   ```bash
   cd OsCabaOrganiza
   ```
4. Execute o script:
   ```bash
   python main.py
   ```
5. Uma janela abrirá para você selecionar a pasta que deseja organizar. Em seguida, escolha a opção desejada no terminal.

## 🧠 O que aprendi com este projeto

Este projeto foi um excelente exercício para consolidar conhecimentos em:
- **Lógica de Programação**: Estruturação de funções reutilizáveis e fluxo de controle.
- **Manipulação de Arquivos**: Entendimento prático de caminhos absolutos/relativos e metadados de arquivos.
- **Tratamento de Erros**: Garantir que o programa continue rodando mesmo se um arquivo estiver em uso ou protegido.
- **UX Simples**: Combinação de CLI (Linha de Comando) com GUI (Interface Gráfica) para facilitar o uso.

## 🔜 Próximos Passos

Planejo evoluir esta ferramenta com as seguintes melhorias:
- [ ] Adicionar um arquivo de configuração (`config.json`) para que o usuário personalize as extensões e pastas.
- [ ] Implementar uma barra de progresso para pastas com muitos arquivos.
- [ ] Criar uma interface gráfica completa (GUI) para substituir o menu do terminal.
- [ ] Adicionar logs de execução para auditoria do que foi movido.

---

*Sinta-se à vontade para contribuir, sugerir melhorias ou usar este código para organizar seus próprios arquivos!*
