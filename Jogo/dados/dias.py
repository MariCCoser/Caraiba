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
#   Uma opção de "escolha" com "condicao" só aparece se ela bate: {"dentro": "Yara"}.
#                "entrega": "Yara" entrega a pessoa ao Irmão Aleixo (ela sai da aldeia).
#   "aleixo_leva" o Irmão Aleixo leva uma pessoa da aldeia, sorteada (o jogador não escolhe):
#                "de_fora" é a frase quando ele leva alguém de fora (%s = o nome) e "morador",
#                quando leva um morador.
#
# "efeitos" soma valores às variáveis do estado.py: {"memoria": 1, "vivos": 1}.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.
#
# Quem é de fora tem a mesma conversa na oca e em todas as noites (dados/conversas.py).

from dados.conversas import conversa_mbae, conversa_potira, conversa_yara

# --- Dia 3: a primeira das três visitas do Irmão Aleixo (dias 3, 6 e 9) ---
# Ninguém chega pela trilha: Aleixo vem até a entrada e finca uma cruz. Ele não traz cura:
# só leva gente para a vila. Ninguém que ele leva volta.
# Ninguém ali conhece "febre": para a aldeia e para ele, é uma maldição.
#
# Em cada visita, ele pede alguém (oferta_aleixo):
#   Entregar alguém de fora: entregues +1, proximidade_vila +1, vivos -1. A pessoa sai da aldeia.
#   Negar:                   recusas_aleixo +1. Mesmo assim ele leva alguém, sorteado entre
#                            todos da aldeia (quem é de fora ou um morador): levados +1, vivos -1.
#                            A cada visita, ele fica mais irritado (FALA_ALEIXO_NEGADO).
# Negar nas três visitas é o "nenhuma entrega" (entregues == 0) dos finais.
#
# As perguntas para ele ficam divididas entre as três visitas: as do dia 6 e do dia 9 já
# estão aqui, para quando esses dias existirem.
ALEIXO = "Irmão Aleixo"
PERGUNTAS_ALEIXO = {
    3: [
        {"pergunta": "O que você quer?",
         "resposta": "Levar para a vila quem precisa de cuidado."},
        {"pergunta": "Por que a cruz?",
         "resposta": "Para eu achar o caminho de volta."},
    ],
    6: [
        {"pergunta": "Os que você levou voltam?",
         "resposta": "[Estão bem na vila]. É longe para voltar."},
        {"pergunta": "De onde vem essa maldição?",
         "resposta": "Do pecado. [Na vila, ela sai]."},
    ],
    9: [
        {"pergunta": "O que tem nesse caderno?",
         "resposta": "Os nomes dos que levei. Cada um com o seu número.",
         "efeitos": {"pistas": 1}},
    ],
}

# O que Aleixo diz quando o jogador nega, visita a visita: cada vez mais irritado.
FALA_ALEIXO_NEGADO = {
    3: "Ninguém? Então eu escolho.",
    6: "De novo, não? A vila não espera. Eu escolho.",
    9: "Chega. Eu levo quem eu quiser.",
}
EFEITOS_ENTREGAR = {"entregues": 1, "proximidade_vila": 1, "vivos": -1}
FALA_ALEIXO_VOLTA = {"tipo": "fala", "quem": ALEIXO, "texto": "Volto daqui a alguns dias."}


