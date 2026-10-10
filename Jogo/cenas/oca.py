# Por dentro de uma oca: mostra quem de fora dorme nela esta noite. "Sair da oca" volta à aldeia.
#
# A oca é a de jogo.oca_atual (a aldeia escolhe antes de entrar). Quem dorme em cada oca:
# dados/aldeia.py, ONDE_DORME. O exame do rosto, na fogueira, entra na próxima etapa.

import pygame

import config
from dados.aldeia import OCA, OCAS, ONDE_DORME
from dados.textos import DIA
from motor import efeitos, imagens, ui
from motor.cena import Cena, desenhar_cenario
from motor.tabua import Tabua

CENTRO_PESSOA_X = 500
CENTRO_PAINEL = (1180, 150)       # meio da borda de cima do painel
LARGURA_PAINEL = 620
POSICAO_BOTAO_MENU = (1420, 60)


class Oca(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        self.nome = getattr(jogo, "oca_atual", None) or "oca1"
        self.oca = OCAS[self.nome]
        estado = jogo.estado

        # Quem de fora dorme nesta oca (na ordem em que entrou na aldeia).
        self.pessoas = [(quem, ONDE_DORME[quem]["imagem"]) for quem in estado.dentro
                        if ONDE_DORME.get(quem, {}).get("oca") == self.nome]

        if self.pessoas:
            texto = OCA["dorme"] % " e ".join(quem for quem, _ in self.pessoas)
        else:
            texto = OCA["vazia"]
        self.titulo = ui.CaixaTexto(self.oca["nome"], LARGURA_PAINEL, CENTRO_PAINEL, ancora="topo",
                                    tamanho=config.TAMANHO_SUBTITULO, nome_fonte="serif_negrito",
                                    alinhamento="centro", fundo=False, margem=20)
        self.caixa = ui.CaixaTexto(texto + "\n" + OCA["em_breve"], LARGURA_PAINEL, (0, 0), ancora="topo",
                                   tamanho=30, alinhamento="centro", fundo=False, margem=24, max_linhas=6)
        self.botao_sair = ui.BlocoOpcao(OCA["sair"], LARGURA_PAINEL)
        self.botao_menu = ui.Botao(DIA["menu"], POSICAO_BOTAO_MENU, tamanho=config.TAMANHO_PEQUENO)
        self.tabua = Tabua(jogo)
        self.painel = pygame.Rect(0, 0, 0, 0)
        self._posicionar()

    def _posicionar(self):
        self.titulo.numero_de_linhas()
        self.titulo.rect.midtop = CENTRO_PAINEL
        self.caixa.posicao = (CENTRO_PAINEL[0], self.titulo.rect.bottom - 16)
        self.caixa.numero_de_linhas()
        self.caixa.rect.midtop = self.caixa.posicao
        self.painel = pygame.Rect(CENTRO_PAINEL[0] - LARGURA_PAINEL // 2, CENTRO_PAINEL[1],
                                  LARGURA_PAINEL, self.caixa.rect.bottom - CENTRO_PAINEL[1])
        self.botao_sair.posicionar((self.painel.left, self.painel.bottom + 18))

    def sair(self):
        self.jogo.ir_para("aldeia")

    def tratar_evento(self, evento):
        if self.tabua.tratar_evento(evento):
            return
        if self.botao_menu.clicado(evento):
            self.jogo.ir_para("menu")
        elif self.botao_sair.clicado(evento):
            self.sair()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.sair()

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        self._posicionar()
        self.tabua.atualizar(dt, self.jogo.mouse)
        if not self.tabua.aberta:
            self.botao_menu.atualizar(self.jogo.mouse)
            self.botao_sair.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, self.oca["dentro"], "noite", self.tempo)
        # Uma pessoa de cada vez ao lado da outra, da esquerda para a direita.
        for i, (_, imagem) in enumerate(self.pessoas):
            pessoa = imagens.personagem(imagem, "noite")
            tela.blit(pessoa, pessoa.get_rect(midbottom=(CENTRO_PESSOA_X + i * 300, config.ALTURA)))

    def desenhar_interface(self, tela):
        self.botao_menu.desenhar(tela)
        self._posicionar()
        ui.painel_arredondado(tela, self.painel, config.PRETO + (205,), contorno=config.FUMACA)
        self.titulo.desenhar(tela)
        self.caixa.desenhar(tela)
        self.botao_sair.desenhar(tela)
        self.tabua.desenhar(tela)
