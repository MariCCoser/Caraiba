# Uma pessoa desenhada dentro do cenário (menor, como se estivesse ali), em que o jogador clica
# para conversar: na aldeia de dia e em volta da fogueira de noite.
#
# Passar o mouse acende o contorno da pessoa e mostra o nome, como nas ocas.
# Por enquanto as imagens são as mesmas de quem fala (de pé, cortadas no meio da coxa):
# para parecer sentada, a pessoa fica mais baixa, com a cintura para fora da tela.

import math

import pygame

import config
from motor import fontes, imagens, ui

# A marca de quem o jogador ainda não conversou (A Honra pede conversar com 5): uma brasa
# pequena acima da cabeça, que pulsa devagar. Some quando o mouse está em cima (aparece o nome).
# O pajé fala com o jogador toda noite: conversar com ele não conta, e ele não tem marca.
NAO_CONTA_COMO_CONVERSA = ["Pajé"]
MARCA_RAIO = 5
MARCA_ACIMA_DA_CABECA = 22
MARCA_PULSO_SEGUNDOS = 2.4


def falta_conversar(estado, nome):
    return nome not in NAO_CONTA_COMO_CONVERSA and nome not in estado.conversou


class PessoaNoCenario:
    def __init__(self, nome, imagem, posicao, escala, filtro, espelhar=False):
        """posicao: o meio da borda de baixo da imagem (x, y na tela 1600x900).
        espelhar: vira a pessoa para o outro lado (ex.: o pajé olhando para o fogo)."""
        self.nome = nome
        original = imagens.personagem(imagem, filtro)
        tamanho = (round(original.get_width() * escala), round(original.get_height() * escala))
        self.imagem = pygame.transform.smoothscale(original, tamanho)
        if espelhar:
            self.imagem = pygame.transform.flip(self.imagem, True, False)
        # Desenho que acaba antes do meio da coxa desce um pouco, para o corte não aparecer.
        x, y = posicao
        self.rect = self.imagem.get_rect(midbottom=(x, y + round(imagens.vazio_embaixo(imagem) * escala)))
        # A "máscara" diz, pixel a pixel, onde está a pessoa (o fundo transparente não conta).
        # Fica só o maior pedaço (o corpo), sem os pixels soltos que sobram do recorte.
        self.mascara = pygame.mask.from_surface(self.imagem).connected_component()
        self.contorno = [(x + self.rect.x, y + self.rect.y) for x, y in self.mascara.outline(2)]

    def contem(self, ponto):
        x, y = ponto[0] - self.rect.x, ponto[1] - self.rect.y
        return 0 <= x < self.rect.width and 0 <= y < self.rect.height and bool(self.mascara.get_at((x, y)))

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def topo_da_cabeca(self):
        if not hasattr(self, "_topo"):   # a conta é feita uma vez só (a marca pede a cada quadro)
            self._topo = self.rect.top + self.mascara.get_bounding_rects()[0].top if self.contorno else self.rect.top
        return self._topo

    def desenhar_marca(self, tela, tempo):
        """A brasa de quem o jogador ainda não conversou (veja falta_conversar)."""
        brilho = 0.65 + 0.35 * math.sin(tempo * 2 * math.pi / MARCA_PULSO_SEGUNDOS)
        centro = (self.rect.centerx, max(MARCA_RAIO * 3, self.topo_da_cabeca() - MARCA_ACIMA_DA_CABECA))
        halo = pygame.Surface((MARCA_RAIO * 6, MARCA_RAIO * 6), pygame.SRCALPHA)
        meio = (MARCA_RAIO * 3, MARCA_RAIO * 3)
        pygame.draw.circle(halo, config.URUCUM + (int(70 * brilho),), meio, MARCA_RAIO * 3)
        pygame.draw.circle(halo, config.URUCUM + (int(255 * brilho),), meio, MARCA_RAIO)
        tela.blit(halo, halo.get_rect(center=centro))

    def desenhar_destaque(self, tela, texto=None, contorno=True):
        """O contorno aceso e uma etiqueta com o nome acima da cabeça (contorno=False: só o nome)."""
        if contorno and len(self.contorno) > 2:
            pygame.draw.lines(tela, config.URUCUM, True, self.contorno, 3)
        fonte = fontes.fonte_escalada("sans", config.TAMANHO_PEQUENO)
        imagem = fonte.render(texto or self.nome, True, config.TABATINGA)
        topo = self.topo_da_cabeca()
        rect = imagem.get_rect(midbottom=(self.rect.centerx, topo - 14))
        rect.clamp_ip(pygame.Rect(24, 110, config.LARGURA - 48, config.ALTURA - 134))
        ui.painel_arredondado(tela, rect.inflate(28, 14), config.PRETO + (200,), raio=12, contorno=config.URUCUM)
        tela.blit(imagem, rect)


# O corpo coberto com a esteira (estado.corpos), deitado no lugar onde a pessoa sentava: do
# tamanho dela sentada vezes ESCALA_ESTEIRA (a arte da esteira tem a altura dos sentados).
ESCALA_ESTEIRA = 0.6


def corpo_no_cenario(corpo, filtro, lugar=None):
    """lugar: {"posicao", "escala", "espelhar"} (ex.: corpo["fogueira"]); sem ele, o lugar
    onde a pessoa morreu."""
    lugar = lugar or corpo
    imagem = "esteira_amaldicoado" if corpo.get("amaldicoado") else "esteira"
    return PessoaNoCenario(corpo["nome"], imagem, tuple(lugar["posicao"]),
                           lugar["escala"] * ESCALA_ESTEIRA, filtro, espelhar=lugar.get("espelhar", False))
