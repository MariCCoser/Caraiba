# Os finais do jogo, na ordem da fila. Edite à vontade: aqui não há lógica.
#
# Fonte: Textos/Caraiba_Os_Finais.pdf. As contas de cada final (o que o jogador precisa
# fazer e em que noite, no mínimo, o final pode acontecer): Textos/Caraiba_Contas_dos_Finais.md.
#
# Como o jogo escolhe o final:
# - No fim de CADA noite, o jogo testa os finais que têm "antecipado": True, na ordem da
#   fila. Se a condição de um deles já bate, o jogo acaba ali (pode ser na noite 4, na 6...).
#   Com "a_partir_da_noite": 9, o final só é testado do fim da noite 9 em diante.
# - Na manhã do dia 10 (DIA_DO_CALCULO), antes de Araci chegar, o jogo testa a fila inteira
#   e fica com o primeiro final que bater. O Vazio, o último, sempre bate. O final aparece
#   no fim da noite 10, e nada do que o jogador faz com Araci o muda.
# - A exceção é quem tem "ultima_noite": True (Rio Acima): ele é testado no fim da noite 10,
#   antes do final calculado de manhã. É a escolha "Ir com ele", quando Krenan volta nessa noite.
#
# A "condicao" é uma lista de jeitos de chegar ao final (basta UM deles). Cada jeito é um
# dicionário com as variáveis do estado.py e a conta que elas precisam passar; todas as
# contas do mesmo jeito precisam bater juntas. As contas podem ser ">= 2", "<= 7" ou "== 0";
# para duas contas na mesma variável, uma lista: "vivos": [">= 3", "<= 4"].
#   Exemplo: [{"entregues": ">= 2"}, {"proximidade_vila": ">= 3"}]
#            = entregou 2 ou mais pessoas, OU ficou próximo demais da vila (3 ou mais).
#
# Cada final tem três telas: a "cena" (o que aconteceu com a aldeia), o "povo" e o "fato"
# (o povo real que fez um caminho parecido e o que aconteceu com ele) e a "fonte".
# Os textos das cenas são um rascunho: o grupo pode reescrever.
# "fundo": a imagem atrás das três telas (dados/arte.py); sem ele, TELA_FINAL["fundo"].
#
# A chance de cada final (aparece na tela da fonte, com "Final 5/10": a posição na fila). Os
# números vêm do simulador (Jogo/ferramentas/simular_finais.py; Textos/Caraiba_Porcentagens_dos_Finais.md):
#   "chance_acaso"     em quantas partidas (%) o final acontece, jogando ao acaso
#   "chance_tentando"  em quantas partidas (%) dá certo, para quem tenta esse final
#                      (None: não se mostra, como em O Vazio, que é o que sobra)
# Mudou o roteiro ou as condições? Rode o simulador de novo e troque os números.
# Ao acaso: 400 partidas em 25/10/2026. "Tentando" ainda sem números atuais (a simulação por
# estratégia não terminou): enquanto for None, a tela mostra só a chance ao acaso.
#
# "vivos" conta só quem é de fora e está vivo na aldeia: a aldeia é o jogador, o pajé e quem
# o jogador deixou entrar (no máximo 5 até o dia 10).

DIA_DO_CALCULO = 10

# "Voltar a honra": a Honra já pediu ouvir as 5 histórias (memoria >= 5), o que obriga a
# conversar com todos os visitantes. Por enquanto está desligado; para voltar, troque para True.
# (Com as histórias desligadas, O Tapiri vem antes da Honra na fila: senão ele nunca aconteceria.)
HONRA_PEDE_HISTORIAS = False
CONDICAO_HONRA = {"vivos": ">= 2", "mortos_saos_por_sua_mao": "== 0", "tapiri_saos": "== 0"}
if HONRA_PEDE_HISTORIAS:
    CONDICAO_HONRA["memoria"] = ">= 5"

