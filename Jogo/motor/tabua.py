# A tábua de barro: no lugar de um caderno, os sinais do pajé ficam riscados numa tábua de barro.
#
# Na tela há um ícone (uma plaquinha de barro com riscos) no canto de cima, à direita.
# Clicando nele, a tábua abre por cima do jogo e mostra os sinais de cada noite.
# Tudo é desenhado em código, com as cores da paleta: não depende de arte.
#
# Uso numa cena:
#     self.tabua = Tabua(jogo)
#     tratar_evento: if self.tabua.tratar_evento(evento): return   (a tábua "engole" o evento)
#     atualizar:     self.tabua.atualizar(dt, self.jogo.mouse)
#     desenhar_interface: self.tabua.desenhar(tela)   (por último, por cima de tudo)

import random

import pygame

import config
from dados.textos import TABUA
from motor import fontes, ui

CENTRO_ICONE = (1540, 60)
TAMANHO_ICONE = (64, 52)
TAMANHO_TABUA = (980, 660)

# Barro claro da tábua: a mistura de Barro com Tabatinga (texto em Noite fica bem legível).
BARRO_CLARO = (0xC2, 0x99, 0x70)


def _riscos(superficie, rect, sorteio, quantos, cor, espessura):
    """Riscos curtos, como marcas de graveto no barro molhado."""
    for _ in range(quantos):
        x = sorteio.randint(rect.left, rect.right)
        y = sorteio.randint(rect.top, rect.bottom)
        dx = sorteio.randint(-6, 6)
        dy = sorteio.randint(4, 12)
        pygame.draw.line(superficie, cor, (x, y), (x + dx, y + dy), espessura)


