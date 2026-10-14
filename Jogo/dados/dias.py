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
#                "morto": "Yara" (o jogador matou Yara), "morto_ontem": "Yara" (matou Yara na
#                noite passada), "dentro": "Yara" (Yara está na aldeia), "tapiri": "Yara"
#                (Yara está no tapiri) ou "na_oca": "Mbaé" (Mbaé está na aldeia, fora do tapiri)
#   Uma opção de "escolha" com "condicao" só aparece se ela bate: {"dentro": "Yara"},
#                {"alguem_dentro": True} (alguém de fora entrou) ou {"se_remedio": True}.
#                "entrega": "Yara" entrega a pessoa ao Irmão Aleixo (ela sai da aldeia).
#
# "efeitos" soma valores às variáveis do estado.py: {"memoria": 1, "vivos": 1}.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.

# --- Dia 3: a primeira aparição do Irmão Aleixo (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf) ---
# Ninguém chega pela trilha: Aleixo vem até a entrada, finca uma cruz e faz a primeira oferta.
# Tudo o que ele oferece funciona de verdade. E ninguém que ele leva volta.
#   Aceitar o remédio: proximidade_vila +1 e 1 remédio guardado (na fogueira, cura a febre de uma
#                      pessoa: a opção "Dar o remédio" de dados/noites.py).
#   Entregar alguém:   entregues +1, proximidade_vila +1, vivos -1. A pessoa sai da aldeia.
#   Recusar:           recusas_aleixo +1. Aceitar o remédio e entregar podem ir juntos;
#                      recusar exclui os dois.
ALEIXO = "Irmão Aleixo"
FALA_ALEIXO_FICA = {"tipo": "fala", "quem": ALEIXO, "texto": "Fico por aqui, ao lado da cruz, se precisarem."}
EFEITOS_ENTREGAR = {"entregues": 1, "proximidade_vila": 1, "vivos": -1}
EFEITOS_REMEDIO = {"proximidade_vila": 1, "remedios": 1}
FALA_REMEDIO = {"tipo": "fala", "quem": ALEIXO,
                "texto": "Uma colher na água, para quem arder em febre. [Cura], com a graça de Deus."}


def entregar(depois):
    """Quem vai com Aleixo: só quem é de fora e entrou. "depois": os passos que vêm em seguida."""
    return {"tipo": "escolha", "texto": "Quem vai com o Irmão Aleixo para a vila?", "opcoes": [
        {"texto": "Yara", "condicao": {"dentro": "Yara"}, "entrega": "Yara", "efeitos": EFEITOS_ENTREGAR,
         "passos": [{"tipo": "fala", "quem": ALEIXO, "texto": "Na vila ela terá teto e doutrina."}] + depois},
        {"texto": "Mbaé", "condicao": {"dentro": "Mbaé"}, "entrega": "Mbaé", "efeitos": EFEITOS_ENTREGAR,
         "passos": [{"tipo": "fala", "quem": ALEIXO,
                     "texto": "Esse homem tem febre. Na vila temos onde deitá-lo."}] + depois},
        {"texto": "Ninguém, afinal", "passos": depois},
    ]}


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
             "texto": "Sonhei com gente tremendo na rede. O mal deixa [a boca com feridas]."},
            {"tipo": "sinal", "texto": "Boca com feridas."},

            {"tipo": "noite"},
        ],
    },
    3: {
        "titulo": "Dia 3",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: primeiro a febre (motor/febre.py, com o nome de quem acordou doente);
            # depois, o corpo de quem o jogador matou na noite 2, com o nome.
            {"tipo": "se", "morto_ontem": "Yara", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Yara amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Mbaé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "na_oca": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "Mbaé tossiu a noite toda na oca Yebá Bëló."},
            ]},

            {"tipo": "aldeia"},

            # A entrada: ninguém chega pela trilha. Aleixo já está lá, fincando a cruz.
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "fala", "quem": "",
             "texto": "Ninguém chega pela trilha. Um homem de batina preta finca uma cruz ao lado da entrada."},
            {"tipo": "visitante", "visitante": "aleixo"},
            {"tipo": "fala", "quem": ALEIXO,
             "texto": "Bom dia. Sou o Irmão Aleixo, da vila. Vou ficar por aqui umas manhãs, se não incomodar."},
            {"tipo": "fala", "quem": ALEIXO, "texto": "Soube que há febre por estes lados. Trouxe o que pude."},
            {"tipo": "perguntas", "botao": "Ouvir a oferta", "perguntas": [
                {"pergunta": "O que você quer?",
                 "resposta": "Ajudar. Trago remédio da botica e lugar na vila para quem precisar de cuidado."},
                {"pergunta": "Por que a cruz?",
                 "resposta": "Para que quem passa saiba que aqui há quem reze por ele."},
                {"pergunta": "Os que vão com você voltam?",
                 "resposta": "Quando sararem, terão trabalho e doutrina. [A vila é longe]."},
                {"pergunta": "De onde vem essa febre?",
                 "resposta": [
                     "Uns dizem que do ar ruim do rio. Outros, que do pecado.",
                     "Eu sei o que vi: [o remédio cura]. E na vila ninguém morre sem cuidado.",
                 ]},
                {"pergunta": "O que tem nesse caderno?",
                 "resposta": [
                     "Os nomes dos que levei para a vila. Cada um com o seu número.",
                     "[Ninguém se perde] no caminho.",
                 ],
                 "efeitos": {"pistas": 1}},
            ]},

            # A oferta.
            {"tipo": "escolha", "texto": "O remédio, ou alguém para levar à vila.", "opcoes": [
                {"texto": "Aceitar o remédio", "efeitos": EFEITOS_REMEDIO, "passos": [
                    FALA_REMEDIO,
                    {"tipo": "escolha", "opcoes": [
                        {"texto": "Entregar alguém também", "condicao": {"alguem_dentro": True},
                         "passos": [entregar([FALA_ALEIXO_FICA])]},
                        {"texto": "Basta o remédio", "passos": [FALA_ALEIXO_FICA]},
                    ]},
                ]},
                {"texto": "Entregar alguém", "condicao": {"alguem_dentro": True}, "passos": [
                    entregar([
                        {"tipo": "escolha", "opcoes": [
                            {"texto": "Aceitar o remédio também", "efeitos": EFEITOS_REMEDIO,
                             "passos": [FALA_REMEDIO, FALA_ALEIXO_FICA]},
                            {"texto": "Basta", "passos": [FALA_ALEIXO_FICA]},
                        ]},
                    ]),
                ]},
                {"texto": "Recusar", "efeitos": {"recusas_aleixo": 1}, "passos": [
                    {"tipo": "fala", "quem": "", "texto": "Ele sorri, como quem entende, e volta para a cruz."},
                    FALA_ALEIXO_FICA,
                ]},
            ]},
            {"tipo": "visitante", "visitante": None},

            # O sinal do pajé: hoje o mal já está do lado de dentro (os amaldiçoados, dados/febre.py).
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com redes vazias, do lado de dentro. O mal passa de rede em rede, [sem deixar sinal]."},
            {"tipo": "sinal", "texto": "Quem dormiu perto do doente pode levar o mal, sem sinal nenhum."},

            # A fogueira da aldeia: sem visitante novo, o jogador examina gente de dentro.
            {"tipo": "noite"},
        ],
    },
}
