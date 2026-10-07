# Cena provisória do fim da introdução. A próxima etapa troca esta cena pela Manhã do Dia 1.

import pygame

import config
from dados.textos import EM_CONSTRUCAO
from motor import efeitos, ui
from motor.cena import Cena, desenhar_cenario


class EmConstrucao(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        self.botao_voltar = ui.Botao(EM_CONSTRUCAO["voltar"], (800, 640), largura_minima=360)

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
        # O dia usa o filtro frio e dessaturado.
        desenhar_cenario(tela, EM_CONSTRUCAO["fundo"], "dia", self.tempo)
        efeitos.escurecer(tela, 60)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, EM_CONSTRUCAO["titulo"], (800, 360), config.TAMANHO_TITULO // 2,
                         nome_fonte="serif_negrito")
        ui.texto_simples(tela, EM_CONSTRUCAO["texto"], (800, 470), config.TAMANHO_FALA,
                         nome_fonte="serif")
        # Mostra que a partida já tem um Estado novo, pronto para o Dia 1.
        estado = self.jogo.estado
        resumo = "dia %d · vivos %d · sanidade %d" % (estado.dia, estado.vivos, estado.sanidade)
        ui.texto_simples(tela, resumo, (800, 540), config.TAMANHO_PEQUENO, nome_fonte="mono",
                         cor=config.BARRO)
        self.botao_voltar.desenhar(tela)
