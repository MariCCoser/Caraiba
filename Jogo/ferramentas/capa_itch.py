# Gera a capa do itch.io: a fogueira do menu e o título. Rodar de dentro de Jogo:
#   python -m ferramentas.capa_itch "Dez Dias, Dez Noites" ../Arte/Itch_io/Capa_itch_io.png
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.getcwd())

import pygame  # noqa: E402

import config  # noqa: E402
from dados.textos import MENU  # noqa: E402
from motor import fontes  # noqa: E402
from motor.cena import desenhar_cenario  # noqa: E402

subtitulo_txt, saida = sys.argv[1], sys.argv[2]
pygame.init()
pygame.display.set_mode((config.LARGURA, config.ALTURA))

fundo = pygame.Surface((config.LARGURA, config.ALTURA))
desenhar_cenario(fundo, MENU["fundo"], "noite", 0.35)

# Capa do itch.io: 630x500 (desenhada em dobro, 1260x1000). Corte com a mesma proporção,
# a fogueira um pouco à direita do centro.
alto = config.ALTURA
largo = round(alto * 630 / 500)
x0 = max(0, min(config.LARGURA - largo, 880 - int(largo * 0.55)))
capa = pygame.transform.smoothscale(fundo.subsurface((x0, 0, largo, alto)), (1260, 1000))

# Escurece o alto da imagem para o título ler bem.
sombra = pygame.Surface((1260, 1000), pygame.SRCALPHA)
for y in range(520):
    a = int(170 * (1 - y / 520) ** 1.6)
    pygame.draw.line(sombra, (0, 0, 0, a), (0, y), (1260, y))
capa.blit(sombra, (0, 0))


def escrever(texto, nome, tamanho, y, deslocamento):
    fonte = fontes.fonte(nome, tamanho)
    while fonte.size(texto)[0] > 1260 - 120:
        tamanho -= 4
        fonte = fontes.fonte(nome, tamanho)
    s = fonte.render(texto, True, config.PRETO)
    t = fonte.render(texto, True, config.TABATINGA)
    x = (1260 - t.get_width()) // 2
    capa.blit(s, (x + deslocamento, y + deslocamento))
    capa.blit(t, (x, y))
    return y + t.get_height()


y = escrever(MENU["titulo"], "serif_negrito", 230, 70, 8)
escrever(subtitulo_txt, "serif_italico", 76, y + 6, 4)

pygame.image.save(capa, saida.replace(".png", "_1260x1000.png"))
pygame.image.save(pygame.transform.smoothscale(capa, (630, 500)), saida)
print("ok", saida)
