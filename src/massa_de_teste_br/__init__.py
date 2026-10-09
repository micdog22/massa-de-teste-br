"""Massa de Teste BR: dados brasileiros fictícios para testes e desenvolvimento."""

from .generators import COMPANY_FIELDS, PERSON_FIELDS, Generator, generate_companies, generate_people

__version__ = "1.0.0"

__all__ = [
    "COMPANY_FIELDS",
    "PERSON_FIELDS",
    "Generator",
    "generate_companies",
    "generate_people",
    "__version__",
]
