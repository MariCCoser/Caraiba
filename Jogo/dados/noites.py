# Roteiro de cada Noite, na fogueira. Edite à vontade: aqui não há lógica.
#
# A noite vem logo depois do sinal do pajé (o passo {"tipo": "noite"} em dados/dias.py).
# Todos sentam em volta do fogo e o jogador clica em quem quer para conversar. Na fogueira,
# ao ar livre, ninguém pega nada. É aqui que o jogador examina o rosto de quem é de fora
# e decide onde a pessoa dorme. Depois, "Ir dormir": o jogador anda pela aldeia, de noite,
# e de lá dorme até o dia seguinte.
#
# Cada noite tem:
#   "titulo"   o que aparece no canto de cima (ex.: "Noite 1")
#   "energia"  quantos olhares o jogador tem na noite inteira
#   "energia_extra"  olhares a mais, se o estado.py bate: {"machado": 1} = +1 para quem aceitou
#              o machado de Yara
#   "fundo"    o cenário da fogueira (dados/arte.py)
#   "dica"     a frase embaixo da tela, enquanto o jogador escolhe com quem falar
#   "dormir"   o texto da seta de ir dormir. Ela só aparece depois de falar com quem é
#              "obrigatorio" e de gastar toda a energia (ou se não sobrou ninguém para examinar)
#   "pessoas"  quem senta em volta do fogo. Cada pessoa tem:
#       "imagem"       o apelido da imagem (dados/arte.py)
#       "imagem"       use a imagem sentada (ex.: "yara_sentada", dados/arte.py)
#       "posicao"      o meio da borda de baixo da imagem (x, y na tela 1600x900): onde a
#                      pessoa encosta no chão
#       "escala"       o tamanho (1 = o tamanho de quem fala)
#       "espelhar"     True: vira a pessoa para o outro lado (o pajé olha para o fogo)
#       "de_fora"      True: só aparece se o jogador a deixou entrar (e se não está no tapiri,
#                      porque quem está no tapiri fica lá, isolado)
#       "uma_vez"      True: depois da conversa ela sai da fogueira (foi dormir)
#       "obrigatorio"  True: o jogador precisa falar com ela antes de ir dormir
#       "passos"       a conversa: os mesmos passos de dados/dias.py, mais os de baixo
#   "fim"      os passos depois de "Ir dormir", para todo mundo
#
# Passos que só a noite usa (e alguns detalhes):
#   "perguntas" com "botao": troca o texto do botão "Decidir" (ex.: "Examinar o rosto").
#               Uma "resposta" pode ser uma lista: a pessoa fala uma frase de cada vez.
#               Uma pergunta com "se_dentro": "Mbaé" só aparece se Mbaé entrou na aldeia.
#   "exame"     o jogador escolhe as zonas do rosto para olhar de perto. Cada zona tem
#               "pergunta" (o nome no botão), "resposta" (o que se vê) e, se o que se vê for
#               um sinal, "sinal": True. Zona com "imagem" (dados/arte.py, DETALHES) mostra o
#               detalhe de perto, à direita, em vez de descrever: a "resposta" fica só com o
#               que a pessoa diz. Cada zona gasta 1 de energia (ou o "custo" dela, se
#               tiver). Zona que custa mais do que sobrou fica apagada. Diga de quem é o exame
#               com "quem". "liberadas": a lista das zonas que dá para olhar nessa noite (ex.:
#               só ["Olhos"] na noite 1). Sem ela, todas as zonas aparecem.
#               As zonas e os sinais seguem Textos/A_Febre_Caraiba.pdf.
#   "texto"     num "exame" ou numa "escolha": a frase que aparece no painel quando eles
#               começam (sem nome em cima, como narração).
#   Uma "fala" com "quem": "" também é narração: aparece sem nome em cima.
#   Nas opções de "escolha":
#     "tapiri": "Yara"       a pessoa vai para o tapiri, o abrigo isolado (sai da oca). Se o
#                            tapiri está cheio (dados/aldeia.py, TAPIRI), a opção fica fechada.
#     "morre": "Yara"        a pessoa morre pela mão do jogador (sai da aldeia)
#     "oca": True            a pessoa dorme na oca. Se ela está com a febre (dados/febre.py),
#                            a febre passa para alguns moradores (quantos é sorteado).
#     "requer_sinais": 2     a opção só abre com essa quantidade de sinais achados no exame
#                            de quem está na "escolha" ("quem"); "texto_bloqueado" é o que o
#                            botão mostra enquanto ela está fechada.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.
# O exame descreve o que se vê, sem dizer o que significa.
#
# Quem é de fora tem a mesma conversa em todas as noites (dados/conversas.py).

