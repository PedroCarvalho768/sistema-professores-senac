# -*- coding: utf-8 -*-
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportUnknownParameterType=false
"""
Interface Gráfica com Raylib para o Sistema de Professores Substitutos
"""

import os
import pyray as rl
from typing import List, Optional
from .database import Database
from .models import Professor, Instituicao, Vaga
from .reports import ReportGenerator

class GUI:
    """Classe principal da interface gráfica"""
    
    def __init__(self, database: Database):
        self.db = database
        self.report_gen = ReportGenerator(database)
        
        # Configurações da janela
        self.width = 1000
        self.height = 700
        
        # Fonte personalizada (Helvetica)
        self.font = None
        self.font_base_size = 32  # tamanho base de carga (podemos desenhar em tamanhos menores)
        self.font_spacing = 1
        
        # Estado da aplicação
        self.tela_atual = "menu_principal"
        self.mensagem = ""
        self.mensagem_tempo = 0
        
        # Campos de formulário
        self.campos: dict[str, str] = {}
        self.campo_ativo: Optional[str] = None
        
        # Listas para exibição
        self.professores_lista: List[Professor] = []
        self.instituicoes_lista: List[Instituicao] = []
        self.vagas_lista: List[Vaga] = []
        self.scroll_offset = 0
        
        # Paleta de cores fornecida
        # 11,5,0 | 254,94,65 | 243,193,120 | 216,241,160 | 0,168,120
        self.cor_escura = rl.Color(36, 27, 20, 255)
        self.cor_acento = rl.Color(254, 94, 65, 255)
        self.cor_areia = rl.Color(243, 193, 120, 255)
        self.cor_verde_claro = rl.Color(216, 241, 160, 255)
        self.cor_verde = rl.Color(0, 168, 120, 255)

        # Mapeamento para UI (layout mais clean/sleek)
        # Dark mode: fundo escuro para reduzir brilho; texto/heading claros
        self.cor_fundo = rl.Color(18, 18, 18, 255)
        self.cor_primaria = rl.WHITE            # títulos/heading text
        self.cor_secundaria = self.cor_verde    # linhas/acentos discretos
        self.cor_sucesso = self.cor_verde       # mensagens de sucesso
        self.cor_erro = self.cor_acento         # mensagens de erro
        self.cor_texto = rl.WHITE               # texto geral
        self.cor_botao = self.cor_verde         # botão principal
        self.cor_botao_hover = rl.color_alpha(self.cor_verde, 0.85)
    
    def inicializar(self):
        """Inicializa a janela do Raylib"""
        rl.init_window(self.width, self.height, "Sistema de Professores Substitutos")
        rl.set_target_fps(60)
        # Carregar fonte Helvetica se disponível
        # Busca por Helvetica.ttf em múltiplos locais comuns
        font_candidates = [
            os.path.join(os.getcwd(), "Helvetica.ttf"),
            os.path.join(os.getcwd(), "assets", "Helvetica.ttf"),
            os.path.join(os.getcwd(), "assets", "fonts", "Helvetica.ttf"),
        ]
        self.font = None
        for path in font_candidates:
            try:
                if os.path.exists(path):
                    self.font = rl.load_font_ex(path, self.font_base_size, None, 0)
                    break
            except Exception:
                self.font = None
    
    def executar(self):
        """Loop principal da aplicação"""
        while not rl.window_should_close():
            self.processar_input()
            self.atualizar()
            self.desenhar()
        
        rl.close_window()
    
    def processar_input(self):
        """Processa input do teclado e mouse"""
        # Processar digitação nos campos de texto
        if self.campo_ativo:
            key = rl.get_char_pressed()
            while key > 0:
                if 32 <= key <= 125:  # Caracteres imprimíveis
                    self.campos[self.campo_ativo] += chr(key)
                key = rl.get_char_pressed()
            
            # Backspace
            if rl.is_key_pressed(rl.KeyboardKey.KEY_BACKSPACE) and len(self.campos.get(self.campo_ativo, "")) > 0:
                self.campos[self.campo_ativo] = self.campos[self.campo_ativo][:-1]
        
        # Scroll com mouse wheel
        wheel = rl.get_mouse_wheel_move()
        if wheel != 0:
            self.scroll_offset -= int(wheel * 30)
            if self.scroll_offset < 0:
                self.scroll_offset = 0
    
    def atualizar(self):
        """Atualiza o estado da aplicação"""
        # Atualizar tempo da mensagem
        if self.mensagem_tempo > 0:
            self.mensagem_tempo -= rl.get_frame_time()
            if self.mensagem_tempo <= 0:
                self.mensagem = ""
    
    def desenhar(self):
        """Desenha a interface"""
        rl.begin_drawing()
        rl.clear_background(self.cor_fundo)
        
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
        
        rl.end_drawing()
    
    def desenhar_titulo(self, texto: str):
        """Desenha o título da página (minimalista, sem barra sólida)"""
        # Título escuro
        self.draw_text_ui(texto, 20, 22, 30, self.cor_primaria)
        # Linha sutil abaixo do título
        rl.draw_line(20, 64, self.width - 20, 64, rl.color_alpha(self.cor_secundaria, 0.5))
    
    def desenhar_botao(self, texto: str, x: int, y: int, largura: int, altura: int) -> bool:
        """Desenha um botão e retorna True se foi clicado"""
        mouse_pos = rl.get_mouse_position()
        rect = rl.Rectangle(x, y, largura, altura)
        
        hover = rl.check_collision_point_rec(mouse_pos, rect)
        fill = self.cor_botao_hover if hover else self.cor_botao
        
        # Botão arredondado com borda sutil
        rl.draw_rectangle_rounded(rect, 0.2, 8, fill)
        rl.draw_rectangle_rounded_lines(rect, 0.2, 8, rl.color_alpha(self.cor_texto, 0.18))
        
        texto_largura = self.measure_text_ui(texto, 20)
        self.draw_text_ui(texto, x + (largura - texto_largura) // 2, y + (altura - 20) // 2, 20, rl.WHITE)
        
        return hover and rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT)
    
    def desenhar_campo_texto(self, label: str, campo_id: str, x: int, y: int, largura: int) -> str:
        """Desenha um campo de texto e retorna o valor"""
        # Label
        self.draw_text_ui(label, x, y, 20, self.cor_texto)
        
        # Campo
        campo_y = y + 25
        rect = rl.Rectangle(x, campo_y, largura, 35)
        
        # Verificar clique no campo
        mouse_pos = rl.get_mouse_position()
        if rl.check_collision_point_rec(mouse_pos, rect) and rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            self.campo_ativo = campo_id
        
        # Campo arredondado com preenchimento sutil e borda conforme foco
        ativo = self.campo_ativo == campo_id
        fill_campo = rl.color_alpha(self.cor_secundaria, 0.04)
        borda = self.cor_secundaria if ativo else rl.color_alpha(self.cor_texto, 0.20)
        rl.draw_rectangle_rounded(rect, 0.12, 8, fill_campo)
        rl.draw_rectangle_rounded_lines(rect, 0.12, 8, borda)
        
        # Texto do campo
        if campo_id not in self.campos:
            self.campos[campo_id] = ""
        
        texto = self.campos[campo_id]
        self.draw_text_ui(texto, x + 10, campo_y + 8, 20, self.cor_texto)
        
        # Cursor piscante
        if self.campo_ativo == campo_id and int(rl.get_time() * 2) % 2 == 0:
            cursor_x = x + 10 + self.measure_text_ui(texto, 20)
            rl.draw_line(cursor_x, campo_y + 5, cursor_x, campo_y + 30, self.cor_texto)
        
        return texto
    
    def desenhar_mensagem(self):
        """Desenha mensagem de feedback (pill discreta)"""
        cor_base = self.cor_sucesso if "sucesso" in self.mensagem.lower() else self.cor_erro
        bg = rl.color_alpha(cor_base, 0.95)
        texto_w = self.measure_text_ui(self.mensagem, 20)
        pad_x, pad_y = 16, 10
        pill_h = 38
        pill_w = texto_w + pad_x * 2
        x = 20
        y = self.height - pill_h - pad_y
        rect = rl.Rectangle(x, y, pill_w, pill_h)
        rl.draw_rectangle_rounded(rect, 0.5, 12, bg)
        self.draw_text_ui(self.mensagem, x + pad_x, y + (pill_h - 20) // 2, 20, rl.WHITE)

    # ===== Helpers de texto com fonte personalizada =====
    def _to_bytes(self, s: str) -> bytes:
        # Mantido para compatibilidade futura; não é usado com draw_text_ex nas stubs atuais
        return s.encode('utf-8', errors='ignore')

    def draw_text_ui(self, texto: str, x: int, y: int, tamanho: int, cor: rl.Color):
        if self.font:
            rl.draw_text_ex(self.font, texto, rl.Vector2(x, y), float(tamanho), float(self.font_spacing), cor)
        else:
            rl.draw_text(texto, x, y, tamanho, cor)

    def measure_text_ui(self, texto: str, tamanho: int) -> int:
        if self.font:
            size = rl.measure_text_ex(self.font, texto, float(tamanho), float(self.font_spacing))
            return int(size.x)
        else:
            return rl.measure_text(texto, tamanho)
    
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
                card = rl.Rectangle(20, y, self.width - 40, 100)
                rl.draw_rectangle_rounded(card, 0.06, 8, rl.color_alpha(self.cor_secundaria, 0.06))
                rl.draw_rectangle_rounded_lines(card, 0.06, 8, rl.color_alpha(self.cor_texto, 0.15))
                
                self.draw_text_ui(f"Nome: {prof.nome}", 30, y + 10, 20, self.cor_texto)
                self.draw_text_ui(f"CPF: {prof.cpf}", 30, y + 35, 18, self.cor_texto)
                self.draw_text_ui(f"Email: {prof.email}", 30, y + 58, 18, self.cor_texto)
                self.draw_text_ui(f"Especialidade: {prof.especialidade}", 400, y + 35, 18, self.cor_texto)
            
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
                card = rl.Rectangle(20, y, self.width - 40, 100)
                rl.draw_rectangle_rounded(card, 0.06, 8, rl.color_alpha(self.cor_secundaria, 0.06))
                rl.draw_rectangle_rounded_lines(card, 0.06, 8, rl.color_alpha(self.cor_texto, 0.15))
                
                self.draw_text_ui(f"Nome: {inst.nome}", 30, y + 10, 20, self.cor_texto)
                self.draw_text_ui(f"CNPJ: {inst.cnpj}", 30, y + 35, 18, self.cor_texto)
                self.draw_text_ui(f"Endereco: {inst.endereco}", 30, y + 58, 18, self.cor_texto)
                self.draw_text_ui(f"Cidade/UF: {inst.cidade}/{inst.estado}", 30, y + 78, 18, self.cor_texto)
            
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
                card = rl.Rectangle(20, y, self.width - 40, 120)
                rl.draw_rectangle_rounded(card, 0.06, 8, rl.color_alpha(self.cor_secundaria, 0.06))
                rl.draw_rectangle_rounded_lines(card, 0.06, 8, rl.color_alpha(self.cor_texto, 0.15))
                
                self.draw_text_ui(f"Disciplina: {vaga.disciplina}", 30, y + 10, 20, self.cor_texto)
                self.draw_text_ui(f"Carga: {vaga.carga_horaria}h", 30, y + 35, 18, self.cor_texto)
                self.draw_text_ui(f"Salario: R$ {vaga.salario:.2f}", 200, y + 35, 18, self.cor_texto)
                self.draw_text_ui(f"Status: {vaga.status}", 400, y + 35, 18, self.cor_texto)
                self.draw_text_ui(f"Desc: {vaga.descricao[:50]}...", 30, y + 58, 16, self.cor_texto)
            
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
