# -*- coding: utf-8 -*-
"""
Interface Gráfica com Raylib para o Sistema de Professores Substitutos
"""

from pyray import *
from typing import List, Optional
from database import Database
from models import Professor, Instituicao, Vaga
from reports import ReportGenerator

class GUI:
    """Classe principal da interface gráfica"""
    
    def __init__(self, database: Database):
        self.db = database
        self.report_gen = ReportGenerator(database)
        
        # Configurações da janela
        self.width = 1000
        self.height = 700
        
        # Estado da aplicação
        self.tela_atual = "menu_principal"
        self.mensagem = ""
        self.mensagem_tempo = 0
        
        # Campos de formulário
        self.campos = {}
        self.campo_ativo = None
        
        # Listas para exibição
        self.professores_lista = []
        self.instituicoes_lista = []
        self.vagas_lista = []
        self.scroll_offset = 0
        
        # Cores
        self.cor_fundo = Color(245, 245, 245, 255)
        self.cor_primaria = Color(41, 128, 185, 255)
        self.cor_secundaria = Color(52, 152, 219, 255)
        self.cor_sucesso = Color(39, 174, 96, 255)
        self.cor_erro = Color(231, 76, 60, 255)
        self.cor_texto = Color(44, 62, 80, 255)
        self.cor_botao = Color(52, 73, 94, 255)
        self.cor_botao_hover = Color(44, 62, 80, 255)
    
    def inicializar(self):
        """Inicializa a janela do Raylib"""
        init_window(self.width, self.height, b"Sistema de Professores Substitutos")
        set_target_fps(60)
    
    def executar(self):
        """Loop principal da aplicação"""
        while not window_should_close():
            self.processar_input()
            self.atualizar()
            self.desenhar()
        
        close_window()
    
    def processar_input(self):
        """Processa input do teclado e mouse"""
        # Processar digitação nos campos de texto
        if self.campo_ativo:
            key = get_char_pressed()
            while key > 0:
                if 32 <= key <= 125:  # Caracteres imprimíveis
                    self.campos[self.campo_ativo] += chr(key)
                key = get_char_pressed()
            
            # Backspace
            if is_key_pressed(KEY_BACKSPACE) and len(self.campos.get(self.campo_ativo, "")) > 0:
                self.campos[self.campo_ativo] = self.campos[self.campo_ativo][:-1]
        
        # Scroll com mouse wheel
        wheel = get_mouse_wheel_move()
        if wheel != 0:
            self.scroll_offset -= int(wheel * 30)
            if self.scroll_offset < 0:
                self.scroll_offset = 0
    
    def atualizar(self):
        """Atualiza o estado da aplicação"""
        # Atualizar tempo da mensagem
        if self.mensagem_tempo > 0:
            self.mensagem_tempo -= get_frame_time()
            if self.mensagem_tempo <= 0:
                self.mensagem = ""
    
    def desenhar(self):
        """Desenha a interface"""
        begin_drawing()
        clear_background(self.cor_fundo)
        
        # Desenhar tela atual
        if self.tela_atual == "menu_principal":
            self.desenhar_menu_principal()
        elif self.tela_atual == "cadastro_professor":
            self.desenhar_cadastro_professor()
        elif self.tela_atual == "lista_professores":
            self.desenhar_lista_professores()
        elif self.tela_atual == "cadastro_instituicao":
            self.desenhar_cadastro_instituicao()
        elif self.tela_atual == "lista_instituicoes":
            self.desenhar_lista_instituicoes()
        elif self.tela_atual == "cadastro_vaga":
            self.desenhar_cadastro_vaga()
        elif self.tela_atual == "lista_vagas":
            self.desenhar_lista_vagas()
        elif self.tela_atual == "relatorios":
            self.desenhar_menu_relatorios()
        
        # Desenhar mensagem (se houver)
        if self.mensagem:
            self.desenhar_mensagem()
        
        end_drawing()
    
    def desenhar_titulo(self, texto: str):
        """Desenha o título da página"""
        draw_rectangle(0, 0, self.width, 80, self.cor_primaria)
        texto_bytes = texto.encode('latin1', errors='replace')
        draw_text(texto_bytes, 20, 25, 30, WHITE)
    
    def desenhar_botao(self, texto: str, x: int, y: int, largura: int, altura: int) -> bool:
        """Desenha um botão e retorna True se foi clicado"""
        mouse_pos = get_mouse_position()
        rect = Rectangle(x, y, largura, altura)
        
        hover = check_collision_point_rec(mouse_pos, rect)
        cor = self.cor_botao_hover if hover else self.cor_botao
        
        draw_rectangle_rec(rect, cor)
        draw_rectangle_lines_ex(rect, 2, self.cor_texto)
        
        texto_bytes = texto.encode('latin1', errors='replace')
        texto_largura = measure_text(texto_bytes, 20)
        draw_text(texto_bytes, x + (largura - texto_largura) // 2, y + (altura - 20) // 2, 20, WHITE)
        
        return hover and is_mouse_button_pressed(MOUSE_LEFT_BUTTON)
    
    def desenhar_campo_texto(self, label: str, campo_id: str, x: int, y: int, largura: int) -> str:
        """Desenha um campo de texto e retorna o valor"""
        # Label
        label_bytes = label.encode('latin1', errors='replace')
        draw_text(label_bytes, x, y, 20, self.cor_texto)
        
        # Campo
        campo_y = y + 25
        rect = Rectangle(x, campo_y, largura, 35)
        
        # Verificar clique no campo
        mouse_pos = get_mouse_position()
        if check_collision_point_rec(mouse_pos, rect) and is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            self.campo_ativo = campo_id
        
        # Cor do campo
        cor_campo = self.cor_secundaria if self.campo_ativo == campo_id else WHITE
        draw_rectangle_rec(rect, cor_campo)
        draw_rectangle_lines_ex(rect, 2, self.cor_texto)
        
        # Texto do campo
        if campo_id not in self.campos:
            self.campos[campo_id] = ""
        
        texto = self.campos[campo_id]
        texto_bytes = texto.encode('latin1', errors='replace')
        draw_text(texto_bytes, x + 10, campo_y + 8, 20, self.cor_texto)
        
        # Cursor piscante
        if self.campo_ativo == campo_id and int(get_time() * 2) % 2 == 0:
            cursor_x = x + 10 + measure_text(texto_bytes, 20)
            draw_line(cursor_x, campo_y + 5, cursor_x, campo_y + 30, self.cor_texto)
        
        return texto
    
    def desenhar_mensagem(self):
        """Desenha mensagem de feedback"""
        cor = self.cor_sucesso if "sucesso" in self.mensagem.lower() else self.cor_erro
        draw_rectangle(0, self.height - 60, self.width, 60, cor)
        msg_bytes = self.mensagem.encode('latin1', errors='replace')
        draw_text(msg_bytes, 20, self.height - 40, 20, WHITE)
    
    def mostrar_mensagem(self, texto: str, tempo: float = 3.0):
        """Mostra uma mensagem temporária"""
        self.mensagem = texto
        self.mensagem_tempo = tempo
    
    # ===== MENU PRINCIPAL =====
    
    def desenhar_menu_principal(self):
        """Desenha o menu principal"""
        self.desenhar_titulo("Sistema de Professores Substitutos - Menu Principal")
        
        y_inicial = 120
        espacamento = 70
        
        if self.desenhar_botao("Cadastrar Professor", 350, y_inicial, 300, 50):
            self.tela_atual = "cadastro_professor"
            self.limpar_campos()
        
        if self.desenhar_botao("Listar Professores", 350, y_inicial + espacamento, 300, 50):
            self.professores_lista = self.db.listar_professores()
            self.scroll_offset = 0
            self.tela_atual = "lista_professores"
        
        if self.desenhar_botao("Cadastrar Instituicao", 350, y_inicial + espacamento * 2, 300, 50):
            self.tela_atual = "cadastro_instituicao"
            self.limpar_campos()
        
        if self.desenhar_botao("Listar Instituicoes", 350, y_inicial + espacamento * 3, 300, 50):
            self.instituicoes_lista = self.db.listar_instituicoes()
            self.scroll_offset = 0
            self.tela_atual = "lista_instituicoes"
        
        if self.desenhar_botao("Cadastrar Vaga", 350, y_inicial + espacamento * 4, 300, 50):
            self.tela_atual = "cadastro_vaga"
            self.limpar_campos()
        
        if self.desenhar_botao("Listar Vagas", 350, y_inicial + espacamento * 5, 300, 50):
            self.vagas_lista = self.db.listar_vagas()
            self.scroll_offset = 0
            self.tela_atual = "lista_vagas"
        
        if self.desenhar_botao("Relatorios", 350, y_inicial + espacamento * 6, 300, 50):
            self.tela_atual = "relatorios"
    
    # ===== CADASTRO DE PROFESSOR =====
    
    def desenhar_cadastro_professor(self):
        """Desenha o formulário de cadastro de professor"""
        self.desenhar_titulo("Cadastro de Professor")
        
        x = 50
        y = 120
        largura = 400
        
        self.desenhar_campo_texto("Nome:", "prof_nome", x, y, largura)
        self.desenhar_campo_texto("CPF:", "prof_cpf", x, y + 80, largura)
        self.desenhar_campo_texto("Email:", "prof_email", x, y + 160, largura)
        self.desenhar_campo_texto("Telefone:", "prof_telefone", x, y + 240, largura)
        self.desenhar_campo_texto("Especialidade:", "prof_especialidade", x, y + 320, largura)
        
        # Botões
        if self.desenhar_botao("Salvar", x, y + 420, 150, 40):
            self.salvar_professor()
        
        if self.desenhar_botao("Voltar", x + 170, y + 420, 150, 40):
            self.tela_atual = "menu_principal"
            self.limpar_campos()
    
    def salvar_professor(self):
        """Salva um novo professor"""
        try:
            professor = Professor(
                nome=self.campos.get("prof_nome", ""),
                cpf=self.campos.get("prof_cpf", ""),
                email=self.campos.get("prof_email", ""),
                telefone=self.campos.get("prof_telefone", ""),
                especialidade=self.campos.get("prof_especialidade", "")
            )
            
            if not professor.nome or not professor.cpf:
                self.mostrar_mensagem("Nome e CPF sao obrigatorios!")
                return
            
            self.db.inserir_professor(professor)
            self.mostrar_mensagem("Professor cadastrado com sucesso!")
            self.limpar_campos()
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao cadastrar: {str(e)}")
    
    # ===== LISTA DE PROFESSORES =====
    
    def desenhar_lista_professores(self):
        """Desenha a lista de professores"""
        self.desenhar_titulo("Lista de Professores")
        
        if self.desenhar_botao("Voltar", 850, 20, 120, 40):
            self.tela_atual = "menu_principal"
            return
        
        y = 100 - self.scroll_offset
        
        for prof in self.professores_lista:
            if y > 80 and y < self.height - 100:
                draw_rectangle(20, y, self.width - 40, 100, WHITE)
                draw_rectangle_lines(20, y, self.width - 40, 100, self.cor_texto)
                
                nome_bytes = f"Nome: {prof.nome}".encode('latin1', errors='replace')
                cpf_bytes = f"CPF: {prof.cpf}".encode('latin1', errors='replace')
                email_bytes = f"Email: {prof.email}".encode('latin1', errors='replace')
                esp_bytes = f"Especialidade: {prof.especialidade}".encode('latin1', errors='replace')
                
                draw_text(nome_bytes, 30, y + 10, 20, self.cor_texto)
                draw_text(cpf_bytes, 30, y + 35, 18, self.cor_texto)
                draw_text(email_bytes, 30, y + 58, 18, self.cor_texto)
                draw_text(esp_bytes, 400, y + 35, 18, self.cor_texto)
            
            y += 110
    
    # ===== CADASTRO DE INSTITUIÇÃO =====
    
    def desenhar_cadastro_instituicao(self):
        """Desenha o formulário de cadastro de instituição"""
        self.desenhar_titulo("Cadastro de Instituicao")
        
        x = 50
        y = 120
        largura = 400
        
        self.desenhar_campo_texto("Nome:", "inst_nome", x, y, largura)
        self.desenhar_campo_texto("CNPJ:", "inst_cnpj", x, y + 80, largura)
        self.desenhar_campo_texto("Endereco:", "inst_endereco", x, y + 160, largura)
        self.desenhar_campo_texto("Cidade:", "inst_cidade", x, y + 240, largura)
        self.desenhar_campo_texto("Estado:", "inst_estado", x, y + 320, largura)
        
        if self.desenhar_botao("Salvar", x, y + 420, 150, 40):
            self.salvar_instituicao()
        
        if self.desenhar_botao("Voltar", x + 170, y + 420, 150, 40):
            self.tela_atual = "menu_principal"
            self.limpar_campos()
    
    def salvar_instituicao(self):
        """Salva uma nova instituição"""
        try:
            instituicao = Instituicao(
                nome=self.campos.get("inst_nome", ""),
                cnpj=self.campos.get("inst_cnpj", ""),
                endereco=self.campos.get("inst_endereco", ""),
                cidade=self.campos.get("inst_cidade", ""),
                estado=self.campos.get("inst_estado", "")
            )
            
            if not instituicao.nome or not instituicao.cnpj:
                self.mostrar_mensagem("Nome e CNPJ sao obrigatorios!")
                return
            
            self.db.inserir_instituicao(instituicao)
            self.mostrar_mensagem("Instituicao cadastrada com sucesso!")
            self.limpar_campos()
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao cadastrar: {str(e)}")
    
    # ===== LISTA DE INSTITUIÇÕES =====
    
    def desenhar_lista_instituicoes(self):
        """Desenha a lista de instituições"""
        self.desenhar_titulo("Lista de Instituicoes")
        
        if self.desenhar_botao("Voltar", 850, 20, 120, 40):
            self.tela_atual = "menu_principal"
            return
        
        y = 100 - self.scroll_offset
        
        for inst in self.instituicoes_lista:
            if y > 80 and y < self.height - 100:
                draw_rectangle(20, y, self.width - 40, 100, WHITE)
                draw_rectangle_lines(20, y, self.width - 40, 100, self.cor_texto)
                
                nome_bytes = f"Nome: {inst.nome}".encode('latin1', errors='replace')
                cnpj_bytes = f"CNPJ: {inst.cnpj}".encode('latin1', errors='replace')
                end_bytes = f"Endereco: {inst.endereco}".encode('latin1', errors='replace')
                cid_bytes = f"Cidade/UF: {inst.cidade}/{inst.estado}".encode('latin1', errors='replace')
                
                draw_text(nome_bytes, 30, y + 10, 20, self.cor_texto)
                draw_text(cnpj_bytes, 30, y + 35, 18, self.cor_texto)
                draw_text(end_bytes, 30, y + 58, 18, self.cor_texto)
                draw_text(cid_bytes, 30, y + 78, 18, self.cor_texto)
            
            y += 110
    
    # ===== CADASTRO DE VAGA =====
    
    def desenhar_cadastro_vaga(self):
        """Desenha o formulário de cadastro de vaga"""
        self.desenhar_titulo("Cadastro de Vaga")
        
        x = 50
        y = 120
        largura = 400
        
        self.desenhar_campo_texto("ID da Instituicao:", "vaga_inst_id", x, y, largura)
        self.desenhar_campo_texto("Disciplina:", "vaga_disciplina", x, y + 80, largura)
        self.desenhar_campo_texto("Carga Horaria:", "vaga_carga", x, y + 160, largura)
        self.desenhar_campo_texto("Salario:", "vaga_salario", x, y + 240, largura)
        self.desenhar_campo_texto("Descricao:", "vaga_descricao", x, y + 320, largura)
        
        if self.desenhar_botao("Salvar", x, y + 420, 150, 40):
            self.salvar_vaga()
        
        if self.desenhar_botao("Voltar", x + 170, y + 420, 150, 40):
            self.tela_atual = "menu_principal"
            self.limpar_campos()
    
    def salvar_vaga(self):
        """Salva uma nova vaga"""
        try:
            vaga = Vaga(
                instituicao_id=int(self.campos.get("vaga_inst_id", "0")),
                disciplina=self.campos.get("vaga_disciplina", ""),
                carga_horaria=int(self.campos.get("vaga_carga", "0")),
                salario=float(self.campos.get("vaga_salario", "0")),
                descricao=self.campos.get("vaga_descricao", ""),
                status="Aberta"
            )
            
            if not vaga.disciplina or vaga.instituicao_id == 0:
                self.mostrar_mensagem("Disciplina e ID da instituicao sao obrigatorios!")
                return
            
            self.db.inserir_vaga(vaga)
            self.mostrar_mensagem("Vaga cadastrada com sucesso!")
            self.limpar_campos()
        except ValueError:
            self.mostrar_mensagem("Erro: Verifique os valores numericos!")
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao cadastrar: {str(e)}")
    
    # ===== LISTA DE VAGAS =====
    
    def desenhar_lista_vagas(self):
        """Desenha a lista de vagas"""
        self.desenhar_titulo("Lista de Vagas")
        
        if self.desenhar_botao("Voltar", 850, 20, 120, 40):
            self.tela_atual = "menu_principal"
            return
        
        y = 100 - self.scroll_offset
        
        for vaga in self.vagas_lista:
            if y > 80 and y < self.height - 100:
                draw_rectangle(20, y, self.width - 40, 120, WHITE)
                draw_rectangle_lines(20, y, self.width - 40, 120, self.cor_texto)
                
                disc_bytes = f"Disciplina: {vaga.disciplina}".encode('latin1', errors='replace')
                carga_bytes = f"Carga: {vaga.carga_horaria}h".encode('latin1', errors='replace')
                sal_bytes = f"Salario: R$ {vaga.salario:.2f}".encode('latin1', errors='replace')
                status_bytes = f"Status: {vaga.status}".encode('latin1', errors='replace')
                desc_bytes = f"Desc: {vaga.descricao[:50]}...".encode('latin1', errors='replace')
                
                draw_text(disc_bytes, 30, y + 10, 20, self.cor_texto)
                draw_text(carga_bytes, 30, y + 35, 18, self.cor_texto)
                draw_text(sal_bytes, 200, y + 35, 18, self.cor_texto)
                draw_text(status_bytes, 400, y + 35, 18, self.cor_texto)
                draw_text(desc_bytes, 30, y + 58, 16, self.cor_texto)
            
            y += 130
    
    # ===== RELATÓRIOS =====
    
    def desenhar_menu_relatorios(self):
        """Desenha o menu de relatórios"""
        self.desenhar_titulo("Relatorios")
        
        y_inicial = 120
        espacamento = 70
        
        if self.desenhar_botao("Relatorio de Professores", 300, y_inicial, 400, 50):
            self.gerar_relatorio("professores")
        
        if self.desenhar_botao("Relatorio de Instituicoes", 300, y_inicial + espacamento, 400, 50):
            self.gerar_relatorio("instituicoes")
        
        if self.desenhar_botao("Relatorio de Vagas", 300, y_inicial + espacamento * 2, 400, 50):
            self.gerar_relatorio("vagas")
        
        if self.desenhar_botao("Relatorio Completo", 300, y_inicial + espacamento * 3, 400, 50):
            self.gerar_relatorio("completo")
        
        if self.desenhar_botao("Voltar", 300, y_inicial + espacamento * 5, 400, 50):
            self.tela_atual = "menu_principal"
    
    def gerar_relatorio(self, tipo: str):
        """Gera e salva um relatório"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if tipo == "professores":
                conteudo = self.report_gen.gerar_relatorio_professores("txt")
                nome_arquivo = f"relatorio_professores_{timestamp}.txt"
            elif tipo == "instituicoes":
                conteudo = self.report_gen.gerar_relatorio_instituicoes("txt")
                nome_arquivo = f"relatorio_instituicoes_{timestamp}.txt"
            elif tipo == "vagas":
                conteudo = self.report_gen.gerar_relatorio_vagas("txt")
                nome_arquivo = f"relatorio_vagas_{timestamp}.txt"
            elif tipo == "completo":
                conteudo = self.report_gen.gerar_relatorio_completo()
                nome_arquivo = f"relatorio_completo_{timestamp}.txt"
            else:
                return
            
            self.report_gen.salvar_relatorio(conteudo, nome_arquivo)
            self.mostrar_mensagem(f"Relatorio salvo: {nome_arquivo}")
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao gerar relatorio: {str(e)}")
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.campos = {}
        self.campo_ativo = None
