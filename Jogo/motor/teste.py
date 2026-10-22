# Modo de teste (config.MODO_TESTE): pular direto para a fogueira de qualquer noite.
#
# ir_para_noite(jogo, noite) começa uma partida nova e monta o Estado como se o jogador tivesse
# chegado até ali deixando todos entrarem e sem matar nem entregar ninguém: quem já chegou está
# na aldeia (dormindo nas ocas desde que chegou), os sinais do pajé estão na tábua e, na noite
# 8, Krenan foi chamado para a fogueira (na 10, ele volta). Quem chega e em que dia, e os
# sinais, saem do próprio roteiro (dados/dias.py): se ele mudar, isto acompanha.
# A partida guardada não muda durante a noite de teste (cenas/dia.py, so_a_noite); se o jogador
# seguir jogando depois dela (a aldeia, o dia seguinte), o jogo passa a guardar por cima.

from dados.dias import DIAS
from estado import Estado
from motor import finais


def _passos(passos):
    """Todos os passos do roteiro, inclusive os de dentro de "se", "escolha" e conversas."""
    for passo in passos:
        yield passo
        yield from _passos(passo.get("passos", []))
        for opcao in passo.get("opcoes", []):
            yield from _passos(opcao.get("passos", []))
            yield opcao
        for pessoa in passo.get("pessoas", []) if isinstance(passo.get("pessoas"), list) else []:
            yield from _passos(pessoa.get("passos", []))


def chegadas():
    """{nome: dia em que chega} (quem tem a opção "entra" no roteiro do dia)."""
    quando = {}
    for dia, roteiro in sorted(DIAS.items()):
        for passo in _passos(roteiro["passos"]):
            if passo.get("entra"):
                quando.setdefault(passo["entra"], dia)
    return quando


def sinais_ate(noite):
    """Os sinais que o pajé contou até essa noite, e em que noite (a tábua de barro)."""
    sinais, noites = [], []
    for dia, roteiro in sorted(DIAS.items()):
        if dia > noite:
            break
        for passo in _passos(roteiro["passos"]):
            if passo.get("tipo") == "sinal" and passo["texto"] not in sinais:
                sinais.append(passo["texto"])
                noites.append(dia)
    return sinais, noites


def ir_para_noite(jogo, noite):
    # Uma partida nova, mas sem apagar a guardada (jogo.nova_partida apagaria).
    jogo.estado = estado = Estado()
    jogo.acoes_para_refazer = None
    jogo.dia_pausado = None
    estado.dia = noite
    quando = chegadas()
    estado.dentro = [nome for nome, dia in sorted(quando.items(), key=lambda item: item[1]) if dia <= noite]
    estado.vivos = len(estado.dentro)
    # Noites dormidas na oca até aqui (o olho de Mbaé piora com elas).
    estado.noites_na_oca = {nome: noite - quando[nome] for nome in estado.dentro}
    estado.tabua, estado.tabua_noites = sinais_ate(noite)
    if noite == 8:
        estado.convidados = ["Krenan"]
    if noite >= 10:
        estado.krenan_volta = 1
        finais.calcular_na_manha(estado)
    jogo.testando_noite = True
    jogo.ir_para("dia")
