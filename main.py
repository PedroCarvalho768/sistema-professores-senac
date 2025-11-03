# -*- coding: utf-8 -*-
"""
Sistema de Cadastro de Professores Substitutos
Aplicativo com interface gráfica usando Raylib

Autor: Sistema de Gestão Acadêmica
Data: Novembro 2025
"""

from app.database import Database
from app.gui import GUI

def main():
    """Função principal do aplicativo"""
    print("Iniciando Sistema de Professores Substitutos...")
    
    # Inicializar banco de dados (usar caminho padrão em data/)
    db = Database()
    print("Banco de dados inicializado!")
    
    # Inicializar interface gráfica
    gui = GUI(db)
    gui.inicializar()
    print("Interface gráfica iniciada!")
    
    # Executar aplicação
    gui.executar()
    
    print("Sistema encerrado.")

if __name__ == "__main__":
    main()
