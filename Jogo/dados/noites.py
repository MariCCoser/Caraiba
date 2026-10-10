# Roteiro de cada Noite, na fogueira. Edite à vontade: aqui não há lógica.
#
# A noite vem logo depois do sinal do pajé (o passo {"tipo": "noite"} em dados/dias.py).
# Na fogueira, ao ar livre, ninguém pega nada: dá para conversar com calma. É aqui que
# quem entrou conta mais de si, e é aqui que o jogador examina o rosto de cada um.
#
# Cada noite tem:
#   "titulo"   o que aparece no canto de cima (ex.: "Noite 1")
#   "energia"  quantos olhares o jogador tem na noite inteira (cada zona examinada gasta 1)
#   "pessoas"  para cada pessoa de fora que pode estar dentro da aldeia, os passos dela na
#              fogueira. Só aparecem as que o jogador deixou entrar, na ordem em que entraram.
#   "ninguem"  os passos de quando ninguém de fora entrou
#   "fim"      os passos do fim da noite, para todo mundo; depois o jogador anda pela aldeia
#
# Os passos são os mesmos de dados/dias.py ("fundo", "visitante", "fala", "perguntas",
# "escolha"), mais estes:
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
        "pessoas": {
            "Yara": [
                {"tipo": "visitante", "visitante": None},
                {"tipo": "fundo", "fundo": "fogueira_perto", "filtro": "noite"},
                {"tipo": "visitante", "visitante": "yara"},
                {"tipo": "fala", "quem": "Yara",
                 "texto": "Aqui a lenha é seca. O fogo quase não faz fumaça."},

                # A conversa da noite: a antiga aldeia de Yara, só se o jogador perguntar.
                {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                    {"pergunta": "Conte da sua aldeia.",
                     "resposta": [
                         "Ficava na boca de um rio grande. Dava para ver os barcos de longe.",
                         "Os barcos queriam pau de tinta. A gente cortava, eles davam ferro.",
                         "Cortar árvore com pedra levava o dia. Com o ferro, leva pouco.",
                     ],
                     "efeitos": {"memoria": 1}},
                    {"pergunta": "Por que saiu de lá?",
                     "resposta": [
                         "Os padres levaram muita gente para perto da vila. Minha mãe foi.",
                         "Eu não fui. Vou para o sul, onde mora [a gente do meu pai].",
                     ]},
                    {"pergunta": "A febre chegou lá?",
                     "resposta": [
                         "Chegou com as chuvas. Quem cuidava dos doentes caía depois.",
                         "Eu saí antes. [Não estou doente].",
                     ]},
                ]},

                # O exame do rosto. Yara está saudável: o olho é de fumaça, a terra é do caminho.
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
        "ninguem": [
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Ninguém de fora dorme aqui esta noite. Descanse enquanto pode."},
            {"tipo": "visitante", "visitante": None},
        ],
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },
}
