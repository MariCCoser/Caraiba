# As conversas de sempre de quem é de fora. Edite à vontade: aqui não há lógica.
#
# Quem é de fora (Yara, Mbaé, Potira, Tamandaré-mirim, Iandé) tem uma conversa só, a mesma na oca (de dia,
# dados/dias.py) e em todas as noites na fogueira (dados/noites.py). Muda só a primeira frase
# de cada noite. (Potira é a exceção: na fogueira, a conversa dela é mais curta.)
#
# Uma pergunta com "historia" soma a "memoria" (estado.py) só na primeira vez que o jogador
# ouve aquela história: ouvir de novo, em outra noite, não soma mais.


def conversa_yara():
    """As perguntas de sempre para Yara (uma lista nova a cada vez)."""
    return [
        {"pergunta": "Conte da sua aldeia.",
         "resposta": [
             "Ficava na boca de um rio grande. Dava para ver os barcos de longe.",
             "Os barcos queriam pau de tinta. A gente cortava, eles davam ferro.",
             "Cortar árvore com pedra levava o dia. Com o ferro, leva pouco.",
         ],
         "historia": "aldeia_yara", "efeitos": {"memoria": 1}},
        {"pergunta": "Por que saiu de lá?",
         "resposta": [
             "Os caraíbas levaram muita gente para perto da vila. Minha mãe foi.",
             "Eu não fui. Vou para o sul, onde mora [a gente do meu pai].",
         ]},
        {"pergunta": "A maldição chegou lá?",
         "resposta": [
             "Chegou com as chuvas. Quem cuidava dos amaldiçoados caía depois.",
             "Eu saí antes. [Não estou amaldiçoada].",
         ]},
    ]


def conversa_mbae():
    """As perguntas de sempre para Mbaé (a conversa dele na oca Yebá Bëló)."""
    return [
        {"pergunta": "Conte de antes.",
         "resposta": [
             "Antes a gente seguia a anta pelo rio inteiro. Sem dono de margem.",
             "Agora desce barco pelo rio, e a caça foge para dentro da mata.",
         ],
         "historia": "antes_mbae", "efeitos": {"memoria": 1}},
        {"pergunta": "Por que olham torto para você?",
         "resposta": "Contam histórias do meu povo. [Nenhuma é verdade]."},
    ]


def conversa_potira():
    """As perguntas de sempre para Potira (a conversa dela na oca Wanadi). Na entrada da
    aldeia, a conversa é mais curta (dados/dias.py, Dia 4). Não há pergunta sobre comida:
    ela já começa a conversa dizendo que não achou nada."""
    return [
        {"pergunta": "Viu gente amaldiçoada?",
         "resposta": "Vi rede vazia pendurada. Não entrei."},
        {"pergunta": "Por que foi sozinha?",
         "resposta": "Quem ia comigo está na rede, com a maldição. Alguém tinha que ir."},
        {"pergunta": "Conte de antes.",
         "resposta": [
             "Minha mãe dizia que a mandioca precisa de gente perto para crescer.",
             "Acho que é verdade.",
         ],
         "historia": "antes_potira", "efeitos": {"memoria": 1}},
    ]


def conversa_tamandare():
    """As perguntas de sempre para Tamandaré-mirim (a conversa dele na oca Yebá Bëló).
    Na entrada da aldeia, a conversa é mais curta (dados/dias.py, Dia 5).
    "Caraíbas", na boca dele, são os homens brancos."""
    return [
        {"pergunta": "Conte do que você prega.",
         "resposta": [
             "Que a terra sem mal está perto.",
             "Que quem largar o trabalho dos caraíbas chega lá.",
         ],
         "historia": "prega_tamandare", "efeitos": {"memoria": 1}},
        {"pergunta": "Por que tosse?",
         "resposta": "[Rouco de pregar]. Grito para as árvores desde a lua nova."},
        {"pergunta": "Por que essa cruz?",
         "resposta": [
             "Tirei dos caraíbas.",
             "Se o deus deles mora nela, agora ele anda comigo.",
         ]},
    ]


def conversa_iande():
    """As perguntas de sempre para Iandé (a conversa dela na oca Yorixiriamori, com Yara).
    Na entrada da aldeia, a conversa é mais curta (dados/dias.py, Dia 7)."""
    return [
        {"pergunta": "Como estava a vila?",
         "resposta": "Todo mundo bem. Tinha festa de santo."},
        {"pergunta": "Viu alguém amaldiçoado?",
         "resposta": "Vi uma casa fechada, com uma cruz na porta."},
        {"pergunta": "Que conta é essa no pulso?", "no_maximo": {"pulseira": 0},   # se não a deu
         "resposta": "Ganhei na festa. É de vidro, brilha no sol."},
        {"pergunta": "Conte da viagem.",
         "resposta": [
             "Fui com o cesto cheio de mandioca. Voltei com ele vazio, e com sal.",
             "Na vila, um caraíba jogou água na minha cabeça. Disse que agora eu tenho outro nome.",
         ],
         "historia": "viagem_iande", "efeitos": {"memoria": 1}},
    ]


def conversa_araci(na_oca=True):
    """As perguntas de sempre para Araci. Na oca Wanadi, a conversa inteira; na fogueira, sem
    as perguntas da criança (o nome e o pai). Na entrada da aldeia, só as duas primeiras
    (dados/dias.py, Dia 10)."""
    perguntas = [
        {"pergunta": "De onde você vem?",
         "resposta": [
             "De onde o mar bate. Não tem mais ninguém lá.",
             "Os caraíbas chegaram com a cruz e com a tosse. A aldeia fugiu.",
             "Quem ficou, ficou nas redes.",
         ]},
        {"pergunta": "Desde quando as manchas?",
         "resposta": "Desde que desceram do rosto. Dois dias."},
    ]
    if na_oca:
        perguntas += [
            {"pergunta": "Como ela vai se chamar?",
             "resposta": [
                 "Se for menina, Jaci.",
                 "Se for menino, eu não pensei ainda.",
             ],
             "historia": "filho_araci", "efeitos": {"memoria": 1}},
            {"pergunta": "Onde está o pai da criança?",
             "resposta": "Ficou na trilha, dois dias atrás. [Ele vem depois]."},
        ]
    perguntas.append({"pergunta": "Você sente dor?",
                      "resposta": "Nas costas. A criança chuta de noite."})
    return perguntas
