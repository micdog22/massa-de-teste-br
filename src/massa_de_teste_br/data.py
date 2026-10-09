"""Listas usadas na geração. Todos os nomes de pessoas e empresas são fictícios."""

FEMALE_NAMES = (
    "Maria", "Ana", "Francisca", "Antônia", "Adriana", "Juliana", "Márcia", "Fernanda",
    "Patrícia", "Aline", "Sandra", "Camila", "Amanda", "Bruna", "Jéssica", "Letícia",
    "Júlia", "Luciana", "Vanessa", "Mariana", "Gabriela", "Beatriz", "Larissa", "Rafaela",
    "Natália", "Bianca", "Daniela", "Priscila", "Tatiane", "Renata", "Simone", "Débora",
    "Carolina", "Isabela", "Laura", "Helena", "Alice", "Valentina", "Sofia", "Lívia",
    "Manuela", "Heloísa", "Lorena", "Yasmin", "Cecília", "Clara", "Raquel", "Viviane",
    "Cristiane", "Eliane",
    "Maria Eduarda", "Maria Clara", "Maria Luiza", "Maria Fernanda", "Maria Júlia",
    "Ana Clara", "Ana Beatriz", "Ana Paula", "Ana Luiza", "Ana Carolina",
)

MALE_NAMES = (
    "José", "João", "Antônio", "Francisco", "Carlos", "Paulo", "Pedro", "Lucas",
    "Luiz", "Marcos", "Gabriel", "Rafael", "Daniel", "Marcelo", "Bruno", "Eduardo",
    "Felipe", "Raimundo", "Rodrigo", "Manoel", "Mateus", "André", "Fernando", "Fábio",
    "Leonardo", "Gustavo", "Guilherme", "Leandro", "Tiago", "Ricardo", "Márcio", "Jorge",
    "Sebastião", "Alexandre", "Roberto", "Diego", "Vítor", "Sérgio", "Cláudio", "Arthur",
    "Heitor", "Davi", "Bernardo", "Samuel", "Miguel", "Henrique", "Caio", "Vinícius",
    "Otávio", "Renato",
    "João Pedro", "João Vitor", "Pedro Henrique", "Luiz Felipe", "Carlos Eduardo",
    "José Carlos", "João Paulo", "Paulo Roberto", "Luiz Fernando", "Marcos Vinícius",
)

SURNAMES = (
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira",
    "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes",
    "Soares", "Fernandes", "Vieira", "Barbosa", "Rocha", "Dias", "Nascimento", "Andrade",
    "Moreira", "Nunes", "Marques", "Machado", "Mendes", "Freitas", "Cardoso", "Ramos",
    "Gonçalves", "Santana", "Teixeira", "Araújo", "Pinto", "Correia", "Cavalcanti",
    "Monteiro", "Moura", "Batista", "Campos", "Barros", "Reis", "Castro", "Duarte",
    "Farias", "Miranda", "Cunha", "Sant'Anna", "D'Ávila",
)

SURNAMES_WITH_PARTICLE = (
    "da Silva", "dos Santos", "de Oliveira", "de Souza", "da Costa", "de Lima",
    "de Carvalho", "de Almeida", "da Rocha", "do Nascimento", "de Andrade", "de Freitas",
    "de Araújo", "de Moura", "de Barros", "dos Reis", "de Castro", "da Cunha",
    "da Conceição", "de Jesus", "das Neves", "da Cruz", "de Moraes", "dos Anjos",
    "de Paula", "da Luz",
)

STREETS = (
    "Rua das Acácias", "Avenida Brasil", "Rua Sete de Setembro", "Rua XV de Novembro",
    "Avenida Getúlio Vargas", "Rua Tiradentes", "Rua Dom Pedro II", "Rua das Flores",
    "Rua dos Ipês", "Rua das Palmeiras", "Avenida Santos Dumont", "Rua Rui Barbosa",
    "Rua São José", "Rua da Paz", "Rua das Laranjeiras", "Rua Bela Vista",
    "Rua Primavera", "Alameda dos Jasmins", "Travessa das Hortênsias", "Rua dos Girassóis",
    "Avenida das Nações", "Rua Castro Alves", "Rua Monteiro Lobato", "Rua Cecília Meireles",
    "Rua Machado de Assis", "Avenida dos Expedicionários", "Rua Barão do Rio Branco",
    "Rua Marechal Deodoro", "Rua Duque de Caxias", "Rua José Bonifácio",
    "Rua das Mangueiras", "Rua dos Cajueiros", "Avenida Beira-Rio", "Rua do Sol",
    "Rua Treze de Maio", "Rua Primeiro de Maio", "Rua Santa Catarina", "Rua Paraná",
    "Rua Goiás", "Avenida Independência",
)

