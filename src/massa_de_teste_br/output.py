"""Formatos de saída: JSON, JSON Lines, CSV e SQL."""
from __future__ import annotations

import codecs
import csv
import json
import re
from typing import Dict, Iterable, Iterator, Sequence, TextIO

FORMATS = ("json", "jsonl", "csv", "sql")
BOM = codecs.BOM_UTF8.decode("utf-8")
_TABLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?$")

Row = Dict[str, str]


def select_fields(rows: Iterable[Row], fields: Sequence[str]) -> Iterator[Row]:
    """Mantém só as colunas pedidas, na ordem pedida."""
    for row in rows:
        yield {field: row[field] for field in fields}


def write_json(rows: Iterable[Row], out: TextIO) -> int:
    count = 0
    out.write("[")
    for row in rows:
        out.write(",\n  " if count else "\n  ")
        out.write(json.dumps(row, ensure_ascii=False, indent=2).replace("\n", "\n  "))
        count += 1
    out.write("\n]\n" if count else "]\n")
    return count


def write_jsonl(rows: Iterable[Row], out: TextIO) -> int:
    count = 0
    for row in rows:
        out.write(json.dumps(row, ensure_ascii=False) + "\n")
        count += 1
    return count


def write_csv(rows: Iterable[Row], out: TextIO, fields: Sequence[str], separator: str = ";", bom: bool = False) -> int:
    """CSV com cabeçalho; campos com separador, aspas ou quebra de linha vão entre aspas."""
    if bom:
        out.write(BOM)
    writer = csv.writer(out, delimiter=separator, quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    writer.writerow(fields)
    count = 0
    for row in rows:
        writer.writerow([row[field] for field in fields])
        count += 1
    return count


def is_valid_table_name(name: str) -> bool:
    """Aceita nomes simples (clientes) ou com esquema (teste.clientes)."""
    return bool(_TABLE_NAME.match(name))


def sql_literal(value: str) -> str:
    """Valor SQL: texto entre aspas simples, com ' duplicado; vazio vira NULL."""
    if value == "":
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def write_sql(rows: Iterable[Row], out: TextIO, table: str, fields: Sequence[str]) -> int:
    if not is_valid_table_name(table):
        raise ValueError(f"nome de tabela inválido: {table!r}")
    columns = ", ".join(fields)
    count = 0
    for row in rows:
        values = ", ".join(sql_literal(row[field]) for field in fields)
        out.write(f"INSERT INTO {table} ({columns}) VALUES ({values});\n")
        count += 1
    return count
