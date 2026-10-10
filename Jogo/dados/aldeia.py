# A aldeia vista de fora, como no Purble Place: clicar numa oca entra nela.
# Edite à vontade: aqui não há lógica.
#
# - OCAS: cada oca, com o nome na tela, o contorno clicável (pontos x, y na tela 1600x900,
#   em volta do telhado e da casa no cenário "aldeia") e o cenário de dentro dela.
# - ABERTAS_POR_NOITE: quais ocas dá para entrar em cada noite. Para abrir mais ocas no
#   decorrer do jogo, acrescente a noite e a lista. Noite que não estiver aqui usa a
#   última noite listada antes dela.
# - ONDE_DORME: em que oca fica cada pessoa de fora que o jogador deixou entrar, e o
#   apelido da imagem dela (dados/arte.py).

ALDEIA = {
    "fundo": "aldeia",
    "titulo": "Noite %d",
    "dica": "Clique numa oca para entrar.",
    "fechada": "%s · fechada esta noite",
}

OCAS = {
    "oca1": {
        "nome": "Oca 1",
        "contorno": [(475, 248), (565, 330), (640, 440), (670, 545), (360, 545), (352, 420), (400, 330)],
        "dentro": "oca1",
    },
    "oca2": {
        "nome": "Oca 2",
        "contorno": [(925, 322), (970, 380), (1005, 445), (1000, 472), (848, 472), (845, 445), (880, 380)],
        "dentro": None,   # ainda sem arte de dentro ligada (Arte/Ocas/Interior_dia_2 e _noite_2)
    },
    "oca3": {
        "nome": "Oca 3",
        "contorno": [(1355, 88), (1420, 230), (1485, 400), (1465, 525), (1210, 600), (1085, 525),
                     (1060, 420), (1135, 400), (1290, 230)],
        "dentro": None,   # ainda sem arte de dentro ligada (Arte/Ocas/Interior_dia_3 e _noite_3)
    },
}

ABERTAS_POR_NOITE = {
    1: ["oca1"],
}

ONDE_DORME = {
    "Yara": {"oca": "oca1", "imagem": "yara"},
}

# Textos de dentro da oca.
OCA = {
    "sair": "Sair da oca",
    "dorme": "%s dorme aqui esta noite.",
    "vazia": "Ninguém de fora dorme aqui esta noite.",
    "em_breve": "O exame do rosto, na fogueira, chega na próxima etapa do jogo.",
}


def ocas_abertas(noite):
    """As ocas em que dá para entrar nessa noite (a última noite listada vale até a próxima)."""
    noites = [n for n in ABERTAS_POR_NOITE if n <= noite]
    return ABERTAS_POR_NOITE[max(noites)] if noites else []
