# A febre: quem está doente de verdade e como ela passa. Edite à vontade: aqui não há lógica.
#
# Fonte: Textos/A_Febre_Caraiba.pdf (fases, sinais e o que cada visitante tem).
# O jogador nunca vê esta lista: ela só serve para a febre e para as contas dos finais.
#   - Levar ao tapiri alguém de DOENTES soma 1 em "tapiri_usos" (final O Tapiri).
#     Levar gente sã não conta, para o tapiri não virar um jeito fácil de ganhar o final.
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

# Quem pega a febre numa noite acorda com febre no dia seguinte e morre no 2º dia.
# Ex.: pegou na noite 2 -> com febre no dia 3 -> morre no dia 4.
DIAS_ATE_MORRER = 2

# O que o jogo mostra de manhã (uma frase para 1 pessoa, outra para mais de uma).
MANHA = {
    "doentes": ("Um morador acordou com febre.", "%d moradores acordaram com febre."),
    "mortos": ("Um morador morreu de febre esta noite.", "%d moradores morreram de febre esta noite."),
}
