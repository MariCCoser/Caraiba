# A aldeia vista de fora: o jogador "anda" clicando nas ocas, como no Purble Place.
#
# Passar o mouse numa oca acende o contorno dela. Clicar numa oca aberta entra nela (cena Oca).
# Quais ocas abrem em cada noite, e onde fica cada uma na imagem: dados/aldeia.py.
#
# De dia (depois da fala do pajé) há uma seta embaixo, para a entrada da aldeia: ela devolve
# o jogador ao Dia, onde chega o visitante. De noite (depois do sinal do pajé) não há seta.

import pygame

import config
from dados.aldeia import ALDEIA, OCAS, ocas_abertas
from dados.textos import DIA
from motor import efeitos, fontes, progresso, ui
from motor.cena import Cena, desenhar_cenario
from motor.tabua import Tabua

POSICAO_BOTAO_MENU = (1420, 60)
CENTRO_SETA = (800, 830)


class Aldeia(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        self.noite = jogo.estado.dia
        self.de_dia = jogo.dia_pausado is not None
        self.filtro = "dia" if self.de_dia else "noite"
        self.abertas = ocas_abertas(self.noite)
        self.sobre = None          # a oca embaixo do mouse (ou None)
        self.sobre_seta = False
        self.rect_seta = pygame.Rect(0, 0, 330, 104)
        self.rect_seta.center = CENTRO_SETA

        # Uma "máscara" por oca: diz, pixel a pixel, se o mouse está dentro do contorno.
        self.mascaras = {}
        for nome, oca in OCAS.items():
            forma = pygame.Surface(config.TAMANHO_LOGICO, pygame.SRCALPHA)
            pygame.draw.polygon(forma, (255, 255, 255, 255), oca["contorno"])
            self.mascaras[nome] = pygame.mask.from_surface(forma)

        self.botao_menu = ui.Botao(DIA["menu"], POSICAO_BOTAO_MENU, tamanho=config.TAMANHO_PEQUENO)
        self.tabua = Tabua(jogo)
        if not self.de_dia:
            # De dia o progresso é o do Dia (que refaz o caminho até aqui).
            progresso.salvar("aldeia", jogo.estado.para_dicionario())

    def _oca_no_ponto(self, ponto):
        x, y = ponto
        if not (0 <= x < config.LARGURA and 0 <= y < config.ALTURA):
            return None
        for nome, mascara in self.mascaras.items():
            if mascara.get_at((x, y)):
                return nome
        return None

    def entrar(self, nome):
        self.jogo.oca_atual = nome
        self.jogo.ir_para("oca")

    def tratar_evento(self, evento):
        if self.tabua.tratar_evento(evento):
            return
        if self.botao_menu.clicado(evento):
            self.jogo.ir_para("menu")
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.de_dia and self.rect_seta.collidepoint(evento.pos):
                self.jogo.voltar_ao_dia()
                return
            nome = self._oca_no_ponto(evento.pos)
            if nome in self.abertas:
                self.entrar(nome)

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        self.tabua.atualizar(dt, self.jogo.mouse)
        if self.tabua.aberta:
            self.sobre = None
            return
        self.botao_menu.atualizar(self.jogo.mouse)
        self.sobre = self._oca_no_ponto(self.jogo.mouse)
        self.sobre_seta = self.de_dia and self.rect_seta.collidepoint(self.jogo.mouse)
        if self.sobre in self.abertas or self.sobre_seta:
            ui.mouse_sobre_botao = True   # cursor de "mãozinha"

    def desenhar_cena(self, tela):
        desenhar_cenario(tela, ALDEIA["fundo"], self.filtro, self.tempo)

    def _rotulo(self, tela, nome, texto, cor_borda):
        """Etiqueta arredondada acima do telhado."""
        topo = self.mascaras[nome].get_bounding_rects()[0].top
        x = OCAS[nome]["contorno"][0][0]
        fonte = fontes.fonte_escalada("sans", config.TAMANHO_PEQUENO)
        imagem = fonte.render(texto, True, config.TABATINGA)
        rect = imagem.get_rect(midbottom=(x, topo - 12))
        if rect.top < 110:
            # Sem espaço acima do telhado (o Menu e a tábua ficam lá): vai para dentro dele.
            rect.top = topo + 110
        rect.right = min(rect.right, config.LARGURA - 24)
        caixa = rect.inflate(28, 14)
        ui.painel_arredondado(tela, caixa, config.PRETO + (200,), raio=12, contorno=cor_borda)
        tela.blit(imagem, rect)

    def desenhar_interface(self, tela):
        titulo = ALDEIA["titulo_dia"] if self.de_dia else ALDEIA["titulo"]
        ui.texto_simples(tela, titulo % self.noite, (40, 60), config.TAMANHO_PEQUENO,
                         nome_fonte="mono", cor=config.BARRO, ancora="esquerda")
        self.botao_menu.desenhar(tela)

        # A oca embaixo do mouse acende: aberta em Urucum, fechada em Fumaça.
        if self.sobre:
            aberta = self.sobre in self.abertas
            luz = pygame.Surface(config.TAMANHO_LOGICO, pygame.SRCALPHA)
            pontos = OCAS[self.sobre]["contorno"]
            if aberta:
                pygame.draw.polygon(luz, config.TABATINGA + (40,), pontos)
            pygame.draw.polygon(luz, (config.URUCUM if aberta else config.FUMACA) + (255,), pontos, 3)
            tela.blit(luz, (0, 0))

        # O nome da oca só aparece quando o mouse passa por cima dela.
        if self.sobre in self.abertas:
            self._rotulo(tela, self.sobre, OCAS[self.sobre]["nome"], config.URUCUM)
        elif self.sobre:
            fechada = ALDEIA["fechada_dia"] if self.de_dia else ALDEIA["fechada"]
            self._rotulo(tela, self.sobre, fechada % OCAS[self.sobre]["nome"], config.FUMACA)

        # A dica, sobre um fundo escuro arredondado (lê bem sobre a mata).
        # De dia ela sobe, para dar lugar à seta.
        dica = ALDEIA["dica_dia"] if self.de_dia else ALDEIA["dica"]
        fonte = fontes.fonte_escalada("sans", config.TAMANHO_PEQUENO + 2)
        rect_dica = pygame.Rect((0, 0), fonte.size(dica))
        rect_dica.center = (800, 730 if self.de_dia else 850)
        ui.painel_arredondado(tela, rect_dica.inflate(36, 18), config.PRETO + (190,), raio=14)
        ui.texto_simples(tela, dica, rect_dica.center, config.TAMANHO_PEQUENO + 2)

        if self.de_dia:
            self._desenhar_seta(tela)

        self.tabua.desenhar(tela)

    def _desenhar_seta(self, tela):
        """Seta para baixo, com o nome do lugar: leva à entrada da aldeia."""
        cor = config.URUCUM if self.sobre_seta else config.FUMACA
        fundo = config.TERRA + (235,) if self.sobre_seta else config.PRETO + (190,)
        ui.painel_arredondado(tela, self.rect_seta, fundo, raio=18, contorno=cor,
                              espessura=3 if self.sobre_seta else 2)
        ui.texto_simples(tela, ALDEIA["seta"], (self.rect_seta.centerx, self.rect_seta.top + 30),
                         config.TAMANHO_PEQUENO + 2)
        # A seta balança um pouco para baixo, chamando o olhar.
        desce = int(4 * abs(((self.tempo * 1.4) % 2) - 1))
        x, y = self.rect_seta.centerx, self.rect_seta.top + 56 + desce
        pygame.draw.polygon(tela, config.TABATINGA, [(x - 26, y), (x + 26, y), (x, y + 28)])
