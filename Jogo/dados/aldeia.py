# A aldeia vista de fora, como no Purble Place: clicar numa oca entra nela.
# Edite à vontade: aqui não há lógica.
#
# - OCAS: cada oca, com o nome que aparece quando o mouse passa por cima, o contorno clicável (pontos x, y na tela 1600x900,
#   rente ao telhado e à casa no cenário "aldeia", sem a vegetação) e o cenário de dentro dela.
# - A aldeia aparece de dia (depois da fala do pajé, com uma seta para a entrada da aldeia,
#   onde chegam os visitantes) e de noite (depois do sinal do pajé).
# - ABERTAS_POR_NOITE: quais ocas dá para entrar em cada noite. Para abrir mais ocas no
#   decorrer do jogo, acrescente a noite e a lista. Noite que não estiver aqui usa a
#   última noite listada antes dela.
# - ONDE_DORME: em que oca fica cada pessoa de fora que o jogador deixou entrar, e o
#   apelido da imagem dela (dados/arte.py).

ALDEIA = {
    "fundo": "aldeia",
    "titulo": "Noite %d",
    "titulo_dia": "Dia %d",
    "dica": "Clique numa oca para entrar.",
    "dica_dia": "Clique numa oca para entrar, ou siga a seta até a entrada da aldeia.",
    "fechada": "%s · fechada esta noite",
    "fechada_dia": "%s · fechada hoje",
    "seta": "Entrada da aldeia",
}

OCAS = {
    "oca1": {
        "nome": "Yorixiriamori",
        "contorno": [(465, 262), (530, 320), (600, 400), (640, 455), (682, 470), (682, 515), (672, 545),
                     (605, 545), (590, 515), (480, 515), (478, 460), (460, 405), (420, 375), (362, 372)],
        "dentro": "oca1",
    },
    "oca2": {
        "nome": "Yebá Bëló",
        "contorno": [(922, 318), (1008, 435), (960, 456), (850, 456), (840, 422)],
        "dentro": None,   # ainda sem arte de dentro ligada (Arte/Ocas/Yebá Bëló_dia_2 e _noite_2)
    },
    "oca3": {
        "nome": "Wanadi",
        "contorno": [(1352, 85), (1420, 200), (1470, 300), (1480, 370), (1440, 400), (1400, 425), (1390, 510),
                     (1250, 515), (1200, 560), (1190, 580), (1090, 580), (1075, 520), (1062, 425), (1125, 410),
                     (1180, 330), (1270, 200)],
        "dentro": None,   # ainda sem arte de dentro ligada (Arte/Ocas/Wanadi_dia_3 e _noite_3)
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
    "vazia_dia": "Por enquanto, ninguém de fora dorme aqui.",
    "em_breve": "O exame do rosto, na fogueira, chega na próxima etapa do jogo.",
}


def ocas_abertas(noite):
    """As ocas em que dá para entrar nessa noite (a última noite listada vale até a próxima)."""
    noites = [n for n in ABERTAS_POR_NOITE if n <= noite]
    return ABERTAS_POR_NOITE[max(noites)] if noites else []
