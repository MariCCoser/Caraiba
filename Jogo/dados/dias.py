# Roteiro de cada Dia: o que acontece, na ordem. Edite à vontade: aqui não há lógica.
#
# Fonte: Proposta.docx. Um dia segue sempre a mesma ordem: alguém chega à entrada,
# o jogador conversa e decide se a pessoa entra, e, entre o dia e a noite, o pajé
# conta o sinal da doença, que fica riscado na tábua de barro.
#
# Cada passo é um dicionário com "tipo":
#   "fundo"      troca o cenário: {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"}
#   "fala"       alguém fala:     {"tipo": "fala", "quem": "Pajé", "texto": "..."}
#                (no máximo 2 linhas na tela; palavras entre [colchetes] ficam em âmbar)
#   "visitante"  mostra uma pessoa à esquerda (apelido de dados/arte.py: quem chega, ou o
#                pajé quando ele fala) ou None para tirar
#   "perguntas"  o jogador escolhe o que perguntar, quantas quiser, e depois clica em "Decidir".
#                Cada pergunta: "pergunta", "resposta" e, se quiser, "efeitos".
#   "escolha"    botões; cada opção tem "texto" e, se quiser, "efeitos", "entra" (o nome de
#                quem passa a estar dentro da aldeia) e "passos" (o que acontece depois)
#   "sinal"      o sinal do pajé fica riscado na tábua de barro: {"tipo": "sinal", "texto": "..."}
#   "aldeia"     o jogador anda pela aldeia de dia (clica nas ocas) e volta pela seta da
#                entrada da aldeia, onde o roteiro continua. Pode ter:
#                  "seta"     o texto da seta (padrão: "Entrada da aldeia")
#                  "dica"     a dica embaixo da tela
#                  "pessoas"  quem está na aldeia: clicar abre a conversa (os "passos" dela)
#                             e, no fim, o jogador volta para onde estava. Cada uma tem "nome",
#                             "imagem" (dados/arte.py), "posicao" (o meio da borda de baixo da
#                             imagem, x e y na tela 1600x900), "escala" (1 = o tamanho de quem
#                             fala; 0.5 = metade) e, se ela espera dentro de uma oca, "oca"
#                             (o nome da oca em dados/aldeia.py): aí ela aparece lá dentro,
#                             no lugar de ONDE_DORME (dados/aldeia.py).
#   "noite"      começa a noite na fogueira: o roteiro dela fica em dados/noites.py
#   "se"         os "passos" de dentro só acontecem se a condição bate:
#                "morto": "Yara" (o jogador matou Yara), "dentro": "Yara" (Yara está na
#                aldeia) ou "tapiri": "Yara" (Yara está no tapiri)
#
# "efeitos" soma valores às variáveis do estado.py: {"memoria": 1, "vivos": 1}.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.