def _desenhar_barro(tamanho, raio, semente):
    """Uma placa de barro: base clara, borda mais escura e marcas de dedo e graveto."""
    sorteio = random.Random(semente)   # semente fixa: a tábua é sempre igual
    placa = pygame.Surface(tamanho, pygame.SRCALPHA)
    rect = placa.get_rect()
    pygame.draw.rect(placa, config.BARRO, rect, border_radius=raio)
    pygame.draw.rect(placa, BARRO_CLARO, rect.inflate(-10, -10), border_radius=max(2, raio - 4))
    # Manchas do barro (mais claras e mais escuras), para não parecer liso demais.
    for _ in range(tamanho[0] * tamanho[1] // 900):
        x = sorteio.randint(8, tamanho[0] - 8)
        y = sorteio.randint(8, tamanho[1] - 8)
        cor = config.BARRO if sorteio.random() < 0.6 else (0xD2, 0xAE, 0x86)
        pygame.draw.circle(placa, cor, (x, y), sorteio.randint(1, 3))
    # Contorno marcado com graveto.
    pygame.draw.rect(placa, config.FUMACA, rect, 3, border_radius=raio)
    pygame.draw.rect(placa, config.FUMACA, rect.inflate(-14, -14), 1, border_radius=max(2, raio - 6))
    return placa


class Tabua:
    def __init__(self, jogo):
        self.jogo = jogo
        self.aberta = False
        self.nova = False            # True quando um sinal novo foi riscado e o jogador ainda não viu
        self.tempo = 0.0
        self.mouse_no_icone = False
        self.rect_icone = pygame.Rect((0, 0), TAMANHO_ICONE)
        self.rect_icone.center = CENTRO_ICONE
        self.rect_tabua = pygame.Rect((0, 0), TAMANHO_TABUA)
        self.rect_tabua.center = (config.LARGURA // 2, config.ALTURA // 2)
        self.botao_fechar = ui.Botao(TABUA["fechar"], (self.rect_tabua.centerx, self.rect_tabua.bottom - 50),
                                     tamanho=config.TAMANHO_PEQUENO, largura_minima=200)
        self._icone = self._desenhar_icone()
        self._placa = _desenhar_barro(TAMANHO_TABUA, 40, 1562)

    def _desenhar_icone(self):
        icone = _desenhar_barro(TAMANHO_ICONE, 12, 7)
        sorteio = random.Random(3)
        # Três linhas de riscos, como sinais já anotados.
        for linha in range(3):
            y = 14 + linha * 11
            x = 14
            while x < TAMANHO_ICONE[0] - 16:
                altura = sorteio.randint(5, 8)
                pygame.draw.line(icone, config.TERRA, (x, y), (x + sorteio.randint(-2, 2), y + altura), 2)
                x += sorteio.randint(5, 9)
        return icone

    def marcar_nova(self):
        """Chame quando um sinal novo for riscado: o ícone brilha até o jogador abrir a tábua."""
        self.nova = True

    # --- eventos e quadro ---------------------------------------------------

    def tratar_evento(self, evento):
        """Devolve True se a tábua usou o evento (aí a cena não deve fazer mais nada com ele)."""
        if self.aberta:
            fechar = (self.botao_fechar.clicado(evento)
                      or (evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_t))
                      or (evento.type == pygame.MOUSEBUTTONUP and evento.button == 1
                          and (self.rect_icone.collidepoint(evento.pos)
                               or not self.rect_tabua.collidepoint(evento.pos))))
            if fechar:
                self.aberta = False
            # Com a tábua aberta, nada passa para o jogo por baixo.
            return evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN)
        abrir = ((evento.type == pygame.MOUSEBUTTONUP and evento.button == 1
                  and self.rect_icone.collidepoint(evento.pos))
                 or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_t))
        if abrir:
            self.aberta = True
            self.nova = False
            return True
        # O "apertar" do clique no ícone também não deve chegar à cena.
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect_icone.collidepoint(evento.pos)

    def atualizar(self, dt, posicao_mouse):
        self.tempo += dt
        self.mouse_no_icone = self.rect_icone.collidepoint(posicao_mouse)
        if self.mouse_no_icone:
            ui.mouse_sobre_botao = True
        if self.aberta:
            self.botao_fechar.atualizar(posicao_mouse)

    # --- desenho ------------------------------------------------------------

    def desenhar(self, tela):
        self._desenhar_icone_na_tela(tela)
        if self.aberta:
            self._desenhar_aberta(tela)

    def _desenhar_icone_na_tela(self, tela):
        tela.blit(self._icone, self.rect_icone)
        if self.nova:
            # Sinal novo: contorno em Urucum pulsando, e um ponto (forma, não só cor).
            forca = 0.5 + 0.5 * abs(((self.tempo * 1.6) % 2) - 1)
            cor = tuple(int(c * forca + p * (1 - forca)) for c, p in zip(config.URUCUM, config.FUMACA))
            pygame.draw.rect(tela, cor, self.rect_icone.inflate(10, 10), 3, border_radius=16)
            pygame.draw.circle(tela, config.URUCUM, (self.rect_icone.right + 2, self.rect_icone.top - 2), 7)
        elif self.mouse_no_icone:
            pygame.draw.rect(tela, config.URUCUM, self.rect_icone.inflate(10, 10), 3, border_radius=16)
        if self.mouse_no_icone and not self.aberta:
            ui.texto_simples(tela, TABUA["dica"], (self.rect_icone.right, self.rect_icone.bottom + 22),
                             config.TAMANHO_PEQUENO, ancora="direita")

    def _desenhar_aberta(self, tela):
        veu = pygame.Surface(config.TAMANHO_LOGICO, pygame.SRCALPHA)
        veu.fill(config.PRETO + (180,))
        tela.blit(veu, (0, 0))
        tela.blit(self._placa, self.rect_tabua)

        esquerda = self.rect_tabua.left + 70
        ui.texto_simples(tela, TABUA["titulo"], (self.rect_tabua.centerx, self.rect_tabua.top + 70),
                         config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito", cor=config.NOITE)
        ui.texto_simples(tela, TABUA["subtitulo"], (self.rect_tabua.centerx, self.rect_tabua.top + 122),
                         config.TAMANHO_PEQUENO + 2, nome_fonte="serif_italico", cor=config.TERRA)
        # Linha riscada embaixo do título.
        y_linha = self.rect_tabua.top + 152
        pygame.draw.line(tela, config.FUMACA, (esquerda, y_linha), (self.rect_tabua.right - 70, y_linha), 2)

        sinais = self.jogo.estado.tabua
        y = y_linha + 50
        if not sinais:
            ui.texto_simples(tela, TABUA["vazia"], (self.rect_tabua.centerx, y + 20),
                             config.TAMANHO_PEQUENO + 4, nome_fonte="serif", cor=config.NOITE)
        fonte = fontes.fonte_escalada("serif", config.TAMANHO_PEQUENO + 6)
        fonte_noite = fontes.fonte_escalada("mono", config.TAMANHO_PEQUENO)
        for numero, sinal in enumerate(sinais, start=1):
            # Marcas de contagem da noite (|||), como riscos de graveto, e o texto do sinal.
            for i in range(numero):
                x = esquerda + i * 9
                pygame.draw.line(tela, config.TERRA, (x, y - 12), (x + 2, y + 12), 3)
            rotulo = fonte_noite.render(TABUA["noite"] % numero, True, config.TERRA)
            tela.blit(rotulo, (esquerda + 110, y - rotulo.get_height() // 2))
            texto = fonte.render(sinal, True, config.NOITE)
            tela.blit(texto, (esquerda + 240, y - texto.get_height() // 2))
            y += 54

        self.botao_fechar.desenhar(tela)
