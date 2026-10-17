# A aldeia vista de fora, como no Purble Place: clicar numa oca entra nela.
# Edite à vontade: aqui não há lógica.
#
# - OCAS: cada oca ("dentro" é o cenário de dentro; "dentro_dia", se houver, é o de dia),
#   com o nome que aparece quando o mouse passa por cima, o contorno clicável (pontos x, y na tela 1600x900,
#   rente ao telhado e à casa no cenário "aldeia", sem a vegetação) e o cenário de dentro dela.
# - A aldeia aparece de dia (depois da fala do pajé, com uma seta para a entrada da aldeia,
#   onde chegam os visitantes) e de noite (depois do sinal do pajé).
# - ABERTAS_POR_NOITE: quais ocas dá para entrar em cada noite. Para abrir mais ocas no
#   decorrer do jogo, acrescente a noite e a lista. Noite que não estiver aqui usa a
#   última noite listada antes dela.
# - ONDE_DORME: em que oca fica cada pessoa de fora que o jogador deixou entrar, e o
#   apelido da imagem dela (dados/arte.py), sentada, e onde ela senta dentro da oca
#   ("posicao": o meio da borda de baixo da imagem; "escala": o tamanho; "espelhar": True
#   vira a pessoa para o outro lado).
# - ONDE_DORME_TAPIRI: o mesmo, dentro do tapiri, para quem o jogador levou para lá.

ALDEIA = {
    "fundo": "aldeia",
    "titulo": "Noite %d",
    "titulo_dia": "Dia %d",
    "dica": "Clique numa oca para entrar.",
    "dica_dormir": "Clique numa oca para entrar, ou durma até o amanhecer.",
    "dica_dia": "Clique numa oca para entrar, ou siga a seta até a entrada da aldeia.",
    "fechada": "%s · fechada esta noite",
    "fechada_dia": "%s · fechada hoje",
    "seta": "Entrada da aldeia",
    "seta_dormir": "Dormir",
}

# O tapiri: o abrigo isolado, longe das ocas. Quem é levado para lá fica "noites" noites
# (e a vaga abre de novo); a doença não passa de lá para ninguém.
# (Textos/Caraiba_Contas_dos_Finais.md: 1 vaga; Potira ergue a 2ª no dia 5.)
TAPIRI = {
    "vagas": 1,
    "noites": 3,
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
        "dentro": "oca2_noite",
        "dentro_dia": "oca2_dia",
        "painel": "esquerda",   # a cama fica à direita: o texto vai para a esquerda
    },
    "oca3": {
        "nome": "Wanadi",
        "contorno": [(1352, 85), (1420, 200), (1470, 300), (1480, 370), (1440, 400), (1400, 425), (1390, 510),
                     (1250, 515), (1200, 560), (1190, 580), (1090, 580), (1075, 520), (1062, 425), (1125, 410),
                     (1180, 330), (1270, 200)],
        "dentro": "oca3_noite",
        "dentro_dia": "oca3_dia",
        "painel": "esquerda",   # a cama fica à direita: o texto vai para a esquerda
    },
    # O tapiri, o abrigo isolado: ao lado da Yebá Bëló, no caminho que entra mais fundo na
    # mata. Lá dentro fica quem o jogador levou ao tapiri (ONDE_DORME_TAPIRI), não quem dorme
    # na oca. O tapiri não aparece no cenário: no lugar dele há uma seta /\ apontando para
    # dentro da mata ("seta": True), sempre à vista.
    "tapiri": {
        "nome": "Tapiri",
        "contorno": [(780, 400), (816, 446), (802, 458), (780, 430), (758, 458), (744, 446)],
        "seta": True,
        "dentro": "tapiri",
        "tapiri": True,
        "painel": "esquerda",   # a esteira fica à direita: o texto vai para a esquerda
    },
}

# O tapiri abre desde a noite 1 (o pajé fala dele na primeira fogueira).
ABERTAS_POR_NOITE = {
    1: ["oca1", "tapiri"],
    2: ["oca1", "oca2", "tapiri"],
    3: ["oca1", "oca2", "oca3", "tapiri"],
}

ONDE_DORME = {
    # Yara senta sobre a cama (a esteira grande do meio), com os pés na beirada da frente.
    # Ocupa quase toda a altura da parede (a parede vai de y 215 a 515: uns 300; Yara, uns 265).
    "Yara": {"oca": "oca1", "imagem": "yara_sentada", "posicao": (700, 600), "escala": 0.5},
    # Mbaé senta sobre a cama (o estrado da direita), na mesma pose da fogueira. Ocupa um pouco
    # mais que a metade da altura da parede (a parede vai de y 235 a 570: uns 335; Mbaé, uns 195).
    "Mbaé": {"oca": "oca2", "imagem": "mbae_sentado", "posicao": (1290, 570), "escala": 0.31},
    # Potira senta sobre a cama da oca Wanadi (a cama fica à direita), virada para o fogo.
    "Potira": {"oca": "oca3", "imagem": "potira_sentada", "posicao": (1240, 652), "escala": 0.33,
               "espelhar": True},
    # Tamandaré-mirim senta no chão da oca Yebá Bëló, à esquerda da porta.
    "Tamandaré-mirim": {"oca": "oca2", "imagem": "tamandare_sentado", "posicao": (590, 592), "escala": 0.33},
    # Iandé divide a oca Yorixiriamori com Yara: senta no chão com as costas no poste do meio,
    # de frente para o fogo (à direita).
    "Iandé": {"oca": "oca1", "imagem": "iande_sentada", "posicao": (1327, 765), "escala": 0.38},
}

# Onde senta, dentro do tapiri, quem o jogador levou para lá: no mesmo lugar, sobre a esteira
# trançada da direita (só cabe um por vez: TAPIRI["vagas"]). A "escala" de cada um deixa todos
# com a mesma altura na tela (uns 235, pouco mais que a metade da parede, que tem uns 390),
# porque os desenhos sentados têm tamanhos diferentes.
ONDE_DORME_TAPIRI = {
    "Yara": {"imagem": "yara_sentada", "posicao": (1225, 668), "escala": 0.44},
    "Mbaé": {"imagem": "mbae_sentado", "posicao": (1225, 668), "escala": 0.446},
    "Potira": {"imagem": "potira_sentada", "posicao": (1225, 668), "escala": 0.42},
    "Tamandaré-mirim": {"imagem": "tamandare_sentado", "posicao": (1225, 668), "escala": 0.453},
    "Iandé": {"imagem": "iande_sentada", "posicao": (1225, 668), "escala": 0.428},
}

# Textos de dentro da oca.
OCA = {
    "sair": "Sair da oca",
    "sair_tapiri": "Sair do tapiri",
    "dorme": "%s dorme aqui esta noite.",
    "dormem": "%s dormem aqui esta noite.",
    "vazia": "Ninguém de fora dorme aqui esta noite.",
    "vazia_dia": "Por enquanto, ninguém de fora dorme aqui.",
    "dorme_dia": "%s dorme aqui.",
    "dormem_dia": "%s dormem aqui.",
    "aqui_dia": "%s está aqui dentro. Clique para conversar.",
    "vazio_tapiri": "Ninguém está no tapiri.",
}


def ocas_abertas(noite):
    """As ocas em que dá para entrar nessa noite (a última noite listada vale até a próxima)."""
    noites = [n for n in ABERTAS_POR_NOITE if n <= noite]
    return ABERTAS_POR_NOITE[max(noites)] if noites else []
