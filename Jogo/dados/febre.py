# A febre: quem está doente de verdade e como ela passa. Edite à vontade: aqui não há lógica.
#
# Fonte: Textos/A_Febre_Caraiba.pdf (fases, sinais e o que cada visitante tem) e
# Textos/Amaldiçoados.txt (quem traz a doença dos brancos e leva a morte para a aldeia).
# O jogador nunca vê esta lista: ela só serve para a febre e para as contas dos finais.
#   - Levar ao tapiri alguém de DOENTES (ou um morador que pegou a febre) soma 1 em
#     "tapiri_usos" (final O Tapiri). Levar gente sã não conta, para o tapiri não virar um
#     jeito fácil de ganhar o final.
#   - Seguir o pajé e levar ao tapiri alguém que NÃO está na lista marca um "inocente"
#     (final A Água do Batismo).

DOENTES = ["Mbaé", "Tamandaré-mirim", "Iandé", "Araci"]

# Se o doente dorme na oca, a febre passa para moradores que dormem com ele. Quantos é sorteado
# entre o mínimo e o máximo (cada partida tem a sua sorte; o "Continuar" repete a mesma).
# O doente que trouxe a febre não morre dela no jogo.
CONTAGIO = {
    "Mbaé": (1, 3),
    "Tamandaré-mirim": (2, 4),
    "Iandé": (3, 5),
}

# Os moradores com nome (o pajé não pega a febre no jogo). Quem pega a febre de um doente
# sai primeiro de quem dorme na mesma oca que ele (PERTO); depois, de qualquer morador.
# Quando acabam os nomes, quem pega é "um morador" (sem nome, não aparece na fogueira).
MORADORES = ["Tainá", "Caiubi", "Moema", "Jaci", "Peri", "Guaraci"]
PERTO = {
    "Mbaé": ["Tainá", "Caiubi", "Moema"],   # dormem na oca Yebá Bëló, com ele
}

# Os amaldiçoados (Textos/Amaldiçoados.txt): quem traz a doença dos brancos e quem pegou dela.
# Um morador que pegou a febre também passa adiante: cada noite em que dorme na oca, a febre
# passa para mais alguns (o sorteio, como no CONTAGIO). Só para no tapiri, com o remédio ou
# com a morte. Quem tomou o remédio do Aleixo não pega a febre de novo. É por isso que deixar
# um amaldiçoado muitos dias na aldeia leva outros junto, e, se a aldeia esvaziar, a partida
# acaba em O Vazio (dados/finais.py).
CONTAGIO_MORADOR = (0, 1)

# Nem todo mundo que pega a febre mostra no rosto: a chance de mostrar (0 a 1). Quem não
# mostra passa no exame como são, mas passa a febre do mesmo jeito e morre no mesmo dia.
CHANCE_DE_MOSTRAR = 0.5

# Quem pega a febre numa noite acorda com febre no dia seguinte e morre no 2º dia.
# Ex.: pegou na noite 2 -> com febre no dia 3 -> morre no dia 4.
DIAS_ATE_MORRER = 2

# O que o jogo mostra de manhã (uma frase para 1 pessoa, outra para mais de uma).
# Quem pegou a febre sem mostrar não aparece em "doentes": ninguém percebeu.
MANHA = {
    "doentes": ("Um morador acordou com febre.", "%d moradores acordaram com febre."),
    "mortos": ("Um morador morreu de febre esta noite.", "%d moradores morreram de febre esta noite."),
    "doente_nome": "%s acordou com febre.",
    "morto_nome": "%s morreu de febre esta noite.",
    "morto_sem_sinal": "%s morreu de febre esta noite. Na véspera, não tinha nada.",
}
