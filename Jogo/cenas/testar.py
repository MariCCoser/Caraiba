# Tela "Testar uma noite" (só com config.MODO_TESTE): um botão para cada noite. O clique monta a
# aldeia como se o jogador tivesse chegado até ali deixando todos entrarem (motor/teste.py) e
# começa direto na fogueira daquela noite. Esc ou "Voltar" volta ao menu.

import pygame

import config
from dados.noites import NOITES
from dados.textos import TESTE
from motor import efeitos, teste, ui
from motor.cena import Cena, desenhar_cenario

Y_PRIMEIRA_LINHA = 300
ESPACO_LINHAS = 80
COLUNAS = (560, 1040)   # duas colunas: noites 1 a 5 e 6 a 10


class Testar(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        noites = sorted(NOITES)
        metade = (len(noites) + 1) // 2
        self.botoes = []
        for i, noite in enumerate(noites):
            x = COLUNAS[i // metade]
            y = Y_PRIMEIRA_LINHA + (i % metade) * ESPACO_LINHAS
            self.botoes.append((ui.Botao(TESTE["noite"] % noite, (x, y), largura_minima=320), noite))
        self.botao_voltar = ui.Botao(TESTE["voltar"], (800, 830), largura_minima=260)

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para("menu")
        elif self.botao_voltar.clicado(evento):
            self.jogo.ir_para("menu")
        else:
            for botao, noite in self.botoes:
                if botao.clicado(evento):
                    teste.ir_para_noite(self.jogo, noite)
                    break

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        for botao, _ in self.botoes:
            botao.atualizar(self.jogo.mouse)
        self.botao_voltar.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, TESTE["fundo"], "noite", self.tempo)
        efeitos.escurecer(tela, 150)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, TESTE["titulo"], (800, 120), config.TAMANHO_SUBTITULO + 8,
                         nome_fonte="serif_negrito")
        ui.texto_simples(tela, TESTE["aviso"], (800, 185), config.TAMANHO_PEQUENO, cor=config.BARRO)
        for botao, _ in self.botoes:
            botao.desenhar(tela)
        self.botao_voltar.desenhar(tela)
