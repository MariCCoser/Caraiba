# O cursor do mouse: uma tocha. A ponta da chama (em cima, à esquerda) é onde o clique acontece.
#
# Há duas tochas: a comum e a "acesa" (chama maior e mais clara), quando o mouse está sobre algo
# que dá para clicar. A tocha é desenhada aqui mesmo, sem arquivo de imagem.

import pygame

import config

TAMANHO = (40, 48)
PONTA = (5, 3)               # a ponta da chama: o ponto do clique

MADEIRA = (92, 58, 34)
MADEIRA_ESCURA = (52, 32, 18)
AMARRA = (150, 112, 70)
CONTORNO = (20, 12, 6)


def _desenhar(acesa):
    tocha = pygame.Surface(TAMANHO, pygame.SRCALPHA)
    # O cabo: de baixo à direita até a cabeça da tocha, inclinado como uma seta.
    pygame.draw.line(tocha, CONTORNO, (34, 44), (15, 19), 8)
    pygame.draw.line(tocha, MADEIRA, (34, 44), (15, 19), 5)
    pygame.draw.line(tocha, MADEIRA_ESCURA, (33, 42), (17, 21), 1)
    # A cabeça da tocha: fibra enrolada, mais grossa que o cabo.
    pygame.draw.circle(tocha, CONTORNO, (15, 19), 6)
    pygame.draw.circle(tocha, AMARRA, (15, 19), 4)
    pygame.draw.line(tocha, MADEIRA_ESCURA, (12, 20), (18, 16), 1)
    # A chama, com línguas de fogo: Urucum por fora, clara por dentro (acesa: maior e mais clara).
    fora = [(6, 4), (9, 8), (11, 5), (13, 10), (17, 8), (17, 14), (13, 18), (9, 17), (6, 13), (5, 8)]
    dentro = [(8, 9), (10, 11), (12, 10), (13, 14), (10, 16), (8, 13)]
    if acesa:
        fora = [(4, 1), (8, 6), (11, 2), (13, 8), (19, 5), (19, 13), (14, 19), (8, 18), (4, 13), (3, 7)]
        dentro = [(7, 7), (10, 10), (13, 8), (15, 13), (11, 17), (7, 13)]
    pygame.draw.polygon(tocha, CONTORNO, fora, 3)
    pygame.draw.polygon(tocha, config.URUCUM, fora)
    pygame.draw.polygon(tocha, config.TABATINGA if acesa else config.BARRO, dentro)
    return tocha


_cursores = {}


def usar(acesa=False):
    """Põe a tocha como cursor. Alguns sistemas (e o navegador) não deixam: aí fica a seta."""
    try:
        if acesa not in _cursores:
            _cursores[acesa] = pygame.cursors.Cursor(PONTA, _desenhar(acesa))
        pygame.mouse.set_cursor(_cursores[acesa])
    except Exception:
        pass
