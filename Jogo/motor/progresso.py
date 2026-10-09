# O progresso da partida, para o botão "Continuar" do menu.
#
# Como funciona: no começo de cada Dia o jogo guarda o Estado daquele momento e, a cada
# clique do jogador (seguir uma fala, fazer uma pergunta, escolher), guarda a ação numa
# lista. Para continuar, o jogo volta ao Estado do começo do dia e refaz as mesmas ações,
# na mesma ordem, sem animação. Como o jogo não tem sorte, o resultado é exatamente o ponto
# em que o jogador parou.

from motor import salvamento

NOME = "progresso"


def salvar(cena, estado_dicionario, acoes=None):
    """cena: o nome da cena (ex.: "dia"); estado_dicionario: o Estado no começo da cena."""
    salvamento.salvar(NOME, {"cena": cena, "estado": estado_dicionario, "acoes": acoes or []})


def carregar():
    """Devolve {"cena", "estado", "acoes"} ou None se não houver partida guardada."""
    dados = salvamento.carregar(NOME)
    if not isinstance(dados, dict) or "cena" not in dados or "estado" not in dados:
        return None
    dados.setdefault("acoes", [])
    return dados


def existe():
    return carregar() is not None


def apagar():
    salvamento.apagar(NOME)
