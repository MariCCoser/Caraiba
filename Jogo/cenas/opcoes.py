# Tela de Opções: tamanho do texto (normal / grande), tela cheia, som (ligado / desligado) e
# "Como se joga" (as regras, que voltam para cá). As escolhas ficam salvas.

import pygame

import config
from dados.textos import MENU, OPCOES
from motor import efeitos, sons, ui
from motor.cena import Cena, desenhar_cenario

X_ESQUERDA = 640   # centro do botão da esquerda de cada par
X_DIREITA = 960    # centro do botão da direita


class Opcoes(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0

        self.botao_normal = ui.Botao(OPCOES["normal"], (X_ESQUERDA, 235), largura_minima=260)
        self.botao_grande = ui.Botao(OPCOES["grande"], (X_DIREITA, 235), largura_minima=260)
        self.botao_desligada = ui.Botao(OPCOES["desligada"], (X_ESQUERDA, 370), largura_minima=260)
        self.botao_ligada = ui.Botao(OPCOES["ligada"], (X_DIREITA, 370), largura_minima=260)
        self.botao_som_desligado = ui.Botao(OPCOES["som_desligado"], (X_ESQUERDA, 505),
                                            largura_minima=260)
        self.botao_som_ligado = ui.Botao(OPCOES["som_ligado"], (X_DIREITA, 505), largura_minima=260)
        self.botao_tutorial = ui.Botao(MENU["tutorial"], (800, 800), largura_minima=360)
        self.botao_voltar = ui.Botao(OPCOES["voltar"], (800, 865), largura_minima=260)

        if config.NO_NAVEGADOR:
            # No navegador quem controla a tela cheia é a página; mostramos o porquê.
            for botao in (self.botao_desligada, self.botao_ligada):
                botao.habilitado = False
            self.botao_ligada.motivo = OPCOES["motivo_navegador"]

        self.botoes = [self.botao_normal, self.botao_grande, self.botao_desligada,
                       self.botao_ligada, self.botao_som_desligado, self.botao_som_ligado,
                       self.botao_tutorial, self.botao_voltar]

        self.exemplo = ui.CaixaTexto(OPCOES["exemplo"], 1100, (800, 652), ancora="centro",
                                     max_linhas=3)

    def som_ambiente(self):
        return "menu"

    def tratar_evento(self, evento):
        preferencias = self.jogo.preferencias
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para("menu")
        elif self.botao_voltar.clicado(evento):
            self.jogo.ir_para("menu")
        elif self.botao_tutorial.clicado(evento):
            self.jogo.ir_para("tutorial")
        elif self.botao_normal.clicado(evento):
            preferencias.tamanho_texto = "normal"
            preferencias.salvar()
        elif self.botao_grande.clicado(evento):
            preferencias.tamanho_texto = "grande"
            preferencias.salvar()
        elif self.botao_ligada.clicado(evento):
            if not preferencias.tela_cheia:
                self.jogo.alternar_tela_cheia()
        elif self.botao_desligada.clicado(evento):
            if preferencias.tela_cheia:
                self.jogo.alternar_tela_cheia()
        elif self.botao_som_ligado.clicado(evento) or self.botao_som_desligado.clicado(evento):
            preferencias.som = self.botao_som_ligado.clicado(evento)
            preferencias.salvar()
            sons.atualizar_volume()

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        preferencias = self.jogo.preferencias
        # O "●" e o contorno mostram a escolha atual.
        self.botao_normal.selecionado = preferencias.tamanho_texto == "normal"
        self.botao_grande.selecionado = preferencias.tamanho_texto == "grande"
        self.botao_ligada.selecionado = preferencias.tela_cheia
        self.botao_desligada.selecionado = not preferencias.tela_cheia
        self.botao_som_ligado.selecionado = preferencias.som
        self.botao_som_desligado.selecionado = not preferencias.som
        for botao in self.botoes:
            botao.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, MENU["fundo"], "noite", self.tempo)
        # Bem mais escuro que o menu: aqui o que importa é ler.
        efeitos.escurecer(tela, 150)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, OPCOES["titulo"], (800, 85), config.TAMANHO_SUBTITULO + 16,
                         nome_fonte="serif_negrito")
        ui.texto_simples(tela, OPCOES["tamanho_texto"], (800, 175), config.TAMANHO_BOTAO)
        ui.texto_simples(tela, OPCOES["tela_cheia"], (800, 310), config.TAMANHO_BOTAO)
        ui.texto_simples(tela, OPCOES["som"], (800, 445), config.TAMANHO_BOTAO)
        for botao in self.botoes:
            botao.desenhar(tela)
        self.exemplo.desenhar(tela)
