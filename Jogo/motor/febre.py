# A febre que passa na oca (os números ficam em dados/febre.py).
#
# A aldeia é só o jogador, o pajé e quem o jogador deixou entrar: a febre passa entre quem é
# de fora e dorme nas ocas (quem está no tapiri fica isolado: não passa nem pega).
#
# - pegar(estado, quem): um doente (CONTAGIO) dormiu na oca nesta noite. Sorteia quantos e
#   quais dos outros de fora pegam a febre e guarda cada um em estado.febre. O sorteio usa a
#   semente da partida (estado.semente): muda de uma partida para outra, mas o "Continuar"
#   refaz exatamente o mesmo.
# - passar_na_oca(estado): no fim de uma noite com amaldiçoados (dados/noites.py): quem pegou
#   a febre numa noite anterior também passa para mais alguém.
# - amanhecer(estado): passa para o dia seguinte. Quem pegou a febre acorda doente no 1º dia
#   e morre no 2º; as frases da manhã (com o nome) ficam em estado.manha, para o Dia mostrar.
# - amaldicoado(estado, nome): o doente de fora que ainda passa a febre.
# - era_amaldicoado(estado, nome) e deixar_corpo(...): quem morre deixa o corpo coberto com a
#   esteira (a de amaldiçoado, se era) no lugar onde estava; quem morre da febre, onde dormia.
# - mostra_febre(estado, nome): quem pegou a febre numa noite anterior e mostra (o exame vê o
#   olho e a boca doentes).
# - quantos_amaldicoados(estado): os doentes de fora na aldeia mais quem pegou deles.
#
# Cada entrada de estado.febre é uma pessoa de fora:
# {"nome": "Yara", "de": "Mbaé", "noite": 2, "visivel": True}. "visivel": False é quem não
# mostra nada.

import random

from dados.aldeia import ONDE_DORME, ONDE_DORME_TAPIRI
from dados.febre import CHANCE_DE_MOSTRAR, CONTAGIO, CONTAGIO_PEGOU, DIAS_ATE_MORRER, DOENTES, MANHA


def _sorte(estado, quem):
    return random.Random("%s:%s:%d" % (estado.semente, quem, estado.dia))


def _na_oca(estado, nome):
    return nome in estado.dentro and nome not in estado.tapiri


def _quem_pode_pegar(estado, quem):
    """Quem dorme na oca e ainda não pegou: os outros de fora, menos os doentes que trazem a
    febre (CONTAGIO: eles não morrem dela)."""
    ja_pegaram = {entrada.get("nome") for entrada in estado.febre}
    return [nome for nome in estado.dentro
            if nome != quem and _na_oca(estado, nome) and nome not in ja_pegaram and nome not in CONTAGIO]


def _contaminar(estado, de, intervalo, sorte):
    minimo, maximo = intervalo
    quantos = sorte.randint(minimo, maximo)
    candidatos = _quem_pode_pegar(estado, de)
    for nome in sorte.sample(candidatos, min(quantos, len(candidatos))):
        estado.febre.append({"nome": nome, "de": de, "noite": estado.dia,
                             "visivel": sorte.random() < CHANCE_DE_MOSTRAR})


def pegar(estado, quem):
    if quem not in CONTAGIO or not _na_oca(estado, quem):
        return
    _contaminar(estado, quem, CONTAGIO[quem], _sorte(estado, quem))


def passar_na_oca(estado):
    """Os amaldiçoados (quem pegou a febre numa noite anterior) passam adiante."""
    for entrada in list(estado.febre):
        nome = entrada.get("nome")
        if entrada["noite"] >= estado.dia or not _na_oca(estado, nome):
            continue
        _contaminar(estado, nome, CONTAGIO_PEGOU, _sorte(estado, nome))


def quantos_amaldicoados(estado):
    """Quantos amaldiçoados há na aldeia: os doentes de fora que estão nela e quem pegou deles."""
    return sum(1 for nome in estado.dentro if nome in CONTAGIO) + len(estado.febre)


def amaldicoado(estado, nome):
    """O doente de fora ainda passa a febre: está na aldeia (não morreu nem foi levado)."""
    return nome in CONTAGIO and nome in estado.dentro


def era_amaldicoado(estado, nome):
    """Chegou com a maldição (dados/febre.py, DOENTES) ou pegou a febre, mostrando ou não."""
    return nome in DOENTES or any(entrada.get("nome") == nome for entrada in estado.febre)


def deixar_corpo(estado, nome, noite, onde, lugar, amaldicoado):
    """O corpo coberto com a esteira fica no lugar onde a pessoa estava, desde a noite em que
    morreu (lugar: o de dados/noites.py ou dados/aldeia.py, com "posicao", "escala" e, se
    tiver, "espelhar")."""
    estado.corpos.append({"nome": nome, "noite": noite, "onde": onde,
                          "posicao": list(lugar["posicao"]), "escala": lugar["escala"],
                          "espelhar": lugar.get("espelhar", False), "amaldicoado": amaldicoado})


def _corpo_na_oca(estado, nome):
    """Quem morre da febre morre onde dormia: na oca dele ou no tapiri."""
    if nome in estado.tapiri and nome in ONDE_DORME_TAPIRI:
        onde, lugar = "tapiri", ONDE_DORME_TAPIRI[nome]
    elif nome in ONDE_DORME:
        onde, lugar = ONDE_DORME[nome]["oca"], ONDE_DORME[nome]
    else:
        return
    # Morreu esta noite: a de ontem (amanhecer já passou para o dia seguinte).
    deixar_corpo(estado, nome, estado.dia - 1, onde, lugar, amaldicoado=True)


def mostra_febre(estado, nome):
    """Pegou a febre na oca numa noite anterior e mostra: está doente à vista."""
    return any(entrada.get("nome") == nome and entrada.get("visivel", True) and entrada["noite"] < estado.dia
               for entrada in estado.febre)


def _frase(chave, nomes):
    um, varios = MANHA[chave]
    if len(nomes) == 1:
        return um % nomes[0]
    return varios % (", ".join(nomes[:-1]) + " e " + nomes[-1])


def amanhecer(estado):
    estado.dia += 1
    estado.manha = []
    estado.energia_hoje = 0   # a energia a mais (negar o Aleixo) vale só para a noite em que veio
    doentes, mortos, mortos_sem_sinal = [], [], []
    for entrada in list(estado.febre):
        nome = entrada.get("nome")
        # Save antigo (moradores sem nome) ou quem já saiu da aldeia (morto, levado): some.
        if nome is None or nome not in estado.dentro:
            estado.febre.remove(entrada)
            continue
        visivel = entrada.get("visivel", True)
        if estado.dia == entrada["noite"] + 1 and visivel:
            doentes.append(nome)
        if estado.dia >= entrada["noite"] + DIAS_ATE_MORRER:
            (mortos if visivel else mortos_sem_sinal).append(nome)
            _corpo_na_oca(estado, nome)
            estado.febre.remove(entrada)
            estado.dentro.remove(nome)
            if nome in estado.tapiri:
                estado.tapiri.remove(nome)
                estado.tapiri_desde.pop(nome, None)
            estado.vivos -= 1
            estado.mortos += 1
    if mortos:
        estado.manha.append(_frase("mortos", mortos))
    if mortos_sem_sinal:
        estado.manha.append(_frase("mortos_sem_sinal", mortos_sem_sinal))
    if doentes:
        estado.manha.append(_frase("doentes", doentes))
