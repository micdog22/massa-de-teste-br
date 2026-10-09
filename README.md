# Massa de Teste BR — gere dados brasileiros fictícios para testes e desenvolvimento (Python)

Precisa popular um banco de homologação, testar um formulário de cadastro ou montar um exemplo para a documentação sem usar dados de gente de verdade? O **Massa de Teste BR** gera pessoas e empresas brasileiras fictícias, mas coerentes: CPF e CNPJ com dígitos verificadores válidos, celular com o DDD da cidade, CEP dentro da faixa da UF e e-mails em domínios reservados para exemplos.

A saída sai em JSON, JSON Lines, CSV ou SQL, e a mesma semente gera sempre os mesmos dados, o que ajuda em testes automatizados.

> **Aviso:** todos os dados são fictícios. Os CPFs e CNPJs são aleatórios, mas matematicamente válidos, e **podem coincidir com documentos reais** (o mesmo vale para telefones). Use apenas em ambientes de teste e desenvolvimento, nunca em cadastros reais nem para fraude ou para se passar por outra pessoa.

## Recursos

- **Pessoas:** nome completo (nomes e sobrenomes comuns no Brasil, às vezes com "da", "de", "dos"), CPF, data de nascimento dentro de uma faixa de idade, e-mail derivado do nome, celular e endereço completo.
- **Empresas:** razão social (Ltda, S.A., ME), nome fantasia, CNPJ, e-mail, telefone fixo, data de abertura e endereço.
- **Coerência:** cidade, UF e DDD sempre combinam (100 cidades de todas as 27 UFs), o CEP fica dentro da faixa da UF e o nono dígito do CPF corresponde à região fiscal da UF.
- **E-mails seguros:** só `example.com`, `example.org` e `example.net`, domínios reservados para exemplos. Nenhuma mensagem de teste chega a alguém de verdade.
- **Formatos:** JSON, JSON Lines, CSV (separador configurável, aspas corretas, BOM opcional para o Excel) e SQL (`INSERT` com aspas escapadas).
- Reprodutível com `--semente`, escolha de colunas com `--campos`, filtro por UF e opção sem máscara (só dígitos).
- Sem dependências: só Python 3.9+.

## Instalação

```bash
pipx install git+https://github.com/micdog22/massa-de-teste-br
# ou
pip install git+https://github.com/micdog22/massa-de-teste-br
```

## Como usar

```bash
massa-de-teste-br pessoas -n 100 --formato csv > pessoas.csv
massa-de-teste-br empresas -n 20 --formato sql --tabela fornecedores > fornecedores.sql
massa-de-teste-br pessoas -n 1000 --formato jsonl --semente 42 -o pessoas.jsonl
massa-de-teste-br pessoas -n 5 --campos nome,cpf,email --uf SP,MG
massa-de-teste-br pessoas -n 50 --idade-min 60 --idade-max 90 --sem-mascara
```

JSON (padrão):

```bash
massa-de-teste-br pessoas -n 1 --semente 42 --data-referencia 2026-10-08
```

```json
[
  {
    "nome": "João Lopes dos Anjos",
    "cpf": "819.600.138-07",
    "data_nascimento": "1966-08-23",
    "email": "joao.anjos78@example.com",
    "celular": "(16) 97863-7940",
    "logradouro": "Avenida Santos Dumont",
    "numero": "2860",
    "complemento": "Bloco C, Apto 302",
    "bairro": "Jardim Bandeirantes",
    "cidade": "São Carlos",
    "uf": "SP",
    "cep": "12029-104"
  }
]
```

CSV com colunas escolhidas (separador `;`, que o Excel em português abre direto):

```
nome;cpf;celular;cidade;uf
João Lopes dos Anjos;819.600.138-07;(16) 97863-7940;São Carlos;SP
Márcia Nascimento D'Ávila;781.618.498-03;(12) 96034-1316;São José dos Campos;SP
Lorena Barros Cavalcanti;283.276.484-38;(82) 97056-4139;Maceió;AL
```

SQL:

```sql
INSERT INTO fornecedores (razao_social, cnpj, telefone, cidade) VALUES ('Jequitibá Distribuidora de Bebidas S.A.', '81.590.830/0001-18', '(14) 5131-8609', 'Bauru');
INSERT INTO fornecedores (razao_social, cnpj, telefone, cidade) VALUES ('Almeida & Oliveira Comércio de Calçados Ltda', '46.281.948/0001-63', '(19) 3518-1909', 'Campinas');
```

