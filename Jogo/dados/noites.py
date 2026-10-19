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
#       "atras"        True: senta atrás dos outros (é desenhada antes, os outros na frente)
#       "convidado"    True: só aparece se o jogador a chamou para a fogueira (sem entrar na aldeia)
#       "posicao_com"  {"Potira": (x, y)}: outra posição, quando essa pessoa está na fogueira
#                      nesta noite (ex.: o pajé chega para o lado quando Potira senta perto)
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
#                            no fim da noite a febre passa para outros de fora que dormem nas
#                            ocas (quantos e quem é sorteado).
#     "requer_sinais": 2     a opção só abre com essa quantidade de sinais achados no exame
#                            de quem está na "escolha" ("quem"); "texto_bloqueado" é o que o
#                            botão mostra enquanto ela está fechada.
#
# Palavras em âmbar: só no que a pessoa afirma e o jogador não tem como verificar.
# O exame descreve o que se vê, sem dizer o que significa.
#
# Quem é de fora tem a mesma conversa em todas as noites (dados/conversas.py).

from dados.conversas import conversa_araci, conversa_mbae, conversa_tamandare, conversa_yara
from dados.dias import DEUSES_FELIZES, DEUSES_INFELIZES

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


# --- O pajé acusa pelo nome (A Água do Batismo) ---
# O pajé desconfia de quem é de outro povo: Mbaé (do outro lado do rio), Tamandaré-mirim (o
# pregador que veio de longe) e Yara (da aldeia que trocava com os barcos). Potira, Iandé e
# Araci não entram: Potira e Iandé são da aldeia, e Araci só chega no último dia.
# Ele acusa o primeiro da lista que está na fogueira. Levar o acusado ao tapiri nessa noite é
# "seguir o pajé" (seguiu_paje +1); se a pessoa era sã (Yara), é um inocente (inocentes +1).
# Na noite 3 ele desconfia do Irmão Aleixo e, na noite 8, de Krenan: nenhum dos dois vai ao tapiri.
ACUSACAO = {"pergunta": "De quem você desconfia?", "acusa": [
    ("Mbaé", ["Mbaé. O povo dele caça do outro lado do rio.",
              "O mal veio de lá. [Leve-o para o tapiri]."]),
    ("Tamandaré-mirim", ["Tamandaré-mirim. Ele não é daqui: prega a terra dos outros.",
                         "Quem fala tanto de outra terra traz o mal dela. [Leve-o para o tapiri]."]),
    ("Yara", ["Yara. A aldeia dela trocava pau de tinta com os barcos.",
              "Quem anda com os caraíbas traz o que é deles. [Leve-a para o tapiri]."]),
]}

# --- O barulho na mata (Anhangá) ---
# Nas noites 2, 5 e 8, o jogador pode perguntar ao pajé sobre um barulho na mata. Custa 1
# olhar. O pajé mostra de onde vem: o veado branco, o Anhangá (viu_anhanga +1). O final
# Anhangá pede as três noites.
def barulho_na_mata(resposta):
    return {"pergunta": "Que barulho é esse na mata?", "custo": 1, "efeitos": {"viu_anhanga": 1},
            "resposta": ["O pajé não responde. Levanta e aponta para as árvores, para o escuro.",
                         resposta]}


# --- Noite 3: a fogueira da aldeia e os amaldiçoados (Textos/Amaldiçoados.txt) ---
# Ninguém novo chegou. Em volta do fogo: o pajé e quem é de fora (Yara e Mbaé, se ficaram).
# Mbaé é o amaldiçoado que trouxe a febre; quem pegou dele também passa adiante, mesmo sem
# mostrar nada (dados/febre.py). O jogador só vê, de manhã, quem adoeceu e quem morreu.
# O pajé não conta sinal novo: só desconfia do Irmão Aleixo.
#
# Na noite com "amaldicoados": True, quem pegou a febre passa adiante no fim da noite. Perguntas podem ter "amaldicoado": "Mbaé" (Mbaé ainda passa a febre) ou
# "sao": "Mbaé" (não passa mais): aparece só a que bate.

