"""Geração de pessoas e empresas fictícias, reproduzível com semente."""
from __future__ import annotations

import datetime as dt
import random
import unicodedata
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Set, Tuple

from . import data
from .documents import format_cnpj, format_cpf, generate_cnpj, generate_cpf

PERSON_FIELDS = (
    "nome", "cpf", "data_nascimento", "email", "celular",
    "logradouro", "numero", "complemento", "bairro", "cidade", "uf", "cep",
)
COMPANY_FIELDS = (
    "razao_social", "nome_fantasia", "cnpj", "email", "telefone", "data_abertura",
    "logradouro", "numero", "complemento", "bairro", "cidade", "uf", "cep",
)
VALID_UFS = tuple(sorted(data.CEP_RANGES))
MAX_AGE = 120


def ascii_slug(text: str) -> str:
    """Só letras e números ASCII, em minúsculas ("D'Ávila" vira "davila")."""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if c.isascii() and c.isalnum()).lower()


def years_before(day: dt.date, years: int) -> dt.date:
    try:
        return day.replace(year=day.year - years)
    except ValueError:  # 29 de fevereiro em ano não bissexto
        return day.replace(year=day.year - years, day=28)


def age_on(birth: dt.date, reference: dt.date) -> int:
    return reference.year - birth.year - ((reference.month, reference.day) < (birth.month, birth.day))