from dados.conversas import conversa_mbae, conversa_potira, conversa_yara

# O que acontece quando o jogador mata alguém (a Proposta: mostra o corpo com nome no dia
# seguinte e derruba a sanidade, mesmo quando ele acerta).
EFEITOS_MATAR = {"vivos": -1, "mortos": 1, "mortos_por_sua_mao": 1, "sanidade": -3}

# Onde cada um senta na fogueira (cenário "fogueira_perto"): (x, y) é onde a imagem encosta embaixo.
# Quem está mais longe (nos troncos do fundo) fica menor.
POSICAO_YARA, ESCALA_YARA = (300, 830), 0.66     # no chão, as costas apoiadas no tronco de baixo
POSICAO_PAJE, ESCALA_PAJE = (1390, 545), 0.6     # sentado em cima do tronco da direita
POSICAO_MBAE, ESCALA_MBAE = (470, 520), 0.5      # na ponta do tronco de cima, à esquerda

TEXTO_EXAME = "Você chega perto do rosto, na luz do fogo."
FALA_MATAR = {"tipo": "fala", "quem": "", "texto": "O fogo estala. Ninguém na aldeia diz nada."}

# Yara está saudável: o olho vermelho é da fumaça, a terra é do caminho.
ZONAS_YARA = [
    {"pergunta": "Testa",
     "resposta": "Fresca. Nenhum suor."},
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_yara",
     "resposta": "[Dormi perto do fogo]."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas. A pele está limpa."},
    {"pergunta": "Boca",
     "resposta": "Ela abre a boca. Por dentro da bochecha, nada. Língua rosada."},
    {"pergunta": "Mãos",
     "resposta": "Firmes. Terra seca debaixo das unhas e calos de carregar peso."},
    {"pergunta": "Respiração",
     "resposta": "Respira fundo e devagar, sem tosse."},
]

# Na noite 2 ainda é o mesmo olho (a arte do olho vermelho vale até a noite 3).
ZONAS_YARA_NOITE_2 = [dict(zona) for zona in ZONAS_YARA]
ZONAS_YARA_NOITE_2[1] = {"pergunta": "Olhos", "imagem": "olho_yara",
                         "resposta": "Dormi perto do fogo. [Já está passando]."}
ZONAS_YARA_NOITE_2[3] = {"pergunta": "Boca",
                         "resposta": "Ela abre a boca e respira fundo, sem tossir. Língua rosada."}

# Mbaé está com a febre: suor, olho vermelho e, abrindo a boca, a tosse e as feridas na língua
# (o sinal que o pajé conta na noite 2).
# (Os pontinhos brancos na bochecha ficam para Tamandaré-mirim, na noite 5.)
# A pintura de jenipapo nunca é sinal de doença.
ZONAS_MBAE = [
    {"pergunta": "Testa", "sinal": True,
     "resposta": "Molhada de suor e quente, mesmo longe do fogo."},
    # Até o 3º dia na oca; depois, o olho doente (Arte/Doenças/Mbaé/OlhoMbaé_Doente, ainda por vir).
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_mbae",
     "resposta": "(tosse) [É o vento do rio]."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas. Só a pintura de jenipapo."},
    {"pergunta": "Boca", "sinal": True,
     "resposta": "Ele abre a boca e tosse. Por dentro, feridas na língua."},
    {"pergunta": "Mãos",
     "resposta": "Calos de arco. Nenhuma bolha na palma."},
    {"pergunta": "Respiração", "sinal": True,
     "resposta": "Respira curto, e o peito chia um pouco."},
]


def escolha_onde_dorme(quem, fala_oca, fala_tapiri):
    """A decisão do fim da conversa: deixar na oca, levar ao tapiri ou matar."""
    return {"tipo": "escolha", "quem": quem, "texto": "Onde %s dorme esta noite?" % quem, "opcoes": [
        {"texto": "Deixar na oca", "oca": True,
         "passos": [{"tipo": "fala", "quem": quem, "texto": fala_oca}]},
        {"texto": "Levar ao tapiri", "tapiri": quem,
         "passos": [{"tipo": "fala", "quem": quem, "texto": fala_tapiri}]},
        {"texto": "Matar", "morre": quem, "efeitos": EFEITOS_MATAR, "passos": [FALA_MATAR]},
    ]}


