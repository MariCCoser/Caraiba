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
#                "amaldicoados_ao_menos": 2 / "amaldicoados_menos_de": 2 (quantos amaldiçoados há
#                na aldeia: os doentes de fora e quem pegou deles)
#                "levou_alguem": True (o Irmão Aleixo já levou alguém, entregue ou sorteado)
#                "entregue": "Yara" (o Irmão Aleixo levou Yara, entregue ou sorteada)
#   Uma opção de "escolha" com "condicao" só aparece se ela bate: {"dentro": "Yara"}.
#                "entrega": "Yara" entrega a pessoa ao Irmão Aleixo (ela sai da aldeia).
#   "aleixo_leva" o Irmão Aleixo leva uma pessoa da aldeia, sorteada (o jogador não escolhe):
#                "de_fora" é a frase quando ele leva alguém (%s = o nome) e "ninguem", quando
#                não há ninguém de fora para levar.
#
# "efeitos" soma valores às variáveis do estado.py: {"memoria": 1, "vivos": 1}.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.
#
# Quem é de fora tem a mesma conversa na oca e em todas as noites (dados/conversas.py).

from dados.conversas import (conversa_iande, conversa_mbae, conversa_potira, conversa_tamandare,
                             conversa_yara)

# --- Dia 3: a primeira das três visitas do Irmão Aleixo (dias 3, 6 e 9) ---
# Ninguém chega pela trilha: Aleixo vem até a entrada e finca uma cruz. Ele não traz cura:
# só leva gente para a vila. Ninguém que ele leva volta.
# Ninguém ali conhece "febre": para a aldeia e para ele, é uma maldição.
#
# Em cada visita, ele pede alguém (oferta_aleixo):
#   Entregar alguém de fora: entregues +1, proximidade_vila +1, vivos -1. A pessoa sai da aldeia.
#   Negar:                   recusas_aleixo +1. Mesmo assim ele leva alguém, sorteado entre
#                            quem é de fora: levados +1, vivos -1. Sem ninguém, vai embora só.
#                            A cada visita, ele fica mais irritado (FALA_ALEIXO_NEGADO).
#                            Negar dá mais energia na noite (ENERGIA_POR_NEGAR).
# Negar nas três visitas é o "nenhuma entrega" (entregues == 0) dos finais.
#
# As perguntas para ele ficam divididas entre as três visitas: as do dia 6 e do dia 9 já
# estão aqui, para quando esses dias existirem.
ALEIXO = "Irmão Aleixo"

# O pajé sobre os deuses: felizes com poucos amaldiçoados na aldeia, infelizes com 2 ou mais
# (os doentes de fora que estão nela e quem pegou deles: motor/febre.py).
DEUSES = 2
DEUSES_FELIZES = {"tipo": "se", "amaldicoados_menos_de": DEUSES, "passos": [
    {"tipo": "fala", "quem": "Pajé", "texto": "Os deuses estão felizes. O sono foi tranquilo."},
]}
DEUSES_INFELIZES = {"tipo": "se", "amaldicoados_ao_menos": DEUSES, "passos": [
    {"tipo": "fala", "quem": "Pajé", "texto": "Os deuses estão infelizes. Há maldição demais entre as redes."},
]}
PERGUNTAS_ALEIXO = {
    3: [
        {"pergunta": "O que você quer?",
         "resposta": "Levar para a vila quem precisa de cuidado."},
        {"pergunta": "Por que a cruz?",
         "resposta": "Para eu achar o caminho de volta."},
    ],
    # Dia 6: só o caderno e o que mudou (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf).
    6: [
        {"pergunta": "O que tem nesse caderno?",
         "resposta": "Os nomes dos que levei. Cada um com o seu número.",
         "efeitos": {"pistas": 1}},
        {"pergunta": "O que mudou?",
         "resposta": [
             "Na vila falam desta aldeia.",
             "Dizem que aqui se esconde gente que devia estar [sob a lei].",
         ]},
    ],
    # Dia 9: tudo o que ele ainda não disse, e o cordão (o da Iandé, que ele batizou).
    9: [
        {"pergunta": "Os que você levou voltam?",
         "resposta": "[Estão bem na vila]. É longe para voltar."},
        {"pergunta": "De onde vem essa maldição?",
         "resposta": "Do pecado. [Na vila, ela sai]."},
        {"pergunta": "Isso é ameaça?",
         "resposta": "É aviso. Eu gosto de vocês. Por isso vim antes dos outros."},
        {"pergunta": "Quem são os outros?",
         "resposta": "Homens com ordem do governador. Não dependem de mim."},
        {"pergunta": "Que cordão é esse no seu pescoço?",
         "resposta": [
             "Uma moça me deu, no domingo em que a batizei. Iandé, do seu povo.",
             "Pediu que eu rezasse por ela. [Eu rezo].",
         ],
         "efeitos": {"pistas": 1}},
    ],
}

