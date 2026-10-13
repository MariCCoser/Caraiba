# Os finais do jogo, na ordem da fila. Edite à vontade: aqui não há lógica.
#
# Fonte: Textos/Caraiba_Os_Finais.pdf. As contas de cada final (o que o jogador precisa
# fazer e em que noite, no mínimo, o final pode acontecer): Textos/Caraiba_Contas_dos_Finais.md.
#
# Como o jogo escolhe o final:
# - No fim de CADA noite, o jogo testa os finais que têm "antecipado": True, na ordem da
#   fila. Se a condição de um deles já bate, o jogo acaba ali (pode ser na noite 4, na 6...).
# - Na manhã do dia 10 (DIA_DO_CALCULO), antes de Araci chegar, o jogo testa a fila inteira
#   e fica com o primeiro final que bater. O Vazio, o último, sempre bate.
#
# A "condicao" é uma lista de jeitos de chegar ao final (basta UM deles). Cada jeito é um
# dicionário com as variáveis do estado.py e a conta que elas precisam passar; todas as
# contas do mesmo jeito precisam bater juntas. As contas podem ser ">= 2", "<= 7" ou "== 0".
#   Exemplo: [{"entregues": ">= 2"}, {"proximidade_vila": ">= 3"}]
#            = entregou 2 ou mais pessoas, OU ficou próximo demais da vila (3 ou mais).
#
# Cada final tem três telas: a "cena" (o que aconteceu com a aldeia), o "povo" e o "fato"
# (o povo real que fez um caminho parecido e o que aconteceu com ele) e a "fonte".
# Os textos das cenas são um rascunho: o grupo pode reescrever.

DIA_DO_CALCULO = 10

