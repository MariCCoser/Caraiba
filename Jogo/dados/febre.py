# A febre: quem está doente de verdade e como ela passa. Edite à vontade: aqui não há lógica.
#
# Fonte: Textos/A_Febre_Caraiba.pdf (fases, sinais e o que cada visitante tem) e
# Textos/Amaldiçoados.txt (quem traz a doença dos brancos e leva a morte para a aldeia).
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

# Os amaldiçoados (Textos/Amaldiçoados.txt): quem traz a doença dos brancos e quem pegou dela.
# Os moradores não aparecem no jogo: quem pega a febre é "um morador". Mas quem pegou também
# passa adiante: a cada noite com amaldiçoados (dados/noites.py), cada morador que pegou a
# febre numa noite anterior passa para mais alguns (o sorteio, como no CONTAGIO), até morrer.
# O doente de fora (Mbaé) para de passar no tapiri, quando o Irmão Aleixo o leva ou com a morte.
# É por isso que deixar um amaldiçoado muitos dias na aldeia leva outros junto, e, se a
# aldeia esvaziar, a partida acaba em O Vazio (dados/finais.py).
CONTAGIO_MORADOR = (0, 1)

# Nem todo mundo que pega a febre mostra: a chance de mostrar (0 a 1). Quem não mostra não
# aparece na manhã como doente, mas passa a febre do mesmo jeito e morre no mesmo dia.
CHANCE_DE_MOSTRAR = 0.5

# Quem pega a febre numa noite acorda com febre no dia seguinte e morre no 2º dia.
# Ex.: pegou na noite 2 -> com febre no dia 3 -> morre no dia 4.
DIAS_ATE_MORRER = 2

# O que o jogo mostra de manhã (uma frase para 1 pessoa, outra para mais de uma).
# Quem pegou a febre sem mostrar não aparece em "doentes": ninguém percebeu.
MANHA = {
    "doentes": ("Um morador acordou com febre.", "%d moradores acordaram com febre."),
    "mortos": ("Um morador morreu de febre esta noite.", "%d moradores morreram de febre esta noite."),
    "mortos_sem_sinal": ("Um morador que não tinha nada morreu de febre esta noite.",
                         "%d moradores que não tinham nada morreram de febre esta noite."),
}