# Sobre quem ele já levou (entregue ou à força): se está curado da maldição e onde está.
# Cada pessoa tem as duas perguntas, que só aparecem se o Aleixo a levou numa visita anterior.
# Ele nunca mente de propósito: responde do jeito dele, e desvia.
SOBRE_OS_LEVADOS = {
    "Yara": ("Yara está curada da maldição?", "Ela reza todos os dias. [Deus vai curá-la].",
             "Onde Yara está?", "Na casa da botica. Dorme numa esteira, perto do altar."),
    "Mbaé": ("Mbaé está curado da maldição?", "A tosse ainda não passou. [Está nas mãos de Deus].",
             "Onde Mbaé está?", "Na enfermaria da vila, com os outros que tossem."),
    "Potira": ("Potira está curada da maldição?", "Ela nunca teve a maldição. [Trabalha bem].",
               "Onde Potira está?", "Na roça dos padres. Planta mandioca para a vila."),
    "Tamandaré-mirim": ("Tamandaré-mirim está curado da maldição?",
                        "O corpo melhora. A língua, não. [Ainda prega contra nós].",
                        "Onde Tamandaré-mirim está?", "Na casa da câmara, até aprender a calar."),
    "Iandé": ("Iandé está curada da maldição?",
              "Agora ela tem nome cristão. [A maldição não fica em quem é batizado].",
              "Onde Iandé está?", "Na casa das moças, aprendendo a fiar e a rezar."),
}


def perguntas_sobre_os_levados():
    """As perguntas sobre cada um que o Aleixo já levou (dias 6 e 9)."""
    perguntas = []
    for nome, (curado, resposta_curado, onde, resposta_onde) in SOBRE_OS_LEVADOS.items():
        perguntas.append({"pergunta": curado, "resposta": resposta_curado, "entregue": nome})
        perguntas.append({"pergunta": onde, "resposta": resposta_onde, "entregue": nome})
    return perguntas


# O que Aleixo diz quando o jogador nega, visita a visita: cada vez mais irritado.
FALA_ALEIXO_NEGADO = {
    3: "Ninguém? Então eu escolho.",
    6: "De novo, não? A vila não espera. Eu escolho.",
    9: "Chega. Eu levo quem eu quiser.",
}
EFEITOS_ENTREGAR = {"entregues": 1, "proximidade_vila": 1, "vivos": -1}
# Negar o pedido do Aleixo dá energia a mais na noite do mesmo dia (olhares na fogueira).
ENERGIA_POR_NEGAR = 1
FALA_ALEIXO_VOLTA = {"tipo": "fala", "quem": ALEIXO, "texto": "Volto daqui a alguns dias."}