FINAIS = [
    {
        "id": "troca",
        "nome": "A Troca",
        "povo": "Tupiniquim",
        "condicao": [{"entregues": ">= 2"}, {"proximidade_vila": ">= 3"}],
        "antecipado": True,
        "cena": "A vila manda gente para cuidar da aldeia, do jeito dela. "
                "Os nomes que foram com o Irmão Aleixo não voltam.",
        "fato": "Os Tupiniquim eram cerca de 90 mil em 1500 e 55 em 1876. Hoje são cerca de "
                "2.500, em Aracruz (ES), numa terra reconhecida em 2007 depois de décadas de "
                "disputa com uma empresa de celulose.",
        "fonte": "Instituto Socioambiental, Povos Indígenas no Brasil: Tupiniquim.",
    },
    {
        "id": "loucura",
        "nome": "A Loucura",
        "povo": "Tupinambá (Santidade de Jaguaripe)",
        "condicao": [{"mortos_por_sua_mao": ">= 3"}],
        "antecipado": True,
        "cena": "Ninguém mais dorme perto de você. Antes do sol, a aldeia manda você para a mata.",
        "fato": "Vinte anos depois de 1562, tupinambá fugidos dos aldeamentos e da escravidão "
                "formaram a Santidade de Jaguaripe (1580-1585), liderada por Antônio e por Maria. "
                "Foi destruída por ordem do governador Manuel Teles Barreto. "
                "O nome “Loucura” fala de você; a Santidade foi resistência.",
        "fonte": "Ronaldo Vainfas, A Heresia dos Índios (1995).",
    },
    {
        "id": "batismo",
        "nome": "A Água do Batismo",
        "povo": "Caeté",
        "condicao": [{"seguiu_paje": ">= 3", "inocentes": ">= 1"}],
        "antecipado": False,
        "cena": "A aldeia sobrevive, mas cada um dorme de costas para o outro. Na vila, um padre "
                "derrama água na testa de um doente, que morre logo depois.",
        "fato": "Em abril de 1563, na aldeia de Santiago, na Bahia, os jesuítas batizaram 84 "
                "indígenas à beira da morte, e todos morreram. No mesmo período, o governador "
                "Mem de Sá declarou que os Caeté podiam ser escravizados onde fossem encontrados.",
        "fonte": "Carta do padre Leonardo do Valle ao padre Gonçalo Vaz, Bahia, 12 de maio de 1563.",
    },
    {
        "id": "rio_acima",
        "nome": "Rio Acima",
        "povo": "Aimoré, hoje Krenak",
        "condicao": [{"rio_acima": ">= 4", "entregues": "== 0"}],
        "antecipado": True,
        "cena": "A aldeia sobe o rio atrás de Krenan. As ocas ficam vazias para trás.",
        "fato": "A carta régia de 13 de maio de 1808 declarou guerra oficial contra os Aimoré, "
                "chamados de Botocudos. Os descendentes incluem os Krenak, que vivem no Vale do "
                "Rio Doce (MG), o Watu, atingido pela lama da barragem de Mariana em 2015.",
        "fonte": "Carta Régia de 13 de maio de 1808; Instituto Socioambiental: Krenak.",
    },
    {
        "id": "anhanga",
        "nome": "Anhangá",
        "povo": "Potiguara",
        "condicao": [{"viu_anhanga": ">= 3", "mortos_por_sua_mao": "== 0", "entregues": "== 0"}],
        "antecipado": False,
        "cena": "Quando Araci chega à entrada, o veado branco está parado atrás dela. Depois some.",
        "fato": "Os missionários transformaram o Anhangá, protetor dos animais, em demônio: o "
                "bandeirante Bartolomeu Bueno da Silva ganhou o apelido de Anhanguera, “diabo "
                "velho”. É o mesmo caminho da palavra caraíba: de sagrado a invasor.",
        "fonte": "José Vieira Couto de Magalhães, O Selvagem (1876); autos de José de Anchieta.",
    },
    {
        "id": "honra",
        "nome": "A Honra",
        "povo": "Tupinambá",
        "condicao": [{"vivos": ">= 9", "memoria": ">= 5", "mortos_por_sua_mao": "== 0",
                      "entregues": "== 0"}],
        "antecipado": False,
        "cena": "A aldeia chega ao fim da febre com as histórias de quem entrou guardadas.",
        "fato": "Um manto tupinambá de penas vermelhas, levado para a Europa no século XVII, "
                "voltou ao Museu Nacional, no Rio, em 2024. Os Tupinambá de Olivença (BA) lutam "
                "hoje pela demarcação da terra.",
        "fonte": "Museu Nacional/UFRJ (2024); Instituto Socioambiental: Tupinambá.",
    },
    {
        "id": "tapiri",
        "nome": "O Tapiri",
        "povo": "Korubo",
        "condicao": [{"tapiri_usos": ">= 3", "vivos": ">= 7", "mortos_por_sua_mao": "== 0",
                      "entregues": "== 0"}],
        "antecipado": False,
        "cena": "Poucas redes em volta da fogueira. Ao longe, o tapiri com uma luz acesa: "
                "o pajé cuida de quem está lá.",
        "fato": "Os Korubo vivem no Vale do Javari (AM), a região com mais povos isolados do "
                "mundo. Em 2020, na covid-19, o STF mandou erguer barreiras sanitárias nas terras "
                "de povos isolados (ADPF 709). O tapiri de 1562 virou decisão da Justiça.",
        "fonte": "Instituto Socioambiental, agosto de 2020: o referendo da ADPF 709 no STF.",
    },
    {
        "id": "vazio",
        "nome": "O Vazio",
        "povo": "Goitacá",
        # Sempre bate (é o que sobra). Antes do dia 10, só acaba o jogo se a aldeia esvaziar.
        "condicao": [{}],
        "antecipado": False,
        "cena": "As redes ficam vazias, uma a uma. Ninguém invadiu: a febre decidiu por você.",
        "fato": "Os Goitacá eram temidos por boato: cronistas os descreveram como ferozes sem "
                "nunca ter convivido com eles. Desapareceram no século XVIII, entre guerras e "
                "epidemias. É o único final de um povo que não existe mais.",
        "fonte": "Anthony Knivet (c. 1597); frei Vicente do Salvador, História do Brasil (1627).",
        # A aldeia esvaziou antes do dia 10: o jogo acaba no fim da noite em que isso acontecer.
        "esvaziou": {"vivos": "<= 7"},
    },
]

# Textos fixos da tela de final.
TELA_FINAL = {
    "povo": "O que aconteceu com vocês aconteceu de verdade com este povo: %s.",
    "fonte": "Fonte",
    "seguir": "Continuar",
    "menu": "Voltar ao menu",
    "fundo": "fogueira_longe",
}