DIAS = {
    1: {
        "titulo": "Dia 1",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A fala inicial do pajé: apresenta o papel do jogador. Ninguém examina ninguém de dia.
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "O cacique foi para a mata. Enquanto ele não volta, a entrada é sua."},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Éramos quarenta antes da febre. Hoje somos doze. Cada rede vazia tem um nome."},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Quem chegar pela trilha, escute. Depois decida se entra ou se segue caminho."},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Quando o dia acabar, eu conto o que vi no sono. O mal sempre deixa [um sinal]."},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Ande pela aldeia. Quando estiver pronto, vá até a entrada."},

            # O corte entre o pajé e a Yara: o jogador anda pela aldeia e vai até a entrada.
            {"tipo": "visitante", "visitante": None},
            {"tipo": "aldeia"},

            # A chegada de Yara, pela trilha na mata. Ninguém comenta nem descreve: o jogador só vê e ouve.
            # Na entrada a conversa é curta. A história da aldeia dela fica para depois que ela
            # entra, na aldeia; e a conversa sobre o que se vê nela, para a fogueira (dados/noites.py).
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "visitante", "visitante": "yara"},
            {"tipo": "fala", "quem": "Yara",
             "texto": "Dormi três noites na beira do fogo. Só preciso de teto até a [chuva passar]."},
            {"tipo": "perguntas", "perguntas": [
                {"pergunta": "De onde você vem?",
                 "resposta": "Da costa, três dias para o norte."},
                {"pergunta": "Por que seus olhos estão assim?",
                 "resposta": "[Fumaça]. A lenha estava verde."},
            ]},
            {"tipo": "escolha", "opcoes": [
                {"texto": "Deixar entrar", "efeitos": {"vivos": 1}, "entra": "Yara", "passos": [
                    {"tipo": "fala", "quem": "Yara",
                     "texto": "Tenho este machado de ferro. É seu, pelo teto."},
                    {"tipo": "escolha", "opcoes": [
                        {"texto": "Aceitar o machado", "efeitos": {"proximidade_vila": 1}, "passos": [
                            {"tipo": "fala", "quem": "Yara", "texto": "Está pago, então."},
                        ]},
                        {"texto": "Recusar o machado", "passos": [
                            {"tipo": "fala", "quem": "Yara", "texto": "Então fico devendo."},
                        ]},
                    ]},

                    # Yara já está dentro, esperando na oca Yorixiriamori: o jogador anda pela
                    # aldeia de novo e, se quiser, entra na oca e clica nela para ouvir sobre a
                    # aldeia antiga dela.
                    {"tipo": "visitante", "visitante": None},
                    {"tipo": "aldeia", "seta": "Esperar a noite",
                     "dica": "Yara está na oca Yorixiriamori. Entre para conversar, ou espere a noite.",
                     "pessoas": [
                        {"nome": "Yara", "oca": "oca1", "passos": [
                            {"tipo": "fundo", "fundo": "oca1", "filtro": "dia"},
                            {"tipo": "visitante", "visitante": "yara"},
                            {"tipo": "fala", "quem": "Yara",
                             "texto": "A sua aldeia lembra a minha. A minha era maior."},
                            {"tipo": "perguntas", "botao": "Terminar a conversa", "perguntas": [
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
                            {"tipo": "visitante", "visitante": None},
                        ]},
                     ]},
                ]},
                {"texto": "Não deixar entrar", "passos": [
                    {"tipo": "fala", "quem": "Yara", "texto": "Então sigo para o sul."},
                ]},
            ]},
            {"tipo": "visitante", "visitante": None},

            # Entre o dia e a noite: o sinal do pajé. Hoje ele acusa uma inocente
            # (o olho de Yara é de fumaça), e o jogo não diz isso.
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com olho vermelho. O mal deixa o branco do olho raiado."},
            {"tipo": "sinal", "texto": "Olho vermelho, com o branco raiado."},

            # A noite na fogueira: conversa, exame do rosto e decisão (dados/noites.py).
            {"tipo": "noite"},
        ],
    },

    2: {
        "titulo": "Dia 2",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: o jogo mostra quem morreu. Quem o jogador matou aparece com o nome.
            {"tipo": "se", "morto": "Yara", "passos": [
                {"tipo": "fala", "quem": "",
                 "texto": "O corpo de Yara amanheceu coberto com uma esteira."},
            ]},

            # O jogador anda pela aldeia e vai até a entrada, como no dia 1.
            {"tipo": "aldeia"},

            # A chegada de Mbaé. Ninguém comenta nem descreve: o jogador vê e ouve.
            # Ele está com a febre e não sabe (ou não diz).
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "visitante", "visitante": "mbae"},
            {"tipo": "fala", "quem": "Mbaé",
             "texto": "Segui uma anta por dois dias. (tosse) [É só cansaço]."},
            {"tipo": "perguntas", "perguntas": [
                {"pergunta": "De onde você vem?",
                 "resposta": "Do outro lado do rio. Meu povo caça onde o seu não vai."},
                {"pergunta": "Você está doente?",
                 "resposta": "[Não]. Dormi no sereno, e a tosse veio junto."},
            ]},
            {"tipo": "escolha", "opcoes": [
                {"texto": "Deixar entrar", "efeitos": {"vivos": 1}, "entra": "Mbaé", "passos": [
                    {"tipo": "fala", "quem": "Mbaé", "texto": "Não vou dar trabalho."},

                    # Mbaé espera na oca Yebá Bëló: lá ele conta de antes, se o jogador quiser.
                    {"tipo": "visitante", "visitante": None},
                    {"tipo": "aldeia", "seta": "Esperar a noite",
                     "dica": "Mbaé está na oca Yebá Bëló. Entre para conversar, ou espere a noite.",
                     "pessoas": [
                        {"nome": "Mbaé", "oca": "oca2", "passos": [
                            {"tipo": "fundo", "fundo": "oca2_dia", "filtro": "dia"},
                            {"tipo": "visitante", "visitante": "mbae"},
                            {"tipo": "fala", "quem": "Mbaé",
                             "texto": "Seu povo me olha torto. Já estou acostumado."},
                            {"tipo": "perguntas", "botao": "Terminar a conversa", "perguntas": [
                                {"pergunta": "Conte de antes.",
                                 "resposta": [
                                     "Antes a gente seguia a anta pelo rio inteiro. Sem dono de margem.",
                                     "Agora desce barco pelo rio, e a caça foge para dentro da mata.",
                                 ],
                                 "efeitos": {"memoria": 1}},
                                {"pergunta": "Por que olham torto para você?",
                                 "resposta": "Contam histórias do meu povo. [Nenhuma é verdade]."},
                            ]},
                            {"tipo": "visitante", "visitante": None},
                        ]},
                     ]},
                ]},
                {"texto": "Não deixar entrar", "passos": [
                    {"tipo": "fala", "quem": "Mbaé", "texto": "Então vou para a vila. Dizem que lá tem remédio."},
                ]},
            ]},
            {"tipo": "visitante", "visitante": None},

            # O sinal do pajé: hoje ele acerta (Mbaé tem a febre).
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com gente tremendo na rede. O mal deixa [o corpo quente]."},
            {"tipo": "sinal", "texto": "Corpo quente e tosse seca."},

            {"tipo": "noite"},
        ],
    },
}
