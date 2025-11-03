# -*- coding: utf-8 -*-
"""
Models para o sistema de cadastro de professores substitutos
"""

from datetime import datetime
from typing import Optional

class Professor:
    """Classe para representar um professor substituto"""
    
    def __init__(self, id: Optional[int] = None, nome: str = "", cpf: str = "", 
                 email: str = "", telefone: str = "", especialidade: str = ""):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.especialidade = especialidade
    
    def __repr__(self):
        return f"Professor({self.id}, {self.nome}, {self.especialidade})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'especialidade': self.especialidade
        }


class Instituicao:
    """Classe para representar uma instituição de ensino"""
    
    def __init__(self, id: Optional[int] = None, nome: str = "", cnpj: str = "",
                 endereco: str = "", cidade: str = "", estado: str = ""):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
    
    def __repr__(self):
        return f"Instituicao({self.id}, {self.nome}, {self.cidade})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado
        }


class Vaga:
    """Classe para representar uma vaga de professor substituto"""
    
    def __init__(self, id: Optional[int] = None, instituicao_id: Optional[int] = None,
                 disciplina: str = "", carga_horaria: int = 0, salario: float = 0.0,
                 descricao: str = "", status: str = "Aberta", professor_id: Optional[int] = None):
        self.id = id
        self.instituicao_id = instituicao_id
        self.disciplina = disciplina
        self.carga_horaria = carga_horaria
        self.salario = salario
        self.descricao = descricao
        self.status = status  # Aberta, Preenchida, Cancelada
        self.professor_id = professor_id
        self.data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __repr__(self):
        return f"Vaga({self.id}, {self.disciplina}, {self.status})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'instituicao_id': self.instituicao_id,
            'disciplina': self.disciplina,
            'carga_horaria': self.carga_horaria,
            'salario': self.salario,
            'descricao': self.descricao,
            'status': self.status,
            'professor_id': self.professor_id,
            'data_cadastro': self.data_cadastro
        }
