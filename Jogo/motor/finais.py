# Escolhe o final da partida a partir das variáveis do Estado (as regras ficam em dados/finais.py).
#
# - fim_da_noite(estado): no fim de cada noite. Devolve o final se o jogo já acabou ali
#   (um final "antecipado" que já bate, ou a aldeia esvaziou), ou None para seguir jogando.
# - calcular_na_manha(estado): na manhã do dia 10, antes de Araci chegar, guarda o final em
#   estado.final_calculado. Nada do que o jogador faz depois (Araci) muda o final.
# - escolher(estado): devolve sempre um final (o primeiro da fila que bate).

from dados.finais import DIA_DO_CALCULO, FINAIS

OPERACOES = {
    ">=": lambda valor, alvo: valor >= alvo,
    "<=": lambda valor, alvo: valor <= alvo,
    "==": lambda valor, alvo: valor == alvo,
}


def conta_bate(valor, conta):
    """conta é um texto como ">= 2"."""
    operacao, alvo = conta.split()
    return OPERACOES[operacao](valor, int(alvo))


def jeito_bate(estado, jeito):
    """Todas as contas do dicionário batem juntas (dicionário vazio sempre bate)."""
    return all(conta_bate(getattr(estado, nome), conta) for nome, conta in jeito.items())


def condicao_bate(estado, final):
    """Basta um dos jeitos da lista."""
    return any(jeito_bate(estado, jeito) for jeito in final["condicao"])


def por_id(identificador):
    return next(final for final in FINAIS if final["id"] == identificador)


def escolher(estado):
    """O cálculo do dia 10: o primeiro final da fila cuja condição bate."""
    for final in FINAIS:
        if condicao_bate(estado, final):
            return final
    return FINAIS[-1]


def calcular_na_manha(estado):
    """Na manhã do dia 10 (depois das mortes, antes de Araci): o final fica guardado."""
    if estado.dia == DIA_DO_CALCULO:
        estado.final_calculado = escolher(estado)["id"]


def fim_da_noite(estado):
    """No fim da noite: o jogo acaba antes do dia 10? Na noite 10, é o final calculado de manhã
    (menos um final "ultima_noite" que já bate: a escolha feita nesta noite)."""
    if estado.dia >= DIA_DO_CALCULO:
        for final in FINAIS:
            if final.get("ultima_noite") and condicao_bate(estado, final):
                return final
        return por_id(estado.final_calculado) if estado.final_calculado else escolher(estado)
    for final in FINAIS:
        if final.get("antecipado") and condicao_bate(estado, final):
            return final
    for final in FINAIS:
        if final.get("esvaziou") and jeito_bate(estado, final["esvaziou"]):
            return final
    return None
