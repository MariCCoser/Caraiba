# Roteiro de cada Dia: o que acontece, na ordem. Edite à vontade: aqui não há lógica.
#
# Fonte: Proposta.docx. Um dia segue sempre a mesma ordem: alguém chega à entrada,
# o jogador conversa e decide se a pessoa entra, e, entre o dia e a noite, o pajé
# conta o sinal da doença, que vai para o caderno.
#
# Cada passo é um dicionário com "tipo":
#   "fundo"      troca o cenário: {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"}
#   "fala"       alguém fala:     {"tipo": "fala", "quem": "Pajé", "texto": "..."}
#                (no máximo 2 linhas na tela; palavras entre [colchetes] ficam em âmbar)
#   "visitante"  mostra a pessoa na entrada (apelido de dados/arte.py) ou None para tirar
#   "perguntas"  o jogador escolhe o que perguntar, quantas quiser, e depois clica em "Decidir".
#                Cada pergunta: "pergunta", "resposta" e, se quiser, "efeitos".
#   "escolha"    botões; cada opção tem "texto" e, se quiser, "efeitos", "entra" (o nome de
#                quem passa a estar dentro da aldeia) e "passos" (o que acontece depois)
#   "sinal"      o pajé anota um sinal no caderno: {"tipo": "sinal", "texto": "..."}
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
            {"tipo": "fala", "quem": "Pajé",
             "texto": "O cacique foi para a mata. Enquanto ele não volta, a entrada é sua."},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Éramos quarenta antes da febre. Hoje somos doze. Cada rede vazia tem um nome."},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Quem chegar pela trilha, escute. Depois decida se entra ou se segue caminho."},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Quando o dia acabar, eu conto o que vi no sono. O mal sempre deixa [um sinal]."},

            # A chegada de Yara. Ninguém comenta nem descreve: o jogador só vê e ouve.
            {"tipo": "visitante", "visitante": "yara"},
            {"tipo": "fala", "quem": "Yara",
             "texto": "Dormi três noites na beira do fogo. Só preciso de teto até a [chuva passar]."},
            {"tipo": "perguntas", "perguntas": [
                {"pergunta": "De onde você vem?",
                 "resposta": "Da costa. Lá a gente troca farinha por ferro com os homens dos barcos."},
                {"pergunta": "Por que seus olhos estão assim?",
                 "resposta": "[Fumaça]. A lenha estava verde, e eu dormi perto demais do fogo."},
                {"pergunta": "Conte da sua aldeia.",
                 "resposta": "Antes a gente cortava árvore com pedra. Levava o dia. Agora leva um pouco.",
                 "efeitos": {"memoria": 1}},
            ]},
            {"tipo": "escolha", "opcoes": [
                {"texto": "Deixar entrar", "efeitos": {"vivos": 1}, "entra": "Yara", "passos": [
                    {"tipo": "fala", "quem": "Yara",
                     "texto": "Tenho este machado de ferro. É seu, pelo teto."},
                    {"tipo": "escolha", "opcoes": [
                        {"texto": "Aceitar o machado", "efeitos": {"proximidade_vila": 1}, "passos": [
                            {"tipo": "fala", "quem": "Yara",
                             "texto": "Corta em pouco tempo o que a pedra levava o dia inteiro."},
                        ]},
                        {"texto": "Recusar o machado", "passos": [
                            {"tipo": "fala", "quem": "Yara", "texto": "Então fico devendo."},
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
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com olho vermelho. O mal deixa o branco do olho raiado."},
            {"tipo": "sinal", "texto": "Olho vermelho, com o branco raiado."},
        ],
    },
}