FINAIS = [
    {
        "id": "guerra_justa",
        "chance_acaso": 1.8, "chance_tentando": None,
        "nome": "Guerra Justa",
        "povo": "Caeté",
        # No dia 9, o jogador atira no Irmão Aleixo com o arco (dados/dias.py, ARCO). É o primeiro
        # da fila e vence todos os outros: acaba o jogo no fim da noite 9.
        "condicao": [{"aleixo_morto": ">= 1"}],
        "antecipado": True,
        "a_partir_da_noite": 9,
        "cena": "No dia 10, a trilha amanhece cheia de homens do governador. Trazem a flecha. "
                "Ninguém pergunta quem tem febre. Ninguém pergunta quem atirou. O morador que você "
                "salvou na trilha sai amarrado com os outros. Na vila, um papel já diz que a guerra "
                "contra esta aldeia é justa.",
        "fato": "Em 1562, o governador Mem de Sá declarou guerra contra os Caeté, como castigo pela "
                "morte do bispo Sardinha seis anos antes. Em poucos meses, mais de 50 mil pessoas "
                "foram capturadas. Cerca de 10 mil chegaram aos engenhos; o resto morreu de varíola "
                "e maus-tratos.",
        "fonte": "John Monteiro, “O escravo índio, esse desconhecido” (1992); Mecenas Santos, "
                 "Embates entre a cruz e a espada (ANPUH, 2011).",
    },
    {
        "id": "troca",
        "chance_acaso": 13.8, "chance_tentando": None,
        "nome": "A Troca",
        "povo": "Tupiniquim",
        "condicao": [{"entregues": ">= 2"}, {"proximidade_vila": ">= 3"}],
        "antecipado": True,
        "fundo": "troca_final",
        "cena": "A vila manda gente para cuidar da aldeia, do jeito dela. "
                "Os nomes que foram com o Irmão Aleixo não voltam.",
        "fato": "Os Tupiniquim eram cerca de 90 mil em 1500 e 55 em 1876. Hoje são cerca de "
                "2.500, em Aracruz (ES), numa terra reconhecida em 2007 depois de décadas de "
                "disputa com uma empresa de celulose.",
        "fonte": "Instituto Socioambiental, Povos Indígenas no Brasil: Tupiniquim.",
    },
    {
        "id": "loucura",
        "chance_acaso": 2.2, "chance_tentando": None,
        "nome": "A Loucura",
        "povo": "Tupinambá (Santidade de Jaguaripe)",
        "condicao": [{"mortos_por_sua_mao": ">= 3"}],
        "antecipado": True,
        "fundo": "loucura_final",
        "cena": "Ninguém mais dorme perto de você. Antes do sol, a aldeia manda você para a mata.",
        "fato": "Vinte anos depois de 1562, tupinambá fugidos dos aldeamentos e da escravidão "
                "formaram a Santidade de Jaguaripe (1580-1585), liderada por Antônio e por Maria. "
                "Foi destruída por ordem do governador Manuel Teles Barreto. "
                "O nome “Loucura” fala de você; a Santidade foi resistência.",
        "fonte": "Ronaldo Vainfas, A Heresia dos Índios (1995).",
    },
    {
        "id": "batismo",
        "chance_acaso": 8.2, "chance_tentando": None,
        "nome": "A Água do Batismo",
        "povo": "Caeté",
        # No dia 9, o jogador deixa o padre novo entrar (dados/dias.py); na noite 9, na fogueira,
        # aceita ser batizado e batizar os outros. Acaba o jogo no fim da noite 9.
        "condicao": [{"converteu": ">= 1"}],
        "antecipado": True,
        "a_partir_da_noite": 9,
        "fundo": "batismo_final",
        "cena": "Antes de a noite acabar, o padre derrama água na sua testa e na de cada um da aldeia. Todos "
                "ganham nomes que não são os seus. Na vila, a mesma água cai na testa de um doente, "
                "que morre logo depois.",
        "fato": "Em abril de 1563, na aldeia de Santiago, na Bahia, os jesuítas batizaram 84 "
                "indígenas à beira da morte, e todos morreram. No mesmo período, o governador "
                "Mem de Sá declarou que os Caeté podiam ser escravizados onde fossem encontrados.",
        "fonte": "Carta do padre Leonardo do Valle ao padre Gonçalo Vaz, Bahia, 12 de maio de 1563.",
    },
    {
        "id": "rio_acima",
        "chance_acaso": 1.0, "chance_tentando": None,
        "nome": "Rio Acima",
        "povo": "Aimoré, hoje Krenak",
        # Na noite 10, Krenan (se voltou) faz o mesmo pedido, e o jogador escolhe ir com ele.
        "condicao": [{"subiu_o_rio": ">= 1"}],
        "antecipado": False,
        "ultima_noite": True,
        "fundo": "rio_acima_final",
        "cena": "A aldeia sobe o rio atrás de Krenan. As ocas ficam vazias para trás.",
        "fato": "A carta régia de 13 de maio de 1808 declarou guerra oficial contra os Aimoré, "
                "chamados de Botocudos. Os descendentes incluem os Krenak, que vivem no Vale do "
                "Rio Doce (MG), o Watu, atingido pela lama da barragem de Mariana em 2015.",
        "fonte": "Carta Régia de 13 de maio de 1808; Instituto Socioambiental: Krenak.",
    },
    {
        "id": "anhanga",
        "chance_acaso": 0.5, "chance_tentando": None,
        "nome": "Anhangá",
        "povo": "Tremembé",
        # As três vezes em que o pajé aponta para a mata (noites 2, 5 e 9); no fim da noite 9,
        # a da 3ª vez, o jogo vai para o final, com a imagem do veado atrás das telas.
        # Entregar alguém ao Aleixo não impede (com 2 entregas, A Troca vem antes na fila).
        "condicao": [{"viu_anhanga": ">= 3", "mortos_por_sua_mao": "== 0"}],
        "antecipado": True,
        "a_partir_da_noite": 9,
        "fundo": "anhanga_final",
        "cena": "Na nona noite, o veado branco sai da mata e para diante do fogo. O pajé abaixa a "
                "cabeça. Depois, o veado some entre as árvores.",
        "fato": "Os missionários chamaram de demônio o Anhangá, protetor dos animais. No "
                "aldeamento de Almofala (CE), os Tremembé continuaram dançando o torém, em roda, "
                "para os encantados da terra. No século XIX, o governo do Ceará disse que eles não "
                "existiam mais. Em 2023, a Terra Indígena Tremembé da Barra do Mundaú foi homologada.",
        "fonte": "José Vieira Couto de Magalhães, O Selvagem (1876); Encantes da Terra: os Tremembé "
                 "de Almofala (revista Ilha, UFSC, 2019); Decreto nº 11.506, de 28 de abril de 2023.",
    },
    {
        "id": "tapiri",
        "chance_acaso": 0, "chance_tentando": None,
        "nome": "O Tapiri",
        "povo": "Korubo",
        # Levar ao tapiri 2 amaldiçoados (chegaram com a maldição ou pegaram a febre) e nunca
        # ninguém são, até o fim do jogo. Matar um amaldiçoado ou entregar alguém ao Aleixo não
        # impede (com 2 entregas, A Troca vem antes na fila); matar alguém são impede.
        "condicao": [{"tapiri_usos": ">= 2", "tapiri_saos": "== 0", "vivos": ">= 2",
                      "mortos_saos_por_sua_mao": "== 0"}],
        "antecipado": False,
        "fundo": "tapiri_final",
        "cena": "Poucas redes em volta da fogueira. Ao longe, o tapiri com uma luz acesa: "
                "o pajé cuida de quem está lá.",
        "fato": "Os Korubo vivem no Vale do Javari (AM), a região com mais povos isolados do "
                "mundo. Em 2020, na covid-19, o STF mandou erguer barreiras sanitárias nas terras "
                "de povos isolados (ADPF 709). O tapiri de 1562 virou decisão da Justiça.",
        "fonte": "Instituto Socioambiental, agosto de 2020: o referendo da ADPF 709 no STF.",
    },
    {
        "id": "honra",
        "chance_acaso": 0, "chance_tentando": None,
        "nome": "A Honra",
        "povo": "Tupinambá",
        # Pelo menos 2 vivos, nunca matar quem era são e nunca levar alguém são ao tapiri. Matar
        # um amaldiçoado ou entregar alguém ao Aleixo não impede (com 2 entregas, A Troca vem
        # antes). As 5 histórias (memoria >= 5) estão desligadas por enquanto: HONRA_PEDE_HISTORIAS.
        "condicao": [CONDICAO_HONRA],
        "antecipado": False,
        "fundo": "honra_final",
        "cena": "A febre vai embora devagar. Ninguém são morreu por sua mão, e os que "
                "sobreviveram ainda se sentam com você em volta do fogo.",
        "fato": "Um manto tupinambá de penas vermelhas, levado para a Europa no século XVII, "
                "voltou ao Museu Nacional, no Rio, em 2024. Os Tupinambá de Olivença (BA) lutam "
                "hoje pela demarcação da terra.",
        "fonte": "Museu Nacional/UFRJ (2024); Instituto Socioambiental: Tupinambá.",
    },
    {
        "id": "ferida",
        "chance_acaso": 0, "chance_tentando": None,
        "nome": "Ferida",
        "povo": "Potiguara",
        # A aldeia sobreviveu com 3 ou 4 vivos, mas o jogador matou alguém são ou levou alguém são
        # ao tapiri. Quem matou 3 ou mais vai para A Loucura antes. Fonte: o documento "Dois finais
        # novos: Ferida (Potiguara) e Guerra Justa (Caeté)". {vivos} e {nome} vêm do estado
        # (motor/finais.py): "cena" quando alguém são morreu; "cena_tapiri" quando quem era são
        # voltou do tapiri.
        "condicao": [{"mortos_saos_por_sua_mao": ">= 1", "vivos": [">= 3", "<= 4"]},
                     {"tapiri_saos": ">= 1", "vivos": [">= 3", "<= 4"]}],
        "antecipado": False,
        "cena": "Quando o cacique volta da mata, encontra a fogueira acesa e {vivos} pessoas em "
                "volta dela. A aldeia ainda existe. Ninguém fala de {nome}. Mas, à noite, cada um "
                "dorme virado para a entrada. Na mata, um parente aprende a desconfiar de outro "
                "parente. A doença foi embora. Isso ficou.",
        "cena_tapiri": "Quando o cacique volta da mata, encontra a fogueira acesa e {vivos} pessoas "
                       "em volta dela. A aldeia ainda existe. {nome} voltou do tapiri. Não senta "
                       "mais perto de você. À noite, cada um dorme virado para a entrada. Na mata, "
                       "um parente aprende a desconfiar de outro parente. A doença foi embora. "
                       "Isso ficou.",
        # Lendo de novo pelo menu, sem a partida.
        "cena_sem_estado": {"vivos": "poucas", "nome": "quem se foi"},
        "fato": "Em 1645, os Potiguara lutaram dos dois lados da guerra entre portugueses e "
                "holandeses. Os primos Felipe Camarão e Pedro Poti trocaram cartas em tupi: um pedia "
                "ao outro que não matasse o próprio sangue. Poti recusou e morreu preso em 1649. Os "
                "Potiguara vivem até hoje no litoral norte da Paraíba, em três terras indígenas. A "
                "última foi homologada em 2024.",
        "fonte": "Regina Célia Gonçalves, “Os Potiguara na Guerra dos Brancos” (ANPUH, 2005); "
                 "Eduardo Navarro, tradução das cartas tupis (USP); Decreto nº 12.288/2024.",
    },
    {
        "id": "vazio",
        "chance_acaso": 72.5, "chance_tentando": None,
        "nome": "O Vazio",
        "povo": "Goitacá",
        # Sempre bate (é o que sobra). Antes do dia 10, só acaba o jogo se a aldeia esvaziar.
        "condicao": [{}],
        "antecipado": False,
        "fundo": "vazio_final",
        "cena": "As redes ficam vazias, uma a uma. Ninguém invadiu: os amaldiçoados dormiram entre os "
                "seus, e a febre decidiu por você.",
        "fato": "Os Goitacá eram temidos por boato: cronistas os descreveram como ferozes sem "
                "nunca ter convivido com eles. Desapareceram no século XVIII, entre guerras e "
                "epidemias. É o único final de um povo que não existe mais.",
        "fonte": "Anthony Knivet (c. 1597); frei Vicente do Salvador, História do Brasil (1627).",
        # A aldeia esvaziou antes do dia 10 (ninguém de fora sobrou, e pelo menos 2 morreram):
        # o jogo acaba no fim da noite em que isso acontecer.
        "esvaziou": {"vivos": "== 0", "mortos": ">= 2"},
    },
]

# Textos fixos da tela de final.
TELA_FINAL = {
    "povo": "O que aconteceu com vocês aconteceu de verdade com este povo: %s.",
    "fonte": "Fonte",
    "seguir": "Continuar",
    "menu": "Voltar ao menu",
    "voltar_finais": "Voltar aos finais",
    "fundo": "fogueira_longe",
    # Embaixo da fonte: a posição na fila e a chance.
    "numero": "Final %d/%d",
    "chance_acaso": "Jogando ao acaso, acontece em %s das partidas",
    "chance_tentando": "Tentando, dá certo em %s",
}

# A tela "Finais" do menu: os finais já vistos, para ler de novo. Os outros ficam escondidos.
LISTA_FINAIS = {
    "titulo": "Finais",
    "vistos": "Você já viu %d de %d finais.",
    "escondido": "Final %d/%d · ainda não visto",
    "voltar": "Voltar",
    "fundo": "fogueira_longe",
}
