# Por dentro de uma oca: mostra quem de fora dorme nela esta noite. "Sair da oca" (a seta embaixo,
# como a da entrada da aldeia) volta à aldeia. O texto do painel some depois de alguns segundos,
# para o jogador olhar a oca.
#
# A oca é a de jogo.oca_atual (a aldeia escolhe antes de entrar). Quem dorme em cada oca:
# dados/aldeia.py, ONDE_DORME. Quem o jogador levou ao tapiri, na fogueira, não dorme na oca:
# fica dentro do tapiri (o "tapiri" de OCAS, com os lugares de ONDE_DORME_TAPIRI).
#
# Quem morreu da febre na noite passada fica no lugar onde dormia, coberto com a esteira de
# amaldiçoado (estado.corpos, motor/febre.py), durante o dia e a noite seguintes.
#
# De dia, quem acabou de entrar na aldeia espera dentro da oca (as "pessoas" com "oca" no
# passo "aldeia" de dados/dias.py): clicar nela abre a conversa e, no fim, volta para a oca.

import pygame

import config
from dados.aldeia import OCA, OCAS, ONDE_DORME, ONDE_DORME_TAPIRI
from dados.textos import DIA
from motor import efeitos, ui
from motor.cena import Cena, desenhar_cenario
from motor.pessoas import PessoaNoCenario, corpo_no_cenario, falta_conversar
from motor.tabua import Tabua

