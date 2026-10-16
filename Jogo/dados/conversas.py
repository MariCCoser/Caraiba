# As conversas de sempre de quem é de fora. Edite à vontade: aqui não há lógica.
#
# Quem é de fora (Yara, Mbaé, Potira) tem uma conversa só, a mesma na oca (de dia,
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
             "Os padres levaram muita gente para perto da vila. Minha mãe foi.",
             "Eu não fui. Vou para o sul, onde mora [a gente do meu pai].",
         ]},
        {"pergunta": "A febre chegou lá?",
         "resposta": [
             "Chegou com as chuvas. Quem cuidava dos doentes caía depois.",
             "Eu saí antes. [Não estou doente].",
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
        {"pergunta": "Viu gente doente?",
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