def oferta_aleixo(dia):
    """O pedido de Aleixo: o jogador entrega alguém de fora ou nega. Negando, ele leva alguém
    sorteado mesmo assim (o passo "aleixo_leva")."""
    return {"tipo": "escolha", "texto": "Ele quer levar alguém para a vila.", "opcoes": [
        {"texto": "Entregar Yara", "condicao": {"dentro": "Yara"}, "entrega": "Yara",
         "efeitos": EFEITOS_ENTREGAR,
         "passos": [{"tipo": "fala", "quem": ALEIXO, "texto": "Na vila ela terá teto e doutrina."}]},
        {"texto": "Entregar Mbaé", "condicao": {"dentro": "Mbaé"}, "entrega": "Mbaé",
         "efeitos": EFEITOS_ENTREGAR,
         "passos": [{"tipo": "fala", "quem": ALEIXO, "texto": "Na vila temos onde deitá-lo."}]},
        {"texto": "Negar", "efeitos": {"recusas_aleixo": 1}, "passos": [
            {"tipo": "fala", "quem": ALEIXO, "texto": FALA_ALEIXO_NEGADO[dia]},
            {"tipo": "aleixo_leva",
             "de_fora": "Ele leva %s pela trilha. Ninguém consegue impedir.",
             "morador": "Ele leva um morador da aldeia pela trilha. Ninguém consegue impedir."},
        ]},
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
                        {"texto": "Aceitar o machado", "efeitos": {"proximidade_vila": 1, "machado": 1}, "passos": [
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
                            {"tipo": "perguntas", "botao": "Terminar a conversa", "perguntas": conversa_yara()},
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
                            {"tipo": "perguntas", "botao": "Terminar a conversa", "perguntas": conversa_mbae()},
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

            # A manhã: primeiro a febre (motor/febre.py: quantos acordaram doentes);
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
            {"tipo": "fala", "quem": ALEIXO, "texto": "Sou o Irmão Aleixo, da vila. Vim buscar quem precisa de cuidado."},
            {"tipo": "perguntas", "botao": "Seguir", "perguntas": PERGUNTAS_ALEIXO[3]},

            # O pedido: entregar alguém ou negar (negando, ele leva alguém do mesmo jeito).
            oferta_aleixo(3),
            FALA_ALEIXO_VOLTA,
            {"tipo": "visitante", "visitante": None},
            {"tipo": "fala", "quem": "", "texto": "A cruz fica na entrada."},

            # Hoje o pajé não conta sinal novo (a tábua não muda): ele só desconfia de Aleixo.
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé", "texto": "Esta noite o sono não me mostrou nada novo."},
            {"tipo": "fala", "quem": "Pajé", "texto": "Mas eu vi a cruz na entrada. Isso eu não precisei sonhar."},

            # A fogueira da aldeia: sem visitante novo.
            {"tipo": "noite"},
        ],
    },

    # --- Dia 4: a que você conhece (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf) ---
    # Potira, 24 anos, é da sua aldeia: saiu para buscar comida e volta com o cesto vazio.
    # Ela é sã: não há armadilha nenhuma, e serve para o jogador baixar a guarda.
    # Na entrada a conversa é curta; a conversa inteira é na oca Wanadi (dados/conversas.py).
    # O pajé conta o sinal do próximo mal (Tamandaré-mirim, no dia 5): o 3º risco da tábua.
    4: {
        "titulo": "Dia 4",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: primeiro a febre (motor/febre.py); depois, quem o jogador matou ontem.
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

            # A chegada de Potira. Ninguém comenta nem descreve: o jogador vê e ouve.
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "visitante", "visitante": "potira"},
            {"tipo": "fala", "quem": "Potira", "texto": "Sou eu, Potira. O cesto voltou vazio."},
            {"tipo": "perguntas", "perguntas": [
                {"pergunta": "Onde você estava?",
                 "resposta": "Nas roças do outro lado do morro. [Não encontrei ninguém]."},
            ]},
            {"tipo": "escolha", "opcoes": [
                {"texto": "Deixar entrar", "efeitos": {"vivos": 1}, "entra": "Potira", "passos": [
                    {"tipo": "fala", "quem": "Potira", "texto": "Obrigada. Com fome, mas viva."},

                    # Potira espera na oca Wanadi: lá a conversa é mais longa, se o jogador quiser.
                    {"tipo": "visitante", "visitante": None},
                    {"tipo": "aldeia", "seta": "Esperar a noite",
                     "dica": "Potira está na oca Wanadi. Entre para conversar, ou espere a noite.",
                     "pessoas": [
                        {"nome": "Potira", "oca": "oca3", "passos": [
                            {"tipo": "fundo", "fundo": "oca3_dia", "filtro": "dia"},
                            {"tipo": "visitante", "visitante": "potira"},
                            {"tipo": "fala", "quem": "Potira",
                             "texto": "Desculpa. Saí para buscar comida e não achei nada."},
                            {"tipo": "perguntas", "botao": "Terminar a conversa", "perguntas": conversa_potira()},
                            {"tipo": "visitante", "visitante": None},
                        ]},
                     ]},
                ]},
                {"texto": "Não deixar entrar", "passos": [
                    {"tipo": "fala", "quem": "Potira", "texto": "Então durmo do lado de fora da cerca."},
                ]},
            ]},
            {"tipo": "visitante", "visitante": None},

            # O sinal do pajé: o mal que vem amanhã (Tamandaré-mirim). Fica riscado como III.
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com uma boca aberta. O mal se esconde [por dentro da bochecha], em pontos brancos."},
            {"tipo": "sinal", "texto": "Pontos brancos por dentro da bochecha."},

            {"tipo": "noite"},
        ],
    },
}
