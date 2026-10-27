# Tela de Opções: tamanho do texto (normal / grande), tela cheia, som (ligado / desligado) e
# efeitos visuais (ligados / desligados: grão, linhas, tremor e o pulsar da fogueira) e a
# descrição dos sinais (a legenda em palavras embaixo de cada imagem do exame).
# As escolhas ficam salvas. ("Como se joga" fica no menu principal.)

import pygame

import config
from dados.textos import MENU, OPCOES
from motor import efeitos, sons, ui
from motor.cena import Cena, desenhar_cenario

# Cada opção numa linha: o nome à esquerda (terminando em X_NOMES) e os dois botões à direita.
# Os espaços cabem também com o texto grande (os botões crescem com ele).
X_NOMES = 750       # onde termina o nome de cada opção
X_ESQUERDA = 920    # centro do botão da esquerda de cada par
X_DIREITA = 1230    # centro do botão da direita
TAMANHO = config.TAMANHO_PEQUENO + 4   # letras dos botões e dos nomes de cada opção
LARGURA = 260       # largura mínima de cada botão do par
Y_PRIMEIRA_LINHA = 180   # a linha da primeira opção
ESPACO_LINHAS = 80       # de uma opção para a seguinte


class Opcoes(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0

        def botao(texto, centro, largura=LARGURA):
            return ui.Botao(texto, centro, tamanho=TAMANHO, largura_minima=largura)

        def y_botoes(linha):
            return Y_PRIMEIRA_LINHA + linha * ESPACO_LINHAS

        self.botao_normal = botao(OPCOES["normal"], (X_ESQUERDA, y_botoes(0)))
        self.botao_grande = botao(OPCOES["grande"], (X_DIREITA, y_botoes(0)))
        self.botao_desligada = botao(OPCOES["desligada"], (X_ESQUERDA, y_botoes(1)))
        self.botao_ligada = botao(OPCOES["ligada"], (X_DIREITA, y_botoes(1)))
        self.botao_som_desligado = botao(OPCOES["som_desligado"], (X_ESQUERDA, y_botoes(2)))
        self.botao_som_ligado = botao(OPCOES["som_ligado"], (X_DIREITA, y_botoes(2)))
        self.botao_efeitos_desligados = botao(OPCOES["efeitos_desligados"], (X_ESQUERDA, y_botoes(3)))
        self.botao_efeitos_ligados = botao(OPCOES["efeitos_ligados"], (X_DIREITA, y_botoes(3)))
        self.botao_legendas_desligadas = botao(OPCOES["legendas_desligadas"], (X_ESQUERDA, y_botoes(4)))
        self.botao_legendas_ligadas = botao(OPCOES["legendas_ligadas"], (X_DIREITA, y_botoes(4)))
        self.botao_voltar = botao(OPCOES["voltar"], (800, 810))

        self.botoes = [self.botao_normal, self.botao_grande, self.botao_desligada,
                       self.botao_ligada, self.botao_som_desligado, self.botao_som_ligado,
                       self.botao_efeitos_desligados, self.botao_efeitos_ligados,
                       self.botao_legendas_desligadas, self.botao_legendas_ligadas,
                       self.botao_voltar]

        # O exemplo fica no tamanho das falas do jogo: mostra o efeito de "Grande".
        self.exemplo = ui.CaixaTexto(OPCOES["exemplo"], 1100, (800, 650), ancora="centro",
                                     max_linhas=3)

    def alvos(self):
        return ui.centros(*self.botoes)

    def som_ambiente(self):
        return "menu"

    def tratar_evento(self, evento):
        preferencias = self.jogo.preferencias
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para("menu")
        elif self.botao_voltar.clicado(evento):
            self.jogo.ir_para("menu")
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
        elif self.botao_efeitos_ligados.clicado(evento) or self.botao_efeitos_desligados.clicado(evento):
            preferencias.efeitos = self.botao_efeitos_ligados.clicado(evento)
            preferencias.salvar()
        elif self.botao_legendas_ligadas.clicado(evento) or self.botao_legendas_desligadas.clicado(evento):
            preferencias.legendas = self.botao_legendas_ligadas.clicado(evento)
            preferencias.salvar()

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
        self.botao_efeitos_ligados.selecionado = preferencias.efeitos
        self.botao_efeitos_desligados.selecionado = not preferencias.efeitos
        self.botao_legendas_ligadas.selecionado = preferencias.legendas
        self.botao_legendas_desligadas.selecionado = not preferencias.legendas
        for botao in self.botoes:
            botao.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, MENU["fundo"], "noite", self.tempo)
        # Bem mais escuro que o menu: aqui o que importa é ler.
        efeitos.escurecer(tela, 150)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, OPCOES["titulo"], (800, 90), config.TAMANHO_SUBTITULO + 8,
                         nome_fonte="serif_negrito")
        def nome(texto, linha):
            ui.texto_simples(tela, texto, (X_NOMES, Y_PRIMEIRA_LINHA + linha * ESPACO_LINHAS), TAMANHO,
                             cor=config.BARRO_TEXTO, ancora="direita")

        nome(OPCOES["tamanho_texto"], 0)
        # No navegador, o F11 é do próprio navegador: o atalho não aparece.
        titulo = OPCOES["tela_cheia_navegador"] if config.NO_NAVEGADOR else OPCOES["tela_cheia"]
        nome(titulo, 1)
        nome(OPCOES["som"], 2)
        nome(OPCOES["efeitos"], 3)
        nome(OPCOES["legendas"], 4)
        for botao in self.botoes:
            botao.desenhar(tela)
        self.exemplo.desenhar(tela)
