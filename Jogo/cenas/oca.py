# Por dentro de uma oca: mostra quem de fora dorme nela esta noite. "Sair da oca" volta à aldeia.
#
# A oca é a de jogo.oca_atual (a aldeia escolhe antes de entrar). Quem dorme em cada oca:
# dados/aldeia.py, ONDE_DORME. Quem o jogador levou ao tapiri, na fogueira, não dorme na oca.
#
# De dia, quem acabou de entrar na aldeia espera dentro da oca (as "pessoas" com "oca" no
# passo "aldeia" de dados/dias.py): clicar nela abre a conversa e, no fim, volta para a oca.

import pygame

import config
from dados.aldeia import OCA, OCAS, ONDE_DORME
from dados.textos import DIA
from motor import efeitos, imagens, ui
from motor.cena import Cena, desenhar_cenario
from motor.pessoas import PessoaNoCenario
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
        # De dia (o Dia está esperando o jogador voltar pela entrada) ou de noite.
        self.de_dia = jogo.dia_pausado is not None
        self.filtro = "dia" if self.de_dia else "noite"

        # Quem de fora dorme nesta oca (na ordem em que entrou na aldeia), menos quem está no tapiri.
        self.pessoas = [(quem, ONDE_DORME[quem]["imagem"]) for quem in estado.dentro
                        if ONDE_DORME.get(quem, {}).get("oca") == self.nome and quem not in estado.tapiri]

        # De dia: quem está esperando aqui dentro, para conversar.
        self.na_oca = []
        self.sobre_pessoa = None
        if self.de_dia:
            passo = jogo.dia_pausado.passo_aldeia or {}
            self.na_oca = [PessoaNoCenario(p["nome"], p["imagem"], p["posicao"], p["escala"], self.filtro)
                           for p in passo.get("pessoas", []) if p.get("oca") == self.nome]

        if self.de_dia:
            # Quem espera para conversar aparece uma vez só (clicável); os outros que dormem aqui
            # aparecem parados.
            nomes = " e ".join(pessoa.nome for pessoa in self.na_oca)
            self.pessoas = [(quem, imagem) for quem, imagem in self.pessoas
                            if quem not in [pessoa.nome for pessoa in self.na_oca]]
            if nomes:
                texto = OCA["aqui_dia"] % nomes
            elif self.pessoas:
                texto = OCA["dorme_dia"] % " e ".join(quem for quem, _ in self.pessoas)
            else:
                texto = OCA["vazia_dia"]
        elif self.pessoas:
            texto = OCA["dorme"] % " e ".join(quem for quem, _ in self.pessoas)
        else:
            texto = OCA["vazia"]
        self.titulo = ui.CaixaTexto(self.oca["nome"], LARGURA_PAINEL, CENTRO_PAINEL, ancora="topo",
                                    tamanho=config.TAMANHO_SUBTITULO, nome_fonte="serif_negrito",
                                    alinhamento="centro", fundo=False, margem=20)
        self.caixa = ui.CaixaTexto(texto, LARGURA_PAINEL, (0, 0), ancora="topo",
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
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and self._pessoa_no_ponto(evento.pos):
            self.jogo.conversar_no_dia(self._pessoa_no_ponto(evento.pos).nome, voltar_para="oca")
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
            self.sobre_pessoa = self._pessoa_no_ponto(self.jogo.mouse)
            if self.sobre_pessoa:
                ui.mouse_sobre_botao = True   # cursor de "mãozinha"

    def _pessoa_no_ponto(self, ponto):
        for pessoa in self.na_oca:
            if pessoa.contem(ponto):
                return pessoa
        return None

    def desenhar_cena(self, tela):
        # A oca pode ter uma arte de dia ("dentro_dia") e outra de noite ("dentro").
        dentro = self.oca.get("dentro_dia", self.oca["dentro"]) if self.de_dia else self.oca["dentro"]
        desenhar_cenario(tela, dentro, self.filtro, self.tempo)
        # Uma pessoa de cada vez ao lado da outra, da esquerda para a direita.
        for i, (_, imagem) in enumerate(self.pessoas):
            pessoa = imagens.personagem(imagem, self.filtro)
            tela.blit(pessoa, pessoa.get_rect(midbottom=(CENTRO_PESSOA_X + i * 300,
                                                         config.ALTURA + imagens.vazio_embaixo(imagem))))
        for pessoa in self.na_oca:
            pessoa.desenhar(tela)

    def desenhar_interface(self, tela):
        self.botao_menu.desenhar(tela)
        if self.sobre_pessoa:
            self.sobre_pessoa.desenhar_destaque(tela)
        self._posicionar()
        ui.painel_arredondado(tela, self.painel, config.PRETO + (205,), contorno=config.FUMACA)
        self.titulo.desenhar(tela)
        self.caixa.desenhar(tela)
        self.botao_sair.desenhar(tela)
        self.tabua.desenhar(tela)
