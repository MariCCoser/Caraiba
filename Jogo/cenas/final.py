# O final da partida: três telas, uma depois da outra (clique, Espaço ou "Continuar"):
# 1) a cena: o que aconteceu com a aldeia; 2) o povo real e o fato; 3) a fonte.
# Depois, "Voltar ao menu". Qual final é: jogo.estado.final (veja motor/finais.py).

import pygame

import config
from dados.finais import TELA_FINAL
from motor import efeitos, finais, progresso, ui
from motor.cena import Cena, desenhar_cenario

TECLAS_AVANCAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)
LARGURA_TEXTO = 1150


class Final(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        self.final = finais.por_id(jogo.estado.final)
        progresso.salvar("final", jogo.estado.para_dicionario())
        # Cada tela: (título, texto).
        self.telas = [
            (self.final["nome"], self.final["cena"]),
            (self.final["povo"], TELA_FINAL["povo"] % self.final["povo"] + "\n\n" + self.final["fato"]),
            (TELA_FINAL["fonte"], self.final["fonte"]),
        ]
        self.indice = 0
        self.botao = ui.Botao(TELA_FINAL["seguir"], (800, 830), largura_minima=300)
        self._mostrar()

    def _mostrar(self):
        _, texto = self.telas[self.indice]
        self.caixa = ui.CaixaTexto(texto, LARGURA_TEXTO, (800, 470), ancora="centro",
                                   tamanho=30, alinhamento="centro", max_linhas=10)
        self.caixa.comecar_digitacao()
        ultima = self.indice == len(self.telas) - 1
        self.botao.texto = TELA_FINAL["menu"] if ultima else TELA_FINAL["seguir"]

    def avancar(self):
        if not self.caixa.terminou():
            self.caixa.completar()
        elif self.indice < len(self.telas) - 1:
            self.indice += 1
            self._mostrar()
        else:
            self.jogo.ir_para("menu")

    def tratar_evento(self, evento):
        if self.botao.clicado(evento):
            self.avancar()
        elif evento.type == pygame.KEYDOWN and evento.key in TECLAS_AVANCAR:
            self.avancar()

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        self.caixa.atualizar(dt)
        self.botao.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, TELA_FINAL["fundo"], "noite", self.tempo)
        efeitos.escurecer(tela, 150)

    def desenhar_interface(self, tela):
        titulo, _ = self.telas[self.indice]
        self.caixa.desenhar(tela)
        ui.texto_simples(tela, titulo, (800, self.caixa.rect.top - 60),
                         config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito")
        self.botao.desenhar(tela)
