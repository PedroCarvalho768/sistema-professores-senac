# -*- coding: utf-8 -*-
"""
Módulo de banco de dados usando SQLite
"""

import sqlite3
from typing import List, Optional
from models import Professor, Instituicao, Vaga

class Database:
    """Classe para gerenciar o banco de dados SQLite"""
    
    def __init__(self, db_name: str = "sistema_professores.db"):
        self.db_name = db_name
        self.create_tables()
    
    def get_connection(self):
        """Cria uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        """Cria as tabelas do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de professores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS professores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                email TEXT,
                telefone TEXT,
                especialidade TEXT
            )
        ''')
        
        # Tabela de instituições
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instituicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cnpj TEXT UNIQUE NOT NULL,
                endereco TEXT,
                cidade TEXT,
                estado TEXT
            )
        ''')
        
        # Tabela de vagas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instituicao_id INTEGER,
                disciplina TEXT NOT NULL,
                carga_horaria INTEGER,
                salario REAL,
                descricao TEXT,
                status TEXT DEFAULT 'Aberta',
                professor_id INTEGER,
                data_cadastro TEXT,
                FOREIGN KEY (instituicao_id) REFERENCES instituicoes(id),
                FOREIGN KEY (professor_id) REFERENCES professores(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ===== PROFESSORES =====
    
    def inserir_professor(self, professor: Professor) -> int:
        """Insere um novo professor no banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO professores (nome, cpf, email, telefone, especialidade)
            VALUES (?, ?, ?, ?, ?)
        ''', (professor.nome, professor.cpf, professor.email, 
              professor.telefone, professor.especialidade))
        
        professor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return professor_id
    
    def listar_professores(self) -> List[Professor]:
        """Lista todos os professores"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM professores')
        rows = cursor.fetchall()
        conn.close()
        
        professores = []
        for row in rows:
            prof = Professor(
                id=row[0], nome=row[1], cpf=row[2],
                email=row[3], telefone=row[4], especialidade=row[5]
            )
            professores.append(prof)
        
        return professores
    
    def buscar_professor(self, professor_id: int) -> Optional[Professor]:
        """Busca um professor pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM professores WHERE id = ?', (professor_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Professor(
                id=row[0], nome=row[1], cpf=row[2],
                email=row[3], telefone=row[4], especialidade=row[5]
            )
        return None
    
    def atualizar_professor(self, professor: Professor):
        """Atualiza os dados de um professor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE professores 
            SET nome=?, cpf=?, email=?, telefone=?, especialidade=?
            WHERE id=?
        ''', (professor.nome, professor.cpf, professor.email,
              professor.telefone, professor.especialidade, professor.id))
        
        conn.commit()
        conn.close()
    
    def deletar_professor(self, professor_id: int):
        """Deleta um professor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM professores WHERE id = ?', (professor_id,))
        
        conn.commit()
        conn.close()
    
    # ===== INSTITUIÇÕES =====
    
    def inserir_instituicao(self, instituicao: Instituicao) -> int:
        """Insere uma nova instituição"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO instituicoes (nome, cnpj, endereco, cidade, estado)
            VALUES (?, ?, ?, ?, ?)
        ''', (instituicao.nome, instituicao.cnpj, instituicao.endereco,
              instituicao.cidade, instituicao.estado))
        
        instituicao_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return instituicao_id
    
    def listar_instituicoes(self) -> List[Instituicao]:
        """Lista todas as instituições"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM instituicoes')
        rows = cursor.fetchall()
        conn.close()
        
        instituicoes = []
        for row in rows:
            inst = Instituicao(
                id=row[0], nome=row[1], cnpj=row[2],
                endereco=row[3], cidade=row[4], estado=row[5]
            )
            instituicoes.append(inst)
        
        return instituicoes
    
    def buscar_instituicao(self, instituicao_id: int) -> Optional[Instituicao]:
        """Busca uma instituição pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM instituicoes WHERE id = ?', (instituicao_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Instituicao(
                id=row[0], nome=row[1], cnpj=row[2],
                endereco=row[3], cidade=row[4], estado=row[5]
            )
        return None
    
    def atualizar_instituicao(self, instituicao: Instituicao):
        """Atualiza os dados de uma instituição"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE instituicoes 
            SET nome=?, cnpj=?, endereco=?, cidade=?, estado=?
            WHERE id=?
        ''', (instituicao.nome, instituicao.cnpj, instituicao.endereco,
              instituicao.cidade, instituicao.estado, instituicao.id))
        
        conn.commit()
        conn.close()
    
    def deletar_instituicao(self, instituicao_id: int):
        """Deleta uma instituição"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM instituicoes WHERE id = ?', (instituicao_id,))
        
        conn.commit()
        conn.close()
    
    # ===== VAGAS =====
    
    def inserir_vaga(self, vaga: Vaga) -> int:
        """Insere uma nova vaga"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO vagas (instituicao_id, disciplina, carga_horaria, salario, 
                              descricao, status, professor_id, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (vaga.instituicao_id, vaga.disciplina, vaga.carga_horaria, vaga.salario,
              vaga.descricao, vaga.status, vaga.professor_id, vaga.data_cadastro))
        
        vaga_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return vaga_id
    
    def listar_vagas(self) -> List[Vaga]:
        """Lista todas as vagas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM vagas')
        rows = cursor.fetchall()
        conn.close()
        
        vagas = []
        for row in rows:
            vaga = Vaga(
                id=row[0], instituicao_id=row[1], disciplina=row[2],
                carga_horaria=row[3], salario=row[4], descricao=row[5],
                status=row[6], professor_id=row[7]
            )
            vaga.data_cadastro = row[8]
            vagas.append(vaga)
        
        return vagas
    
    def buscar_vaga(self, vaga_id: int) -> Optional[Vaga]:
        """Busca uma vaga pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM vagas WHERE id = ?', (vaga_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            vaga = Vaga(
                id=row[0], instituicao_id=row[1], disciplina=row[2],
                carga_horaria=row[3], salario=row[4], descricao=row[5],
                status=row[6], professor_id=row[7]
            )
            vaga.data_cadastro = row[8]
            return vaga
        return None
    
    def atualizar_vaga(self, vaga: Vaga):
        """Atualiza os dados de uma vaga"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE vagas 
            SET instituicao_id=?, disciplina=?, carga_horaria=?, salario=?, 
                descricao=?, status=?, professor_id=?
            WHERE id=?
        ''', (vaga.instituicao_id, vaga.disciplina, vaga.carga_horaria, vaga.salario,
              vaga.descricao, vaga.status, vaga.professor_id, vaga.id))
        
        conn.commit()
        conn.close()
    
    def deletar_vaga(self, vaga_id: int):
        """Deleta uma vaga"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM vagas WHERE id = ?', (vaga_id,))
        
        conn.commit()
        conn.close()