No SQL, aspas simples são duplicadas (`D'Ávila` vira `'D''Ávila'`) e campos vazios viram `NULL`.

### Opções

| Opção | O que faz |
| --- | --- |
| `pessoas` ou `empresas` | O que gerar. |
| `-n`, `--quantidade N` | Quantos registros (padrão: 10). |
| `--formato` | `json` (padrão), `jsonl`, `csv` ou `sql`. |
| `--semente N` | Gera sempre os mesmos dados. |
| `--campos LISTA` | Colunas separadas por vírgula, na ordem desejada. |
| `--uf LISTA` | Só cidades destas UFs, ex.: `SP,RJ`. |
| `--sem-mascara` | CPF, CNPJ, CEP e telefones só com dígitos. |
| `--idade-min N`, `--idade-max N` | Faixa de idade das pessoas (padrão: 18 a 80). |
| `--data-referencia AAAA-MM-DD` | Data usada para idades e datas (padrão: hoje). |
| `--separador C` | Separador do CSV (padrão: `;`; aceita `tab`). |
| `--bom` | CSV com BOM UTF-8, para o Excel reconhecer os acentos. |
| `--tabela NOME` | Tabela do `INSERT` (padrão: `pessoas` ou `empresas`). |
| `-o`, `--saida ARQUIVO` | Grava em arquivo (UTF-8) em vez da saída padrão. |

Campos de pessoas: `nome`, `cpf`, `data_nascimento`, `email`, `celular`, `logradouro`, `numero`, `complemento`, `bairro`, `cidade`, `uf`, `cep`.

Campos de empresas: `razao_social`, `nome_fantasia`, `cnpj`, `email`, `telefone`, `data_abertura`, `logradouro`, `numero`, `complemento`, `bairro`, `cidade`, `uf`, `cep`.

As datas de nascimento e de abertura são calculadas a partir da data de hoje. Para obter exatamente a mesma saída em dias diferentes, use `--semente` junto com `--data-referencia`.

### Como biblioteca

```python
from massa_de_teste_br import generate_companies, generate_people

for pessoa in generate_people(3, seed=42, ufs=["SP"], min_age=25, max_age=40):
    print(pessoa["nome"], pessoa["cpf"], pessoa["cidade"])

empresas = list(generate_companies(10, seed=7, masked=False))
```

## Como rodar localmente

```bash
git clone https://github.com/micdog22/massa-de-teste-br
cd massa-de-teste-br
PYTHONPATH=src python3 -m massa_de_teste_br pessoas -n 5
```

## Testes

```bash
python3 -m unittest discover -s tests -v
```

Os testes conferem os dígitos verificadores com um validador independente, a coerência entre cidade, UF, DDD e CEP, os domínios de e-mail, a reprodutibilidade com semente, as aspas do CSV e o escape de `'` no SQL.

## Como funciona

- **CPF:** oito dígitos aleatórios, o nono é a região fiscal da UF (por exemplo, 8 para SP, 7 para RJ e ES, 6 para MG) e os dois últimos são os verificadores pelo módulo 11 (pesos de 10 a 2 e de 11 a 2). Sequências repetidas como `111.111.111-11` são descartadas.
- **CNPJ:** oito dígitos aleatórios, filial `0001` (matriz) e dois verificadores pelo módulo 11 (pesos 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2 e depois 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2). São gerados só CNPJs numéricos.
- **CEP:** os cinco primeiros dígitos ficam dentro da faixa da UF (SP de 01000 a 19999, RJ de 20000 a 28999 e assim por diante) e o sufixo vai de 000 a 899, faixa usada por logradouros.
- **Telefones:** celular com nove dígitos começando com 9; fixo com oito dígitos começando com 2, 3, 4 ou 5; sempre com o DDD da cidade sorteada.
- **E-mails:** montados a partir do nome, sem acentos (`marcia.davila25@example.net`), e únicos dentro de cada geração.

## Contribuindo

Issues e pull requests são bem-vindos.

## Licença

MIT — veja [LICENSE](LICENSE).
