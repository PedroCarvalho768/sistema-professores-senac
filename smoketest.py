from app.database import Database
from app.models import Professor, Instituicao, Vaga
from app.reports import ReportGenerator
import os

db_path = 'tmp_smoketest.db'
try:
    os.remove(db_path)
except FileNotFoundError:
    pass

# Initialize DB
db = Database(db_path)

# Insert sample data
p_id = db.inserir_professor(Professor(nome='Ana Silva', cpf='11122233344', email='ana@example.com', telefone='9999-0000', especialidade='Matematica'))
i_id = db.inserir_instituicao(Instituicao(nome='Escola A', cnpj='12.345.678/0001-00', endereco='Rua 1', cidade='Cidade', estado='UF'))

v_id = db.inserir_vaga(Vaga(instituicao_id=i_id, disciplina='Matematica', carga_horaria=20, salario=3500.0, descricao='Substituicao de 2 meses'))

# Query back
profs = db.listar_professores()
insts = db.listar_instituicoes()
vagas = db.listar_vagas()

print('Counts', len(profs), len(insts), len(vagas))
print('Professor 1:', profs[0].to_dict())
print('Instituicao 1:', insts[0].to_dict())
print('Vaga 1:', vagas[0].to_dict())

# Reports
rep = ReportGenerator(db)
print('\n--- Relatorio Professores (TXT) ---')
print(rep.gerar_relatorio_professores('txt').splitlines()[0])
print('CSV header:', rep.gerar_relatorio_professores('csv').splitlines()[0])

print('\n--- Relatorio Vagas (TXT) ---')
rv = rep.gerar_relatorio_vagas('txt')
print(rv.splitlines()[0], '| total lines:', len(rv.splitlines()))

# Cleanup
os.remove(db_path)
print('OK')