# -*- coding: utf-8 -*-
"""
Pacote principal do sistema de Professores Substitutos.

Exporta classes centrais para facilitar importações a partir de `app`.
"""

from .database import Database
from .models import Professor, Instituicao, Vaga
from .reports import ReportGenerator
from .gui import GUI

__all__ = [
    "Database",
    "Professor",
    "Instituicao",
    "Vaga",
    "ReportGenerator",
    "GUI",
]
