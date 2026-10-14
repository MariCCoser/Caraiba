# A febre que passa na oca (os números ficam em dados/febre.py).
#
# - pegar(estado, quem): um doente dormiu na oca nesta noite. Sorteia quantos moradores pegam
#   a febre e quais (de PERTO dele primeiro) e guarda cada um em estado.febre. O sorteio usa a
#   semente da partida (estado.semente): muda de uma partida para outra, mas o "Continuar"
#   refaz exatamente o mesmo.
# - passar_na_oca(estado): no fim de uma noite com amaldiçoados (dados/noites.py): cada
#   morador que pegou a febre numa noite anterior e dorme na oca passa para mais alguns.
# - amanhecer(estado): passa para o dia seguinte. Quem pegou a febre acorda doente no 1º dia
#   e morre no 2º; as frases da manhã ficam em estado.manha, para o Dia mostrar.
# - amaldicoado(estado, nome), com_sinais(estado, nome), curar(estado, nome), tirar(estado, nome).
#
# Cada entrada de estado.febre é um morador: {"nome": "Tainá" (ou None), "de": "Mbaé",
# "noite": 2, "visivel": True}. "visivel": False é quem não mostra nada no rosto.

import random

from dados.febre import (CHANCE_DE_MOSTRAR, CONTAGIO, CONTAGIO_MORADOR, DIAS_ATE_MORRER, MANHA,
                         MORADORES, PERTO)


def _sorte(estado, quem):
    return random.Random("%s:%s:%d" % (estado.semente, quem, estado.dia))


def _livres(estado, primeiro):
    """Moradores com nome que ainda podem pegar a febre: os de "primeiro" na frente."""
    fora = {entrada["nome"] for entrada in estado.febre} | set(estado.mortos_nomes) \
        | set(estado.mortos_febre) | set(estado.tapiri) | set(estado.curados)
    ordem = list(primeiro) + [nome for nome in MORADORES if nome not in primeiro]
    return [nome for nome in ordem if nome not in fora]


def _contaminar(estado, de, quantos, sorte, perto=()):
    livres = _livres(estado, perto)
    # Embaralha dentro de cada grupo (os de perto continuam na frente).
    perto_livres = [nome for nome in livres if nome in perto]
    outros = [nome for nome in livres if nome not in perto]
    sorte.shuffle(perto_livres)
    sorte.shuffle(outros)
    livres = perto_livres + outros
    for i in range(quantos):
        nome = livres[i] if i < len(livres) else None
        estado.febre.append({"nome": nome, "de": de, "noite": estado.dia,
                             "visivel": sorte.random() < CHANCE_DE_MOSTRAR})


def pegar(estado, quem):
    if quem not in CONTAGIO or quem in estado.curados:
        return
    minimo, maximo = CONTAGIO[quem]
    sorte = _sorte(estado, quem)
    _contaminar(estado, quem, sorte.randint(minimo, maximo), sorte, PERTO.get(quem, ()))


def passar_na_oca(estado):
    """Os moradores amaldiçoados que dormem na oca esta noite passam a febre adiante."""
    minimo, maximo = CONTAGIO_MORADOR
    for entrada in list(estado.febre):
        nome = entrada.get("nome")
        if not nome or entrada["noite"] >= estado.dia or nome in estado.tapiri:
            continue
        sorte = _sorte(estado, nome)
        _contaminar(estado, nome, sorte.randint(minimo, maximo), sorte)


def amaldicoado(estado, nome):
    """O morador pegou a febre (com ou sem sinal), ou é um doente que ainda a passa."""
    if nome in CONTAGIO:
        return nome in estado.dentro and nome not in estado.curados
    return any(entrada.get("nome") == nome for entrada in estado.febre)


def com_sinais(estado, nome):
    """Pegou a febre numa noite anterior e ela aparece no rosto."""
    return any(entrada.get("nome") == nome and entrada.get("visivel") and entrada["noite"] < estado.dia
               for entrada in estado.febre)


def curar(estado, nome):
    """O remédio do Aleixo: a febre sai (não morre, não passa mais e não pega de novo)."""
    tirar(estado, nome)
    if nome not in estado.curados:
        estado.curados.append(nome)


def tirar(estado, nome):
    """O morador sai da febre (morreu pela mão do jogador, foi curado...)."""
    estado.febre = [entrada for entrada in estado.febre if entrada.get("nome") != nome]


def _frase(chave, quantos):
    um, varios = MANHA[chave]
    return um if quantos == 1 else varios % quantos


def amanhecer(estado):
    estado.dia += 1
    estado.manha = []
    doentes, mortos = [], []
    for entrada in list(estado.febre):
        # Save antigo: {"de", "adoecem", "noite"}, sem nome. Vira um morador sem nome por pessoa.
        quantos = entrada.get("adoecem", 1)
        nome = entrada.get("nome")
        visivel = entrada.get("visivel", True)
        if estado.dia == entrada["noite"] + 1 and visivel:
            doentes += [nome] * quantos
        if estado.dia >= entrada["noite"] + DIAS_ATE_MORRER:
            mortos += [(nome, visivel)] * quantos
            estado.febre.remove(entrada)
    if mortos:
        estado.vivos -= len(mortos)
        estado.mortos += len(mortos)
        sem_nome = sum(1 for nome, _ in mortos if not nome)
        for nome, visivel in mortos:
            if nome:
                estado.mortos_febre.append(nome)
                estado.manha.append(MANHA["morto_nome" if visivel else "morto_sem_sinal"] % nome)
        if sem_nome:
            estado.manha.append(_frase("mortos", sem_nome))
    if doentes:
        for nome in doentes:
            if nome:
                estado.manha.append(MANHA["doente_nome"] % nome)
        sem_nome = sum(1 for nome in doentes if not nome)
        if sem_nome:
            estado.manha.append(_frase("doentes", sem_nome))
