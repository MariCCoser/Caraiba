# Os sons do jogo e onde cada um toca. Edite à vontade: aqui não há lógica.
#
# Os arquivos ficam em assets/sons, em .ogg (funciona no computador e no navegador). Para
# converter um mp3 ou wav (e cortar um som longo): python -m ferramentas.converter_sons.
#
# AMBIENTES: o fundo de cada lugar, tocando em loop. Cada ambiente é uma mistura de sons, com o
# volume de cada um (0 a 1). Na troca de lugar, o que sai some devagar e o que entra aparece
# devagar (TROCA_MS); um som que está nos dois lugares continua tocando, sem recomeçar.
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
    # A introdução (os cartões de texto): só a flauta.
    "introducao": {"flauta": 0.5},
    # De dia: a entrada da aldeia, a aldeia e as ocas.
    "dia": {"floresta_dia": 0.6},
    "dia_na_oca": {"floresta_dia": 0.3},
    # De noite, longe do fogo: a aldeia e as ocas.
    "noite": {"floresta_noite": 0.6, "fogueira": 0.15},
    "noite_na_oca": {"floresta_noite": 0.3, "fogueira": 0.1},
    # De noite, na fogueira (o sinal do pajé e a conversa em volta do fogo): o maracá do pajé.
    "fogueira": {"fogueira": 0.6, "floresta_noite": 0.25, "maraca": 0.3},
    # A visão do Anhangá: o pajé aponta a mata (noites 2, 5 e 9, "Que barulho é esse na mata?").
    "anhanga": {"anhanga": 0.7, "floresta_noite": 0.2},
    # As telas do final.
    "final": {"flauta": 0.55, "fogueira": 0.25},
    "final_anhanga": {"anhanga": 0.6, "flauta": 0.25},
}

# Finais com um ambiente próprio (o "id" de dados/finais.py); os outros tocam o "final".
AMBIENTE_DO_FINAL = {"anhanga": "final_anhanga"}

# Cenários com um ambiente próprio, no Dia (o apelido de dados/arte.py começando assim).
AMBIENTE_DO_CENARIO = {"anhanga_": "anhanga"}

# Sons curtos, tocados uma vez: o volume e em quantos milissegundos ele some (0 = toca inteiro).
# "passos": alguém novo sobe a trilha até a entrada da aldeia (o passo "visitante" de
# dados/dias.py, com o cenário CENARIO_DOS_PASSOS). Dentro da oca ou na fogueira, não toca.
CENARIO_DOS_PASSOS = "floresta"
EFEITOS = {
    "passos": {"volume": 0.8, "some_em_ms": 6000},
}

TROCA_MS = 1200
