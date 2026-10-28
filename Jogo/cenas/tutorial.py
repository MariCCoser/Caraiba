# Tela "Como se joga", aberta pelo menu. Três abas no alto, cada uma num quadrinho com um ícone:
# Regras (as regras do jogo), Mouse (como jogar com o mouse) e Teclado (como jogar só com o
# teclado). Os textos ficam em dados/textos.py (TUTORIAL["abas"]). Esc ou "Voltar" volta ao menu.

import pygame

import config
from dados.textos import TUTORIAL
from motor import efeitos, fontes, ui
from motor.cena import Cena, desenhar_cenario

Y_TITULO = 90
Y_ABAS = 185
LARGURA_ABA = 270
ESPACO_ENTRE_ABAS = 300     # de um centro de aba ao seguinte
TOPO_TEXTO = 250            # onde começa o texto da aba aberta
TAMANHO_TEXTO = 26
TAMANHO_ABA = config.TAMANHO_PEQUENO + 4
LADO_ICONE = 40             # o quadrinho do ícone, dentro da aba


def desenhar_icone(tela, nome, centro, cor):
    """Os ícones das abas, desenhados com linhas (sem imagem): cabem num quadrado de 40."""
    cx, cy = centro
    if nome == "mouse":
        # O corpo do mouse, os dois botões e a rodinha.
        pygame.draw.rect(tela, cor, (cx - 9, cy - 14, 18, 28), 2, border_radius=9)
        pygame.draw.line(tela, cor, (cx - 9, cy - 3), (cx + 8, cy - 3), 2)
        pygame.draw.line(tela, cor, (cx, cy - 14), (cx, cy - 3), 2)
        pygame.draw.rect(tela, cor, (cx - 1, cy - 11, 3, 5))
    elif nome == "teclado":
        # O teclado: duas fileiras de teclas e a barra de espaço.
        pygame.draw.rect(tela, cor, (cx - 16, cy - 11, 32, 22), 2, border_radius=3)
        for linha in (cy - 6, cy - 1):
            for coluna in range(4):
                pygame.draw.rect(tela, cor, (cx - 11 + coluna * 6, linha, 4, 3))
        pygame.draw.line(tela, cor, (cx - 7, cy + 6), (cx + 7, cy + 6), 2)
    else:
        # As regras: uma lista, três pontos e três linhas.
        for linha in (cy - 8, cy, cy + 8):
            pygame.draw.circle(tela, cor, (cx - 10, linha), 2)
            pygame.draw.line(tela, cor, (cx - 5, linha), (cx + 12, linha), 2)


class Aba:
    """Uma aba: um quadrinho com o ícone e o nome ao lado. Funciona como o ui.Botao (visivel,
    habilitado, retangulo, atualizar, clicado, desenhar), então o teclado também anda por elas.

    A aba aberta fica com o fundo aceso, o contorno claro e uma barra embaixo: dá para ver qual
    é sem depender de cor.
    """

    MARGEM_X = 20
    MARGEM_Y = 10

    def __init__(self, texto, icone, centro):
        self.texto = texto
        self.icone = icone
        self.centro = centro
        self.visivel = True
        self.habilitado = True
        self.selecionado = False
        self.mouse_em_cima = False

    def retangulo(self):
        fonte = fontes.fonte_escalada("sans", TAMANHO_ABA)
        largura = max(LARGURA_ABA, LADO_ICONE + 14 + fonte.size(self.texto)[0] + 2 * self.MARGEM_X)
        altura = max(LADO_ICONE, fonte.get_height()) + 2 * self.MARGEM_Y
        rect = pygame.Rect(0, 0, largura, altura)
        rect.center = self.centro
        return rect

    def atualizar(self, posicao_mouse):
        self.mouse_em_cima = self.retangulo().collidepoint(posicao_mouse)
        if self.mouse_em_cima:
            ui.mouse_sobre_botao = True   # a tocha do cursor acende (motor/cursor.py)

    def clicado(self, evento):
        return (evento.type == pygame.MOUSEBUTTONUP and evento.button == 1
                and self.retangulo().collidepoint(evento.pos))

    def desenhar(self, tela):
        rect = self.retangulo()
        fundo = pygame.Surface(rect.size, pygame.SRCALPHA)
        fundo.fill(config.TERRA + (235,) if self.selecionado or self.mouse_em_cima else config.PRETO + (170,))
        tela.blit(fundo, rect.topleft)
        if self.mouse_em_cima:
            pygame.draw.rect(tela, config.URUCUM, rect, 3)
        elif self.selecionado:
            pygame.draw.rect(tela, config.TABATINGA, rect, 2)
        if self.selecionado:
            # A barra embaixo da aba aberta: mostra qual é pela forma, não só pela cor.
            pygame.draw.rect(tela, config.TABATINGA, (rect.left + 12, rect.bottom - 6, rect.width - 24, 4))

        quadrinho = pygame.Rect(0, 0, LADO_ICONE, LADO_ICONE)
        quadrinho.midleft = (rect.left + self.MARGEM_X, rect.centery)
        pygame.draw.rect(tela, config.BARRO_TEXTO, quadrinho, 2, border_radius=6)
        desenhar_icone(tela, self.icone, quadrinho.center, config.TABATINGA)

        fonte = fontes.fonte_escalada("sans", TAMANHO_ABA)
        imagem = fonte.render(self.texto, True, config.TABATINGA)
        tela.blit(imagem, imagem.get_rect(midleft=(quadrinho.right + 14, rect.centery)))


class Tutorial(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        abas = TUTORIAL["abas"]
        primeiro_x = 800 - ESPACO_ENTRE_ABAS * (len(abas) - 1) // 2
        self.abas = [Aba(aba["nome"], aba["icone"], (primeiro_x + i * ESPACO_ENTRE_ABAS, Y_ABAS))
                     for i, aba in enumerate(abas)]
        self.botao_voltar = ui.Botao(TUTORIAL["voltar"], (800, 840), largura_minima=260)
        self.abrir(0)

    def abrir(self, indice):
        """Mostra o texto da aba `indice` (0 = Regras)."""
        self.aberta = indice
        for i, aba in enumerate(self.abas):
            aba.selecionado = i == indice
        self.caixa = ui.CaixaTexto(TUTORIAL["abas"][indice]["texto"], 1400, (800, TOPO_TEXTO),
                                   ancora="topo", tamanho=TAMANHO_TEXTO, max_linhas=14)

    def alvos(self):
        return ui.centros(*self.abas, self.botao_voltar)

    def som_ambiente(self):
        return "menu"

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_RETURN,
                                                             pygame.K_KP_ENTER):
            self.jogo.ir_para("menu")
        elif self.botao_voltar.clicado(evento):
            self.jogo.ir_para("menu")
        else:
            for i, aba in enumerate(self.abas):
                if aba.clicado(evento):
                    self.abrir(i)

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        for aba in self.abas:
            aba.atualizar(self.jogo.mouse)
        self.botao_voltar.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, TUTORIAL["fundo"], "noite", self.tempo)
        efeitos.escurecer(tela, 140)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, TUTORIAL["titulo"], (800, Y_TITULO),
                         config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito")
        for aba in self.abas:
            aba.desenhar(tela)
        self.caixa.desenhar(tela)
        self.botao_voltar.desenhar(tela)
