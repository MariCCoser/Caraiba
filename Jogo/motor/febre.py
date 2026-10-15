# A febre que passa na oca (os números ficam em dados/febre.py).
#
# - pegar(estado, quem): um doente dormiu na oca nesta noite. Sorteia quantos moradores pegam
#   a febre e guarda cada um em estado.febre. O sorteio usa a semente da partida
#   (estado.semente): muda de uma partida para outra, mas o "Continuar" refaz exatamente o mesmo.
# - passar_na_oca(estado): no fim de uma noite com amaldiçoados (dados/noites.py): cada
#   morador que pegou a febre numa noite anterior passa para mais alguns.
# - amanhecer(estado): passa para o dia seguinte. Quem pegou a febre acorda doente no 1º dia
#   e morre no 2º; as frases da manhã ficam em estado.manha, para o Dia mostrar.
# - amaldicoado(estado, nome): o doente de fora que ainda passa a febre.
#
# Cada entrada de estado.febre é um morador (sem nome, ele não aparece no jogo):
# {"de": "Mbaé", "noite": 2, "visivel": True}. "visivel": False é quem não mostra nada.

import random

from dados.febre import CHANCE_DE_MOSTRAR, CONTAGIO, CONTAGIO_MORADOR, DIAS_ATE_MORRER, MANHA


def _sorte(estado, quem):
    return random.Random("%s:%s:%d" % (estado.semente, quem, estado.dia))


def _contaminar(estado, de, quantos, sorte):
    for _ in range(quantos):
        estado.febre.append({"de": de, "noite": estado.dia, "visivel": sorte.random() < CHANCE_DE_MOSTRAR})


def pegar(estado, quem):
    if quem not in CONTAGIO:
        return
    minimo, maximo = CONTAGIO[quem]
    sorte = _sorte(estado, quem)
    _contaminar(estado, quem, sorte.randint(minimo, maximo), sorte)


def passar_na_oca(estado):
    """Os moradores amaldiçoados (que pegaram a febre numa noite anterior) passam adiante."""
    minimo, maximo = CONTAGIO_MORADOR
    for i, entrada in enumerate(list(estado.febre)):
        if entrada["noite"] >= estado.dia:
            continue
        sorte = _sorte(estado, "morador%d" % i)
        _contaminar(estado, "morador", sorte.randint(minimo, maximo), sorte)


def amaldicoado(estado, nome):
    """O doente de fora ainda passa a febre: está na aldeia (não morreu nem foi levado)."""
    return nome in CONTAGIO and nome in estado.dentro


def _frase(chave, quantos):
    um, varios = MANHA[chave]
    return um if quantos == 1 else varios % quantos


def amanhecer(estado):
    estado.dia += 1
    estado.manha = []
    doentes = mortos = mortos_sem_sinal = 0
    for entrada in list(estado.febre):
        # Save antigo: {"de", "adoecem", "noite"}, vários moradores numa entrada só.
        quantos = entrada.get("adoecem", 1)
        visivel = entrada.get("visivel", True)
        if estado.dia == entrada["noite"] + 1 and visivel:
            doentes += quantos
        if estado.dia >= entrada["noite"] + DIAS_ATE_MORRER:
            if visivel:
                mortos += quantos
            else:
                mortos_sem_sinal += quantos
            estado.febre.remove(entrada)
    if mortos or mortos_sem_sinal:
        estado.vivos -= mortos + mortos_sem_sinal
        estado.mortos += mortos + mortos_sem_sinal
    if mortos:
        estado.manha.append(_frase("mortos", mortos))
    if mortos_sem_sinal:
        estado.manha.append(_frase("mortos_sem_sinal", mortos_sem_sinal))
    if doentes:
        estado.manha.append(_frase("doentes", doentes))