NEIGHBORHOODS = (
    "Centro", "Jardim América", "Vila Nova", "Jardim das Flores", "Vila São José",
    "Bela Vista", "Boa Vista", "Santa Cruz", "Jardim Europa", "Vila Industrial",
    "Parque São Jorge", "Jardim Primavera", "Vila Esperança", "Cidade Nova",
    "Alto da Boa Vista", "Jardim Brasil", "Vila Rica", "Jardim Itália", "Planalto",
    "Nova Esperança", "São Cristóvão", "Santo Antônio", "Jardim Botânico", "Vila Maria",
    "Jardim Bandeirantes", "Parque das Árvores", "Jardim dos Ipês", "Vila Operária",
    "Morada do Sol", "Jardim Tropical",
)

# Cidade, UF e DDD.
CITIES = (
    ("São Paulo", "SP", "11"), ("Guarulhos", "SP", "11"), ("Osasco", "SP", "11"),
    ("Santo André", "SP", "11"), ("Jundiaí", "SP", "11"),
    ("São José dos Campos", "SP", "12"), ("Taubaté", "SP", "12"),
    ("Santos", "SP", "13"), ("Guarujá", "SP", "13"),
    ("Bauru", "SP", "14"), ("Marília", "SP", "14"),
    ("Sorocaba", "SP", "15"),
    ("Ribeirão Preto", "SP", "16"), ("São Carlos", "SP", "16"), ("Franca", "SP", "16"),
    ("São José do Rio Preto", "SP", "17"),
    ("Presidente Prudente", "SP", "18"),
    ("Campinas", "SP", "19"), ("Piracicaba", "SP", "19"), ("Limeira", "SP", "19"),
    ("Americana", "SP", "19"),
    ("Rio de Janeiro", "RJ", "21"), ("Niterói", "RJ", "21"), ("São Gonçalo", "RJ", "21"),
    ("Campos dos Goytacazes", "RJ", "22"), ("Macaé", "RJ", "22"),
    ("Volta Redonda", "RJ", "24"), ("Petrópolis", "RJ", "24"),
    ("Vitória", "ES", "27"), ("Vila Velha", "ES", "27"), ("Serra", "ES", "27"),
    ("Belo Horizonte", "MG", "31"), ("Contagem", "MG", "31"), ("Betim", "MG", "31"),
    ("Juiz de Fora", "MG", "32"),
    ("Governador Valadares", "MG", "33"),
    ("Uberlândia", "MG", "34"), ("Uberaba", "MG", "34"),
    ("Poços de Caldas", "MG", "35"), ("Varginha", "MG", "35"),
    ("Divinópolis", "MG", "37"),
    ("Montes Claros", "MG", "38"),
    ("Curitiba", "PR", "41"), ("São José dos Pinhais", "PR", "41"),
    ("Ponta Grossa", "PR", "42"),
    ("Londrina", "PR", "43"),
    ("Maringá", "PR", "44"),
    ("Cascavel", "PR", "45"), ("Foz do Iguaçu", "PR", "45"),
    ("Joinville", "SC", "47"), ("Blumenau", "SC", "47"), ("Itajaí", "SC", "47"),
    ("Florianópolis", "SC", "48"), ("Criciúma", "SC", "48"),
    ("Chapecó", "SC", "49"),
    ("Porto Alegre", "RS", "51"), ("Canoas", "RS", "51"),
    ("Pelotas", "RS", "53"),
    ("Caxias do Sul", "RS", "54"), ("Passo Fundo", "RS", "54"),
    ("Santa Maria", "RS", "55"),
    ("Brasília", "DF", "61"),
    ("Goiânia", "GO", "62"), ("Anápolis", "GO", "62"),
    ("Palmas", "TO", "63"),
    ("Rio Verde", "GO", "64"),
    ("Cuiabá", "MT", "65"),
    ("Rondonópolis", "MT", "66"),
    ("Campo Grande", "MS", "67"), ("Dourados", "MS", "67"),
    ("Rio Branco", "AC", "68"),
    ("Porto Velho", "RO", "69"),
    ("Salvador", "BA", "71"),
    ("Ilhéus", "BA", "73"), ("Itabuna", "BA", "73"),
    ("Feira de Santana", "BA", "75"),
    ("Vitória da Conquista", "BA", "77"),
    ("Aracaju", "SE", "79"),
    ("Recife", "PE", "81"), ("Olinda", "PE", "81"), ("Caruaru", "PE", "81"),
    ("Maceió", "AL", "82"),
    ("João Pessoa", "PB", "83"), ("Campina Grande", "PB", "83"),
    ("Natal", "RN", "84"), ("Mossoró", "RN", "84"),
    ("Fortaleza", "CE", "85"),
    ("Teresina", "PI", "86"),
    ("Petrolina", "PE", "87"),
    ("Juazeiro do Norte", "CE", "88"), ("Sobral", "CE", "88"),
    ("Belém", "PA", "91"), ("Ananindeua", "PA", "91"),
    ("Manaus", "AM", "92"),
    ("Santarém", "PA", "93"),
    ("Marabá", "PA", "94"),
    ("Boa Vista", "RR", "95"),
    ("Macapá", "AP", "96"),
    ("São Luís", "MA", "98"),
    ("Imperatriz", "MA", "99"),
)