# O que Aleixo diz de cada um que o jogador entrega (só aparece quem está na aldeia).
FALA_ENTREGUE = {
    "Yara": "Na vila ela terá teto e doutrina.",
    "Mbaé": "Na vila temos onde deitá-lo.",
    "Potira": "Na vila há comida para quem trabalha.",
    "Tamandaré-mirim": "Esse eu conheço. Na vila há lugar para ele.",
    "Iandé": "Esta eu batizei no domingo. Na vila ela já tem nome.",
}


def oferta_aleixo(dia):
    """O pedido de Aleixo: o jogador entrega alguém de fora ou nega. Negando, ele leva alguém
    que ele quer mesmo assim (sorteado: o passo "aleixo_leva")."""
    entregar = [
        {"texto": "Entregar " + nome, "condicao": {"dentro": nome}, "entrega": nome,
         "efeitos": EFEITOS_ENTREGAR, "passos": [{"tipo": "fala", "quem": ALEIXO, "texto": fala}]}
        for nome, fala in FALA_ENTREGUE.items()]
    return {"tipo": "escolha", "texto": "Ele quer levar alguém para a vila.", "opcoes": entregar + [
        {"texto": "Negar", "efeitos": {"recusas_aleixo": 1, "energia_hoje": ENERGIA_POR_NEGAR}, "passos": [
            {"tipo": "fala", "quem": ALEIXO, "texto": FALA_ALEIXO_NEGADO[dia]},
            {"tipo": "aleixo_leva",
             "de_fora": "Ele leva %s pela trilha. Ninguém consegue impedir.",
             "ninguem": "Ele olha as redes, não acha quem levar e fecha o caderno."},
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
             "texto": "Éramos quarenta antes da maldição. Hoje somos dois. Cada rede vazia tem um nome."},
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
                {"pergunta": "Você está amaldiçoado?",
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

    # --- Dia 5: Tamandaré-mirim, o caraíba que prega (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf) ---
    # Ele vem "dos caraíbas" (é assim que ele chama os homens brancos). Está com a maldição
    # (sarampo, antes das manchas na pele): os pontos brancos por dentro da bochecha, o sinal III
    # da tábua. Ele acha que está só rouco de pregar.
    # Na entrada a conversa é curta; a conversa inteira é na oca Yebá Bëló (dados/conversas.py).
    # O pajé não conta sinal novo: só diz se os deuses estão felizes (poucos amaldiçoados na
    # aldeia) ou infelizes (2 ou mais: DEUSES).
    5: {
        "titulo": "Dia 5",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: primeiro a febre (motor/febre.py); depois, quem o jogador matou ontem.
            {"tipo": "se", "morto_ontem": "Yara", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Yara amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Mbaé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Potira", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Potira amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "na_oca": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "Mbaé tossiu a noite toda na oca Yebá Bëló."},
            ]},

            {"tipo": "aldeia"},

            # A chegada de Tamandaré-mirim. Ninguém comenta nem descreve: o jogador vê e ouve.
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "visitante", "visitante": "tamandare"},
            {"tipo": "fala", "quem": "Tamandaré-mirim",
             "texto": "Ninguém precisa mais trabalhar para os caraíbas. Eu vim dizer isso. E dormir."},
            {"tipo": "perguntas", "perguntas": [
                {"pergunta": "De onde você vem?",
                 "resposta": "Dos caraíbas. Saí antes da lua nova. [Ninguém me seguiu]."},
                {"pergunta": "Você está amaldiçoado?",
                 "resposta": "[Rouco de pregar]. Só isso."},
            ]},
            {"tipo": "escolha", "opcoes": [
                {"texto": "Deixar entrar", "efeitos": {"vivos": 1}, "entra": "Tamandaré-mirim", "passos": [
                    {"tipo": "fala", "quem": "Tamandaré-mirim",
                     "texto": "Que a terra sem mal chegue a esta aldeia também."},

                    # Ele espera na oca Yebá Bëló, à esquerda da porta: lá ele conta o que prega.
                    {"tipo": "visitante", "visitante": None},
                    {"tipo": "aldeia", "seta": "Esperar a noite",
                     "dica": "Tamandaré-mirim está na oca Yebá Bëló. Entre para conversar, ou espere a noite.",
                     "pessoas": [
                        {"nome": "Tamandaré-mirim", "oca": "oca2", "passos": [
                            {"tipo": "fundo", "fundo": "oca2_dia", "filtro": "dia"},
                            {"tipo": "visitante", "visitante": "tamandare"},
                            {"tipo": "fala", "quem": "Tamandaré-mirim",
                             "texto": "Sente. Eu falo baixo, que a voz já acabou."},
                            {"tipo": "perguntas", "botao": "Terminar a conversa", "perguntas": conversa_tamandare()},
                            {"tipo": "visitante", "visitante": None},
                        ]},
                     ]},
                ]},
                {"texto": "Não deixar entrar", "passos": [
                    {"tipo": "fala", "quem": "Tamandaré-mirim", "texto": "Então prego para as árvores. Elas escutam melhor."},
                ]},
            ]},
            {"tipo": "visitante", "visitante": None},

            # O pajé não conta sinal novo: só diz como estão os deuses.
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            DEUSES_FELIZES,
            DEUSES_INFELIZES,

            {"tipo": "noite"},
        ],
    },

    # --- Dia 6: ele para de sorrir (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf) ---
    # A segunda visita do Irmão Aleixo. Ele não traz de volta quem levou. As perguntas são só
    # o caderno e o que mudou. O pedido é o mesmo do dia 3: entregar alguém ou negar (e, negando,
    # ele leva quem quer). De noite, o pajé conta o 4º sinal: manchas pelo corpo.
    6: {
        "titulo": "Dia 6",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: primeiro a febre (motor/febre.py); depois, quem o jogador matou ontem.
            {"tipo": "se", "morto_ontem": "Yara", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Yara amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Mbaé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Potira", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Potira amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Tamandaré-mirim", "passos": [
                {"tipo": "fala", "quem": "",
                 "texto": "O corpo de Tamandaré-mirim amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "na_oca": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "Mbaé tossiu a noite toda na oca Yebá Bëló."},
            ]},

            {"tipo": "aldeia"},

            # A entrada: Aleixo está ao lado da cruz, e não sorri desta vez.
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "fala", "quem": "",
             "texto": "Ninguém chega pela trilha. O Irmão Aleixo está ao lado da cruz. Desta vez, não sorri."},
            {"tipo": "se", "levou_alguem": True, "passos": [
                {"tipo": "fala", "quem": "", "texto": "Ele veio sozinho. Quem foi com ele não voltou."},
            ]},
            {"tipo": "visitante", "visitante": "aleixo"},
            {"tipo": "fala", "quem": ALEIXO, "texto": "Voltei, como disse que voltaria."},
            {"tipo": "perguntas", "botao": "Seguir",
             "perguntas": PERGUNTAS_ALEIXO[6] + perguntas_sobre_os_levados()},

            # O pedido, como no dia 3: entregar alguém ou negar.
            oferta_aleixo(6),
            FALA_ALEIXO_VOLTA,
            {"tipo": "visitante", "visitante": None},
            {"tipo": "fala", "quem": "", "texto": "A cruz fica na entrada."},

            # O sinal do pajé: o 4º risco da tábua.
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com manchas pelo corpo. Começam [atrás da orelha] e descem pela pele."},
            {"tipo": "sinal", "texto": "Manchas brancas atrás da orelha."},

            {"tipo": "noite"},
        ],
    },

    # --- Dia 7: a que está perfeita (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf) ---
    # Iandé, 27 anos, é da sua aldeia: foi à vila trocar mandioca e voltou sorrindo. Ela está
    # com a maldição (varíola, nos primeiros dias), sem nenhum sinal: não há nada para achar.
    # Ela não mente: ela não sabe. Na entrada a conversa é curta; a conversa inteira é na oca
    # Yorixiriamori, que ela divide com Yara (dados/conversas.py).
    # O pajé não conta sinal novo.
    7: {
        "titulo": "Dia 7",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: primeiro a febre (motor/febre.py); depois, quem o jogador matou ontem.
            {"tipo": "se", "morto_ontem": "Yara", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Yara amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Mbaé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Potira", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Potira amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Tamandaré-mirim", "passos": [
                {"tipo": "fala", "quem": "",
                 "texto": "O corpo de Tamandaré-mirim amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "na_oca": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "Mbaé tossiu a noite toda na oca Yebá Bëló."},
            ]},

            {"tipo": "aldeia"},

            # A chegada de Iandé. Ninguém comenta nem descreve: o jogador vê e ouve.
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "visitante", "visitante": "iande"},
            {"tipo": "fala", "quem": "Iandé", "texto": "Voltei! Troquei toda a mandioca."},
            {"tipo": "perguntas", "perguntas": [
                {"pergunta": "Como estava a vila?",
                 "resposta": "Todo mundo bem. Tinha festa de santo."},
            ]},
            {"tipo": "escolha", "opcoes": [
                {"texto": "Deixar entrar", "efeitos": {"vivos": 1}, "entra": "Iandé", "passos": [
                    {"tipo": "fala", "quem": "Iandé", "texto": "Eu sabia! Ninguém fecha a porta para mim."},

                    # Iandé espera na oca Yorixiriamori, com Yara: lá ela conta da viagem.
                    {"tipo": "visitante", "visitante": None},
                    {"tipo": "aldeia", "seta": "Esperar a noite",
                     "dica": "Iandé está na oca Yorixiriamori. Entre para conversar, ou espere a noite.",
                     "pessoas": [
                        {"nome": "Iandé", "oca": "oca1", "passos": [
                            {"tipo": "fundo", "fundo": "oca1", "filtro": "dia"},
                            {"tipo": "visitante", "visitante": "iande"},
                            {"tipo": "fala", "quem": "Iandé", "texto": "Senta aqui! Tenho tanta coisa para contar."},
                            {"tipo": "perguntas", "botao": "Terminar a conversa", "perguntas": conversa_iande()},
                            {"tipo": "visitante", "visitante": None},
                        ]},
                     ]},
                ]},
                {"texto": "Não deixar entrar", "passos": [
                    {"tipo": "fala", "quem": "Iandé", "texto": "Você não me reconhece? Sou eu, Iandé."},
                ]},
            ]},
            {"tipo": "visitante", "visitante": None},

            # O pajé não conta sinal novo (a tábua não muda).
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé", "texto": "O mal anda com quem parece bem. Eu não sei dizer mais que isso."},

            {"tipo": "noite"},
        ],
    },

    # --- Dia 8: a saída (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf, Ubiratã) ---
    # Krenan, da gente que subiu o rio, chega de canoa. Não pede teto: pede fogo para conversar.
    # A oferta é na fogueira (dados/noites.py, Noite 8), se o jogador o chama para lá ("convida":
    # ele não entra na aldeia, só senta ao fogo). Se o jogador não o deixa entrar, ele vai embora.
    # Ele fala um português antigo e duro.
    8: {
        "titulo": "Dia 8",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: primeiro a febre (motor/febre.py); depois, quem o jogador matou ontem.
            {"tipo": "se", "morto_ontem": "Yara", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Yara amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Mbaé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Potira", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Potira amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Tamandaré-mirim", "passos": [
                {"tipo": "fala", "quem": "",
                 "texto": "O corpo de Tamandaré-mirim amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Iandé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Iandé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "na_oca": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "Mbaé tossiu a noite toda na oca Yebá Bëló."},
            ]},

            {"tipo": "aldeia"},

            # A chegada de Krenan, de canoa, rio abaixo.
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "visitante", "visitante": "krenan"},
            {"tipo": "fala", "quem": "Krenan",
             "texto": "Não vim a pedir pousada. Venho a dar-vos aviso, e há de ser ao pé do fogo."},
            {"tipo": "escolha", "opcoes": [
                {"texto": "Chamar para a fogueira", "convida": "Krenan", "passos": [
                    {"tipo": "fala", "quem": "Krenan", "texto": "Pois lá vos aguardarei, quando a luz se for."},
                ]},
                {"texto": "Não deixar entrar", "passos": [
                    {"tipo": "fala", "quem": "Krenan",
                     "texto": "Guardai, pois, a vossa porta. O rio não carece de vós, nem vós dele, ao que parece."},
                ]},
            ]},
            {"tipo": "visitante", "visitante": None},

            # O pajé não conta sinal novo.
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com a minha própria mãe na porta. Não soube o que fazer."},

            {"tipo": "noite"},
        ],
    },

    # --- Dia 9: a última vez que ele vem (Textos/Caraíba — Dez Dias, Dez Fogueiras.pdf) ---
    # A terceira e última visita do Irmão Aleixo. Ele diz tudo o que ainda não tinha dito,
    # e o cordão no pescoço dele é o de Iandé. O pedido é o mesmo: entregar alguém ou negar.
    # De noite, o pajé conta o 5º sinal: manchas brancas no pescoço.
    9: {
        "titulo": "Dia 9",
        "passos": [
            {"tipo": "fundo", "fundo": "aldeia", "filtro": "dia"},

            # A manhã: primeiro a febre (motor/febre.py); depois, quem o jogador matou ontem.
            {"tipo": "se", "morto_ontem": "Yara", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Yara amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Mbaé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Potira", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Potira amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Tamandaré-mirim", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Tamandaré-mirim amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "morto_ontem": "Iandé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "O corpo de Iandé amanheceu coberto com uma esteira."},
            ]},
            {"tipo": "se", "na_oca": "Mbaé", "passos": [
                {"tipo": "fala", "quem": "", "texto": "Mbaé tossiu a noite toda na oca Yebá Bëló."},
            ]},

            {"tipo": "aldeia"},

            # A entrada: Aleixo, pela última vez.
            {"tipo": "fundo", "fundo": "floresta", "filtro": "dia"},
            {"tipo": "fala", "quem": "",
             "texto": "O Irmão Aleixo está ao lado da cruz, com o caderno aberto e a pena na mão."},
            {"tipo": "se", "levou_alguem": True, "passos": [
                {"tipo": "fala", "quem": "", "texto": "Ele veio sozinho de novo."},
            ]},
            {"tipo": "visitante", "visitante": "aleixo"},
            {"tipo": "fala", "quem": ALEIXO, "texto": "Esta é a última vez que consigo ficar aqui."},
            {"tipo": "fala", "quem": ALEIXO, "texto": "Depois disso, não depende mais de mim."},
            {"tipo": "perguntas", "botao": "Seguir",
             "perguntas": PERGUNTAS_ALEIXO[9] + perguntas_sobre_os_levados()},

            # O pedido, como nas outras visitas: entregar alguém ou negar.
            oferta_aleixo(9),
            {"tipo": "fala", "quem": ALEIXO, "texto": "Que Deus guarde esta aldeia. Eu não posso mais."},
            {"tipo": "visitante", "visitante": None},
            {"tipo": "fala", "quem": "", "texto": "A cruz fica na entrada."},

            # O sinal do pajé: o 5º risco da tábua.
            {"tipo": "fundo", "fundo": "fogueira_longe", "filtro": "noite"},
            {"tipo": "visitante", "visitante": "paje"},
            {"tipo": "fala", "quem": "Pajé",
             "texto": "Sonhei com um pescoço marcado. O mal deixa [manchas brancas no pescoço]."},
            {"tipo": "sinal", "texto": "Manchas brancas no pescoço."},

            {"tipo": "noite"},
        ],
    },
}
