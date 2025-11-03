# -*- coding: utf-8 -*-
"""
Módulo de geração de relatórios
"""

from datetime import datetime
from io import StringIO
import csv
import os
from typing import List, Optional
from .database import Database
from .models import Professor, Instituicao, Vaga

class ReportGenerator:
    """Classe para gerar relatórios do sistema"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def gerar_relatorio_professores(self, formato: str = "txt") -> str:
        """Gera relatório de todos os professores cadastrados"""
        professores = self.db.listar_professores()
        
        if formato == "txt":
            return self._relatorio_professores_txt(professores)
        elif formato == "csv":
            return self._relatorio_professores_csv(professores)
        return ""
    
    def _relatorio_professores_txt(self, professores: List[Professor]) -> str:
        """Gera relatório de professores em formato TXT"""
        linhas: List[str] = []
        linhas.append("=" * 80)
        linhas.append("RELATÓRIO DE PROFESSORES SUBSTITUTOS")
        linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("=" * 80)
        linhas.append("")
        linhas.append(f"Total de professores cadastrados: {len(professores)}")
        linhas.append("")
        
        for i, prof in enumerate(professores, 1):
            linhas.append(f"{i}. Professor: {prof.nome}")
            linhas.append(f"   CPF: {prof.cpf}")
            linhas.append(f"   Email: {prof.email}")
            linhas.append(f"   Telefone: {prof.telefone}")
            linhas.append(f"   Especialidade: {prof.especialidade}")
            linhas.append("")
        
        linhas.append("=" * 80)
        
        return "\n".join(linhas)
    
    def _relatorio_professores_csv(self, professores: List[Professor]) -> str:
        """Gera relatório de professores em formato CSV (com aspas corretas)"""
        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(["ID", "Nome", "CPF", "Email", "Telefone", "Especialidade"])
        for prof in professores:
            writer.writerow([prof.id, prof.nome, prof.cpf, prof.email, prof.telefone, prof.especialidade])
        return buf.getvalue().rstrip("\n")
    
    def gerar_relatorio_instituicoes(self, formato: str = "txt") -> str:
        """Gera relatório de todas as instituições cadastradas"""
        instituicoes = self.db.listar_instituicoes()
        
        if formato == "txt":
            return self._relatorio_instituicoes_txt(instituicoes)
        elif formato == "csv":
            return self._relatorio_instituicoes_csv(instituicoes)
        return ""
    
    def _relatorio_instituicoes_txt(self, instituicoes: List[Instituicao]) -> str:
        """Gera relatório de instituições em formato TXT"""
        linhas: List[str] = []
        linhas.append("=" * 80)
        linhas.append("RELATÓRIO DE INSTITUIÇÕES DE ENSINO")
        linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("=" * 80)
        linhas.append("")
        linhas.append(f"Total de instituições cadastradas: {len(instituicoes)}")
        linhas.append("")
        
        for i, inst in enumerate(instituicoes, 1):
            linhas.append(f"{i}. Instituição: {inst.nome}")
            linhas.append(f"   CNPJ: {inst.cnpj}")
            linhas.append(f"   Endereço: {inst.endereco}")
            linhas.append(f"   Cidade/Estado: {inst.cidade}/{inst.estado}")
            linhas.append("")
        
        linhas.append("=" * 80)
        
        return "\n".join(linhas)
    
    def _relatorio_instituicoes_csv(self, instituicoes: List[Instituicao]) -> str:
        """Gera relatório de instituições em formato CSV (com aspas corretas)"""
        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(["ID", "Nome", "CNPJ", "Endereco", "Cidade", "Estado"])
        for inst in instituicoes:
            writer.writerow([inst.id, inst.nome, inst.cnpj, inst.endereco, inst.cidade, inst.estado])
        return buf.getvalue().rstrip("\n")
    
    def gerar_relatorio_vagas(self, formato: str = "txt", filtro_status: Optional[str] = None) -> str:
        """Gera relatório de vagas"""
        vagas = self.db.listar_vagas()

        if filtro_status:
            vagas = [v for v in vagas if v.status == filtro_status]

        if formato == "txt":
            return self._relatorio_vagas_txt(vagas, filtro_status)
        elif formato == "csv":
            return self._relatorio_vagas_csv(vagas)
        return ""
    
    def _relatorio_vagas_txt(self, vagas: List[Vaga], filtro_status: Optional[str] = None) -> str:
        """Gera relatório de vagas em formato TXT"""
        linhas: List[str] = []
        linhas.append("=" * 80)
        titulo = "RELATÓRIO DE VAGAS"
        if filtro_status:
            titulo += f" - {filtro_status.upper()}"
        linhas.append(titulo)
        linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("=" * 80)
        linhas.append("")
        linhas.append(f"Total de vagas: {len(vagas)}")
        linhas.append("")
        
        for i, vaga in enumerate(vagas, 1):
            inst_nome = "N/A"
            if vaga.instituicao_id is not None:
                instituicao = self.db.buscar_instituicao(vaga.instituicao_id)
                inst_nome = instituicao.nome if instituicao else "N/A"
            
            linhas.append(f"{i}. Vaga: {vaga.disciplina}")
            linhas.append(f"   Instituição: {inst_nome}")
            linhas.append(f"   Carga Horária: {vaga.carga_horaria}h")
            linhas.append(f"   Salário: R$ {vaga.salario:.2f}")
            linhas.append(f"   Status: {vaga.status}")
            
            if vaga.professor_id:
                professor = self.db.buscar_professor(vaga.professor_id)
                prof_nome = professor.nome if professor else "N/A"
                linhas.append(f"   Professor: {prof_nome}")
            
            linhas.append(f"   Descrição: {vaga.descricao}")
            linhas.append(f"   Data de Cadastro: {vaga.data_cadastro}")
            linhas.append("")
        
        linhas.append("=" * 80)
        
        return "\n".join(linhas)
    
    def _relatorio_vagas_csv(self, vagas: List[Vaga]) -> str:
        """Gera relatório de vagas em formato CSV (com aspas corretas)"""
        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(["ID", "Instituicao_ID", "Disciplina", "Carga_Horaria", "Salario", "Status", "Professor_ID", "Data_Cadastro"])
        for vaga in vagas:
            writer.writerow([vaga.id, vaga.instituicao_id, vaga.disciplina, vaga.carga_horaria, vaga.salario, vaga.status, vaga.professor_id, vaga.data_cadastro])
        return buf.getvalue().rstrip("\n")
    
    def gerar_relatorio_completo(self) -> str:
        """Gera um relatório completo do sistema"""
        linhas: List[str] = []
        linhas.append("=" * 80)
        linhas.append("RELATÓRIO COMPLETO DO SISTEMA")
        linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("=" * 80)
        linhas.append("")
        
        # Estatísticas gerais
        professores = self.db.listar_professores()
        instituicoes = self.db.listar_instituicoes()
        vagas = self.db.listar_vagas()
        
        linhas.append("ESTATÍSTICAS GERAIS:")
        linhas.append(f"  - Total de Professores: {len(professores)}")
        linhas.append(f"  - Total de Instituições: {len(instituicoes)}")
        linhas.append(f"  - Total de Vagas: {len(vagas)}")
        
        vagas_abertas = len([v for v in vagas if v.status == "Aberta"])
        vagas_preenchidas = len([v for v in vagas if v.status == "Preenchida"])
        vagas_canceladas = len([v for v in vagas if v.status == "Cancelada"])
        
        linhas.append(f"  - Vagas Abertas: {vagas_abertas}")
        linhas.append(f"  - Vagas Preenchidas: {vagas_preenchidas}")
        linhas.append(f"  - Vagas Canceladas: {vagas_canceladas}")
        linhas.append("")
        
        # Especialidades mais demandadas
        especialidades: dict[str, int] = {}
        for vaga in vagas:
            if vaga.status == "Aberta":
                disc = vaga.disciplina
                especialidades[disc] = especialidades.get(disc, 0) + 1
        
        if especialidades:
            linhas.append("DISCIPLINAS COM VAGAS ABERTAS:")
            for disc, count in sorted(especialidades.items(), key=lambda x: x[1], reverse=True):
                linhas.append(f"  - {disc}: {count} vaga(s)")
            linhas.append("")
        
        linhas.append("=" * 80)
        
        return "\n".join(linhas)

    # === Novos relatórios especializados ===
    def gerar_resumo_demanda_por_disciplina(self, formato: str = "txt", somente_abertas: bool = False) -> str:
        """Resumo de demanda por disciplina (contagem de vagas por disciplina, opcionalmente apenas Abertas)."""
        vagas = self.db.listar_vagas()
        if somente_abertas:
            vagas = [v for v in vagas if v.status == "Aberta"]

        contagem: dict[str, int] = {}
        for v in vagas:
            contagem[v.disciplina] = contagem.get(v.disciplina, 0) + 1

        if formato == "csv":
            buf = StringIO()
            writer = csv.writer(buf)
            writer.writerow(["Disciplina", "Quantidade"])
            for disc, qtd in sorted(contagem.items(), key=lambda x: x[1], reverse=True):
                writer.writerow([disc, qtd])
            return buf.getvalue().rstrip("\n")

        linhas: List[str] = []
        linhas.append("=" * 80)
        titulo = "RESUMO DE DEMANDA POR DISCIPLINA"
        if somente_abertas:
            titulo += " - APENAS VAGAS ABERTAS"
        linhas.append(titulo)
        linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("=" * 80)
        for disc, qtd in sorted(contagem.items(), key=lambda x: x[1], reverse=True):
            linhas.append(f"- {disc}: {qtd} vaga(s)")
        return "\n".join(linhas)

    def gerar_aging_vagas_abertas(self, formato: str = "txt") -> str:
        """Relatório de aging das vagas Abertas (há quantos dias estão abertas)."""
        vagas = [v for v in self.db.listar_vagas() if v.status == "Aberta"]

        def _dias_aberta(data_str: str) -> int:
            try:
                dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                return max(0, (datetime.now() - dt).days)
            except Exception:
                return 0

        linhas_dados = [
            (v.id, v.disciplina, v.instituicao_id, _dias_aberta(v.data_cadastro))
            for v in vagas
        ]
        linhas_dados.sort(key=lambda x: x[3], reverse=True)

        if formato == "csv":
            buf = StringIO()
            writer = csv.writer(buf)
            writer.writerow(["Vaga_ID", "Disciplina", "Instituicao_ID", "Dias_Aberta"])
            writer.writerows(linhas_dados)
            return buf.getvalue().rstrip("\n")

        linhas: List[str] = []
        linhas.append("=" * 80)
        linhas.append("AGING DE VAGAS ABERTAS (dias abertas)")
        linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("=" * 80)
        for (vaga_id, disc, inst_id, dias) in linhas_dados:
            linhas.append(f"Vaga {vaga_id} | {disc} | Inst {inst_id} | {dias} dia(s)")
        return "\n".join(linhas)

    def gerar_salarios_por_disciplina(self, formato: str = "txt") -> str:
        """Estatísticas de salários por disciplina (min/média/máx)."""
        vagas = self.db.listar_vagas()
        grupos: dict[str, list[float]] = {}
        for v in vagas:
            grupos.setdefault(v.disciplina, []).append(float(v.salario))

        stats: list[tuple[str, int, float, float, float]] = []  # (disc, count, min, avg, max)
        for disc, valores in grupos.items():
            if valores:
                mmin = min(valores)
                mmax = max(valores)
                media = sum(valores) / len(valores)
                stats.append((disc, len(valores), mmin, media, mmax))
        stats.sort(key=lambda x: x[4], reverse=True)

        if formato == "csv":
            buf = StringIO()
            writer = csv.writer(buf)
            writer.writerow(["Disciplina", "Qtd", "Salario_Min", "Salario_Medio", "Salario_Max"])
            for disc, qtd, mmin, media, mmax in stats:
                writer.writerow([disc, qtd, f"{mmin:.2f}", f"{media:.2f}", f"{mmax:.2f}"])
            return buf.getvalue().rstrip("\n")

        linhas: List[str] = []
        linhas.append("=" * 80)
        linhas.append("SALÁRIOS POR DISCIPLINA (min/médio/máx)")
        linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append("=" * 80)
        for disc, qtd, mmin, media, mmax in stats:
            linhas.append(f"- {disc}: qtd={qtd}, min=R$ {mmin:.2f}, médio=R$ {media:.2f}, máx=R$ {mmax:.2f}")
        return "\n".join(linhas)
    
    def salvar_relatorio(self, conteudo: str, nome_arquivo: str):
        """Salva o relatório em arquivo dentro da pasta 'output/'"""
        try:
            out_dir = os.path.join(os.getcwd(), 'output')
            os.makedirs(out_dir, exist_ok=True)
            destino = os.path.join(out_dir, nome_arquivo)
            with open(destino, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            return True
        except Exception as e:
            print(f"Erro ao salvar relatório: {e}")
            return False
