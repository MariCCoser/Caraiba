# A febre que passa na oca (os números ficam em dados/febre.py).
#
# - pegar(estado, quem): um doente dormiu na oca nesta noite. Sorteia quantos moradores pegam
#   a febre e guarda em estado.febre. O sorteio usa a semente da partida (estado.semente):
#   muda de uma partida para outra, mas o "Continuar" refaz exatamente o mesmo.
# - amanhecer(estado): passa para o dia seguinte. Quem pegou a febre acorda doente no 1º dia
#   e morre no 2º; as frases da manhã ficam em estado.manha, para o Dia mostrar.

import random

from dados.febre import CONTAGIO, DIAS_ATE_MORRER, MANHA


def pegar(estado, quem):
    if quem not in CONTAGIO:
        return
    minimo, maximo = CONTAGIO[quem]
    sorte = random.Random("%s:%s:%d" % (estado.semente, quem, estado.dia))
    estado.febre.append({"de": quem, "adoecem": sorte.randint(minimo, maximo), "noite": estado.dia})


def _frase(chave, quantos):
    um, varios = MANHA[chave]
    return um if quantos == 1 else varios % quantos


def amanhecer(estado):
    estado.dia += 1
    estado.manha = []
    doentes = mortos = 0
    for febre in list(estado.febre):
        if estado.dia == febre["noite"] + 1:
            doentes += febre["adoecem"]
        if estado.dia >= febre["noite"] + DIAS_ATE_MORRER:
            mortos += febre["adoecem"]
            estado.febre.remove(febre)
    if mortos:
        estado.vivos -= mortos
        estado.mortos += mortos
        estado.manha.append(_frase("mortos", mortos))
    if doentes:
        estado.manha.append(_frase("doentes", doentes))