# Faixas de CEP por UF (cinco primeiros dígitos, inclusive).
CEP_RANGES = {
    "SP": ((1000, 19999),),
    "RJ": ((20000, 28999),),
    "ES": ((29000, 29999),),
    "MG": ((30000, 39999),),
    "BA": ((40000, 48999),),
    "SE": ((49000, 49999),),
    "PE": ((50000, 56999),),
    "AL": ((57000, 57999),),
    "PB": ((58000, 58999),),
    "RN": ((59000, 59999),),
    "CE": ((60000, 63999),),
    "PI": ((64000, 64999),),
    "MA": ((65000, 65999),),
    "PA": ((66000, 68899),),
    "AP": ((68900, 68999),),
    "AM": ((69000, 69299), (69400, 69899)),
    "RR": ((69300, 69399),),
    "AC": ((69900, 69999),),
    "DF": ((70000, 72799), (73000, 73699)),
    "GO": ((72800, 72999), (73700, 76799)),
    "RO": ((76800, 76999),),
    "TO": ((77000, 77999),),
    "MT": ((78000, 78899),),
    "MS": ((79000, 79999),),
    "PR": ((80000, 87999),),
    "SC": ((88000, 89999),),
    "RS": ((90000, 99999),),
}

# Nono dígito do CPF: região fiscal onde o documento foi emitido.
CPF_REGION_DIGIT = {
    "RS": 0,
    "DF": 1, "GO": 1, "MS": 1, "MT": 1, "TO": 1,
    "AC": 2, "AM": 2, "AP": 2, "PA": 2, "RO": 2, "RR": 2,
    "CE": 3, "MA": 3, "PI": 3,
    "AL": 4, "PB": 4, "PE": 4, "RN": 4,
    "BA": 5, "SE": 5,
    "MG": 6,
    "ES": 7, "RJ": 7,
    "SP": 8,
    "PR": 9, "SC": 9,
}

EMAIL_DOMAINS = ("example.com", "example.org", "example.net")

COMPANY_NAMES = (
    "Horizonte Azul", "Vale Sereno", "Sol Poente", "Estrela Guia", "Ponto Firme",
    "Raiz Forte", "Nova Trilha", "Serra Clara", "Maré Mansa", "Ipê Roxo", "Bem-te-vi",
    "Sabiá", "Jequitibá", "Mandacaru", "Cajueiro", "Girassol", "Juriti",
    "Quatro Ventos", "Rosa dos Ventos", "Bom Caminho", "Colheita Farta", "Lua Cheia",
    "Céu Aberto", "Pedra Branca", "Rio Manso", "Lagoa Azul", "Remanso",
    "Três Coqueiros", "Pé de Serra", "Vento Sul",
)

# Atividade usada na razão social e modelo do nome fantasia.
ACTIVITIES = (
    ("Comércio de Alimentos", "Mercado {nome}"),
    ("Materiais de Construção", "Depósito {nome}"),
    ("Transportes", "Transportadora {nome}"),
    ("Serviços de Limpeza", "{nome} Limpeza"),
    ("Tecnologia da Informação", "{nome} Sistemas"),
    ("Consultoria Empresarial", "{nome} Consultoria"),
    ("Indústria de Móveis", "Móveis {nome}"),
    ("Confecções", "Confecções {nome}"),
    ("Padaria e Confeitaria", "Padaria {nome}"),
    ("Comércio de Autopeças", "{nome} Autopeças"),
    ("Distribuidora de Bebidas", "Distribuidora {nome}"),
    ("Engenharia", "{nome} Engenharia"),
    ("Comércio de Calçados", "Calçados {nome}"),
    ("Papelaria", "Papelaria {nome}"),
    ("Agropecuária", "Agropecuária {nome}"),
    ("Logística", "{nome} Logística"),
    ("Serviços Contábeis", "{nome} Contabilidade"),
    ("Clínica Veterinária", "Clínica Veterinária {nome}"),
    ("Escola de Idiomas", "Escola de Idiomas {nome}"),
    ("Restaurante", "Restaurante {nome}"),
)

COMPANY_SUFFIXES = (("Ltda", 6), ("S.A.", 1), ("ME", 3))

COMPANY_EMAIL_PREFIXES = ("contato", "financeiro", "comercial", "atendimento", "vendas")
