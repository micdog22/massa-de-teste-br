import codecs
import csv
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from massa_de_teste_br import __version__  # noqa: E402
from massa_de_teste_br.cli import main  # noqa: E402

FIXED = ["--semente", "42", "--data-referencia", "2026-10-08"]


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            code = main(list(args))
        except SystemExit as exit_:
            code = exit_.code
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_json_people(self):
        code, out, _ = run("pessoas", "-n", "5", *FIXED)
        self.assertEqual(code, 0)
        people = json.loads(out)
        self.assertEqual(len(people), 5)
        self.assertIn("cpf", people[0])

    def test_same_seed_same_output(self):
        self.assertEqual(run("empresas", "-n", "8", *FIXED)[1], run("empresas", "-n", "8", *FIXED)[1])

    def test_csv_with_selected_fields(self):
        code, out, _ = run("pessoas", "-n", "3", "--formato", "csv", "--campos", "nome, cpf,EMAIL", *FIXED)
        self.assertEqual(code, 0)
        rows = list(csv.reader(io.StringIO(out), delimiter=";"))
        self.assertEqual(rows[0], ["nome", "cpf", "email"])
        self.assertEqual(len(rows), 4)

    def test_csv_tab_separator(self):
        _, out, _ = run("empresas", "-n", "1", "--formato", "csv", "--separador", "tab", "--campos", "cnpj,uf", *FIXED)
        self.assertEqual(out.splitlines()[0], "cnpj\tuf")

    def test_sql_and_jsonl(self):
        _, out, _ = run("empresas", "-n", "4", "--formato", "sql", "--tabela", "fornecedores", *FIXED)
        lines = out.splitlines()
        self.assertEqual(len(lines), 4)
        self.assertTrue(all(line.startswith("INSERT INTO fornecedores (razao_social,") for line in lines))
        _, out, _ = run("pessoas", "-n", "4", "--formato", "jsonl", "--sem-mascara", *FIXED)
        records = [json.loads(line) for line in out.splitlines()]
        self.assertTrue(all(r["cpf"].isdigit() for r in records))

    def test_uf_and_age_options(self):
        _, out, _ = run("pessoas", "-n", "30", "--uf", "ba,se", "--idade-min", "20", "--idade-max", "25", *FIXED)
        people = json.loads(out)
        self.assertLessEqual({p["uf"] for p in people}, {"BA", "SE"})
        self.assertTrue(all("2000-10-09" <= p["data_nascimento"] <= "2006-10-08" for p in people))

    def test_output_file(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "pessoas.csv"
            code, out, err = run("pessoas", "-n", "2", "--formato", "csv", "--bom", "-o", str(target), *FIXED)
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            self.assertIn("2 registros gravados", err)
            raw = target.read_bytes()
            self.assertTrue(raw.startswith(codecs.BOM_UTF8 + b"nome;cpf"))

    def test_usage_errors(self):
        cases = [
            ("pessoas", "--campos", "nome,idade"),
            ("pessoas", "--uf", "XX"),
            ("pessoas", "-n", "0"),
            ("pessoas", "--idade-min", "60", "--idade-max", "30"),
            ("empresas", "--formato", "sql", "--tabela", "x; DROP TABLE y"),
            ("pessoas", "--data-referencia", "08/10/2026"),
            ("pessoas", "--separador", ";;"),
            ("animais",),
        ]
        for args in cases:
            code, _, err = run(*args)
            self.assertEqual(code, 2, args)
            self.assertIn("erro:", err)

    def test_module_entry_point(self):
        env = dict(os.environ, PYTHONPATH=str(SRC))
        result = subprocess.run(
            [sys.executable, "-m", "massa_de_teste_br", "--version"], capture_output=True, text=True, env=env
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), f"massa-de-teste-br {__version__}")


if __name__ == "__main__":
    unittest.main()
