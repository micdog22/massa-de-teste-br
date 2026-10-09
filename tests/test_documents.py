import random
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from massa_de_teste_br.documents import format_cnpj, format_cpf, generate_cnpj, generate_cpf  # noqa: E402


def cpf_is_valid(cpf: str) -> bool:
    """Validador independente, escrito de forma diferente do gerador."""
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False
    numbers = [int(c) for c in digits]
    for size in (9, 10):
        total = 0
        weight = size + 1
        for number in numbers[:size]:
            total += number * weight
            weight -= 1
        expected = (total * 10) % 11 % 10
        if numbers[size] != expected:
            return False
    return True


def cnpj_is_valid(cnpj: str) -> bool:
    digits = re.sub(r"\D", "", cnpj)
    if len(digits) != 14 or digits == digits[0] * 14:
        return False
    numbers = [int(c) for c in digits]
    for size in (12, 13):
        weights = list(range(size - 7, 1, -1)) + list(range(9, 1, -1))
        total = sum(n * w for n, w in zip(numbers[:size], weights))
        remainder = total % 11
        expected = 0 if remainder < 2 else 11 - remainder
        if numbers[size] != expected:
            return False
    return True


class ValidatorSanityTest(unittest.TestCase):
    def test_known_examples(self):
        self.assertTrue(cpf_is_valid("111.444.777-35"))
        self.assertFalse(cpf_is_valid("111.444.777-36"))
        self.assertFalse(cpf_is_valid("111.111.111-11"))
        self.assertTrue(cnpj_is_valid("11.222.333/0001-81"))
        self.assertFalse(cnpj_is_valid("11.222.333/0001-82"))
        self.assertFalse(cnpj_is_valid("00.000.000/0000-00"))


class CpfTest(unittest.TestCase):
    def test_generated_cpfs_are_valid(self):
        rng = random.Random(1)
        for _ in range(2000):
            cpf = generate_cpf(rng)
            self.assertRegex(cpf, r"^\d{11}$")
            self.assertTrue(cpf_is_valid(cpf), cpf)

    def test_region_digit(self):
        rng = random.Random(2)
        for region in range(10):
            for _ in range(50):
                cpf = generate_cpf(rng, region)
                self.assertEqual(cpf[8], str(region))
                self.assertTrue(cpf_is_valid(cpf))

    def test_format(self):
        self.assertEqual(format_cpf("11144477735"), "111.444.777-35")


class CnpjTest(unittest.TestCase):
    def test_generated_cnpjs_are_valid_and_head_office(self):
        rng = random.Random(3)
        for _ in range(2000):
            cnpj = generate_cnpj(rng)
            self.assertRegex(cnpj, r"^\d{8}0001\d{2}$")
            self.assertTrue(cnpj_is_valid(cnpj), cnpj)

    def test_branch_number(self):
        cnpj = generate_cnpj(random.Random(4), branch=12)
        self.assertEqual(cnpj[8:12], "0012")
        self.assertTrue(cnpj_is_valid(cnpj))

    def test_format(self):
        self.assertEqual(format_cnpj("11222333000181"), "11.222.333/0001-81")


if __name__ == "__main__":
    unittest.main()
