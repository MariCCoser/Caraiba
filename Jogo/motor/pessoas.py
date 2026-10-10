# Uma pessoa desenhada dentro do cenário (menor, como se estivesse ali), em que o jogador clica
# para conversar: na aldeia de dia e em volta da fogueira de noite.
#
# Passar o mouse acende o contorno da pessoa e mostra o nome, como nas ocas.
# Por enquanto as imagens são as mesmas de quem fala (de pé, cortadas no meio da coxa):
# para parecer sentada, a pessoa fica mais baixa, com a cintura para fora da tela.

import pygame

import config
from motor import fontes, imagens, ui


class PessoaNoCenario:
    def __init__(self, nome, imagem, posicao, escala, filtro):
        """posicao: o meio da borda de baixo da imagem (x, y na tela 1600x900)."""
        self.nome = nome
        original = imagens.personagem(imagem, filtro)
        tamanho = (round(original.get_width() * escala), round(original.get_height() * escala))
        self.imagem = pygame.transform.smoothscale(original, tamanho)
        self.rect = self.imagem.get_rect(midbottom=posicao)
        # A "máscara" diz, pixel a pixel, onde está a pessoa (o fundo transparente não conta).
        # Fica só o maior pedaço (o corpo), sem os pixels soltos que sobram do recorte.
        self.mascara = pygame.mask.from_surface(self.imagem).connected_component()
        self.contorno = [(x + self.rect.x, y + self.rect.y) for x, y in self.mascara.outline(2)]

    def contem(self, ponto):
        x, y = ponto[0] - self.rect.x, ponto[1] - self.rect.y
        return 0 <= x < self.rect.width and 0 <= y < self.rect.height and bool(self.mascara.get_at((x, y)))

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def desenhar_destaque(self, tela, texto=None):
        """O contorno aceso e uma etiqueta com o nome acima da cabeça."""
        if len(self.contorno) > 2:
            pygame.draw.lines(tela, config.URUCUM, True, self.contorno, 3)
        fonte = fontes.fonte_escalada("sans", config.TAMANHO_PEQUENO)
        imagem = fonte.render(texto or self.nome, True, config.TABATINGA)
        topo = self.rect.top + self.mascara.get_bounding_rects()[0].top if self.contorno else self.rect.top
        rect = imagem.get_rect(midbottom=(self.rect.centerx, topo - 14))
        rect.clamp_ip(pygame.Rect(24, 110, config.LARGURA - 48, config.ALTURA - 134))
        ui.painel_arredondado(tela, rect.inflate(28, 14), config.PRETO + (200,), raio=12, contorno=config.URUCUM)
        tela.blit(imagem, rect)
