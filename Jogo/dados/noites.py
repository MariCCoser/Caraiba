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
#   "fundo"    o cenário da fogueira (dados/arte.py)
#   "dica"     a frase embaixo da tela, enquanto o jogador escolhe com quem falar
#   "dormir", "dormir_bloqueado"  o botão de ir dormir; fechado, mostra quem ainda falta (%s)
#   "pessoas"  quem senta em volta do fogo. Cada pessoa tem:
#       "imagem"       o apelido da imagem (dados/arte.py)
#       "posicao"      o meio da borda de baixo da imagem (x, y na tela 1600x900). Por enquanto
#                      as imagens são de pé: para parecer sentada, a pessoa fica mais baixa,
#                      com a cintura para fora da tela (y maior que 900).
#       "escala"       o tamanho (1 = o tamanho de quem fala)
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
#               um sinal, "sinal": True. Cada zona gasta 1 de energia ("custo": 2 para abrir a
#               boca). Zona que custa mais do que sobrou fica apagada. Diga de quem é o exame
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
#     "contagio": {...}      a pessoa é doente e dorme na oca: "adoecem" moradores pegam a
#                            febre no "dia" indicado (Textos/A_Febre_Caraiba.pdf)
#     "requer_sinais": 2     a opção só abre com essa quantidade de sinais achados no exame
#                            de quem está na "escolha" ("quem"); "texto_bloqueado" é o que o
#                            botão mostra enquanto ela está fechada.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.
# O exame descreve o que se vê, sem dizer o que significa.

# O que acontece quando o jogador mata alguém (a Proposta: mostra o corpo com nome no dia
# seguinte e derruba a sanidade, mesmo quando ele acerta).
EFEITOS_MATAR = {"vivos": -1, "mortos": 1, "mortos_por_sua_mao": 1, "sanidade": -3}

TEXTO_EXAME = "Você chega perto do rosto, na luz do fogo."
FALA_MATAR = {"tipo": "fala", "quem": "", "texto": "O fogo estala. Ninguém na aldeia diz nada."}

