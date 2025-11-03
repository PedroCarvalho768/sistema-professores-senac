# Sistema de Cadastro de Professores Substitutos

Sistema completo de gestão de professores substitutos com interface gráfica usando Raylib.

## Funcionalidades

- ✅ Cadastro de Professores
- ✅ Cadastro de Instituições de Ensino
- ✅ Cadastro de Vagas
- ✅ Listagem de todos os cadastros
- ✅ Geração de Relatórios (TXT/CSV)
- ✅ Interface gráfica interativa

## Requisitos

- Python 3.8+
- raylib-py (biblioteca gráfica)

## Instalação

1. Instale as dependências:
```bash
pip install raylib
```

2. Execute o aplicativo:
```bash
python main.py
```

## Estrutura do Projeto

```
.
├── main.py           # Arquivo principal do aplicativo
├── models.py         # Classes de modelo (Professor, Instituição, Vaga)
├── database.py       # Gerenciamento do banco de dados SQLite
├── gui.py            # Interface gráfica com Raylib
├── reports.py        # Geração de relatórios
└── README.md         # Este arquivo
```

## Como Usar

### Menu Principal
Ao executar o aplicativo, você verá um menu com as seguintes opções:

1. **Cadastrar Professor** - Formulário para adicionar novos professores
2. **Listar Professores** - Visualizar todos os professores cadastrados
3. **Cadastrar Instituição** - Adicionar novas instituições de ensino
4. **Listar Instituições** - Ver todas as instituições
5. **Cadastrar Vaga** - Criar novas vagas de professor substituto
6. **Listar Vagas** - Visualizar todas as vagas
7. **Relatórios** - Gerar relatórios do sistema

### Cadastro de Professor
Campos:
- Nome (obrigatório)
- CPF (obrigatório)
- Email
- Telefone
- Especialidade

### Cadastro de Instituição
Campos:
- Nome (obrigatório)
- CNPJ (obrigatório)
- Endereço
- Cidade
- Estado

### Cadastro de Vaga
Campos:
- ID da Instituição (obrigatório)
- Disciplina (obrigatório)
- Carga Horária
- Salário
- Descrição

### Relatórios
Tipos de relatórios disponíveis:
- Relatório de Professores
- Relatório de Instituições
- Relatório de Vagas
- Relatório Completo (estatísticas gerais)

Os relatórios são salvos em arquivos TXT na pasta do projeto.

## Banco de Dados

O sistema usa SQLite para armazenamento de dados. O arquivo do banco de dados (`sistema_professores.db`) é criado automaticamente na primeira execução.

### Tabelas:
- **professores**: id, nome, cpf, email, telefone, especialidade
- **instituicoes**: id, nome, cnpj, endereco, cidade, estado
- **vagas**: id, instituicao_id, disciplina, carga_horaria, salario, descricao, status, professor_id, data_cadastro

## Status de Vagas

- **Aberta**: Vaga disponível para candidatura
- **Preenchida**: Vaga já ocupada por um professor
- **Cancelada**: Vaga cancelada pela instituição

## Navegação

- Use o mouse para clicar nos botões
- Clique nos campos de texto para editá-los
- Use a roda do mouse para rolar listas longas
- Botão "Voltar" para retornar ao menu principal

## Atalhos de Teclado

- Digite normalmente nos campos de texto ativos
- Backspace para apagar caracteres
- ESC (na janela) para fechar o aplicativo

## Observações

- CPF e CNPJ devem ser únicos no sistema
- IDs são gerados automaticamente pelo banco de dados
- Relatórios incluem timestamp na data de geração
- Mensagens de feedback aparecem na parte inferior da tela

## Desenvolvido com

- **Python** - Linguagem de programação
- **SQLite** - Banco de dados
- **Raylib** - Biblioteca gráfica para a interface

---

Para mais informações ou suporte, consulte a documentação do código-fonte.
