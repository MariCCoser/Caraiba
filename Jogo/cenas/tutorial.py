# Tela "Como se joga": as regras do jogo, abertas pelo menu a qualquer momento. Esc ou "Voltar" volta ao menu.

import pygame

import config
from dados.textos import TUTORIAL
from motor import efeitos, ui
from motor.cena import Cena, desenhar_cenario


class Tutorial(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        # Mesmo formato do último cartão da introdução, mas o texto já aparece inteiro.
        self.caixa = ui.CaixaTexto(TUTORIAL["texto"], 1300, (800, 460), ancora="centro",
                                   tamanho=30, max_linhas=14)
        self.botao_voltar = ui.Botao(TUTORIAL["voltar"], (800, 830), largura_minima=260)

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_RETURN,
                                                             pygame.K_KP_ENTER):
            self.jogo.ir_para("menu")
        elif self.botao_voltar.clicado(evento):
            self.jogo.ir_para("menu")

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        self.botao_voltar.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, TUTORIAL["fundo"], "noite", self.tempo)
        efeitos.escurecer(tela, 140)

    def desenhar_interface(self, tela):
        self.caixa.desenhar(tela)
        ui.texto_simples(tela, TUTORIAL["titulo"], (800, self.caixa.rect.top - 55),
                         config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito")
        self.botao_voltar.desenhar(tela)