# --- Noite 3: a fogueira da aldeia e os amaldiçoados (Textos/Amaldiçoados.txt) ---
# Ninguém novo chegou. Em volta do fogo: o pajé e quem é de fora (Yara e Mbaé, se ficaram).
# Mbaé é o amaldiçoado que trouxe a febre; os moradores que pegaram dele também passam adiante,
# mesmo sem mostrar nada (dados/febre.py). Eles não aparecem: o jogador só vê, de manhã, quem
# adoeceu e quem morreu. O pajé não conta sinal novo: só desconfia do Irmão Aleixo.
#
# Na noite com "amaldicoados": True, os moradores que pegaram a febre passam adiante no fim
# da noite. Perguntas podem ter "amaldicoado": "Mbaé" (Mbaé ainda passa a febre) ou
# "sao": "Mbaé" (não passa mais): aparece só a que bate.

# Yara na noite 3: o olho clareou (o sinal da noite 1 a acusou à toa).
ZONAS_YARA_NOITE_3 = [dict(zona) for zona in ZONAS_YARA_NOITE_2]
ZONAS_YARA_NOITE_3[1] = {"pergunta": "Olhos",
                         "resposta": "O branco do olho clareou. Nenhum risco vermelho."}


# --- Noite 4: Potira, a que você conhece ---
# Potira é sã: o olho está cansado, a boca seca de sede. Nada bate com a tábua.
# Ainda não há arte dela sentada: na fogueira ela fica em pé, na frente, à direita, com a
# borda de baixo da imagem rente à borda da tela.
POSICAO_POTIRA, ESCALA_POTIRA = (1270, 900), 0.45