CENTRO_PAINEL = (1180, 150)       # meio da borda de cima do painel
CENTRO_PAINEL_ESQUERDA = (420, 150)   # oca com "painel": "esquerda" (dados/aldeia.py)
SEGUNDOS_DO_TEXTO = 5             # o painel com o nome e o texto fica na tela só esse tempo...
SEGUNDOS_PARA_SUMIR = 1.0         # ...e depois some aos poucos
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
        self.centro_painel = CENTRO_PAINEL_ESQUERDA if self.oca.get("painel") == "esquerda" else CENTRO_PAINEL

        # Quem de fora dorme nesta oca (na ordem em que entrou na aldeia), menos quem está no tapiri.
        # No tapiri, ao contrário: só quem o jogador levou para lá.
        self.no_tapiri = bool(self.oca.get("tapiri"))
        if self.no_tapiri:
            self.lugares = ONDE_DORME_TAPIRI
            self.pessoas = [(quem, ONDE_DORME_TAPIRI[quem]["imagem"]) for quem in estado.tapiri
                            if quem in ONDE_DORME_TAPIRI]
        else:
            self.lugares = ONDE_DORME
            self.pessoas = [(quem, ONDE_DORME[quem]["imagem"]) for quem in estado.dentro
                            if ONDE_DORME.get(quem, {}).get("oca") == self.nome and quem not in estado.tapiri]

        # De dia: quem está esperando aqui dentro, para conversar.
        self.na_oca = []
        self.sobre_pessoa = None
        if self.de_dia:
            passo = jogo.dia_pausado.passo_aldeia or {}
            self.na_oca = [self._sentada(p["nome"]) for p in passo.get("pessoas", [])
                           if p.get("oca") == self.nome]

        if self.de_dia:
            # Quem espera para conversar aparece uma vez só (clicável); os outros que dormem aqui
            # aparecem parados.
            nomes = " e ".join(pessoa.nome for pessoa in self.na_oca)
            self.pessoas = [(quem, imagem) for quem, imagem in self.pessoas
                            if quem not in [pessoa.nome for pessoa in self.na_oca]]
            if nomes:
                texto = OCA["aqui_dia_varios" if len(self.na_oca) > 1 else "aqui_dia"] % nomes
            elif self.pessoas:
                chave = "dormem_dia" if len(self.pessoas) > 1 else "dorme_dia"
                texto = OCA[chave] % " e ".join(quem for quem, _ in self.pessoas)
            else:
                texto = OCA["vazio_tapiri"] if self.no_tapiri else OCA["vazia_dia"]
        elif self.pessoas:
            chave = "dormem" if len(self.pessoas) > 1 else "dorme"
            texto = OCA[chave] % " e ".join(quem for quem, _ in self.pessoas)
        else:
            texto = OCA["vazio_tapiri"] if self.no_tapiri else OCA["vazia"]
        # Quem morreu da febre aqui na noite passada: o corpo, onde a pessoa dormia.
        onde = "tapiri" if self.no_tapiri else self.nome
        corpos = [corpo for corpo in estado.corpos if corpo["onde"] == onde and corpo["noite"] == estado.dia - 1]
        self.corpos = [corpo_no_cenario(corpo, self.filtro) for corpo in corpos]
        if corpos:
            nomes = [corpo["nome"] for corpo in corpos]
            frase = OCA["corpos" if len(nomes) > 1 else "corpo"] % " e ".join(nomes)
            texto = frase if texto in (OCA["vazio_tapiri"], OCA["vazia"], OCA["vazia_dia"]) else frase + " " + texto
        # Quem dorme aqui e não está esperando para conversar: sentado no lugar dele, parado.
        self.paradas = [self._sentada(quem) for quem, _ in self.pessoas]
        self.titulo = ui.CaixaTexto(self.oca["nome"], LARGURA_PAINEL, self.centro_painel, ancora="topo",
                                    tamanho=config.TAMANHO_SUBTITULO, nome_fonte="serif_negrito",
                                    alinhamento="centro", fundo=False, margem=20)
        self.caixa = ui.CaixaTexto(texto, LARGURA_PAINEL, (0, 0), ancora="topo",
                                   tamanho=30, alinhamento="centro", fundo=False, margem=24, max_linhas=6)
        self.botao_sair = ui.Seta(OCA["sair_tapiri"] if self.no_tapiri else OCA["sair"])
        self.botao_menu = ui.Botao(DIA["menu"], POSICAO_BOTAO_MENU, tamanho=config.TAMANHO_PEQUENO)
        self.tabua = Tabua(jogo)
        self.painel = pygame.Rect(0, 0, 0, 0)
        self._posicionar()

    def _sentada(self, nome):
        """A pessoa no lugar dela dentro da oca (dados/aldeia.py, ONDE_DORME ou ONDE_DORME_TAPIRI)."""
        lugar = self.lugares[nome]
        # "posicao_com": {"Araci": (x, y)}: com essa pessoa na mesma oca, senta em outro lugar.
        juntos = [quem for quem, _ in self.pessoas] + [pessoa.nome for pessoa in self.na_oca]
        posicao = next((outra for quem, outra in lugar.get("posicao_com", {}).items() if quem in juntos),
                       lugar["posicao"])
        return PessoaNoCenario(nome, lugar["imagem"], posicao, lugar["escala"], self.filtro,
                               espelhar=lugar.get("espelhar", False))

    def _posicionar(self):
        self.titulo.numero_de_linhas()
        self.titulo.rect.midtop = self.centro_painel
        self.caixa.posicao = (self.centro_painel[0], self.titulo.rect.bottom - 16)
        self.caixa.numero_de_linhas()
        self.caixa.rect.midtop = self.caixa.posicao
        self.painel = pygame.Rect(self.centro_painel[0] - LARGURA_PAINEL // 2, self.centro_painel[1],
                                  LARGURA_PAINEL, self.caixa.rect.bottom - self.centro_painel[1])

    def sair(self):
        self.jogo.ir_para("aldeia")

    def alvos(self):
        """Para o teclado: quem está na oca, a seta de sair, o Menu e a tábua."""
        if self.tabua.aberta:
            return self.tabua.alvos()
        # A primeira da lista ganha o clique (_pessoa_no_ponto): as de antes ficam "na frente".
        pessoas = [pessoa.ponto_de_foco(self.na_oca[:i]) for i, pessoa in enumerate(self.na_oca)]
        return ([ponto for ponto in pessoas if ponto]
                + ui.centros(self.botao_sair, self.botao_menu) + self.tabua.alvos())

    def som_ambiente(self):
        return "dia_na_oca" if self.de_dia else "noite_na_oca"

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
                ui.mouse_sobre_botao = True   # a tocha do cursor acende (motor/cursor.py)

    def _pessoa_no_ponto(self, ponto):
        for pessoa in self.na_oca:
            if pessoa.contem(ponto):
                return pessoa
        return None

    def desenhar_cena(self, tela):
        # A oca pode ter uma arte de dia ("dentro_dia") e outra de noite ("dentro").
        dentro = self.oca.get("dentro_dia", self.oca["dentro"]) if self.de_dia else self.oca["dentro"]
        desenhar_cenario(tela, dentro, self.filtro, self.tempo)
        for pessoa in self.corpos + self.paradas + self.na_oca:
            pessoa.desenhar(tela)

    def opacidade_do_texto(self):
        """1 nos primeiros SEGUNDOS_DO_TEXTO; depois cai até 0 (o painel some)."""
        passou = self.tempo - SEGUNDOS_DO_TEXTO
        return max(0.0, min(1.0, 1 - passou / SEGUNDOS_PARA_SUMIR))

    def desenhar_interface(self, tela):
        self.botao_menu.desenhar(tela)
        for pessoa in self.na_oca:
            if pessoa is not self.sobre_pessoa and falta_conversar(self.jogo.estado, pessoa.nome):
                pessoa.desenhar_marca(tela, self.tempo)
        if self.sobre_pessoa:
            self.sobre_pessoa.desenhar_destaque(tela)
        opacidade = self.opacidade_do_texto()
        if opacidade > 0:
            self._posicionar()
            camada = pygame.Surface(config.TAMANHO_LOGICO, pygame.SRCALPHA)
            ui.painel_arredondado(camada, self.painel, config.PRETO + (205,), contorno=config.FUMACA)
            self.titulo.desenhar(camada)
            self.caixa.desenhar(camada)
            camada.set_alpha(int(255 * opacidade))
            tela.blit(camada, (0, 0))
        self.botao_sair.desenhar(tela, self.tempo)
        self.tabua.desenhar(tela)
