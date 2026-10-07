# Introdução: cartões de texto que aparecem letra a letra sobre o cenário. Clique/Espaço avança, "Pular" pula tudo.

import pygame

import config
from dados.textos import INTRODUCAO
from motor import efeitos, imagens, ui
from motor.cena import Cena, desenhar_cenario

DURACAO_TROCA_DE_FUNDO = 0.8   # segundos que um cenário leva para se misturar no outro
TECLAS_AVANCAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)


class Introducao(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.cartoes = INTRODUCAO["cartoes"]
        self.indice = 0
        self.tempo = 0.0
        self.fundo_anterior = None      # (apelido, filtro) do cartão anterior, durante a mistura
        self.tempo_troca = DURACAO_TROCA_DE_FUNDO

        self.caixa = ui.CaixaTexto("", 1150, (800, 700), ancora="centro", max_linhas=3)
        self.botao_pular = ui.Botao(INTRODUCAO["pular"], (1490, 60), tamanho=config.TAMANHO_PEQUENO)
        self._mostrar_cartao()

    def _cartao(self):
        return self.cartoes[self.indice]

    def _mostrar_cartao(self):
        self.caixa.definir_texto(self._cartao()["texto"])
        self.caixa.comecar_digitacao()

    def avancar(self):
        """Clique ou Espaço: primeiro completa o texto; se já estava completo, vai para o próximo."""
        if not self.caixa.terminou():
            self.caixa.completar()
            return
        if self.indice + 1 >= len(self.cartoes):
            self.terminar()
            return
        anterior = (self._cartao()["fundo"], self._cartao()["filtro"])
        self.indice += 1
        atual = (self._cartao()["fundo"], self._cartao()["filtro"])
        if atual != anterior:
            self.fundo_anterior = anterior
            self.tempo_troca = 0.0
        self._mostrar_cartao()

    def terminar(self):
        self.jogo.ir_para("em_construcao")

    def tratar_evento(self, evento):
        if self.botao_pular.clicado(evento):
            self.terminar()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.terminar()
        elif evento.type == pygame.KEYDOWN and evento.key in TECLAS_AVANCAR:
            self.avancar()
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.avancar()

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        self.tempo_troca += dt
        self.caixa.atualizar(dt)
        self.botao_pular.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        cartao = self._cartao()
        if self.fundo_anterior and self.tempo_troca < DURACAO_TROCA_DE_FUNDO:
            # Mistura: o cenário anterior por baixo, o novo aparecendo por cima.
            apelido, filtro = self.fundo_anterior
            desenhar_cenario(tela, apelido, filtro, self.tempo)
            novo = imagens.cenario(cartao["fundo"], cartao["filtro"])
            novo.set_alpha(int(255 * self.tempo_troca / DURACAO_TROCA_DE_FUNDO))
            tela.blit(novo, (0, 0))
            novo.set_alpha(None)  # devolve a imagem do cache como estava
        else:
            desenhar_cenario(tela, cartao["fundo"], cartao["filtro"], self.tempo)
        # Escurece um pouco: o cenário é ambiente, quem manda aqui é o texto.
        # (O dia escurece menos, para continuar parecendo dia.)
        efeitos.escurecer(tela, 30 if cartao["filtro"] == "dia" else 70)

    def desenhar_interface(self, tela):
        self.caixa.desenhar(tela)
        self.botao_pular.desenhar(tela)

        # Em que cartão estamos (ex.: 3 / 8), discreto, em fonte monoespaçada.
        contador = "%d / %d" % (self.indice + 1, len(self.cartoes))
        ui.texto_simples(tela, contador, (40, 60), config.TAMANHO_PEQUENO, nome_fonte="mono",
                         cor=config.BARRO, ancora="esquerda")

        if self.caixa.terminou():
            ui.texto_simples(tela, "▸ " + INTRODUCAO["continuar"],
                             (self.caixa.rect.right, self.caixa.rect.bottom + 30),
                             config.TAMANHO_PEQUENO, ancora="direita")
