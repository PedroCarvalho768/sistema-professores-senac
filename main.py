# -*- coding: utf-8 -*-
"""
Sistema de Cadastro de Professores Substitutos
Aplicativo com interface gráfica usando Raylib

Autor: Sistema de Gestão Acadêmica
Data: Novembro 2025
"""

from database import Database
from gui import GUI

def main():
    """Função principal do aplicativo"""
    print("Iniciando Sistema de Professores Substitutos...")
    
    # Inicializar banco de dados
    db = Database("sistema_professores.db")
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
