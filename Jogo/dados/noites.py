# Roteiro de cada Noite, na fogueira. Edite à vontade: aqui não há lógica.
#
# A noite vem logo depois do sinal do pajé (o passo {"tipo": "noite"} em dados/dias.py).
# Todos sentam em volta do fogo e o jogador clica em quem quer para conversar. Na fogueira,
# ao ar livre, ninguém pega nada. É aqui que o jogador examina o rosto de quem é de fora
# e decide onde a pessoa dorme. Depois, "Ir dormir": o jogador anda pela aldeia, de noite.
#
# Cada noite tem:
#   "titulo"   o que aparece no canto de cima (ex.: "Noite 1")
#   "energia"  quantos olhares o jogador tem na noite inteira (cada zona examinada gasta 1)
#   "fundo"    o cenário da fogueira (dados/arte.py)
#   "dica"     a frase embaixo da tela, enquanto o jogador escolhe com quem falar
#   "dormir", "dormir_bloqueado"  o botão de ir dormir; fechado, mostra quem ainda falta (%s)
#   "pessoas"  quem senta em volta do fogo. Cada pessoa tem:
#       "imagem"       o apelido da imagem (dados/arte.py)
#       "posicao"      o meio da borda de baixo da imagem (x, y na tela 1600x900). Por enquanto
#                      as imagens são de pé: para parecer sentada, a pessoa fica mais baixa,
#                      com a cintura para fora da tela (y maior que 900).
#       "escala"       o tamanho (1 = o tamanho de quem fala)
#       "de_fora"      True: só aparece se o jogador a deixou entrar
#       "uma_vez"      True: depois da conversa ela sai da fogueira (foi dormir)
#       "obrigatorio"  True: o jogador precisa falar com ela antes de ir dormir
#       "passos"       a conversa: os mesmos passos de dados/dias.py, mais os de baixo
#   "fim"      os passos depois de "Ir dormir", para todo mundo
#
# Passos que só a noite usa (e alguns detalhes):
#   "perguntas" com "botao": troca o texto do botão "Decidir" (ex.: "Examinar o rosto").
#               Uma "resposta" pode ser uma lista: a pessoa fala uma frase de cada vez.
#   "exame"     o jogador escolhe as zonas do rosto para olhar de perto. Cada zona tem
#               "pergunta" (o nome no botão), "resposta" (o que se vê) e, se o que se vê for
#               um sinal, "sinal": True. Cada zona gasta 1 de energia; sem energia, só sobra
#               "Terminar o exame". Diga de quem é o exame com "quem".
#   "texto"     num "exame" ou numa "escolha": a frase que aparece no painel quando eles
#               começam (sem nome em cima, como narração).
#   Uma "fala" com "quem": "" também é narração: aparece sem nome em cima.
#   Nas opções de "escolha":
#     "tapiri": "Yara"       a pessoa vai para o tapiri, o abrigo isolado (sai da oca)
#     "morre": "Yara"        a pessoa morre pela mão do jogador (sai da aldeia)
#     "requer_sinais": 2     a opção só abre com essa quantidade de sinais achados no exame
#                            de quem está na "escolha" ("quem"); "texto_bloqueado" é o que o
#                            botão mostra enquanto ela está fechada.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.
# O exame descreve o que se vê, sem dizer o que significa.

# O que acontece quando o jogador mata alguém (a Proposta: mostra o corpo com nome no dia
# seguinte e derruba a sanidade, mesmo quando ele acerta).
EFEITOS_MATAR = {"vivos": -1, "mortos": 1, "mortos_por_sua_mao": 1, "sanidade": -3}

NOITES = {
    1: {
        "titulo": "Noite 1",
        "energia": 3,
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
            # história da aldeia dela ficou para o dia, na aldeia (dados/dias.py).
            # Yara está saudável: o olho é de fumaça, a terra é do caminho.
            "Yara": {
                "imagem": "yara", "posicao": (290, 1040), "escala": 0.72,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "Você não para de olhar para mim."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Seus olhos ainda estão vermelhos.",
                         "resposta": "Três noites de fumaça não saem num dia só."},
                        {"pergunta": "Que terra é essa nas suas unhas?",
                         "resposta": "Do caminho. [Cavei raiz para comer]."},
                        {"pergunta": "Esse pano é dos estrangeiros?",
                         "resposta": "Troquei por farinha, na costa. É só pano."},
                    ]},

                    {"tipo": "exame", "quem": "Yara",
                     "texto": "Você chega perto do rosto dela, na luz do fogo.", "zonas": [
                        {"pergunta": "Olhos", "sinal": True,
                         "resposta": "O branco do olho está raiado de vermelho. Lacrimeja perto do fogo."},
                        {"pergunta": "Boca",
                         "resposta": "Ela abre a boca. Por dentro da bochecha, nada. Língua rosada."},
                        {"pergunta": "Pele",
                         "resposta": "Fresca, sem manchas. Cheira a fumaça de lenha."},
                        {"pergunta": "Pescoço",
                         "resposta": "Nenhum caroço, nenhuma mancha. Ela engole sem dor."},
                        {"pergunta": "Mãos",
                         "resposta": "Firmes. Terra seca debaixo das unhas e calos de carregar peso."},
                    ]},

                    {"tipo": "escolha", "quem": "Yara",
                     "texto": "Onde Yara dorme esta noite?", "opcoes": [
                        {"texto": "Deixar na oca", "passos": [
                            {"tipo": "fala", "quem": "Yara",
                             "texto": "Durmo perto da porta. Saio cedo, se a chuva deixar."},
                        ]},
                        {"texto": "Levar ao tapiri", "tapiri": "Yara", "passos": [
                            {"tipo": "fala", "quem": "Yara",
                             "texto": "Sozinha, então. Já dormi em lugar pior."},
                        ]},
                        {"texto": "Matar", "texto_bloqueado": "Matar · só com dois sinais",
                         "requer_sinais": 2, "morre": "Yara", "efeitos": EFEITOS_MATAR, "passos": [
                            {"tipo": "fala", "quem": "",
                             "texto": "O fogo estala. Ninguém na aldeia diz nada."},
                        ]},
                    ]},
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
