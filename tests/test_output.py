import codecs
import csv
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from massa_de_teste_br.output import (  # noqa: E402
    is_valid_table_name,
    select_fields,
    sql_literal,
    write_csv,
    write_json,
    write_jsonl,
    write_sql,
)

ROWS = [
    {"nome": "Maria D'Ávila", "obs": "texto; com separador", "cidade": "São Paulo"},
    {"nome": 'Loja "Exemplo"', "obs": "linha 1\nlinha 2", "cidade": ""},
]
FIELDS = ["nome", "obs", "cidade"]


class CsvTest(unittest.TestCase):
    def test_quoting_round_trip(self):
        out = io.StringIO()
        self.assertEqual(write_csv(ROWS, out, FIELDS), 2)
        text = out.getvalue()
        self.assertTrue(text.startswith("nome;obs;cidade\n"))
        self.assertIn('"texto; com separador"', text)
        self.assertIn('"Loja ""Exemplo"""', text)
        self.assertIn('"linha 1\nlinha 2"', text)
        parsed = list(csv.reader(io.StringIO(text), delimiter=";"))
        self.assertEqual(parsed[0], FIELDS)
        self.assertEqual(parsed[1], [ROWS[0][f] for f in FIELDS])
        self.assertEqual(parsed[2], [ROWS[1][f] for f in FIELDS])

    def test_other_separator_and_bom(self):
        out = io.StringIO()
        write_csv(ROWS[:1], out, FIELDS, separator=",", bom=True)
        encoded = out.getvalue().encode("utf-8")
        self.assertTrue(encoded.startswith(codecs.BOM_UTF8 + b"nome,obs,cidade\n"))
        self.assertIn("Maria D'Ávila,texto; com separador,São Paulo", out.getvalue())


class SqlTest(unittest.TestCase):
    def test_literal_escapes_single_quotes(self):
        self.assertEqual(sql_literal("D'Ávila"), "'D''Ávila'")
        self.assertEqual(sql_literal("''"), "''''''")
        self.assertEqual(sql_literal(""), "NULL")

    def test_insert_statements(self):
        out = io.StringIO()
        self.assertEqual(write_sql(ROWS, out, "teste.clientes", FIELDS), 2)
        lines = out.getvalue().splitlines()
        self.assertEqual(
            lines[0],
            "INSERT INTO teste.clientes (nome, obs, cidade) VALUES ('Maria D''Ávila', 'texto; com separador', 'São Paulo');",
        )
        self.assertTrue(out.getvalue().endswith("NULL);\n"))

    def test_table_name_validation(self):
        for name in ("pessoas", "_tmp1", "esquema.tabela"):
            self.assertTrue(is_valid_table_name(name), name)
        for name in ("", "1abc", "tabela; DROP TABLE x", "a.b.c", "nome-com-hifen", "a b"):
            self.assertFalse(is_valid_table_name(name), name)
        with self.assertRaises(ValueError):
            write_sql(ROWS, io.StringIO(), "x;y", FIELDS)


class JsonTest(unittest.TestCase):
    def test_json_array(self):
        out = io.StringIO()
        write_json(ROWS, out)
        self.assertEqual(json.loads(out.getvalue()), ROWS)
        self.assertIn("São Paulo", out.getvalue())

    def test_empty_json_array(self):
        out = io.StringIO()
        write_json([], out)
        self.assertEqual(json.loads(out.getvalue()), [])

    def test_json_lines(self):
        out = io.StringIO()
        write_jsonl(ROWS, out)
        lines = out.getvalue().splitlines()
        self.assertEqual([json.loads(line) for line in lines], ROWS)

    def test_select_fields_keeps_requested_order(self):
        selected = list(select_fields(ROWS, ["cidade", "nome"]))
        self.assertEqual(list(selected[0]), ["cidade", "nome"])


if __name__ == "__main__":
    unittest.main()