ZONAS_POTIRA = [
    {"pergunta": "Testa",
     "resposta": "Fresca. Poeira do caminho, nenhum suor."},
    {"pergunta": "Olhos", "imagem": "olho_potira",
     "resposta": "[É sono]. Andei desde antes do sol."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas. A pele está limpa."},
    {"pergunta": "Boca",
     "resposta": "Lábios rachados de sede. Por dentro da bochecha, nada."},
    {"pergunta": "Mãos",
     "resposta": "Vazias, unhas limpas. Arranhões de mato nos braços."},
    {"pergunta": "Respiração",
     "resposta": "Respira fundo, sem tosse."},
]


NOITES = {
    1: {
        "titulo": "Noite 1",
        # Na noite 1 só os olhos podem ser examinados (veja "liberadas" no exame de Yara).
        "energia": 1,
        "fundo": "fogueira_perto",
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé, à direita do fogo: fala do sinal e do tapiri. Dá para voltar a ele.
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. O fogo está bom hoje."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "Olho vermelho, raiado. Vi o mesmo antes de as redes esvaziarem."},
                        {"pergunta": "Todo olho vermelho é o mal?",
                         "resposta": "O sonho mostra o sinal. Quem olha de perto é você."},
                        {"pergunta": "O que é o tapiri?",
                         "resposta": "O abrigo longe das ocas. Quem dorme lá não divide a rede."},
                        # O que "Como se joga" não conta (dados/textos.py, REGRAS): o jogador descobre aqui.
                        {"pergunta": "O mal passa aqui no fogo?",
                         "resposta": "Ao ar livre, não. O mal passa nas redes, dentro da oca."},
                        {"pergunta": "E se eu tiver certeza de que é o mal?",
                         "resposta": [
                             "Então a decisão é sua. Há quem tire a vida para salvar a aldeia.",
                             "Mas quem faz isso carrega o peso. Eu vi homens que não dormiram mais.",
                         ]},
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Yara, à esquerda do fogo. A conversa é a de sempre (a mesma da oca, no dia).
            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "Você não para de olhar para mim."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    # Na noite 1 só os olhos: é o sinal que o pajé contou.
                    {"tipo": "exame", "quem": "Yara", "liberadas": ["Olhos"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA},
                    escolha_onde_dorme("Yara", "Durmo perto da porta. Saio cedo, se a chuva deixar.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },

    2: {
        "titulo": "Noite 2",
        # Na noite 2, 1 olhar só, e só os olhos ou a boca (a tosse): veja "liberadas".
        # Quem aceitou o machado de Yara (dia 1) tem 2: com o ferro, a lenha rende mais.
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé fala do sinal, do tapiri (um lugar só) e do que a aldeia diz de Mbaé:
            # a aldeia quer Mbaé fora pelo povo dele, não pela tosse.
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. Hoje o fogo custou a pegar."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "Gente tremendo na rede, com a boca ferida. Foi assim da outra vez."},
                        {"pergunta": "Por que olham torto para Mbaé?", "se_dentro": "Mbaé",
                         "resposta": [
                             "Não é a tosse. É o povo dele.",
                             "Contam histórias do outro lado do rio desde antes de eu nascer.",
                         ]},
                        {"pergunta": "O tapiri tem lugar?",
                         "resposta": "Um lugar só. Quem entra fica três noites, longe de todos."},
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Yara, se ainda está na aldeia e não está no tapiri. Não é obrigatório falar com ela.
            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "A chuva não passou. Fico mais esta noite."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_2},
                    escolha_onde_dorme("Yara", "Então volto para a mesma rede.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Mbaé, entre Yara e o fogo. Está com a febre: se dormir na oca, de 1 a 3 moradores
            # pegam a febre, acordam doentes no dia 3 e morrem no dia 4 (dados/febre.py).
            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) O fogo ajuda. Daqui a pouco passa."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },
    3: {
        "titulo": "Noite 3",
        # Como na noite 2: 1 olhar (2 com o machado), e só os olhos ou a boca. Nenhum sinal novo.
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        # Os moradores que pegaram a febre passam adiante no fim da noite (dados/febre.py).
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé só desconfia do Irmão Aleixo: Aleixo fala em tirar a maldição, e isso é coisa de pajé.
            # Não há sinal novo hoje.
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. O homem da cruz já foi, mas a cruz ficou."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você acha do Irmão Aleixo?",
                         "resposta": [
                             "Chega falando em cuidar de quem carrega a maldição.",
                             "Quem tira a maldição de uma aldeia é o pajé. [Ele sabe disso].",
                         ]},
                        {"pergunta": "Por que ele leva gente para a vila?",
                         "resposta": "Quem vai com ele não volta para contar como é lá."},
                        {"pergunta": "Ele vai voltar?",
                         "resposta": "Volta. Homem assim volta quando a aldeia está mais fraca."},
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Yara, se ficou e não está no tapiri: o olho clareou. Não é obrigatório falar com ela.
            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "A chuva parou. Logo eu sigo para o sul."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_3},
                    escolha_onde_dorme("Yara", "Mais uma noite, então. Obrigada.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Mbaé, se ficou e não está no tapiri: o amaldiçoado que trouxe a febre. Se dormir
            # na oca de novo, ela passa outra vez (dados/febre.py, CONTAGIO).
            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) Mais uma noite e eu sigo caminho."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },

    4: {
        "titulo": "Noite 4",
        # Como nas noites 2 e 3: 1 olhar (2 com o machado). Só dá para investigar os sinais já
        # riscados na tábua: os olhos e a boca (o sinal novo, a bochecha, também é na boca).
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        # Os moradores que pegaram a febre continuam passando adiante (dados/febre.py).
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé fala do sinal da noite, continua explicando o tapiri e fala de Potira,
            # que ele viu nascer.
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. Hoje o fogo está quieto."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": [
                             "Pontos brancos, por dentro da bochecha.",
                             "Ainda não vi em ninguém. [Mas vai chegar].",
                         ]},
                        {"pergunta": "O tapiri tem lugar?",
                         "resposta": "Um lugar só. Quem entra fica três noites, longe de todos."},
                        {"pergunta": "E quem sai do tapiri?",
                         "resposta": [
                             "Quem passa as três noites e não piora volta para a rede.",
                             "Quem piora, [não leva o mal para ninguém]. É para isso que ele serve.",
                         ]},
                        {"pergunta": "E a Potira?", "se_dentro": "Potira",
                         "resposta": "Essa eu vi nascer. Senta perto do fogo, menina."},
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Yara, se ficou e não está no tapiri. Não é obrigatório falar com ela.
            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "A chuva voltou. Mais uma noite e eu sigo."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_3},
                    escolha_onde_dorme("Yara", "Mais uma noite, então. Obrigada.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Mbaé, se ficou e não está no tapiri: ainda passa a febre se dormir na oca.
            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) Assim eu não subo o rio."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Potira, se entrou: em pé, na frente, à direita do fogo.
            "Potira": {
                "imagem": "potira", "posicao": POSICAO_POTIRA, "escala": ESCALA_POTIRA,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "potira"},
                    {"tipo": "fala", "quem": "Potira", "texto": "Não achei nada. Desculpa."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_potira()},
                    {"tipo": "exame", "quem": "Potira", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA},
                    escolha_onde_dorme("Potira", "Durmo na rede de sempre.",
                                       "Sozinha? Se você manda, eu vou."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },
}
