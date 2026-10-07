# Introdução: cartões de texto que aparecem letra a letra sobre o cenário. Clique/Espaço avança, "Pular" pula tudo.
#
# Os cartões ficam em dados/textos.py (INTRODUCAO). Cartão sem "fundo" é tela preta,
# sem filtros (o aviso de conteúdo). Cartão com "titulo" fica no meio da tela (o aviso e as regras).

import pygame

import config
from dados.textos import INTRODUCAO
from motor import efeitos, imagens, ui
from motor.cena import Cena, desenhar_cenario

DURACAO_TROCA_DE_FUNDO = 0.8   # segundos que um cenário leva para se misturar no outro
TECLAS_AVANCAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)

LARGURA_CAIXA = 1150
POSICAO_CAIXA = (800, 700)             # cartão comum: embaixo, sobre o cenário
POSICAO_CAIXA_COM_TITULO = (800, 480)  # cartão com título: no meio da tela
DISTANCIA_TITULO = 55                  # do meio do título até o topo da caixa


class Introducao(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.cartoes = INTRODUCAO["cartoes"]
        self.indice = 0
        self.tempo = 0.0
        self.fundo_anterior = None      # (apelido, filtro) do cartão anterior, durante a mistura
        self.tempo_troca = DURACAO_TROCA_DE_FUNDO
        self._veu_preto = pygame.Surface(config.TAMANHO_LOGICO)
        self._veu_preto.fill(config.PRETO)

        self.botao_pular = ui.Botao(INTRODUCAO["pular"], (1490, 60), tamanho=config.TAMANHO_PEQUENO)
        self._mostrar_cartao()

    def _cartao(self):
        return self.cartoes[self.indice]

    def _fundo(self, cartao):
        """(apelido, filtro) do cenário do cartão. Apelido None = tela preta."""
        return (cartao.get("fundo"), cartao.get("filtro", "noite"))

    def _mostrar_cartao(self):
        cartao = self._cartao()
        if cartao.get("titulo"):
            posicao = POSICAO_CAIXA_COM_TITULO
        else:
            posicao = POSICAO_CAIXA
        self.caixa = ui.CaixaTexto(cartao["texto"], cartao.get("largura", LARGURA_CAIXA), posicao,
                                   ancora="centro",
                                   tamanho=cartao.get("tamanho", config.TAMANHO_FALA),
                                   alinhamento=cartao.get("alinhamento", "esquerda"),
                                   max_linhas=cartao.get("max_linhas", 3))
        self.caixa.comecar_digitacao()

    def avancar(self):
        """Clique ou Espaço: primeiro completa o texto; se já estava completo, vai para o próximo."""
        if not self.caixa.terminou():
            self.caixa.completar()
            return
        if self.indice + 1 >= len(self.cartoes):
            self.terminar()
            return
        anterior = self._fundo(self._cartao())
        self.indice += 1
        if self._fundo(self._cartao()) != anterior:
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

    def desenhar(self, tela):
        # Igual a Cena.desenhar, mas a tela preta (aviso) fica limpa, sem grão nem vinheta.
        self.desenhar_cena(tela)
        if self._cartao().get("fundo"):
            self.tratamento.aplicar(tela)
        self.desenhar_interface(tela)

    def _desenhar_fundo(self, tela, apelido, filtro):
        if apelido is None:
            tela.fill(config.PRETO)
        else:
            desenhar_cenario(tela, apelido, filtro, self.tempo)

    def desenhar_cena(self, tela):
        apelido, filtro = self._fundo(self._cartao())
        if self.fundo_anterior and self.tempo_troca < DURACAO_TROCA_DE_FUNDO:
            # Mistura: o cenário anterior por baixo, o novo aparecendo por cima.
            self._desenhar_fundo(tela, *self.fundo_anterior)
            if apelido is None:
                novo = self._veu_preto
            else:
                novo = imagens.cenario(apelido, filtro)
            novo.set_alpha(int(255 * self.tempo_troca / DURACAO_TROCA_DE_FUNDO))
            tela.blit(novo, (0, 0))
            novo.set_alpha(None)  # devolve a imagem do cache como estava
        else:
            self._desenhar_fundo(tela, apelido, filtro)
        if apelido is None:
            return
        # Escurece: o cenário é ambiente, quem manda aqui é o texto.
        # O dia escurece menos, para continuar parecendo dia; as regras, mais, para ler bem.
        if self._cartao().get("titulo"):
            efeitos.escurecer(tela, 140)
        elif filtro == "dia":
            efeitos.escurecer(tela, 30)
        else:
            efeitos.escurecer(tela, 70)

    def desenhar_interface(self, tela):
        cartao = self._cartao()
        self.caixa.desenhar(tela)
        if cartao.get("titulo"):
            # A caixa já montou o layout ao desenhar, então rect está certo.
            ui.texto_simples(tela, cartao["titulo"],
                             (800, self.caixa.rect.top - DISTANCIA_TITULO),
                             config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito")
        self.botao_pular.desenhar(tela)

        # Em que cartão estamos (ex.: 3 / 10), discreto, em fonte monoespaçada.
        contador = "%d / %d" % (self.indice + 1, len(self.cartoes))
        ui.texto_simples(tela, contador, (40, 60), config.TAMANHO_PEQUENO, nome_fonte="mono",
                         cor=config.BARRO, ancora="esquerda")

        if self.caixa.terminou():
            ui.texto_simples(tela, "▸ " + INTRODUCAO["continuar"],
                             (self.caixa.rect.right, self.caixa.rect.bottom + 30),
                             config.TAMANHO_PEQUENO, ancora="direita")
