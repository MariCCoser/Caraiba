# Tela de Opções: tamanho do texto (normal / grande), tela cheia, som (ligado / desligado) e
# "Como se joga" (as regras, que voltam para cá). As escolhas ficam salvas.

import pygame

import config
from dados.textos import MENU, OPCOES
from motor import efeitos, sons, ui
from motor.cena import Cena, desenhar_cenario

X_ESQUERDA = 680   # centro do botão da esquerda de cada par
X_DIREITA = 920    # centro do botão da direita
TAMANHO = config.TAMANHO_PEQUENO + 4   # letras dos botões e dos nomes de cada opção
LARGURA = 220      # largura mínima de cada botão do par


class Opcoes(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0

        def botao(texto, centro, largura=LARGURA):
            return ui.Botao(texto, centro, tamanho=TAMANHO, largura_minima=largura)

        self.botao_normal = botao(OPCOES["normal"], (X_ESQUERDA, 205))
        self.botao_grande = botao(OPCOES["grande"], (X_DIREITA, 205))
        self.botao_desligada = botao(OPCOES["desligada"], (X_ESQUERDA, 320))
        self.botao_ligada = botao(OPCOES["ligada"], (X_DIREITA, 320))
        self.botao_som_desligado = botao(OPCOES["som_desligado"], (X_ESQUERDA, 435))
        self.botao_som_ligado = botao(OPCOES["som_ligado"], (X_DIREITA, 435))
        self.botao_tutorial = botao(MENU["tutorial"], (800, 740), largura=300)
        self.botao_voltar = botao(OPCOES["voltar"], (800, 800))

        self.botoes = [self.botao_normal, self.botao_grande, self.botao_desligada,
                       self.botao_ligada, self.botao_som_desligado, self.botao_som_ligado,
                       self.botao_tutorial, self.botao_voltar]

        # O exemplo fica no tamanho das falas do jogo: mostra o efeito de "Grande".
        self.exemplo = ui.CaixaTexto(OPCOES["exemplo"], 1100, (800, 600), ancora="centro",
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
            if not self.jogo.em_tela_cheia():
                self.jogo.alternar_tela_cheia()
        elif self.botao_desligada.clicado(evento):
            if self.jogo.em_tela_cheia():
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
        tela_cheia = self.jogo.em_tela_cheia()
        self.botao_ligada.selecionado = tela_cheia
        self.botao_desligada.selecionado = not tela_cheia
        self.botao_som_ligado.selecionado = preferencias.som
        self.botao_som_desligado.selecionado = not preferencias.som
        for botao in self.botoes:
            botao.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, MENU["fundo"], "noite", self.tempo)
        # Bem mais escuro que o menu: aqui o que importa é ler.
        efeitos.escurecer(tela, 150)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, OPCOES["titulo"], (800, 90), config.TAMANHO_SUBTITULO + 8,
                         nome_fonte="serif_negrito")
        ui.texto_simples(tela, OPCOES["tamanho_texto"], (800, 155), TAMANHO, cor=config.BARRO)
        # No navegador, o F11 é do próprio navegador: o atalho não aparece.
        titulo = OPCOES["tela_cheia_navegador"] if config.NO_NAVEGADOR else OPCOES["tela_cheia"]
        ui.texto_simples(tela, titulo, (800, 270), TAMANHO, cor=config.BARRO)
        ui.texto_simples(tela, OPCOES["som"], (800, 385), TAMANHO, cor=config.BARRO)
        for botao in self.botoes:
            botao.desenhar(tela)
        self.exemplo.desenhar(tela)