class Generator:
    """Gera registros fictícios. A mesma semente produz sempre os mesmos dados."""

    def __init__(
        self,
        seed: Optional[int] = None,
        *,
        ufs: Optional[Iterable[str]] = None,
        masked: bool = True,
        reference_date: Optional[dt.date] = None,
        min_age: int = 18,
        max_age: int = 80,
    ) -> None:
        selected = {uf.strip().upper() for uf in ufs} if ufs else set()
        unknown = sorted(selected - set(VALID_UFS))
        if unknown:
            raise ValueError(f"UF inválida: {', '.join(unknown)}. Use uma destas: {', '.join(VALID_UFS)}.")
        if not (0 <= min_age <= max_age <= MAX_AGE):
            raise ValueError(f"As idades devem ficar entre 0 e {MAX_AGE}, com a mínima menor ou igual à máxima.")
        self.rng = random.Random(seed)
        self.masked = masked
        self.reference = reference_date or dt.date.today()
        self.min_age = min_age
        self.max_age = max_age
        self.cities = [city for city in data.CITIES if not selected or city[1] in selected]
        self._cpfs: Set[str] = set()
        self._cnpjs: Set[str] = set()
        self._emails: Set[str] = set()

    @staticmethod
    def _unique(seen: Set[str], factory: Callable[[], str]) -> str:
        while True:
            value = factory()
            if value not in seen:
                seen.add(value)
                return value

    def _unique_email(self, local: str, domain: str) -> str:
        email = f"{local}@{domain}"
        counter = 2
        while email in self._emails:
            email = f"{local}{counter}@{domain}"
            counter += 1
        self._emails.add(email)
        return email

    def _digits(self, count: int) -> str:
        return "".join(str(self.rng.randint(0, 9)) for _ in range(count))

    def _date_between(self, start: dt.date, end: dt.date) -> dt.date:
        return start + dt.timedelta(days=self.rng.randint(0, (end - start).days))

    def _surnames(self) -> List[str]:
        rng = self.rng
        count = 1 if rng.random() < 0.25 else 2
        chosen: List[str] = []
        for index in range(count):
            last = index == count - 1
            options = data.SURNAMES_WITH_PARTICLE if last and rng.random() < 0.4 else data.SURNAMES
            while True:
                candidate = rng.choice(options)
                core = candidate.split()[-1]
                if all(core != other.split()[-1] for other in chosen):
                    break
            chosen.append(candidate)
        return chosen

    def _person_email(self, first_name: str, surnames: List[str]) -> str:
        rng = self.rng
        given = ascii_slug(first_name.split()[0])
        family = ascii_slug(surnames[-1].split()[-1])
        pattern = rng.randrange(5)
        if pattern == 0:
            local = f"{given}.{family}"
        elif pattern == 1:
            local = f"{given}{family}"
        elif pattern == 2:
            local = f"{given}_{family}"
        elif pattern == 3:
            local = f"{given[0]}{family}"
        else:
            local = f"{given}.{family}{rng.randint(1, 99)}"
        return self._unique_email(local, rng.choice(data.EMAIL_DOMAINS))

    def _cep(self, uf: str) -> str:
        ranges = data.CEP_RANGES[uf]
        pick = self.rng.randrange(sum(high - low + 1 for low, high in ranges))
        prefix = ranges[0][0]
        for low, high in ranges:
            size = high - low + 1
            if pick < size:
                prefix = low + pick
                break
            pick -= size
        # Sufixos de 000 a 899 são os usados por logradouros.
        digits = f"{prefix:05d}{self.rng.randint(0, 899):03d}"
        return f"{digits[:5]}-{digits[5:]}" if self.masked else digits

    def _complement(self, company: bool) -> str:
        rng = self.rng
        roll = rng.random()
        if company:
            if roll < 0.3:
                return f"Sala {rng.randint(1, 20)}{rng.randint(1, 12):02d}"
            if roll < 0.4:
                return f"Loja {rng.randint(1, 30)}"
            if roll < 0.45:
                return f"Galpão {rng.randint(1, 8)}"
            return ""
        if roll < 0.3:
            return f"Apto {rng.randint(1, 20)}{rng.randint(1, 4):02d}"
        if roll < 0.4:
            return f"Casa {rng.randint(1, 4)}"
        if roll < 0.45:
            return f"Bloco {rng.choice('ABCDEF')}, Apto {rng.randint(1, 12)}{rng.randint(1, 4):02d}"
        return ""

    def _address(self, city: Tuple[str, str, str], company: bool) -> Dict[str, str]:
        name, uf, _ = city
        return {
            "logradouro": self.rng.choice(data.STREETS),
            "numero": str(self.rng.randint(1, 3999)),
            "complemento": self._complement(company),
            "bairro": self.rng.choice(data.NEIGHBORHOODS),
            "cidade": name,
            "uf": uf,
            "cep": self._cep(uf),
        }

    def person(self) -> Dict[str, str]:
        rng = self.rng
        first_name = rng.choice(data.FEMALE_NAMES if rng.random() < 0.5 else data.MALE_NAMES)
        surnames = self._surnames()
        city = rng.choice(self.cities)
        _, uf, ddd = city
        cpf = self._unique(self._cpfs, lambda: generate_cpf(rng, data.CPF_REGION_DIGIT[uf]))
        latest = years_before(self.reference, self.min_age)
        earliest = years_before(self.reference, self.max_age + 1) + dt.timedelta(days=1)
        birth = self._date_between(earliest, latest)
        email = self._person_email(first_name, surnames)
        mobile = "9" + str(rng.randint(6, 9)) + self._digits(7)
        record = {
            "nome": " ".join([first_name] + surnames),
            "cpf": format_cpf(cpf) if self.masked else cpf,
            "data_nascimento": birth.isoformat(),
            "email": email,
            "celular": f"({ddd}) {mobile[:5]}-{mobile[5:]}" if self.masked else ddd + mobile,
        }
        record.update(self._address(city, company=False))
        return record

    def company(self) -> Dict[str, str]:
        rng = self.rng
        activity, fantasy_template = rng.choice(data.ACTIVITIES)
        if rng.random() < 0.3:
            base = " & ".join(rng.sample(data.SURNAMES, 2))
        else:
            base = rng.choice(data.COMPANY_NAMES)
        suffixes, weights = zip(*data.COMPANY_SUFFIXES)
        suffix = rng.choices(suffixes, weights=weights)[0]
        city = rng.choice(self.cities)
        _, _, ddd = city
        cnpj = self._unique(self._cnpjs, lambda: generate_cnpj(rng))
        prefix = rng.choice(data.COMPANY_EMAIL_PREFIXES)
        email = self._unique_email(f"{prefix}.{ascii_slug(base)}", rng.choice(data.EMAIL_DOMAINS))
        phone = str(rng.randint(2, 5)) + self._digits(7)
        opened = self._date_between(years_before(self.reference, 40), self.reference - dt.timedelta(days=30))
        record = {
            "razao_social": f"{base} {activity} {suffix}",
            "nome_fantasia": fantasy_template.format(nome=base),
            "cnpj": format_cnpj(cnpj) if self.masked else cnpj,
            "email": email,
            "telefone": f"({ddd}) {phone[:4]}-{phone[4:]}" if self.masked else ddd + phone,
            "data_abertura": opened.isoformat(),
        }
        record.update(self._address(city, company=True))
        return record


def generate_people(count: int, seed: Optional[int] = None, **options) -> Iterator[Dict[str, str]]:
    """Gera ``count`` pessoas fictícias (veja ``Generator`` para as opções)."""
    generator = Generator(seed, **options)
    for _ in range(count):
        yield generator.person()


def generate_companies(count: int, seed: Optional[int] = None, **options) -> Iterator[Dict[str, str]]:
    """Gera ``count`` empresas fictícias (veja ``Generator`` para as opções)."""
    generator = Generator(seed, **options)
    for _ in range(count):
        yield generator.company()
