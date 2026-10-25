# Tela "Finais", aberta pelo menu depois do primeiro final visto: os dez finais, na ordem da
# fila. Os já vistos (em qualquer partida) são botões: o clique abre o final de novo, com as três
# telas (cenas/final.py). Os outros aparecem escondidos. Esc ou "Voltar" volta ao menu.

import pygame

import config
from dados.finais import FINAIS, LISTA_FINAIS
from motor import efeitos, finais, ui
from motor.cena import Cena, desenhar_cenario

Y_PRIMEIRO = 230
ESPACO = 62


class Finais(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        vistos = finais.vistos()
        self.total = len(FINAIS)
        self.quantos_vistos = len(vistos)
        # Os vistos: (botão, id). Os outros: (texto, y), escritos apagados, sem botão.
        self.linhas = []
        self.escondidos = []
        for i, final in enumerate(FINAIS):
            numero, y = i + 1, Y_PRIMEIRO + i * ESPACO
            if final["id"] in vistos:
                texto = "%d/%d · %s" % (numero, self.total, final["nome"])
                self.linhas.append((ui.Botao(texto, (800, y), largura_minima=520), final["id"]))
            else:
                self.escondidos.append((LISTA_FINAIS["escondido"] % (numero, self.total), y))
        self.botao_voltar = ui.Botao(LISTA_FINAIS["voltar"], (800, 830), largura_minima=260)

    def abrir(self, identificador):
        self.jogo.final_revendo = identificador
        self.jogo.ir_para("final")

    def tratar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para("menu")
        elif self.botao_voltar.clicado(evento):
            self.jogo.ir_para("menu")
        else:
            for botao, identificador in self.linhas:
                if botao.clicado(evento):
                    self.abrir(identificador)
                    break

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        for botao, _ in self.linhas:
            botao.atualizar(self.jogo.mouse)
        self.botao_voltar.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, LISTA_FINAIS["fundo"], "noite", self.tempo)
        efeitos.escurecer(tela, 150)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, LISTA_FINAIS["titulo"], (800, 100),
                         config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito")
        ui.texto_simples(tela, LISTA_FINAIS["vistos"] % (self.quantos_vistos, self.total),
                         (800, 155), config.TAMANHO_PEQUENO, cor=config.BARRO)
        for botao, _ in self.linhas:
            botao.desenhar(tela)
        for texto, y in self.escondidos:
            ui.texto_simples(tela, texto, (800, y), config.TAMANHO_BOTAO, cor=config.BARRO)
        self.botao_voltar.desenhar(tela)
