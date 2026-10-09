"""Interface de linha de comando do massa-de-teste-br."""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from typing import List, Optional, Sequence

from . import __version__
from .generators import COMPANY_FIELDS, PERSON_FIELDS, VALID_UFS, Generator
from .output import FORMATS, is_valid_table_name, select_fields, write_csv, write_json, write_jsonl, write_sql

MAX_COUNT = 1_000_000

_TRANSLATIONS = (
    ("the following arguments are required", "os seguintes argumentos são obrigatórios"),
    ("unrecognized arguments", "argumentos não reconhecidos"),
    ("expected one argument", "esperava um valor"),
    ("invalid choice", "opção inválida"),
    ("choose from", "escolha entre"),
    ("ambiguous option", "opção ambígua"),
    ("could match", "pode ser"),
    ("argument ", "argumento "),
)


class _Formatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        return super().add_usage(usage, actions, groups, "uso: " if prefix is None else prefix)


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # type: ignore[override]
        for english, portuguese in _TRANSLATIONS:
            message = message.replace(english, portuguese)
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: erro: {message}\n")


def _int_between(low: int, high: int):
    def parse(value: str) -> int:
        try:
            number = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"número inteiro inválido: {value!r}")
        if not low <= number <= high:
            raise argparse.ArgumentTypeError(f"use um número de {low} a {high}")
        return number

    return parse


def _integer(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"número inteiro inválido: {value!r}")


def _date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"data inválida: {value!r} (use AAAA-MM-DD)")


def _separator(value: str) -> str:
    if value.lower() in ("tab", "\\t"):
        return "\t"
    if len(value) != 1 or value in '"\r\n':
        raise argparse.ArgumentTypeError("use um único caractere (ex.: ; , |) ou 'tab'")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(
        prog="massa-de-teste-br",
        description="Gera dados brasileiros fictícios (pessoas e empresas) para testes e desenvolvimento.",
        epilog=(
            "exemplos:\n"
            "  massa-de-teste-br pessoas -n 100 --formato csv > pessoas.csv\n"
            "  massa-de-teste-br empresas -n 20 --formato sql --tabela fornecedores\n"
            "  massa-de-teste-br pessoas -n 5 --campos nome,cpf,email --semente 42\n\n"
            f"campos de pessoas: {', '.join(PERSON_FIELDS)}\n"
            f"campos de empresas: {', '.join(COMPANY_FIELDS)}\n\n"
            "Os dados são fictícios. CPFs e CNPJs são aleatórios, mas matematicamente válidos,\n"
            "e podem coincidir com documentos reais: use só em ambientes de teste."
        ),
        formatter_class=_Formatter,
        add_help=False,
    )
    parser._positionals.title = "argumentos"
    parser._optionals.title = "opções"
    parser.add_argument("tipo", choices=("pessoas", "empresas"), metavar="TIPO", help="o que gerar: pessoas ou empresas")
    parser.add_argument("-h", "--help", action="help", help="mostra esta ajuda e sai")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}", help="mostra a versão e sai")
    parser.add_argument(
        "-n", "--quantidade", type=_int_between(1, MAX_COUNT), default=10, metavar="N",
        help="quantos registros gerar (padrão: 10)",
    )
    parser.add_argument("--formato", choices=FORMATS, default="json", help="json, jsonl, csv ou sql (padrão: json)")
    parser.add_argument("--semente", type=_integer, metavar="N", help="semente para gerar sempre os mesmos dados")
    parser.add_argument("--campos", metavar="LISTA", help="colunas separadas por vírgula, na ordem desejada")
    parser.add_argument("--uf", metavar="LISTA", help="limita a cidades destas UFs, ex.: SP,RJ")
    parser.add_argument("--sem-mascara", action="store_true", help="CPF, CNPJ, CEP e telefones só com dígitos")
    parser.add_argument("--idade-min", type=_int_between(0, 120), default=18, metavar="N", help="idade mínima (padrão: 18)")
    parser.add_argument("--idade-max", type=_int_between(0, 120), default=80, metavar="N", help="idade máxima (padrão: 80)")
    parser.add_argument(
        "--data-referencia", type=_date, metavar="AAAA-MM-DD",
        help="data usada para calcular idades e datas (padrão: hoje)",
    )
    parser.add_argument("--separador", type=_separator, default=";", metavar="C", help="separador do CSV (padrão: ;)")
    parser.add_argument("--bom", action="store_true", help="CSV com BOM UTF-8, para o Excel reconhecer os acentos")
    parser.add_argument("--tabela", metavar="NOME", help="tabela do INSERT no formato sql (padrão: o tipo)")
    parser.add_argument("-o", "--saida", metavar="ARQUIVO", help="grava em um arquivo em vez da saída padrão")
    return parser


def _parse_fields(parser: argparse.ArgumentParser, raw: Optional[str], available: Sequence[str]) -> List[str]:
    if not raw:
        return list(available)
    fields: List[str] = []
    for name in (part.strip().lower() for part in raw.split(",")):
        if not name:
            continue
        if name not in available:
            parser.error(f"campo desconhecido: {name}. Campos disponíveis: {', '.join(available)}")
        if name not in fields:
            fields.append(name)
    if not fields:
        parser.error("informe pelo menos um campo em --campos")
    return fields


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    available = PERSON_FIELDS if args.tipo == "pessoas" else COMPANY_FIELDS
    fields = _parse_fields(parser, args.campos, available)
    ufs = [uf.strip().upper() for uf in args.uf.split(",") if uf.strip()] if args.uf else None
    table = args.tabela or args.tipo
    if args.formato == "sql" and not is_valid_table_name(table):
        parser.error(f"nome de tabela inválido: {table!r} (use letras, números e _, ex.: clientes ou teste.clientes)")
    try:
        generator = Generator(
            args.semente,
            ufs=ufs,
            masked=not args.sem_mascara,
            reference_date=args.data_referencia,
            min_age=args.idade_min,
            max_age=args.idade_max,
        )
    except ValueError as error:
        parser.error(str(error))

    make = generator.person if args.tipo == "pessoas" else generator.company
    rows = select_fields((make() for _ in range(args.quantidade)), fields)

    if args.saida:
        try:
            out = open(args.saida, "w", encoding="utf-8", newline="")
        except OSError as error:
            print(f"massa-de-teste-br: não foi possível criar {args.saida}: {error.strerror}", file=sys.stderr)
            return 1
    else:
        out = sys.stdout
        if not out.isatty() and hasattr(out, "reconfigure"):
            out.reconfigure(encoding="utf-8")
    try:
        if args.formato == "json":
            count = write_json(rows, out)
        elif args.formato == "jsonl":
            count = write_jsonl(rows, out)
        elif args.formato == "csv":
            count = write_csv(rows, out, fields, args.separador, args.bom)
        else:
            count = write_sql(rows, out, table, fields)
    except BrokenPipeError:
        # Quem lia a saída (ex.: head) fechou o pipe antes do fim.
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        return 0
    finally:
        if args.saida:
            out.close()
    if args.saida:
        print(f"{count} {'registro gravado' if count == 1 else 'registros gravados'} em {args.saida}.", file=sys.stderr)
    return 0
