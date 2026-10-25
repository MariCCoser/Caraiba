# As conversas da noite (dados/historias.py): cada vez que o jogador conversa com alguém na oca
# ("Conversar") ou senta perto dele na fogueira ("Sentar perto"), aparece a próxima fala dele.
#
# - proxima(estado, onde, nome): onde é "oca" ou "fogueira". Devolve a fala em partes (uma por
#   tela) e conta mais uma conversa (estado.conversas_oca / estado.conversas_fogueira). Depois da
#   10ª, repete a última.

import re

from dados.historias import FOGUEIRA, OCA, TAMANHO_DA_PARTE

FALAS = {"oca": OCA, "fogueira": FOGUEIRA}


def _contador(estado, onde):
    return estado.conversas_oca if onde == "oca" else estado.conversas_fogueira


def tem_fala(onde, nome):
    return bool(FALAS[onde].get(nome))


def partes(texto):
    """Quebra uma fala longa no fim das frases, em pedaços de até TAMANHO_DA_PARTE letras."""
    frases = re.findall(r"[^.!?]+[.!?]+\]?\s*", texto) or [texto]
    pedacos, atual = [], ""
    for frase in frases:
        # Nunca corta dentro de um [trecho em âmbar]: ele precisa abrir e fechar na mesma parte.
        fora_dos_colchetes = atual.count("[") == atual.count("]")
        if atual and fora_dos_colchetes and len(atual) + len(frase) > TAMANHO_DA_PARTE:
            pedacos.append(atual.strip())
            atual = ""
        atual += frase
    if atual.strip():
        pedacos.append(atual.strip())
    return pedacos


def proxima(estado, onde, nome):
    falas = FALAS[onde][nome]
    contador = _contador(estado, onde)
    vez = contador.get(nome, 0)
    contador[nome] = vez + 1
    return partes(falas[min(vez, len(falas) - 1)])