# Yara está saudável: o olho vermelho é da fumaça, a terra é do caminho.
ZONAS_YARA = [
    {"pergunta": "Testa",
     "resposta": "Fresca. Nenhum suor."},
    {"pergunta": "Olhos", "sinal": True,
     "resposta": "O branco do olho está raiado de vermelho. Lacrimeja perto do fogo."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas. A pele está limpa."},
    {"pergunta": "Boca", "custo": 2,
     "resposta": "Ela abre a boca. Por dentro da bochecha, nada. Língua rosada."},
    {"pergunta": "Mãos",
     "resposta": "Firmes. Terra seca debaixo das unhas e calos de carregar peso."},
    {"pergunta": "Respiração",
     "resposta": "Respira fundo e devagar, sem tosse."},
]

# Na noite 2 o olho de Yara já clareou: a fumaça foi passando.
ZONAS_YARA_NOITE_2 = [dict(zona) for zona in ZONAS_YARA]
ZONAS_YARA_NOITE_2[1] = {"pergunta": "Olhos",
                         "resposta": "Ainda um pouco vermelhos, mas o branco clareou desde ontem."}

# Mbaé está com a febre, na fase "Quente": suor, olho vermelho, tosse seca e, abrindo a boca,
# os pontinhos brancos. A pintura de jenipapo nunca é sinal de doença.
ZONAS_MBAE = [
    {"pergunta": "Testa", "sinal": True,
     "resposta": "Molhada de suor e quente, mesmo longe do fogo."},
    {"pergunta": "Olhos", "sinal": True,
     "resposta": "Vermelhos e úmidos. Ele pisca devagar."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas. Só a pintura de jenipapo."},
    {"pergunta": "Boca", "custo": 2, "sinal": True,
     "resposta": "Por dentro da bochecha, pontinhos brancos, como grão de sal."},
    {"pergunta": "Mãos",
     "resposta": "Calos de arco. Nenhuma bolha na palma."},
    {"pergunta": "Respiração", "sinal": True,
     "resposta": "Uma tosse seca e curta, que volta a cada pouco."},
]


def escolha_onde_dorme(quem, fala_oca, fala_tapiri, contagio=None):
    """A decisão do fim da conversa: deixar na oca, levar ao tapiri ou matar."""
    oca = {"texto": "Deixar na oca", "passos": [{"tipo": "fala", "quem": quem, "texto": fala_oca}]}
    if contagio:
        oca["contagio"] = contagio
    return {"tipo": "escolha", "quem": quem, "texto": "Onde %s dorme esta noite?" % quem, "opcoes": [
        oca,
        {"texto": "Levar ao tapiri", "tapiri": quem,
         "passos": [{"tipo": "fala", "quem": quem, "texto": fala_tapiri}]},
        {"texto": "Matar", "morre": quem, "efeitos": EFEITOS_MATAR, "passos": [FALA_MATAR]},
    ]}


NOITES = {
    1: {
        "titulo": "Noite 1",
        # Na noite 1 só os olhos podem ser examinados (veja "liberadas" no exame de Yara).
        "energia": 1,
        "fundo": "fogueira_perto",
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "dormir_bloqueado": "Ir dormir · antes, fale com %s",
        "pessoas": {
            # O pajé, à direita do fogo: fala do sinal e do tapiri. Dá para voltar a ele.
            "Pajé": {
                "imagem": "paje", "posicao": (1330, 1040), "escala": 0.72,
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
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Yara, à esquerda do fogo. A conversa é curta e só sobre o que se vê nela; a
            # história da aldeia dela ficou para o dia, na oca (dados/dias.py).
            "Yara": {
                "imagem": "yara", "posicao": (290, 1040), "escala": 0.72,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "Você não para de olhar para mim."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Seus olhos ainda estão vermelhos.",
                         "resposta": "Três noites de fumaça não saem num dia só."},
                        {"pergunta": "Como você sobreviveu sozinha?",
                         "resposta": "Dormindo perto do fogo e [comendo raiz do caminho]."},
                        {"pergunta": "Esse pano é dos estrangeiros?",
                         "resposta": "Troquei por farinha, na costa. É só pano."},
                    ]},
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
        "energia": 4,
        "fundo": "fogueira_perto",
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "dormir_bloqueado": "Ir dormir · antes, fale com %s",
        "pessoas": {
            # O pajé fala do sinal, do tapiri (um lugar só) e do que a aldeia diz de Mbaé:
            # a aldeia quer Mbaé fora pelo povo dele, não pela tosse.
            "Pajé": {
                "imagem": "paje", "posicao": (1380, 1040), "escala": 0.72,
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. Hoje o fogo custou a pegar."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "Gente tremendo na rede, tossindo seco. Foi assim da outra vez."},
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
                "imagem": "yara", "posicao": (200, 1040), "escala": 0.72,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "A chuva não passou. Fico mais esta noite."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Seus olhos melhoraram.",
                         "resposta": "Aqui a lenha é seca. [Logo passa de vez]."},
                    ]},
                    {"tipo": "exame", "quem": "Yara", "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_2},
                    escolha_onde_dorme("Yara", "Então volto para a mesma rede.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Mbaé, entre Yara e o fogo. Está com a febre: se dormir na oca, 2 moradores
            # pegam a febre e aparecem doentes no dia 4 (Textos/A_Febre_Caraiba.pdf).
            "Mbaé": {
                "imagem": "mbae", "posicao": (600, 1080), "escala": 0.62,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) O fogo ajuda. Daqui a pouco passa."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Você está tremendo.",
                         "resposta": "[É o sereno]. Do outro lado do rio faz mais frio."},
                        {"pergunta": "Essa tosse vem de onde?",
                         "resposta": "Da água fria do rio. [Já tive pior]."},
                    ]},
                    {"tipo": "exame", "quem": "Mbaé", "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça.",
                                       contagio={"adoecem": 2, "dia": 4}),
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
