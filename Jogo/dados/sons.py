# Os sons do jogo e onde cada um toca. Edite à vontade: aqui não há lógica.
#
# Os arquivos ficam em assets/sons, em .ogg (funciona no computador e no navegador). Para
# converter um mp3 ou wav (e cortar um som longo): python -m ferramentas.converter_sons.
#
# AMBIENTES: o fundo de cada lugar, tocando em loop. Cada ambiente é uma mistura de sons, com o
# volume de cada um (0 a 1). Na troca de lugar, o que sai some devagar e o que entra aparece
# devagar (TROCA_MS); um som que está nos dois lugares continua tocando, sem recomeçar, e só
# muda de volume (também devagar: ao entrar na oca, a mata fica mais baixa aos poucos).
# Quem escolhe o ambiente é a cena (o método som_ambiente de cada arquivo em cenas/).

SONS = {
    "fogueira": "sons/Fogueira.ogg",
    "floresta_dia": "sons/FlorestaDia.ogg",
    "floresta_noite": "sons/FlorestaNoite.ogg",
    "maraca": "sons/Maraca.ogg",
    "flauta": "sons/Flauta.ogg",
    "passos": "sons/Passos.ogg",
    "anhanga": "sons/Anhanga.ogg",
}

AMBIENTES = {
    # Menu, Opções, Como se joga e a lista de Finais: a fogueira de longe e a flauta.
    "menu": {"fogueira": 0.45, "flauta": 0.5},
    # A introdução (os cartões de texto): a flauta e a mata de dia, que começa baixinha e cresce
    # a cada cartão (CRESCEM) até o volume do dia, quando o pajé fala no Dia 1.
    "introducao": {"flauta": 0.45, "floresta_dia": 0.6},
    # De dia: a entrada da aldeia, a aldeia e as ocas.
    "dia": {"floresta_dia": 0.6},
    "dia_na_oca": {"floresta_dia": 0.3},
    # De noite, longe do fogo: a aldeia e as ocas.
    "noite": {"floresta_noite": 0.6, "fogueira": 0.15},
    "noite_na_oca": {"floresta_noite": 0.3, "fogueira": 0.1},
    # De noite, na fogueira (o sinal do pajé e a conversa em volta do fogo): o maracá do pajé.
    "fogueira": {"fogueira": 0.6, "floresta_noite": 0.25, "maraca": 0.3},
    # A visão do Anhangá, na mata (noites 2, 5 e 9, "Que barulho é esse na mata?"): o som do
    # Anhangá bem baixo, por baixo da mata, só para parecer algo místico.
    "anhanga": {"floresta_noite": 0.6, "anhanga": 0.25},
    # As telas do final.
    "final": {"flauta": 0.55, "fogueira": 0.25},
}

# Os sons que crescem aos poucos num ambiente: o volume deles vai de quase nada até o de
# AMBIENTES, conforme a cena avança (Cena.som_intensidade: na introdução, a cada cartão).
CRESCEM = {"introducao": ["floresta_dia"]}
# A introdução começa com a mata nesta fração do volume (e chega a 1 no último cartão).
INTENSIDADE_INICIAL_INTRODUCAO = 0.15

# Finais com um ambiente próprio (o "id" de dados/finais.py); os outros tocam o "final".
AMBIENTE_DO_FINAL = {}

# Cenários com um ambiente próprio, no Dia (o apelido de dados/arte.py começando assim).
AMBIENTE_DO_CENARIO = {"anhanga_": "anhanga"}

# Sons curtos, tocados uma vez: o volume e em quantos milissegundos ele some (0 = toca inteiro).
# "passos": alguém novo sobe a trilha até a entrada da aldeia (o passo "visitante" de
# dados/dias.py, com o cenário CENARIO_DOS_PASSOS). Dentro da oca ou na fogueira, não toca.
CENARIO_DOS_PASSOS = "floresta"
EFEITOS = {
    "passos": {"volume": 0.8, "some_em_ms": 3500},
}

TROCA_MS = 2000   # quanto um som leva para ir do silêncio ao volume 1 (e de volta)