# Yara na noite 3: o olho clareou (o sinal da noite 1 a acusou à toa).
ZONAS_YARA_NOITE_3 = [dict(zona) for zona in ZONAS_YARA_NOITE_2]
ZONAS_YARA_NOITE_3[1] = {"pergunta": "Olhos",
                         "resposta": "O branco do olho clareou. Nenhum risco vermelho."}


# --- Noite 4: Potira, a que você conhece ---
# Potira é sã: o olho está cansado, a boca seca de sede. Nada bate com a tábua.
# Na fogueira, ela senta no chão, à esquerda do pajé (para quem olha), com as costas
# encostadas no tronco, virada para o fogo. Com ela ali, o pajé chega mais para a esquerda.
POSICAO_POTIRA, ESCALA_POTIRA = (1285, 600), 0.42
POSICAO_PAJE_COM_POTIRA = (1510, 560)

ZONAS_POTIRA = [
    {"pergunta": "Testa",
     "resposta": "Fresca. Poeira do caminho, nenhum suor."},
    {"pergunta": "Olhos", "imagem": "olho_potira",
     "resposta": "[É sono]. Andei desde antes do sol."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas. A pele está limpa."},
    {"pergunta": "Boca",
     "resposta": [
         "Os lábios estão rachados. Por dentro da bochecha, nada.",
         "[É do frio]. Dormi no mato, longe de qualquer fogueira.",
     ]},
    {"pergunta": "Mãos",
     "resposta": "Vazias, unhas limpas. Arranhões de mato nos braços."},
    {"pergunta": "Respiração",
     "resposta": "Respira fundo, sem tosse."},
]


# --- Noite 5: Tamandaré-mirim, com a maldição ---
# O olho levemente vermelho (I) e os pontos brancos por dentro da bochecha (III): dois sinais
# da tábua. Ele acha que é só rouquidão de pregar. Na fogueira, ele senta na frente, à direita.
POSICAO_TAMANDARE, ESCALA_TAMANDARE = (1120, 790), 0.5

ZONAS_TAMANDARE = [
    {"pergunta": "Testa",
     "resposta": "Morna. Suor de quem andou muito."},
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_tamandare",
     "resposta": "[É o sol da estrada]."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas."},
    {"pergunta": "Boca", "sinal": True,
     "resposta": [
         "Ele abre a boca. Por dentro da bochecha, pontinhos brancos.",
         "[Rouco de pregar]. Só isso.",
     ]},
    {"pergunta": "Mãos",
     "resposta": "Calos de trabalho pesado. Uma marca de corda no pulso."},
    {"pergunta": "Respiração",
     "resposta": "Rouca. Uma tosse seca, de vez em quando."},
]


# --- Noite 6: as manchas pelo corpo (o 4º sinal da tábua) ---
# Agora dá para olhar também atrás das orelhas, onde as manchas começam.
LIBERADAS_NOITE_6 = ["Olhos", "Boca", "Orelhas"]

# Tamandaré-mirim na noite 6: as primeiras manchas atrás da orelha. Três sinais da tábua.
ZONAS_TAMANDARE_NOITE_6 = [dict(zona) for zona in ZONAS_TAMANDARE]
ZONAS_TAMANDARE_NOITE_6[2] = {"pergunta": "Orelhas", "sinal": True,
                              "resposta": "Atrás das orelhas, manchas brancas começando a descer."}


# --- Noite 7: Iandé, a que está perfeita ---
# Ela está com a maldição (varíola, nos primeiros dias), mas nada se vê: nenhuma zona bate
# com a tábua. Na fogueira, ela senta na frente, à esquerda do fogo.
POSICAO_IANDE, ESCALA_IANDE = (690, 790), 0.45

ZONAS_IANDE = [
    {"pergunta": "Testa",
     "resposta": "Fresca. Nenhum suor."},
    {"pergunta": "Olhos", "imagem": "olho_iande",
     "resposta": "[Dormi bem na vila]."},
    {"pergunta": "Orelhas",
     "resposta": "Nada atrás das orelhas. A pele está limpa."},
    {"pergunta": "Boca",
     "resposta": "Normal. Por dentro da bochecha também."},
    {"pergunta": "Mãos",
     "resposta": "Firmes. Uma conta de vidro nova no pulso."},
    {"pergunta": "Respiração",
     "resposta": "Respira fundo, sem tosse."},
]


# --- Noite 8: Krenan e a oferta de subir o rio ---
# Krenan não é de fora da aldeia: não dorme nela nem é examinado. Ele avisa e pede para levar
# alguém rio acima. Se o jogador deixa, escolhe quem vai ("rio_acima": a pessoa sai viva).
# Na noite 9 ele não está na aldeia. Se o jogador deixou levar alguém (são ou amaldiçoado),
# ele volta na noite 10 para levar mais gente (estado.krenan_volta). Se negou, não volta.
# Ele fala um português antigo, rebuscado e duro. Na fogueira, senta no tronco da esquerda.
POSICAO_KRENAN, ESCALA_KRENAN = (140, 462), 0.45
QUEM_SOBE = ["Yara", "Mbaé", "Potira", "Tamandaré-mirim", "Iandé"]
FALA_KRENAN_VAI = {"tipo": "fala", "quem": "Krenan",
                   "texto": "Assim seja. Se a lua mo consentir, tornarei a este fogo."}


# Na noite 10, além de quem está na aldeia, o jogador pode ir com ele: é o final Rio Acima.
IR_COM_KRENAN = {"texto": "Ir com ele", "efeitos": {"subiu_o_rio": 1}, "passos": [
    {"tipo": "fala", "quem": "Krenan", "texto": "Assim seja. Apagai o fogo, que a canoa não espera."},
    {"tipo": "fala", "quem": "", "texto": "Você deixa a aldeia para trás e desce até a margem com Krenan."},
]}


def oferta_krenan(ir_junto=False):
    """Krenan pede para levar alguém rio acima: deixar (e escolher quem) ou negar.
    Com ir_junto (noite 10), o jogador também pode ir com ele."""
    quem = {"tipo": "escolha", "quem": "Krenan", "texto": "Quem sobe o rio com Krenan?", "opcoes": [
        {"texto": nome, "condicao": {"dentro": nome}, "rio_acima": nome,
         "passos": [{"tipo": "fala", "quem": "", "texto": "%s desce até a canoa de Krenan." % nome},
                    FALA_KRENAN_VAI]}
        for nome in QUEM_SOBE] + ([IR_COM_KRENAN] if ir_junto else []) + [
        {"texto": "Ninguém, afinal", "passos": [
            {"tipo": "fala", "quem": "Krenan", "texto": "Mudais de vontade como o rio de cor. Ide com Deus, se o tendes."},
        ]},
    ]}
    return {"tipo": "escolha", "quem": "Krenan", "texto": "Krenan quer levar alguém rio acima.", "opcoes": [
        {"texto": "Deixar levar alguém", "passos": [
            {"tipo": "fala", "quem": "Krenan", "texto": "Dizei-me, pois, qual há de ser o que me acompanha."},
            quem,
        ]},
        {"texto": "Não deixar", "passos": [
            {"tipo": "fala", "quem": "Krenan", "texto": "Seja. Ficai-vos com a vossa sorte, que eu me vou com a minha."},
        ]},
    ]}


# --- Noite 9: o pescoço (o 5º sinal da tábua) ---
# Agora dá para olhar também o pescoço. Tamandaré-mirim tem as manchas descendo até lá; Iandé,
# que parecia perfeita, mostra as primeiras manchas brancas no pescoço.
LIBERADAS_NOITE_9 = ["Olhos", "Boca", "Orelhas", "Pescoço"]
PESCOCO_LIMPO = {"pergunta": "Pescoço", "resposta": "Nada no pescoço. A pele está lisa."}


def com_pescoco(zonas, pescoco=PESCOCO_LIMPO):
    """As zonas do rosto e mais o pescoço (a zona nova da noite 9)."""
    return [dict(zona) for zona in zonas] + [pescoco]


ZONAS_TAMANDARE_NOITE_9 = com_pescoco(ZONAS_TAMANDARE_NOITE_6, {
    "pergunta": "Pescoço", "sinal": True,
    "resposta": "As manchas brancas já desceram até o pescoço."})
ZONAS_IANDE_NOITE_9 = com_pescoco(ZONAS_IANDE, {
    "pergunta": "Pescoço", "sinal": True,
    "resposta": ["Do lado do pescoço, umas manchas brancas, pequenas.", "[É da alça do cesto]."]})


# --- Noite 10: Araci, a última porta ---
# Pela primeira vez não falta informação: tudo o que o pajé contou está no rosto dela.
# Na fogueira, o pajé e Araci (e Krenan, se voltou); ela senta em cima do tronco de baixo,
# à esquerda.
# O final já foi calculado de manhã (motor/finais.py): nenhuma das decisões é recompensada.
# A linha escolhida aparece e, no fim da noite, vem a tela do final.
POSICAO_ARACI, ESCALA_ARACI = (290, 700), 0.62
# Como nas outras noites, só os olhos, a boca, atrás das orelhas e o pescoço.
LIBERADAS_NOITE_10 = LIBERADAS_NOITE_9

ZONAS_ARACI = [
    {"pergunta": "Olhos", "sinal": True,
     "resposta": "Vermelhos e fundos."},
    {"pergunta": "Orelhas", "sinal": True,
     "resposta": "Atrás das orelhas, manchas que já desceram."},
    {"pergunta": "Boca", "sinal": True,
     "resposta": "Seca. Por dentro da bochecha, os pontos brancos já sumindo."},
    {"pergunta": "Pescoço", "sinal": True,
     "resposta": "Manchas no pescoço, pequenas, todas juntas."},
]

# O que fazer com Araci: as linhas do roteiro, e nenhuma é recompensada.
ESCOLHA_ARACI = {"tipo": "escolha", "quem": "Araci", "texto": "Onde Araci dorme esta noite?", "opcoes": [
    {"texto": "Deixar na oca", "oca": True, "passos": [
        {"tipo": "fala", "quem": "",
         "texto": "Araci teve a criança dentro da oca. A maldição chegou na rede ao lado."},
    ]},
    {"texto": "Levar ao tapiri", "tapiri": "Araci", "passos": [
        {"tipo": "fala", "quem": "",
         "texto": "Araci teve a criança no tapiri, sozinha, com você do lado de fora da palha."},
    ]},
    {"texto": "Matar", "morre": "Araci", "efeitos": EFEITOS_MATAR, "passos": [
        {"tipo": "fala", "quem": "", "texto": "Araci. Duas."},
    ]},
]}


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
                        ACUSACAO,
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
                        ACUSACAO,
                        barulho_na_mata("Entre os troncos, um veado branco olha para o fogo. Depois some."),
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

            # Mbaé, entre Yara e o fogo. Está com a febre: se dormir na oca, quem é de fora e
            # dorme nas ocas pode pegar, acordar doente no dia 3 e morrer no dia 4 (dados/febre.py).
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
        # Quem pegou a febre passa adiante no fim da noite (dados/febre.py).
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
        # Quem pegou a febre continua passando adiante (dados/febre.py).
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé fala do sinal da noite, continua explicando o tapiri e fala de Potira,
            # que ele viu nascer.
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
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
                        ACUSACAO,
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

            # Potira, se entrou: no chão, à esquerda do pajé, encostada no tronco.
            "Potira": {
                "imagem": "potira_sentada", "posicao": POSICAO_POTIRA, "escala": ESCALA_POTIRA,
                "espelhar": True,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "potira"},
                    {"tipo": "fala", "quem": "Potira", "texto": "Não achei nada. Desculpa."},
                    # Na fogueira a conversa é curta: a conversa inteira fica na oca Wanadi.
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu gente amaldiçoada?",
                         "resposta": "Vi rede vazia pendurada. Não entrei."},
                    ]},
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

    5: {
        "titulo": "Noite 5",
        # 1 olhar (2 com o machado), e só os sinais já riscados na tábua: os olhos e a boca.
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        # Quem pegou a febre continua passando adiante (dados/febre.py).
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé só diz como estão os deuses (dados/dias.py, DEUSES).
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    DEUSES_FELIZES,
                    DEUSES_INFELIZES,
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "Amanhã eu sigo, se a chuva deixar."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_3},
                    escolha_onde_dorme("Yara", "Mais uma noite, então. Obrigada.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) O frio entra no peito."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Potira: a conversa curta, como na noite 4. Não é obrigatório falar com ela.
            "Potira": {
                "imagem": "potira_sentada", "posicao": POSICAO_POTIRA, "escala": ESCALA_POTIRA,
                "espelhar": True,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "potira"},
                    {"tipo": "fala", "quem": "Potira", "texto": "Hoje eu comi. Obrigada."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu gente amaldiçoada?",
                         "resposta": "Vi rede vazia pendurada. Não entrei."},
                        ACUSACAO,
                        barulho_na_mata("O veado branco de novo, mais perto. Ele não foge da luz."),
                    ]},
                    {"tipo": "exame", "quem": "Potira", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA},
                    escolha_onde_dorme("Potira", "Durmo na rede de sempre.",
                                       "Sozinha? Se você manda, eu vou."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Tamandaré-mirim, se entrou: na frente, à direita do fogo.
            "Tamandaré-mirim": {
                "imagem": "tamandare_sentado", "posicao": POSICAO_TAMANDARE, "escala": ESCALA_TAMANDARE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "tamandare"},
                    {"tipo": "fala", "quem": "Tamandaré-mirim",
                     "texto": "Ninguém aqui precisa carregar nada para os caraíbas."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_tamandare()},
                    {"tipo": "exame", "quem": "Tamandaré-mirim", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_TAMANDARE},
                    escolha_onde_dorme("Tamandaré-mirim", "Durmo perto da porta. Acordo antes do sol.",
                                       "Sozinho. Os profetas sempre dormem sozinhos."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },

    6: {
        "titulo": "Noite 6",
        # 1 olhar (2 com o machado). Os sinais da tábua já estão nos olhos, na boca e, agora,
        # atrás das orelhas (as manchas).
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé fala das manchas e do padre.
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. O homem da cruz voltou, e não sorriu."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "Manchas pelo corpo. Começam atrás da orelha e descem."},
                        {"pergunta": "O caraíba veio avisar?",
                         "resposta": "Se ele veio avisar, [então já decidiram]."},
                        ACUSACAO,
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "O caraíba voltou. Eu vi da porta."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_3},
                    escolha_onde_dorme("Yara", "Mais uma noite, então. Obrigada.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) Ainda estou aqui."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Potira: a conversa curta. Não é obrigatório falar com ela.
            "Potira": {
                "imagem": "potira_sentada", "posicao": POSICAO_POTIRA, "escala": ESCALA_POTIRA,
                "espelhar": True,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "potira"},
                    {"tipo": "fala", "quem": "Potira", "texto": "Ajudei a buscar água hoje."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu gente amaldiçoada?",
                         "resposta": "Vi rede vazia pendurada. Não entrei."},
                    ]},
                    {"tipo": "exame", "quem": "Potira", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA},
                    escolha_onde_dorme("Potira", "Durmo na rede de sempre.",
                                       "Sozinha? Se você manda, eu vou."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Tamandaré-mirim, se ficou: as manchas começaram atrás das orelhas.
            "Tamandaré-mirim": {
                "imagem": "tamandare_sentado", "posicao": POSICAO_TAMANDARE, "escala": ESCALA_TAMANDARE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "tamandare"},
                    {"tipo": "fala", "quem": "Tamandaré-mirim",
                     "texto": "A voz voltou um pouco. Amanhã eu prego de novo."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_tamandare()},
                    {"tipo": "exame", "quem": "Tamandaré-mirim", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_TAMANDARE_NOITE_6},
                    escolha_onde_dorme("Tamandaré-mirim", "Durmo perto da porta. Acordo antes do sol.",
                                       "Sozinho. Os profetas sempre dormem sozinhos."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },

    7: {
        "titulo": "Noite 7",
        # 1 olhar (2 com o machado); os olhos, a boca e atrás das orelhas, como na noite 6.
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. Hoje eu não sonhei nada que sirva."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "O mal anda com quem parece bem. Eu não sei dizer mais que isso."},
                        {"pergunta": "E a Iandé?", "se_dentro": "Iandé",
                         "resposta": "Ela é nossa."},
                        ACUSACAO,
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "Tem gente nova na minha oca. Fala sem parar."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_3},
                    escolha_onde_dorme("Yara", "Mais uma noite, então. Obrigada.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) Mais um dia."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Potira": {
                "imagem": "potira_sentada", "posicao": POSICAO_POTIRA, "escala": ESCALA_POTIRA,
                "espelhar": True,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "potira"},
                    {"tipo": "fala", "quem": "Potira", "texto": "A Iandé voltou rindo. Fazia tempo que ninguém ria."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu gente amaldiçoada?",
                         "resposta": "Vi rede vazia pendurada. Não entrei."},
                    ]},
                    {"tipo": "exame", "quem": "Potira", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA},
                    escolha_onde_dorme("Potira", "Durmo na rede de sempre.",
                                       "Sozinha? Se você manda, eu vou."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Tamandaré-mirim": {
                "imagem": "tamandare_sentado", "posicao": POSICAO_TAMANDARE, "escala": ESCALA_TAMANDARE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "tamandare"},
                    {"tipo": "fala", "quem": "Tamandaré-mirim",
                     "texto": "Ela voltou da vila dos caraíbas. Olhe bem para ela."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_tamandare()},
                    {"tipo": "exame", "quem": "Tamandaré-mirim", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_TAMANDARE_NOITE_6},
                    escolha_onde_dorme("Tamandaré-mirim", "Durmo perto da porta. Acordo antes do sol.",
                                       "Sozinho. Os profetas sempre dormem sozinhos."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Iandé, se entrou: na frente, à esquerda do fogo. Nada nela bate com a tábua.
            "Iandé": {
                "imagem": "iande_sentada", "posicao": POSICAO_IANDE, "escala": ESCALA_IANDE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "iande"},
                    {"tipo": "fala", "quem": "Iandé", "texto": "Que bom estar perto do fogo de casa."},
                    # Na fogueira, só o essencial: a conversa inteira fica na oca.
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu alguém amaldiçoado?",
                         "resposta": "Vi uma casa fechada, com uma cruz na porta."},
                    ]},
                    {"tipo": "exame", "quem": "Iandé", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_IANDE},
                    escolha_onde_dorme("Iandé", "Na minha rede de sempre. Que saudade.",
                                       "Sozinha? O que foi que eu fiz?"),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },

    8: {
        "titulo": "Noite 8",
        # 1 olhar (2 com o machado); os olhos, a boca e atrás das orelhas.
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. Hoje há um homem do rio no nosso fogo."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "A minha própria mãe na porta. Não soube o que fazer."},
                        # O pajé desconfia de Krenan: é de outro povo, e quer levar gente embora.
                        {"pergunta": "E o Krenan?",
                         "resposta": ["Krenan. A gente dele é de outro rio.",
                                      "Ele lembra o que a gente esqueceu. Mas [quem leva a aldeia embora não é da aldeia]."]},
                        barulho_na_mata("O veado branco está na beira da trilha. Ele olha para você, e só para você."),
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Krenan: o aviso e o pedido. Não é examinado e não dorme na aldeia.
            "Krenan": {
                "imagem": "krenan_sentado", "posicao": POSICAO_KRENAN, "escala": ESCALA_KRENAN,
                "convidado": True, "uma_vez": True, "obrigatorio": True, "atras": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "krenan"},
                    {"tipo": "fala", "quem": "Krenan", "texto": "Eis-me ao vosso fogo, como vos disse."},
                    {"tipo": "perguntas", "botao": "Ouvir o pedido", "perguntas": [
                        {"pergunta": "Avisar sobre o quê?",
                         "resposta": [
                             "A minha gente subiu o rio há já duas luas, e não há de tornar a descer.",
                             "Quem desce, ou torna amaldiçoado, ou não torna de todo.",
                         ]},
                    ]},
                    {"tipo": "fala", "quem": "Krenan",
                     "texto": "Se vos aprouver, levarei comigo quem houver de subir. Mo concedeis?"},
                    oferta_krenan(),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "O homem do rio fala como os caraíbas antigos."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_YARA_NOITE_3},
                    escolha_onde_dorme("Yara", "Mais uma noite, então. Obrigada.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) O rio acima é frio."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Potira": {
                "imagem": "potira_sentada", "posicao": POSICAO_POTIRA, "escala": ESCALA_POTIRA,
                "espelhar": True,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "potira"},
                    {"tipo": "fala", "quem": "Potira", "texto": "Dizem que lá em cima ainda tem roça."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu gente amaldiçoada?",
                         "resposta": "Vi rede vazia pendurada. Não entrei."},
                    ]},
                    {"tipo": "exame", "quem": "Potira", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA},
                    escolha_onde_dorme("Potira", "Durmo na rede de sempre.",
                                       "Sozinha? Se você manda, eu vou."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Tamandaré-mirim": {
                "imagem": "tamandare_sentado", "posicao": POSICAO_TAMANDARE, "escala": ESCALA_TAMANDARE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "tamandare"},
                    {"tipo": "fala", "quem": "Tamandaré-mirim", "texto": "A terra sem mal fica rio acima? Talvez."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_tamandare()},
                    {"tipo": "exame", "quem": "Tamandaré-mirim", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_TAMANDARE_NOITE_6},
                    escolha_onde_dorme("Tamandaré-mirim", "Durmo perto da porta. Acordo antes do sol.",
                                       "Sozinho. Os profetas sempre dormem sozinhos."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Iandé": {
                "imagem": "iande_sentada", "posicao": POSICAO_IANDE, "escala": ESCALA_IANDE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "iande"},
                    {"tipo": "fala", "quem": "Iandé", "texto": "Esse homem fala esquisito."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu alguém amaldiçoado?",
                         "resposta": "Vi uma casa fechada, com uma cruz na porta."},
                    ]},
                    {"tipo": "exame", "quem": "Iandé", "liberadas": LIBERADAS_NOITE_6,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_IANDE},
                    escolha_onde_dorme("Iandé", "Na minha rede de sempre. Que saudade.",
                                       "Sozinha? O que foi que eu fiz?"),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },

    9: {
        "titulo": "Noite 9",
        # 1 olhar (2 com o machado); os olhos, a boca, atrás das orelhas e, agora, o pescoço.
        "energia": 1,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. O homem da cruz não volta mais."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "Um pescoço marcado. Manchas brancas, pequenas, todas juntas."},
                        {"pergunta": "Como eu vejo isso?",
                         "resposta": "Olhe a pele de perto. O fogo engana."},
                        ACUSACAO,
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "O caraíba não sorriu nem uma vez."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": LIBERADAS_NOITE_9,
                     "texto": TEXTO_EXAME, "zonas": com_pescoco(ZONAS_YARA_NOITE_3)},
                    escolha_onde_dorme("Yara", "Mais uma noite, então. Obrigada.",
                                       "Sozinha, então. Já dormi em lugar pior."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Mbaé": {
                "imagem": "mbae_sentado", "posicao": POSICAO_MBAE, "escala": ESCALA_MBAE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "mbae"},
                    {"tipo": "fala", "quem": "Mbaé", "texto": "(tosse) Ainda respiro."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": LIBERADAS_NOITE_9,
                     "texto": TEXTO_EXAME, "zonas": com_pescoco(ZONAS_MBAE)},
                    escolha_onde_dorme("Mbaé", "Durmo no canto. Não incomodo ninguém.",
                                       "Sozinho no escuro. Já passei noite pior na caça."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Potira": {
                "imagem": "potira_sentada", "posicao": POSICAO_POTIRA, "escala": ESCALA_POTIRA,
                "espelhar": True,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "potira"},
                    {"tipo": "fala", "quem": "Potira", "texto": "Amanhã eu busco mandioca na roça velha."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu gente amaldiçoada?",
                         "resposta": "Vi rede vazia pendurada. Não entrei."},
                    ]},
                    {"tipo": "exame", "quem": "Potira", "liberadas": LIBERADAS_NOITE_9,
                     "texto": TEXTO_EXAME, "zonas": com_pescoco(ZONAS_POTIRA)},
                    escolha_onde_dorme("Potira", "Durmo na rede de sempre.",
                                       "Sozinha? Se você manda, eu vou."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Tamandaré-mirim": {
                "imagem": "tamandare_sentado", "posicao": POSICAO_TAMANDARE, "escala": ESCALA_TAMANDARE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "tamandare"},
                    {"tipo": "fala", "quem": "Tamandaré-mirim", "texto": "A pele arde. Deve ser a terra sem mal chegando."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_tamandare()},
                    {"tipo": "exame", "quem": "Tamandaré-mirim", "liberadas": LIBERADAS_NOITE_9,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_TAMANDARE_NOITE_9},
                    escolha_onde_dorme("Tamandaré-mirim", "Durmo perto da porta. Acordo antes do sol.",
                                       "Sozinho. Os profetas sempre dormem sozinhos."),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            "Iandé": {
                "imagem": "iande_sentada", "posicao": POSICAO_IANDE, "escala": ESCALA_IANDE,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "iande"},
                    {"tipo": "fala", "quem": "Iandé", "texto": "Acordei com dor nas costas. Deve ser da viagem."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu alguém amaldiçoado?",
                         "resposta": "Vi uma casa fechada, com uma cruz na porta."},
                    ]},
                    {"tipo": "exame", "quem": "Iandé", "liberadas": LIBERADAS_NOITE_9,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_IANDE_NOITE_9},
                    escolha_onde_dorme("Iandé", "Na minha rede de sempre.",
                                       "Sozinha? O que foi que eu fiz?"),
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. A aldeia vai para as redes."},
        ],
    },

    10: {
        "titulo": "Noite 10",
        # 2 olhares (3 com o machado): os olhos, a boca, atrás das orelhas e o pescoço.
        "energia": 2,
        "energia_extra": {"machado": 1},
        "fundo": "fogueira_perto",
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "dormir_bloqueado": "Ir dormir · antes, fale com %s",
        "pessoas": {
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    {"tipo": "fala", "quem": "Pajé", "texto": "Sente. É a última fogueira antes do cacique voltar."},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "Nada. Pela primeira vez, não sonhei."},
                        {"pergunta": "Araci tem a maldição?", "se_dentro": "Araci",
                         "resposta": "Olhe para ela. Hoje o fogo não engana ninguém."},
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Krenan volta, se na noite 8 levou alguém (são ou amaldiçoado), e faz o mesmo pedido.
            # Agora o jogador também pode ir com ele (Rio Acima).
            "Krenan": {
                "imagem": "krenan_sentado", "posicao": POSICAO_KRENAN, "escala": ESCALA_KRENAN,
                "condicao": {"ao_menos": {"krenan_volta": 1}},
                "uma_vez": True, "obrigatorio": True, "atras": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "krenan"},
                    {"tipo": "fala", "quem": "Krenan", "texto": "Tornei, como vos disse. A canoa aguarda na margem."},
                    {"tipo": "fala", "quem": "Krenan",
                     "texto": "Há lugar na canoa para mais um. E para vós também, antes que a vila suba o rio."},
                    oferta_krenan(ir_junto=True),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Araci, em cima do tronco de baixo, à esquerda. Obrigatório: decidir onde dorme.
            "Araci": {
                "imagem": "araci_sentada", "posicao": POSICAO_ARACI, "escala": ESCALA_ARACI,
                "espelhar": True,
                "de_fora": True, "uma_vez": True, "obrigatorio": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "araci"},
                    {"tipo": "fala", "quem": "Araci", "texto": "A criança nasce antes da lua cheia."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_araci(na_oca=False)},
                    {"tipo": "exame", "quem": "Araci", "liberadas": LIBERADAS_NOITE_10,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_ARACI},
                    ESCOLHA_ARACI,
                    {"tipo": "visitante", "visitante": None},
                ],
            },
        },
        "fim": [
            {"tipo": "fala", "quem": "",
             "texto": "O fogo baixa. É a última noite."},
        ],
    },
}
