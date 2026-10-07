# Carrega as fontes dos arquivos em assets/fontes/, uma vez só para cada tamanho.

import os

import pygame

import config
from motor import preferencias

# Guarda as fontes já abertas: {(nome, tamanho): pygame.font.Font}
_cache = {}


def fonte(nome, tamanho):
    """Devolve a fonte `nome` (veja config.FONTES) no tamanho exato pedido, em pixels."""
    chave = (nome, tamanho)
    if chave not in _cache:
        caminho = os.path.join(config.PASTA_FONTES, config.FONTES[nome])
        _cache[chave] = pygame.font.Font(caminho, tamanho)
    return _cache[chave]


def fonte_escalada(nome, tamanho_base):
    """Como fonte(), mas aplica a opção de tamanho do texto (normal / grande)."""
    tamanho = round(tamanho_base * preferencias.atual.escala_texto())
    return fonte(nome, tamanho)


def limpar_cache():
    """Esquece as fontes abertas (necessário ao fechar o pygame)."""
    _cache.clear()
