# Sistema de Professores Substitutos

Sistema de gestão de professores substitutos para instituições de ensino, com interface gráfica em dark mode e geração de relatórios.

## 🚀 Início Rápido

```bash
# Clone o repositório
git clone https://github.com/PedroCarvalho768/sistema-professores-senac.git
cd sistema-professores-senac

# Crie um ambiente virtual e instale dependências
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

# Execute o sistema
python main.py
```

## ✨ Funcionalidades

### Cadastros
- **Professores** - Nome, CPF, email, telefone, especialidade
- **Instituições** - Nome, CNPJ, endereço, cidade, estado
- **Vagas** - Disciplina, carga horária, salário, descrição, status

### Relatórios
- Listagens completas (professores, instituições, vagas)
- Resumo de demanda por disciplina
- Aging de vagas abertas (dias em aberto)
- Estatísticas salariais por disciplina
- Exportação em TXT e CSV

### Interface
- Dark mode com paleta de cores personalizada
- Fonte Helvetica para melhor legibilidade
- Navegação por mouse e teclado
- Scroll suave em listas longas
- Feedback visual de operações

## 📁 Estrutura do Projeto

```
sistema-professores-senac/
├── app/                          # Pacote principal
│   ├── __init__.py              # Exporta Database, GUI, Models, Reports
│   ├── database.py              # SQLite com PRAGMA foreign keys e índices
│   ├── gui.py                   # Interface Raylib (dark mode)
│   ├── models.py                # Classes: Professor, Instituicao, Vaga
│   └── reports.py               # Geração de relatórios TXT/CSV
│
├── data/                         # Banco de dados (auto-criado)
│   └── sistema_professores.db   # SQLite database
│
├── output/                       # Relatórios exportados (auto-criado)
│   └── relatorio_*.txt          # Arquivos gerados
│
├── main.py                       # Ponto de entrada
├── smoketest.py                  # Validação rápida (sem GUI)
├── requirements.txt              # Dependências: raylib-py
├── Helvetica.ttf                 # Fonte customizada
└── README.md
```

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem principal
- **SQLite3** - Banco de dados (com foreign keys e índices)
- **Raylib (pyray)** - Interface gráfica 2D
- **CSV module** - Exportação segura de dados

## 📖 Guia de Uso

### Navegação
- **Menu Principal** - 7 opções de cadastro, listagem e relatórios
- **Mouse** - Clique em botões e campos de texto
- **Teclado** - Digite nos campos ativos, Backspace para apagar
- **Scroll** - Roda do mouse para navegar listas longas
- **ESC** - Fecha a aplicação

### Cadastros

#### Professor
- **Nome*** e **CPF*** são obrigatórios
- CPF deve ser único no sistema
- Campos: email, telefone, especialidade

#### Instituição
- **Nome*** e **CNPJ*** são obrigatórios
- CNPJ deve ser único no sistema
- Campos: endereço, cidade, estado

#### Vaga
- **Disciplina*** e **ID da Instituição*** são obrigatórios
- Status inicial: "Aberta"
- Campos: carga horária (horas), salário (R$), descrição
- A vaga pode ser vinculada a um professor depois

### Relatórios

Todos os relatórios são salvos em `output/` com timestamp no nome.

**Relatórios Básicos:**
- Professores, Instituições, Vagas (TXT ou CSV)
- Relatório Completo (estatísticas gerais do sistema)

**Relatórios Especializados:**
- **Demanda por Disciplina** - Contagem de vagas por disciplina
- **Aging de Vagas** - Dias que cada vaga está aberta
- **Salários por Disciplina** - Min/Médio/Max por área

## 💾 Banco de Dados

### Localização
- Arquivo: `data/sistema_professores.db`
- Criado automaticamente na primeira execução
- Ignorado pelo Git (via `.gitignore`)

### Tabelas

**professores**
- id (PK), nome, cpf (UNIQUE), email, telefone, especialidade

**instituicoes**
- id (PK), nome, cnpj (UNIQUE), endereco, cidade, estado

**vagas**
- id (PK), instituicao_id (FK), disciplina, carga_horaria
- salario, descricao, status, professor_id (FK), data_cadastro

### Integridade
- Foreign keys habilitadas (PRAGMA)
- Índices em: cpf, cnpj, status, disciplina, instituicao_id
- Cascade deletes configurados

## 🎨 Interface

### Cores (Dark Mode)
- **Fundo:** Cinza escuro (18,18,18)
- **Texto:** Branco para legibilidade
- **Primário:** Verde (0,168,120) - botões e acentos
- **Acento:** Coral (254,94,65) - erros e alertas
- **Bordas:** Sutis, com transparência

### Fonte
Sistema busca `Helvetica.ttf` em:
1. Raiz do projeto (`./Helvetica.ttf`)
2. `./assets/Helvetica.ttf`
3. `./assets/fonts/Helvetica.ttf`

Fallback: fonte padrão do Raylib se não encontrada.

## 🧪 Testes

```bash
# Teste rápido sem GUI (CRUD + relatórios)
python smoketest.py

# Teste manual
python main.py  # Navegue pela interface e teste funcionalidades
```

## 📝 Notas de Desenvolvimento

### Organização do Código
- Módulos organizados no pacote `app/`
- Imports relativos entre módulos internos
- Type hints em funções críticas
- Docstrings em português

### Boas Práticas
- Foreign keys habilitadas em todas as conexões SQLite
- Índices para melhorar performance de queries comuns
- CSV exports usando `csv.writer` para escaping correto
- Separação clara de responsabilidades (MVC-like)

### .gitignore
Ignora automaticamente:
- `.venv/` - ambiente virtual
- `data/` - bancos de dados
- `output/` - relatórios gerados
- `__pycache__/` - bytecode Python
- `*.db`, `*.pyc` - arquivos temporários

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença especificada no arquivo [LICENSE](LICENSE).

## 👤 Autor

**Pedro Carvalho**  
GitHub: [@PedroCarvalho768](https://github.com/PedroCarvalho768)

---

**Sistema de Professores Substitutos** - Desenvolvido com Python 🐍 e Raylib 🎮
