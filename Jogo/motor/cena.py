# Cena (uma "tela" do jogo: menu, introdução, fogueira...) e o GerenciadorCenas, que troca de uma para outra com fade.

import pygame

import config
from dados import arte
from motor import efeitos, imagens


class Cena:
    """Modelo de toda cena. Cada cena nova copia este formato e preenche o que precisa.

    O jogo chama, a cada quadro, nesta ordem:
        tratar_evento(evento)  para cada clique/tecla (posição do mouse já em 1600x900)
        atualizar(dt)          dt = segundos desde o quadro anterior
        desenhar(tela)         que por sua vez chama:
            desenhar_cena(tela)       o cenário e as pessoas
            tratamento.aplicar(tela)  linhas, grão, vinheta (se a cena tiver tratamento)
            desenhar_interface(tela)  textos e botões, SEM tratamento (para ficarem legíveis)
    """

    def __init__(self, jogo):
        self.jogo = jogo           # acesso ao jogo: trocar de cena, estado, preferências, mouse
        self.tratamento = None     # um efeitos.Tratamento, ou None para cena sem tratamento

    def ao_entrar(self):
        """Chamado quando a cena aparece (depois do fade). Bom lugar para começar animações."""

    def tratar_evento(self, evento):
        pass

    def atualizar(self, dt):
        if self.tratamento:
            self.tratamento.atualizar(dt)

    def desenhar(self, tela):
        self.desenhar_cena(tela)
        if self.tratamento:
            self.tratamento.aplicar(tela)
        self.desenhar_interface(tela)

    def desenhar_cena(self, tela):
        tela.fill(config.NOITE)

    def desenhar_interface(self, tela):
        pass


class GerenciadorCenas:
    """Guarda a cena atual e faz a troca com um escurecimento rápido (fade) em preto.

    Durante o fade, cliques e teclas são ignorados, para o jogador não clicar
    "sem querer" num botão da cena que está sumindo.
    """

    def __init__(self):
        self.atual = None
        self._proxima = None
        self._fase = None          # None, "saindo" (escurecendo) ou "entrando" (clareando)
        self._tempo = 0.0
        self._veu = pygame.Surface(config.TAMANHO_LOGICO)
        self._veu.fill(config.PRETO)

    def trocar(self, nova_cena, com_fade=True):
        if not com_fade or self.atual is None:
            self.atual = nova_cena
            self._fase = None
            nova_cena.ao_entrar()
            return
        self._proxima = nova_cena
        self._fase = "saindo"
        self._tempo = 0.0

    def em_transicao(self):
        return self._fase is not None

    def tratar_evento(self, evento):
        if self.atual and not self.em_transicao():
            self.atual.tratar_evento(evento)

    def atualizar(self, dt):
        if self._fase == "saindo":
            self._tempo += dt
            if self._tempo >= config.DURACAO_FADE:
                self.atual = self._proxima
                self._proxima = None
                self._fase = "entrando"
                self._tempo = 0.0
                self.atual.ao_entrar()
        elif self._fase == "entrando":
            self._tempo += dt
            if self._tempo >= config.DURACAO_FADE:
                self._fase = None
        if self.atual:
            self.atual.atualizar(dt)

    def desenhar(self, tela):
        if self.atual:
            self.atual.desenhar(tela)
        if self._fase:
            progresso = min(1.0, self._tempo / config.DURACAO_FADE)
            if self._fase == "saindo":
                opacidade = progresso
            else:
                opacidade = 1.0 - progresso
            self._veu.set_alpha(int(255 * opacidade))
            tela.blit(self._veu, (0, 0))


def desenhar_cenario(tela, apelido, filtro, tempo):
    """Desenha um cenário inteiro na tela. Se for de noite e tiver fogueira, a luz pulsa.

    tempo: segundos desde que a cena começou (para a luz do fogo oscilar).
    """
    tela.blit(imagens.cenario(apelido, filtro), (0, 0))
    if filtro == "noite" and apelido in arte.CENTRO_DO_FOGO:
        efeitos.luz_de_fogo(tela, tempo, arte.CENTRO_DO_FOGO[apelido])
