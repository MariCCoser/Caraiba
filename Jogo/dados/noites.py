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
#              o machado de Yara; {"pulseira": 1} = +1 para quem aceitou a pulseira de Iandé;
#              {"mandioca": 1} = +1 para quem comeu a mandioca de Potira (noites 4 a 10)
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
#               detalhe de perto (o olho ou a boca), em vez de descrever: a "resposta" fica só
#               com o que a pessoa diz. A mesma zona pode vir duas vezes, com condições opostas
#               (ex.: "sem_febre"/"com_febre", "noites_na_oca_menos_de"/"noites_na_oca_ao_menos",
#               cenas/dia.py): aparece só a que bate. Cada zona gasta 1 de energia (ou o "custo" dela, se
#               tiver). Zona que custa mais do que sobrou fica apagada. Diga de quem é o exame
#               com "quem". "liberadas": a lista das zonas que dá para olhar nessa noite (ex.:
#               só ["Olhos"] na noite 1). Sem ela, todas as zonas aparecem.
#               As zonas e os sinais seguem Textos/A_Maldicao_Caraiba.pdf.
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

# --- Quem é são pode pegar a febre na oca (dados/febre.py) ---
# Quem pegou e mostra (acorda com febre no dia seguinte) tem, na noite em que ainda está viva, o
# olho e a boca doentes. Quem pegou sem mostrar segue com o rosto de sempre.
# As diferenças de cada um: Textos/Caraiba_Sinais_dos_Personagens.md.
# --- O tapiri cura (cenas/dia.py, _liberar_tapiri) ---
# Quem é amaldiçoado e completa as noites do tapiri sai curado (estado.curados): não passa mais
# a febre, e o rosto e a fala mostram isso. "curado"/"nao_curado" levam o nome (cenas/dia.py).
def fala_ou_curado(quem, texto, texto_curado):
    """A fala de sempre e, se a pessoa já saiu curada do tapiri, a outra."""
    return [{"tipo": "se", "nao_curado": quem, "passos": [{"tipo": "fala", "quem": quem, "texto": texto}]},
            {"tipo": "se", "curado": quem, "passos": [{"tipo": "fala", "quem": quem, "texto": texto_curado}]}]


def pode_se_curar(zonas, quem, curado):
    """Como pode_pegar_febre, ao contrário: cada zona de `curado` ganha a versão de quem saiu
    curado do tapiri (sem sinal), logo depois da de sempre. Zona que já vem em duas versões (o
    olho que piora com as noites na oca) ganha uma versão curada só."""
    novas, feitas = [], set()
    for zona in zonas:
        if zona["pergunta"] not in curado:
            novas.append(dict(zona))
            continue
        novas.append(dict(zona, nao_curado=quem))
        if zona["pergunta"] not in feitas:
            feitas.add(zona["pergunta"])
            novas.append(dict(curado[zona["pergunta"]], pergunta=zona["pergunta"], curado=quem))
    return novas


def pode_pegar_febre(zonas, quem, doente):
    """As zonas de quem é são, e, para cada zona de `doente` ({"Olhos": zona, ...}), a versão
    doente logo depois da sã: aparece só uma das duas ("sem_febre"/"com_febre", cenas/dia.py)."""
    novas = []
    for zona in zonas:
        if zona["pergunta"] in doente:
            novas.append(dict(zona, sem_febre=quem))
            novas.append(dict(doente[zona["pergunta"]], pergunta=zona["pergunta"], com_febre=quem))
        else:
            novas.append(dict(zona))
    return novas


# Yara está saudável: o olho vermelho é da fumaça (noites 1 e 2), a terra é do caminho.
ZONAS_YARA = [
    {"pergunta": "Testa",
     "resposta": "Fresca. Nenhum suor."},
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_yara_vermelho",
     "resposta": "[Dormi perto do fogo]."},
    {"pergunta": "Orelhas", "imagem": "orelha_pescoco_yara",
     "resposta": "Só poeira do caminho."},
    {"pergunta": "Boca", "imagem": "boca_yara",
     "resposta": "Pode olhar. Não tenho nada."},
    {"pergunta": "Mãos",
     "resposta": "Firmes. Terra seca debaixo das unhas e calos de carregar peso."},
    {"pergunta": "Respiração",
     "resposta": "Respira fundo e devagar, sem tosse."},
]

# Na noite 2 ainda é o mesmo olho (a arte do olho vermelho vale até a noite 3).
ZONAS_YARA_NOITE_2 = [dict(zona) for zona in ZONAS_YARA]
ZONAS_YARA_NOITE_2[1] = {"pergunta": "Olhos", "imagem": "olho_yara_vermelho",
                         "resposta": "Dormi perto do fogo. [Já está passando]."}
ZONAS_YARA_NOITE_2[3] = {"pergunta": "Boca", "imagem": "boca_yara",
                         "resposta": "Respiro fundo, viu? Nem uma tosse."}

