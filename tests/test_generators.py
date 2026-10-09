import datetime as dt
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from massa_de_teste_br import data  # noqa: E402
from massa_de_teste_br.generators import (  # noqa: E402
    COMPANY_FIELDS,
    PERSON_FIELDS,
    Generator,
    age_on,
    generate_companies,
    generate_people,
)
from test_documents import cnpj_is_valid, cpf_is_valid  # noqa: E402

REFERENCE = dt.date(2026, 10, 8)
CITY_TABLE = {(city, uf): ddd for city, uf, ddd in data.CITIES}
RESERVED_DOMAINS = {"example.com", "example.org", "example.net"}


def cep_matches_uf(cep: str, uf: str) -> bool:
    prefix = int(re.sub(r"\D", "", cep)[:5])
    return any(low <= prefix <= high for low, high in data.CEP_RANGES[uf])


class DeterminismTest(unittest.TestCase):
    def test_same_seed_same_data(self):
        first = list(generate_people(50, seed=42, reference_date=REFERENCE))
        second = list(generate_people(50, seed=42, reference_date=REFERENCE))
        self.assertEqual(first, second)
        self.assertEqual(
            list(generate_companies(20, seed=7, reference_date=REFERENCE)),
            list(generate_companies(20, seed=7, reference_date=REFERENCE)),
        )

    def test_different_seed_different_data(self):
        self.assertNotEqual(
            list(generate_people(10, seed=1, reference_date=REFERENCE)),
            list(generate_people(10, seed=2, reference_date=REFERENCE)),
        )

    def test_masking_does_not_change_the_sequence(self):
        masked = list(generate_people(20, seed=5, reference_date=REFERENCE))
        plain = list(generate_people(20, seed=5, reference_date=REFERENCE, masked=False))
        for a, b in zip(masked, plain):
            self.assertEqual(re.sub(r"\D", "", a["cpf"]), b["cpf"])
            self.assertEqual(a["nome"], b["nome"])


class PeopleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people = list(generate_people(1500, seed=2026, reference_date=REFERENCE))

    def test_fields_in_order(self):
        self.assertEqual(tuple(self.people[0]), PERSON_FIELDS)

    def test_city_uf_ddd_cep_are_consistent(self):
        for person in self.people:
            key = (person["cidade"], person["uf"])
            self.assertIn(key, CITY_TABLE)
            self.assertRegex(person["celular"], r"^\(\d{2}\) 9[6-9]\d{3}-\d{4}$")
            self.assertEqual(person["celular"][1:3], CITY_TABLE[key])
            self.assertRegex(person["cep"], r"^\d{5}-\d{3}$")
            self.assertTrue(cep_matches_uf(person["cep"], person["uf"]), person)
            self.assertLessEqual(int(person["cep"][-3:]), 899)

    def test_cpf_valid_unique_and_from_the_right_region(self):
        cpfs = [p["cpf"] for p in self.people]
        self.assertEqual(len(set(cpfs)), len(cpfs))
        for person in self.people:
            self.assertRegex(person["cpf"], r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
            self.assertTrue(cpf_is_valid(person["cpf"]))
            self.assertEqual(int(person["cpf"][10]), data.CPF_REGION_DIGIT[person["uf"]])

    def test_emails_use_reserved_domains_and_are_unique(self):
        emails = [p["email"] for p in self.people]
        self.assertEqual(len(set(emails)), len(emails))
        for email in emails:
            local, domain = email.split("@")
            self.assertIn(domain, RESERVED_DOMAINS)
            self.assertRegex(local, r"^[a-z0-9._]+$")

    def test_names_have_first_name_and_surname(self):
        particles = 0
        for person in self.people:
            parts = person["nome"].split()
            self.assertGreaterEqual(len(parts), 2)
            particles += any(p in ("da", "de", "do", "dos", "das") for p in parts)
        self.assertGreater(particles, 100)

    def test_default_age_range(self):
        for person in self.people:
            age = age_on(dt.date.fromisoformat(person["data_nascimento"]), REFERENCE)
            self.assertTrue(18 <= age <= 80, person["data_nascimento"])

    def test_custom_age_range_including_leap_day(self):
        for reference in (dt.date(2028, 2, 29), dt.date(2027, 3, 1)):
            people = generate_people(400, seed=9, reference_date=reference, min_age=30, max_age=31)
            ages = {age_on(dt.date.fromisoformat(p["data_nascimento"]), reference) for p in people}
            self.assertEqual(ages, {30, 31})

    def test_uf_filter(self):
        people = list(generate_people(200, seed=1, ufs=["sp", "RJ"], reference_date=REFERENCE))
        self.assertEqual({p["uf"] for p in people}, {"SP", "RJ"})

    def test_unmasked(self):
        person = next(generate_people(1, seed=3, masked=False, reference_date=REFERENCE))
        self.assertRegex(person["cpf"], r"^\d{11}$")
        self.assertRegex(person["celular"], r"^\d{2}9\d{8}$")
        self.assertRegex(person["cep"], r"^\d{8}$")

    def test_invalid_options(self):
        with self.assertRaises(ValueError):
            Generator(ufs=["XX"])
        with self.assertRaises(ValueError):
            Generator(min_age=50, max_age=20)
        with self.assertRaises(ValueError):
            Generator(max_age=121)


class CompaniesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.companies = list(generate_companies(800, seed=11, reference_date=REFERENCE))

    def test_fields_in_order(self):
        self.assertEqual(tuple(self.companies[0]), COMPANY_FIELDS)

    def test_cnpj_valid_and_unique(self):
        cnpjs = [c["cnpj"] for c in self.companies]
        self.assertEqual(len(set(cnpjs)), len(cnpjs))
        for cnpj in cnpjs:
            self.assertRegex(cnpj, r"^\d{2}\.\d{3}\.\d{3}/0001-\d{2}$")
            self.assertTrue(cnpj_is_valid(cnpj))

    def test_names_suffixes_and_contacts(self):
        for company in self.companies:
            self.assertTrue(company["razao_social"].endswith((" Ltda", " S.A.", " ME")), company["razao_social"])
            self.assertTrue(company["nome_fantasia"])
            self.assertIn(company["email"].split("@")[1], RESERVED_DOMAINS)
            key = (company["cidade"], company["uf"])
            self.assertIn(key, CITY_TABLE)
            self.assertRegex(company["telefone"], r"^\(\d{2}\) [2-5]\d{3}-\d{4}$")
            self.assertEqual(company["telefone"][1:3], CITY_TABLE[key])
            self.assertTrue(cep_matches_uf(company["cep"], company["uf"]))

    def test_opening_date_range(self):
        for company in self.companies:
            opened = dt.date.fromisoformat(company["data_abertura"])
            self.assertGreaterEqual(opened, dt.date(1986, 10, 8))
            self.assertLessEqual(opened, REFERENCE - dt.timedelta(days=30))


class CityTableTest(unittest.TestCase):
    def test_every_uf_has_cities_and_cep_ranges(self):
        ufs = {uf for _, uf, _ in data.CITIES}
        self.assertEqual(len(ufs), 27)
        self.assertEqual(ufs, set(data.CEP_RANGES))
        self.assertEqual(ufs, set(data.CPF_REGION_DIGIT))

    def test_sample_rows_from_the_table(self):
        self.assertEqual(CITY_TABLE[("Limeira", "SP")], "19")
        self.assertEqual(CITY_TABLE[("Petrolina", "PE")], "87")
        self.assertEqual(CITY_TABLE[("Rio Verde", "GO")], "64")
        self.assertEqual(CITY_TABLE[("Imperatriz", "MA")], "99")
        self.assertEqual(len(data.CITIES), 100)


if __name__ == "__main__":
    unittest.main()
