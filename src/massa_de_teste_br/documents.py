"""CPF e CNPJ aleatórios com dígitos verificadores válidos."""
from __future__ import annotations

import random
from typing import List, Optional, Sequence

CNPJ_FIRST_WEIGHTS = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
CNPJ_SECOND_WEIGHTS = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def _check_digit(digits: Sequence[int], weights: Sequence[int]) -> int:
    remainder = sum(d * w for d, w in zip(digits, weights)) % 11
    return 0 if remainder < 2 else 11 - remainder


def _random_digits(rng: random.Random, count: int) -> List[int]:
    return [rng.randint(0, 9) for _ in range(count)]


def generate_cpf(rng: random.Random, region_digit: Optional[int] = None) -> str:
    """Gera os 11 dígitos de um CPF válido.

    ``region_digit`` é o nono dígito (região fiscal de emissão). Sequências com
    todos os dígitos iguais, inválidas por convenção, são descartadas.
    """
    while True:
        base = _random_digits(rng, 8)
        base.append(rng.randint(0, 9) if region_digit is None else region_digit)
        if len(set(base)) > 1:
            break
    first = _check_digit(base, range(10, 1, -1))
    second = _check_digit(base + [first], range(11, 1, -1))
    return "".join(str(d) for d in base + [first, second])


def generate_cnpj(rng: random.Random, branch: int = 1) -> str:
    """Gera os 14 dígitos de um CNPJ numérico válido (filial 0001 = matriz)."""
    while True:
        root = _random_digits(rng, 8)
        if len(set(root)) > 1:
            break
    base = root + [int(c) for c in f"{branch:04d}"]
    first = _check_digit(base, CNPJ_FIRST_WEIGHTS)
    second = _check_digit(base + [first], CNPJ_SECOND_WEIGHTS)
    return "".join(str(d) for d in base + [first, second])


def format_cpf(digits: str) -> str:
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"


def format_cnpj(digits: str) -> str:
    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