# Mbaé está com a febre: suor, olho vermelho e, abrindo a boca, a tosse e as feridas na língua
# (o sinal que o pajé conta na noite 2).
# (Os pontinhos brancos na bochecha ficam para Tamandaré-mirim, na noite 5.)
# A pintura de jenipapo nunca é sinal de doença.
# O olho piora com a febre: depois de 3 noites dormindo na oca, aparece o olho doente.
NOITES_ATE_O_OLHO_PIORAR = 3
ZONAS_MBAE = [
    {"pergunta": "Testa", "sinal": True,
     "resposta": "Molhada de suor e quente, mesmo longe do fogo."},
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_mbae",
     "noites_na_oca_menos_de": {"Mbaé": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "(tosse) [É o vento do rio]."},
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_mbae_doente",
     "noites_na_oca_ao_menos": {"Mbaé": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "(tosse) [É o vento do rio]. De noite arde mais."},
    # Como o olho: as manchas atrás da orelha aparecem depois de 3 noites dormindo na oca.
    {"pergunta": "Orelhas", "imagem": "orelha_pescoco_mbae",
     "noites_na_oca_menos_de": {"Mbaé": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "Só a pintura de jenipapo."},
    {"pergunta": "Orelhas", "sinal": True, "imagem": "orelha_mbae_doente",
     "noites_na_oca_ao_menos": {"Mbaé": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "(tosse) [É a pintura de jenipapo descascando]."},
    {"pergunta": "Boca", "sinal": True, "imagem": "boca_mbae_doente",
     "resposta": "(tosse) [Mordi a língua comendo peixe]."},
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
# Nas noites 2, 5 e 9, o jogador pode perguntar ao pajé sobre um barulho na mata. Custa 1
# olhar. O pajé aponta, e a mata aparece na tela inteira (viu_anhanga +1). A imagem e a frase
# seguem a vez, não a noite: na 1ª vez, só o escuro (Arte/Ar_livre/Anhanga_um); na 2ª, uma
# sombra clara (Anhanga_dois); na 3ª, o veado branco (Anhanga_tres). O final Anhangá pede as
# três e fecha no fim da noite 9 (dados/finais.py).
# "por_vez" (cenas/dia.py): depois dos efeitos, a vez é o valor da variável; cada vez tem o
# "fundo" (dados/arte.py) e a "resposta" que aparece com ele.
ANHANGA_POR_VEZ = {"variavel": "viu_anhanga", "vezes": [
    {"fundo": "anhanga_um", "resposta": "Só o escuro entre os troncos. Mas alguma coisa olha de lá."},
    {"fundo": "anhanga_dois", "resposta": "Entre as folhas, uma sombra clara. Some quando você pisca."},
    {"fundo": "anhanga_tres",
     "resposta": "O veado branco está na beira da trilha. Ele olha para você, e só para você."},
]}


def barulho_na_mata():
    return {"pergunta": "Que barulho é esse na mata?", "custo": 1, "efeitos": {"viu_anhanga": 1},
            "resposta": "O pajé não responde. Levanta e aponta para as árvores, para o escuro.",
            "por_vez": ANHANGA_POR_VEZ}


# --- Noite 3: a fogueira da aldeia e os amaldiçoados (Textos/Amaldiçoados.txt) ---
# Ninguém novo chegou. Em volta do fogo: o pajé e quem é de fora (Yara e Mbaé, se ficaram).
# Mbaé é o amaldiçoado que trouxe a febre; quem pegou dele também passa adiante, mesmo sem
# mostrar nada (dados/febre.py). O jogador só vê, de manhã, quem adoeceu e quem morreu.
# O pajé não conta sinal novo: só desconfia do Irmão Aleixo.
#
# Na noite com "amaldicoados": True, quem pegou a febre passa adiante no fim da noite. Perguntas podem ter "amaldicoado": "Mbaé" (Mbaé ainda passa a febre) ou
# "sao": "Mbaé" (não passa mais): aparece só a que bate.

# Yara na noite 3: o olho clareou (o sinal da noite 1 a acusou à toa). Mas, se ela pegou a
# febre de Mbaé na oca e mostra, o olho segue vermelho e a boca fica ferida.
ZONAS_YARA_NOITE_3 = [dict(zona) for zona in ZONAS_YARA_NOITE_2]
ZONAS_YARA_NOITE_3[1] = {"pergunta": "Olhos", "imagem": "olho_yara",
                         "resposta": "Viu? [Era a fumaça]."}
ZONAS_YARA_NOITE_3 = pode_pegar_febre(ZONAS_YARA_NOITE_3, "Yara", {
    "Olhos": {"sinal": True, "imagem": "olho_yara_vermelho",
              "resposta": "(treme) [É frio], só isso."},
    "Orelhas": {"sinal": True, "imagem": "orelha_yara_doente",
                "resposta": "(treme) Coça. [É mordida de mosquito]."},
    "Boca": {"sinal": True, "imagem": "boca_yara_doente",
             "resposta": "(tosse) Dói para engolir."},
})


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
    {"pergunta": "Orelhas", "imagem": "orelha_pescoco_potira",
     "resposta": "Pode olhar. A pele está boa."},
    {"pergunta": "Boca", "imagem": "boca_potira",
     "resposta": [
         "Os lábios? Estão secos.",
         "[É do frio]. Dormi no mato, longe de qualquer fogueira.",
     ]},
    {"pergunta": "Mãos",
     "resposta": "Vazias, unhas limpas. Arranhões de mato nos braços."},
    {"pergunta": "Respiração",
     "resposta": "Respira fundo, sem tosse."},
]
# Da noite 5 em diante, Potira já dorme na aldeia: o cansaço e o frio não são mais do caminho.
ZONAS_POTIRA_DEPOIS = [dict(zona) for zona in ZONAS_POTIRA]
ZONAS_POTIRA_DEPOIS[1] = {"pergunta": "Olhos", "imagem": "olho_potira",
                          "resposta": "[É sono]. Desde que voltei, durmo pouco."}
ZONAS_POTIRA_DEPOIS[3] = {"pergunta": "Boca", "imagem": "boca_potira",
                          "resposta": ["Os lábios? Estão secos.", "[É do frio]. As noites esfriaram."]}
# Se Potira pegou a febre na oca e mostra: o olho vermelho e a boca ferida.
POTIRA_COM_FEBRE = {
    "Olhos": {"sinal": True, "imagem": "olho_potira_doente",
              "resposta": "(treme) [Dormi mal], só isso."},
    "Boca": {"sinal": True, "imagem": "boca_potira_doente",
             "resposta": "(tosse) Arde por dentro."},
    "Orelhas": {"sinal": True, "imagem": "orelha_potira_doente",
                "resposta": "(treme) Coça. [É do mato]."},
}
ZONAS_POTIRA = pode_pegar_febre(ZONAS_POTIRA, "Potira", POTIRA_COM_FEBRE)
ZONAS_POTIRA_DEPOIS = pode_pegar_febre(ZONAS_POTIRA_DEPOIS, "Potira", POTIRA_COM_FEBRE)


# --- Noite 5: Tamandaré-mirim, com a maldição ---
# O olho levemente vermelho (I) e os pontos brancos por dentro da bochecha (III): dois sinais
# da tábua. Ele acha que é só rouquidão de pregar. Na fogueira, ele senta na frente, à direita.
POSICAO_TAMANDARE, ESCALA_TAMANDARE = (1120, 790), 0.5

ZONAS_TAMANDARE = [
    {"pergunta": "Testa",
     "resposta": "Morna. Suor de quem andou muito."},
    # Como Mbaé, o olho piora depois de 3 noites dormindo na oca.
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_tamandare",
     "noites_na_oca_menos_de": {"Tamandaré-mirim": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "[É o sol da estrada]."},
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_tamandare_doente",
     "noites_na_oca_ao_menos": {"Tamandaré-mirim": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "[É o sol da estrada]. Agora arde."},
    {"pergunta": "Orelhas", "imagem": "orelha_pescoco_tamandare",
     "resposta": "Nada aí. [Só a poeira da estrada]."},
    {"pergunta": "Boca", "sinal": True, "imagem": "boca_tamandare_doente",
     "resposta": "[Rouco de pregar]. Só isso."},
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
ZONAS_TAMANDARE_NOITE_6[3] = {"pergunta": "Orelhas", "sinal": True, "imagem": "orelha_tamandare_doente",
                              "resposta": "[O sol da estrada queimou a pele]."}


# --- Noite 7: Iandé, a que está perfeita ---
# Ela está com a maldição (varíola, nos primeiros dias), mas nada se vê: nenhuma zona bate
# com a tábua. Na fogueira, ela senta na frente, à esquerda do fogo.
POSICAO_IANDE, ESCALA_IANDE = (690, 790), 0.45

ZONAS_IANDE = [
    {"pergunta": "Testa",
     "resposta": "Fresca. Nenhum suor."},
    {"pergunta": "Olhos", "imagem": "olho_iande",
     "resposta": "[Dormi bem na vila]."},
    {"pergunta": "Orelhas", "imagem": "orelha_pescoco_iande",
     "resposta": "Pode olhar. Está tudo bem."},
    {"pergunta": "Boca", "imagem": "boca_iande",
     "resposta": "Pode olhar. Está tudo bem."},
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
POSICAO_PADRE, ESCALA_PADRE = (165, 575), 0.62  # noite 9: ajoelhado, rezando, na frente do tronco de cima
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
# que parecia perfeita, mostra as primeiras manchas avermelhadas no pescoço.
LIBERADAS_NOITE_9 = ["Olhos", "Boca", "Orelhas", "Pescoço"]
PESCOCO_LIMPO = {"pergunta": "Pescoço", "resposta": "Nada no pescoço. A pele está lisa."}


def com_pescoco(zonas, pescoco=PESCOCO_LIMPO):
    """As zonas do rosto e mais o pescoço (a zona nova da noite 9). pescoco pode ser uma lista:
    a mesma zona em versões com condições opostas (ex.: sem e com febre)."""
    pescocos = pescoco if isinstance(pescoco, list) else [pescoco]
    return [dict(zona) for zona in zonas] + [dict(zona) for zona in pescocos]


# Yara: o pescoço limpo, ou com as manchas, se pegou a febre na oca e mostra.
PESCOCO_YARA = pode_pegar_febre([{"pergunta": "Pescoço", "imagem": "orelha_pescoco_yara",
                                  "resposta": "Pode olhar. Não tem nada."}], "Yara", {
    "Pescoço": {"sinal": True, "imagem": "pescoco_yara_doente", "resposta": "(tosse) [É do sol], só isso."},
})
# Potira: o pescoço limpo, ou com as manchas, se pegou a febre na oca e mostra.
PESCOCO_POTIRA = pode_pegar_febre([{"pergunta": "Pescoço", "imagem": "orelha_pescoco_potira",
                                    "resposta": "Nada aí. Pode olhar."}], "Potira", {
    "Pescoço": {"sinal": True, "imagem": "pescoco_potira_doente", "resposta": "(tosse) [É do sol da roça]."},
})
# Mbaé: o pescoço limpo até 3 noites na oca; depois, as manchas.
PESCOCO_MBAE = [
    {"pergunta": "Pescoço", "imagem": "orelha_pescoco_mbae",
     "noites_na_oca_menos_de": {"Mbaé": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "(tosse) Pode olhar."},
    {"pergunta": "Pescoço", "sinal": True, "imagem": "pescoco_mbae_doente",
     "noites_na_oca_ao_menos": {"Mbaé": NOITES_ATE_O_OLHO_PIORAR},
     "resposta": "(tosse) [Picada de formiga, na caça]."},
]


ZONAS_TAMANDARE_NOITE_9 = com_pescoco(ZONAS_TAMANDARE_NOITE_6, {
    "pergunta": "Pescoço", "sinal": True, "imagem": "pescoco_tamandare_doente",
    "resposta": "[A terra sem mal marca quem anda até ela]."})
# Atrás das orelhas, as manchas não estão mais "começando": já descem pelo pescoço.
ZONAS_TAMANDARE_NOITE_9[3] = {"pergunta": "Orelhas", "sinal": True, "imagem": "orelha_tamandare_doente",
                              "resposta": "Agora desce pelo pescoço. [Não dói]."}
# Na noite 8, Iandé já dormiu na aldeia (não mais na vila).
ZONAS_IANDE_NOITE_8 = [dict(zona) for zona in ZONAS_IANDE]
ZONAS_IANDE_NOITE_8[1] = {"pergunta": "Olhos", "imagem": "olho_iande",
                          "resposta": "[Dormi bem]. A rede daqui é macia."}
# Na noite 9 a maldição de Iandé aparece também no olho e na boca.
ZONAS_IANDE_NOITE_9 = [dict(zona) for zona in ZONAS_IANDE]
ZONAS_IANDE_NOITE_9[1] = {"pergunta": "Olhos", "sinal": True, "imagem": "olho_iande_doente",
                          "resposta": "Não dormi. [É a dor nas costas]."}
ZONAS_IANDE_NOITE_9[3] = {"pergunta": "Boca", "sinal": True, "imagem": "boca_iande_doente",
                          "resposta": "(tosse) [Comi farinha velha na vila]."}
ZONAS_IANDE_NOITE_9[2] = {"pergunta": "Orelhas", "sinal": True, "imagem": "orelha_iande_doente",
                          "resposta": "Coça um pouco. [É do cabelo sujo da viagem]."}
ZONAS_IANDE_NOITE_9 = com_pescoco(ZONAS_IANDE_NOITE_9, {
    "pergunta": "Pescoço", "sinal": True, "imagem": "pescoco_iande_doente",
    "resposta": "[É da alça do cesto]."})


# --- Noite 10: Araci, a última porta ---
# Pela primeira vez não falta informação: tudo o que o pajé contou está no rosto dela.
# Na fogueira, o pajé e Araci (e Krenan, se voltou); ela senta no chão, na frente, à direita,
# virada para o fogo (o lugar de Yara, à esquerda, fica com Yara se ela também está lá).
# O final já foi calculado de manhã (motor/finais.py): nenhuma das decisões é recompensada.
# A linha escolhida aparece e, no fim da noite, vem a tela do final.
POSICAO_ARACI, ESCALA_ARACI = (1420, 880), 0.62
# Como nas outras noites, só os olhos, a boca, atrás das orelhas e o pescoço.
LIBERADAS_NOITE_10 = LIBERADAS_NOITE_9

ZONAS_ARACI = [
    {"pergunta": "Olhos", "sinal": True, "imagem": "olho_araci_doente",
     "resposta": "Não durmo. [A criança não deixa]."},
    {"pergunta": "Orelhas", "sinal": True, "imagem": "orelha_pescoco_araci_doente",
     "resposta": "Começou aqui, atrás da orelha."},
    {"pergunta": "Boca", "sinal": True, "imagem": "boca_araci_doente",
     "resposta": "[É sede]. Andei o dia inteiro."},
    {"pergunta": "Pescoço", "sinal": True, "imagem": "orelha_pescoco_araci_doente",
     "resposta": "Agora desce pelo pescoço. [Não dói]."},
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


# Quem sai curado do tapiri: o rosto limpo, as manchas secando (pode_se_curar, lá em cima).
MBAE_CURADO = {
    "Testa": {"resposta": "Fresca. A febre passou."},
    "Olhos": {"imagem": "olho_mbae", "resposta": "O tapiri me fez bem."},
    "Boca": {"imagem": "boca_mbae", "resposta": "Pode olhar. As feridas fecharam."},
    "Respiração": {"resposta": "Respira fundo, sem chiado."},
    "Orelhas": {"imagem": "orelha_pescoco_mbae", "resposta": "Só a pintura de jenipapo."},
    "Pescoço": {"imagem": "orelha_pescoco_mbae", "resposta": "Pode olhar. Não tem nada."},
}
TAMANDARE_CURADO = {
    "Olhos": {"imagem": "olho_tamandare", "resposta": "O sol da estrada já não arde."},
    "Boca": {"imagem": "boca_tamandare", "resposta": "A rouquidão foi embora."},
    "Orelhas": {"imagem": "orelha_pescoco_tamandare", "resposta": "As manchas secaram. [A terra sem mal me poupou]."},
    "Pescoço": {"imagem": "orelha_pescoco_tamandare", "resposta": "Pode olhar. Secou tudo."},
    "Respiração": {"resposta": "Respira fundo, sem tosse."},
}
IANDE_CURADA = {
    "Olhos": {"imagem": "olho_iande", "resposta": "Dormi bem, enfim."},
    "Boca": {"imagem": "boca_iande", "resposta": "Pode olhar. Está tudo bem."},
    "Orelhas": {"imagem": "orelha_pescoco_iande", "resposta": "Não coça mais."},
    "Pescoço": {"imagem": "orelha_pescoco_iande", "resposta": "As manchas sumiram. [Foi o tapiri]."},
}
ZONAS_MBAE_NOITE_9 = pode_se_curar(com_pescoco(ZONAS_MBAE, PESCOCO_MBAE), "Mbaé", MBAE_CURADO)
ZONAS_MBAE = pode_se_curar(ZONAS_MBAE, "Mbaé", MBAE_CURADO)
ZONAS_TAMANDARE = pode_se_curar(ZONAS_TAMANDARE, "Tamandaré-mirim", TAMANDARE_CURADO)
ZONAS_TAMANDARE_NOITE_6 = pode_se_curar(ZONAS_TAMANDARE_NOITE_6, "Tamandaré-mirim", TAMANDARE_CURADO)
ZONAS_TAMANDARE_NOITE_9 = pode_se_curar(ZONAS_TAMANDARE_NOITE_9, "Tamandaré-mirim", TAMANDARE_CURADO)
ZONAS_IANDE_NOITE_9 = pode_se_curar(ZONAS_IANDE_NOITE_9, "Iandé", IANDE_CURADA)


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
                         "resposta": [
                             "O abrigo longe das ocas. Quem dorme lá não divide a rede, e o mal não passa para ninguém.",
                             "E quem tem a maldição e fica as três noites lá volta curado.",
                         ]},
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
                         "resposta": [
                             "Um lugar só. Quem entra fica três noites, longe de todos.",
                             "Lá o mal não passa para ninguém. E quem tem a maldição sai curado.",
                         ]},
                        ACUSACAO,
                        barulho_na_mata(),
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
        "energia_extra": {"machado": 1, "mandioca": 1},
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
                        {"pergunta": "E quem sai do tapiri?",
                         "resposta": [
                             "Quem passa as três noites lá volta para a rede curado da maldição.",
                             "E enquanto está lá, o mal não passa para ninguém. É para isso que ele serve.",
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
                    {"tipo": "fala", "quem": "Potira", "texto": "Só achei aquela mandioca. Desculpa."},
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
        "energia_extra": {"machado": 1, "mandioca": 1},
        "fundo": "fogueira_perto",
        # Quem pegou a febre continua passando adiante (dados/febre.py).
        "amaldicoados": True,
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "pessoas": {
            # O pajé diz como estão os deuses (dados/dias.py, DEUSES). É com ele a acusação e o
            # barulho na mata (a 2ª vez do Anhangá), como nas outras noites.
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
                "passos": [
                    {"tipo": "visitante", "visitante": "paje"},
                    DEUSES_FELIZES,
                    DEUSES_INFELIZES,
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        ACUSACAO,
                        barulho_na_mata(),
                    ]},
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
                    *fala_ou_curado("Mbaé", "(tosse) O frio entra no peito.",
                                    "O tapiri me devolveu o fôlego."),
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
                    ]},
                    {"tipo": "exame", "quem": "Potira", "liberadas": ["Olhos", "Boca"],
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA_DEPOIS},
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
        "energia_extra": {"machado": 1, "mandioca": 1},
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
                    *fala_ou_curado("Mbaé", "(tosse) Ainda estou aqui.",
                                    "Respiro sem tossir. Fazia tempo."),
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
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA_DEPOIS},
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
        "energia_extra": {"machado": 1, "mandioca": 1, "pulseira": 1},
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
                    *fala_ou_curado("Mbaé", "(tosse) Mais um dia.",
                                    "Mais um dia, e sem tosse."),
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
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA_DEPOIS},
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
        "energia_extra": {"machado": 1, "mandioca": 1, "pulseira": 1},
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
                    *fala_ou_curado("Mbaé", "(tosse) O rio acima é frio.",
                                    "O rio acima é frio. Agora eu aguento."),
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
                     "texto": TEXTO_EXAME, "zonas": ZONAS_POTIRA_DEPOIS},
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
                     "texto": TEXTO_EXAME, "zonas": ZONAS_IANDE_NOITE_8},
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
        "energia_extra": {"machado": 1, "mandioca": 1, "pulseira": 1},
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
                    {"tipo": "se", "no_maximo": {"padre_entrou": 0}, "passos": [
                        {"tipo": "fala", "quem": "Pajé", "texto": "Sente. O homem da cruz não volta mais."},
                    ]},
                    {"tipo": "se", "ao_menos": {"padre_entrou": 1}, "passos": [
                        {"tipo": "fala", "quem": "Pajé",
                         "texto": "Sente. Você deixou entrar o homem de preto. Cuidado com a água dele."},
                    ]},
                    {"tipo": "perguntas", "botao": "Voltar para a fogueira", "perguntas": [
                        {"pergunta": "O que você viu no sono?",
                         "resposta": "Um pescoço marcado. Manchas avermelhadas, pequenas, todas juntas."},
                        {"pergunta": "Como eu vejo isso?",
                         "resposta": "Olhe a pele de perto. O fogo engana."},
                        {"pergunta": "O que você acha do padre?", "ao_menos": {"padre_entrou": 1},
                         "resposta": [
                             "Ele fala de cura. Mas os que ele molha morrem do mesmo jeito.",
                             "A escolha é sua. Só não esqueça que [a água não tira a maldição].",
                         ]},
                        ACUSACAO,
                        # A 3ª vez do Anhangá: no fim desta noite, o final (dados/finais.py).
                        barulho_na_mata(),
                    ]},
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # O padre novo, se o jogador o deixou entrar de dia (dados/dias.py): em pé, atrás do
            # tronco da esquerda, onde o Krenan sentou na noite 8. Tenta convencer o jogador a ser
            # batizado e a batizar os outros. Aceitar é A Água do Batismo, no fim desta noite.
            "Padre": {
                "imagem": "padre_sentado", "posicao": POSICAO_PADRE, "escala": ESCALA_PADRE,
                "condicao": {"ao_menos": {"padre_entrou": 1}},
                "uma_vez": True, "atras": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "padre"},
                    {"tipo": "fala", "quem": "Padre", "texto": "Sente comigo. O fogo de vocês é bom."},
                    {"tipo": "perguntas", "botao": "Ouvir o pedido", "perguntas": [
                        {"pergunta": "Por que você veio?",
                         "resposta": "Para salvar quem ainda dá tempo. [Em quem é batizado, a maldição não fica]."},
                        {"pergunta": "E os que você batizou na vila?",
                         "resposta": ["Rezam por vocês todos os dias.", "[Os que morreram, morreram em paz]."]},
                        {"pergunta": "Por que eu?",
                         "resposta": "Você guarda a entrada. Se você aceitar, os outros aceitam."},
                    ]},
                    {"tipo": "fala", "quem": "Padre",
                     "texto": "Aceite a água hoje, e antes de o fogo apagar eu batizo todos os seus."},
                    {"tipo": "escolha", "texto": "O padre espera a sua resposta.", "opcoes": [
                        {"texto": "Aceitar o batismo e batizar os outros", "efeitos": {"converteu": 1}, "passos": [
                            {"tipo": "fala", "quem": "Padre", "texto": "Ajoelhe. Antes de a noite acabar, eu batizo os outros."},
                        ]},
                        {"texto": "Recusar", "passos": [
                            {"tipo": "fala", "quem": "Padre", "texto": "A porta da igreja fica aberta. Por pouco tempo."},
                        ]},
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
                     "texto": TEXTO_EXAME, "zonas": com_pescoco(ZONAS_YARA_NOITE_3, PESCOCO_YARA)},
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
                    *fala_ou_curado("Mbaé", "(tosse) Ainda respiro.",
                                    "Já posso subir o rio de novo."),
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": LIBERADAS_NOITE_9,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE_NOITE_9},
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
                     "texto": TEXTO_EXAME, "zonas": com_pescoco(ZONAS_POTIRA_DEPOIS, PESCOCO_POTIRA)},
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
                    *fala_ou_curado("Tamandaré-mirim", "A pele arde. Deve ser a terra sem mal chegando.",
                                    "A pele secou. A terra sem mal me poupou."),
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
        "energia_extra": {"machado": 1, "mandioca": 1, "pulseira": 1},
        "fundo": "fogueira_perto",
        "dica": "Clique em quem está perto do fogo para conversar.",
        "dormir": "Ir dormir",
        "dormir_bloqueado": "Ir dormir · antes, fale com %s",
        "pessoas": {
            "Pajé": {
                "imagem": "paje_sentado", "posicao": POSICAO_PAJE, "escala": ESCALA_PAJE, "espelhar": True,
                "posicao_com": {"Potira": POSICAO_PAJE_COM_POTIRA},
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

            # Quem o jogador deixou entrar (e não morreu nem foi levado) também está no fogo.
            "Yara": {
                "imagem": "yara_sentada", "posicao": POSICAO_YARA, "escala": ESCALA_YARA,
                "de_fora": True, "uma_vez": True,
                "passos": [
                    {"tipo": "visitante", "visitante": "yara"},
                    {"tipo": "fala", "quem": "Yara", "texto": "Amanhã o cacique volta. Vai olhar para todos nós."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_yara()},
                    {"tipo": "exame", "quem": "Yara", "liberadas": LIBERADAS_NOITE_10,
                     "texto": TEXTO_EXAME, "zonas": com_pescoco(ZONAS_YARA_NOITE_3, PESCOCO_YARA)},
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
                    *fala_ou_curado("Mbaé", "(tosse) Se eu não acordar, devolvam meu arco ao rio.",
                                    "Quando o cacique voltar, eu sigo caminho."),
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_mbae()},
                    {"tipo": "exame", "quem": "Mbaé", "liberadas": LIBERADAS_NOITE_10,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_MBAE_NOITE_9},
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
                    {"tipo": "fala", "quem": "Potira", "texto": "Trouxe mandioca da roça velha. Dá para todos."},
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu gente amaldiçoada?",
                         "resposta": "Vi rede vazia pendurada. Não entrei."},
                    ]},
                    {"tipo": "exame", "quem": "Potira", "liberadas": LIBERADAS_NOITE_10,
                     "texto": TEXTO_EXAME, "zonas": com_pescoco(ZONAS_POTIRA_DEPOIS, PESCOCO_POTIRA)},
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
                    *fala_ou_curado("Tamandaré-mirim", "A terra sem mal está perto. Sinto na pele.",
                                    "A terra sem mal está perto. A pele já não arde."),
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": conversa_tamandare()},
                    {"tipo": "exame", "quem": "Tamandaré-mirim", "liberadas": LIBERADAS_NOITE_10,
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
                    *fala_ou_curado("Iandé", "As costas doem mais hoje. Deve ser a chuva.",
                                    "As costas pararam de doer. O tapiri me fez bem."),
                    {"tipo": "perguntas", "botao": "Examinar o rosto", "perguntas": [
                        {"pergunta": "Viu alguém amaldiçoado?",
                         "resposta": "Vi uma casa fechada, com uma cruz na porta."},
                    ]},
                    {"tipo": "exame", "quem": "Iandé", "liberadas": LIBERADAS_NOITE_10,
                     "texto": TEXTO_EXAME, "zonas": ZONAS_IANDE_NOITE_9},
                    escolha_onde_dorme("Iandé", "Na minha rede de sempre.",
                                       "Sozinha? O que foi que eu fiz?"),
                    {"tipo": "visitante", "visitante": None},
                ],
            },

            # Araci, no chão, na frente, à direita. Obrigatório: decidir onde dorme.
            "Araci": {
                "imagem": "araci_sentada", "posicao": POSICAO_ARACI, "escala": ESCALA_ARACI,
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


# --- As conversas da noite (dados/historias.py) ---
# Em toda noite, quem é de fora tem uma fala nova: "Conversar" (a oca, o agora) antes do exame,
# no lugar das perguntas que se repetiam, e "Sentar perto" (a fogueira, o passado) depois de
# decidir onde ela dorme. A pergunta da história de cada um (a memória, para a Honra) continua
# aparecendo até ser ouvida. Krenan só tem "Sentar perto", no fim da conversa dele.
from dados.conversas import conversa_iande, conversa_potira  # noqa: E402
from dados.historias import CONVERSAR, OCA, SENTAR_PERTO, VOLTAR  # noqa: E402

HISTORIA_DE = {}
for _conversa in (conversa_yara(), conversa_mbae(), conversa_potira(), conversa_tamandare(),
                  conversa_iande(), conversa_araci()):
    for _pergunta in _conversa:
        if _pergunta.get("historia"):
            HISTORIA_DE[_pergunta["historia"]] = _pergunta
NOME_DA_HISTORIA = {"aldeia_yara": "Yara", "antes_mbae": "Mbaé", "antes_potira": "Potira",
                    "prega_tamandare": "Tamandaré-mirim", "viagem_iande": "Iandé", "filho_araci": "Araci"}


def conversa_da_noite(nome):
    """"Conversar" e, se ainda não foi ouvida, a pergunta da história da pessoa."""
    perguntas = []
    if nome in OCA:
        perguntas.append({"pergunta": CONVERSAR, "fala_da_noite": ("oca", nome)})
    for historia, quem in NOME_DA_HISTORIA.items():
        if quem == nome and historia in HISTORIA_DE:
            perguntas.append(dict(HISTORIA_DE[historia], nao_ouviu=historia))
    return perguntas


def sentar_perto(nome):
    return {"tipo": "perguntas", "botao": VOLTAR,
            "perguntas": [{"pergunta": SENTAR_PERTO, "fala_da_noite": ("fogueira", nome)}]}


for _noite in NOITES.values():
    for _nome, _pessoa in _noite["pessoas"].items():
        _passos = _pessoa["passos"]
        if _nome == "Krenan":
            # No fim da conversa, antes de ele sair da tela.
            _passos.insert(len(_passos) - 1, sentar_perto(_nome))
            continue
        if not _pessoa.get("de_fora"):
            continue
        for _i, _passo in enumerate(_passos):
            if _passo["tipo"] == "perguntas" and _passo.get("botao") == "Examinar o rosto":
                _passos[_i] = dict(_passo, perguntas=conversa_da_noite(_nome))
        for _i, _passo in enumerate(list(_passos)):
            if _passo["tipo"] == "escolha" and _passo.get("quem") == _nome:
                # Depois da decisão; se a pessoa morreu ou foi levada, não há com quem sentar.
                _passos.insert(_i + 1, {"tipo": "se", "dentro": _nome, "passos": [sentar_perto(_nome)]})
                break


# --- As perguntas ao pajé, em dois caminhos (como as do Irmão Aleixo, dados/dias.py) ---
# Primeiro o jogador escolhe o assunto (ou volta para a fogueira); depois aparecem as perguntas
# daquele assunto. Dá para voltar ao pajé e escolher o outro. As perguntas de cada noite continuam escritas acima, numa
# lista só: as que estão em PERGUNTAS_DO_SONHO vão para o 1º caminho; as outras, para o 2º.
# Noite em que um dos caminhos fica vazio mostra as perguntas direto, sem a escolha.
CAMINHOS_PAJE = {
    "texto": "O que perguntar ao pajé?",
    "sonho": "Perguntar sobre o sonho",
    "pessoas": "Perguntar sobre as pessoas",
}
PERGUNTAS_DO_SONHO = {
    "O que você viu no sono?", "Todo olho vermelho é o mal?", "O mal passa aqui no fogo?",
    "E se eu tiver certeza de que é o mal?", "Como eu vejo isso?", "O que é o tapiri?",
    "O tapiri tem lugar?", "E quem sai do tapiri?", "Que barulho é esse na mata?",
}


def _caminho(texto, botao, perguntas):
    opcao = {"texto": texto, "passos": [{"tipo": "perguntas", "botao": botao, "perguntas": perguntas}]}
    # Caminho só com perguntas sobre uma pessoa ("se_dentro"): só aparece se ela está na aldeia.
    quem = {pergunta.get("se_dentro") for pergunta in perguntas}
    if len(quem) == 1 and None not in quem:
        opcao["condicao"] = {"dentro": quem.pop()}
    return opcao


def perguntas_paje(passo):
    """O passo "perguntas" do pajé, dividido nos dois caminhos."""
    sonho = [pergunta for pergunta in passo["perguntas"] if pergunta["pergunta"] in PERGUNTAS_DO_SONHO]
    pessoas = [pergunta for pergunta in passo["perguntas"] if pergunta["pergunta"] not in PERGUNTAS_DO_SONHO]
    if not sonho or not pessoas:
        return passo
    return {"tipo": "escolha", "texto": CAMINHOS_PAJE["texto"], "opcoes": [
        _caminho(CAMINHOS_PAJE["sonho"], passo["botao"], sonho),
        _caminho(CAMINHOS_PAJE["pessoas"], passo["botao"], pessoas),
        {"texto": passo["botao"], "passos": []},   # sair sem perguntar nada
    ]}


def _dividir_perguntas_do_paje(passos):
    for _i, _passo in enumerate(passos):
        if _passo["tipo"] == "perguntas":
            passos[_i] = perguntas_paje(_passo)
        elif _passo["tipo"] == "se":
            _dividir_perguntas_do_paje(_passo["passos"])


for _noite in NOITES.values():
    _dividir_perguntas_do_paje(_noite["pessoas"]["Pajé"]["passos"])
