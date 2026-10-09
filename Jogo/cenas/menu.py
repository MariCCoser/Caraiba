# Menu inicial: a fogueira ao fundo (luz pulsando), o título e os botões Continuar, Começar,
# Como se joga, Opções e Sair. "Continuar" só aparece se houver uma partida guardada.

import pygame

import config
from dados.textos import MENU
from motor import efeitos, fontes, progresso, ui
from motor.cena import Cena, desenhar_cenario

# Coluna da esquerda, onde ficam título e botões (o fogo fica no meio da imagem).
X_COLUNA = 120
Y_PRIMEIRO_BOTAO = 530
ESPACO_ENTRE_BOTOES = 72


class Menu(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0

        def botao(texto):
            return ui.Botao(texto, (X_COLUNA, 0), largura_minima=320, alinhamento="esquerda")

        self.botao_continuar = botao(MENU["continuar"])
        self.botao_comecar = botao(MENU["comecar"])
        self.botao_tutorial = botao(MENU["tutorial"])
        self.botao_opcoes = botao(MENU["opcoes"])
        self.botao_sair = botao(MENU["sair"])
        # "Continuar" só aparece se houver partida guardada.
        self.botao_continuar.visivel = progresso.existe()
        # No navegador não dá para "fechar o jogo": o botão Sair some.
        self.botao_sair.visivel = not config.NO_NAVEGADOR
        self.botoes = [self.botao_continuar, self.botao_comecar, self.botao_tutorial,
                       self.botao_opcoes, self.botao_sair]
        # Empilha só os visíveis, sem deixar buraco.
        y = Y_PRIMEIRO_BOTAO
        for b in self.botoes:
            if b.visivel:
                b.centro = (X_COLUNA, y)
                y += ESPACO_ENTRE_BOTOES

    def tratar_evento(self, evento):
        # Atalho: Enter começa o jogo.
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.comecar()
        elif self.botao_continuar.clicado(evento):
            self.jogo.continuar()
        elif self.botao_comecar.clicado(evento):
            self.comecar()
        elif self.botao_tutorial.clicado(evento):
            self.jogo.ir_para("tutorial")
        elif self.botao_opcoes.clicado(evento):
            self.jogo.ir_para("opcoes")
        elif self.botao_sair.clicado(evento):
            self.jogo.sair()

    def comecar(self):
        self.jogo.nova_partida()
        self.jogo.ir_para("introducao")

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        for botao in self.botoes:
            botao.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, MENU["fundo"], "noite", self.tempo)

    def desenhar_interface(self, tela):
        # Título com uma sombra preta embaixo: lê-se bem mesmo sobre a parte clara da imagem.
        fonte_titulo = fontes.fonte_escalada("serif_negrito", config.TAMANHO_TITULO)
        sombra = fonte_titulo.render(MENU["titulo"], True, config.PRETO)
        titulo = fonte_titulo.render(MENU["titulo"], True, config.TABATINGA)
        tela.blit(sombra, (X_COLUNA + 5, 150 + 6))
        tela.blit(titulo, (X_COLUNA, 150))

        fonte_sub = fontes.fonte_escalada("serif_italico", config.TAMANHO_SUBTITULO)
        y_sub = 150 + titulo.get_height() + 4
        sombra_sub = fonte_sub.render(MENU["subtitulo"], True, config.PRETO)
        subtitulo = fonte_sub.render(MENU["subtitulo"], True, config.TABATINGA)
        tela.blit(sombra_sub, (X_COLUNA + 8 + 3, y_sub + 3))
        tela.blit(subtitulo, (X_COLUNA + 8, y_sub))

        fonte_chamada = fontes.fonte_escalada("serif_italico", config.TAMANHO_PEQUENO)
        y_chamada = y_sub + subtitulo.get_height() + 14
        sombra_chamada = fonte_chamada.render(MENU["chamada"], True, config.PRETO)
        chamada = fonte_chamada.render(MENU["chamada"], True, config.TABATINGA)
        tela.blit(sombra_chamada, (X_COLUNA + 8 + 2, y_chamada + 2))
        tela.blit(chamada, (X_COLUNA + 8, y_chamada))

        for botao in self.botoes:
            botao.desenhar(tela)

        ui.texto_simples(tela, MENU["rodape"], (config.LARGURA - 40, config.ALTURA - 36),
                         config.TAMANHO_PEQUENO, cor=config.BARRO, ancora="direita")
