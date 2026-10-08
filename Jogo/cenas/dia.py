# O Dia: a fala do pajé, a chegada do visitante na entrada, a conversa, a decisão e o sinal da noite.
#
# A cena só "toca" o roteiro de dados/dias.py, passo a passo. Para mudar o que acontece
# num dia, edite lá; aqui fica só o jeito de mostrar cada tipo de passo.

import pygame

import config
from dados.dias import DIAS
from dados.textos import DIA
from motor import efeitos, fontes, imagens, ui
from motor.cena import Cena, desenhar_cenario

DURACAO_TROCA_DE_FUNDO = 0.8   # segundos que um cenário leva para se misturar no outro
DURACAO_CHEGADA = 0.9          # segundos que o visitante leva para aparecer
SUBIDA_CHEGADA = 30            # pixels que o visitante sobe enquanto aparece
TECLAS_AVANCAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)

# Onde fica cada coisa na tela 1600x900
CENTRO_VISITANTE_X = 560       # o visitante fica à esquerda; as perguntas, à direita
X_BOTOES = 980                 # borda esquerda da coluna de botões
Y_PRIMEIRO_BOTAO = 290
ESPACO_ENTRE_BOTOES = 72
TAMANHO_BOTAO_DIA = 26
POSICAO_FALA = (800, 870)      # meio da borda de baixo da caixa de fala
LARGURA_FALA = 1400


class Dia(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.estado = jogo.estado
        self.roteiro = DIAS[self.estado.dia]
        self.fila = list(self.roteiro["passos"])   # passos que ainda vão acontecer
        self.tempo = 0.0

        self.fundo = ("aldeia", "dia")
        self.fundo_anterior = None
        self.tempo_troca = DURACAO_TROCA_DE_FUNDO
        self.visitante = None
        self.tempo_chegada = DURACAO_CHEGADA

        self.modo = None          # "fala", "perguntas" ou "escolha"
        self.caixa = None         # a fala que está na tela
        self.quem = ""            # quem está falando
        self.pergunta = ""        # a pergunta que o jogador fez (aparece em cima da resposta)
        self.botoes = []          # [(Botao, o que fazer ao clicar)]
        self.perguntas_feitas = set()

        self.botao_menu = ui.Botao(DIA["menu"], (1490, 60), tamanho=config.TAMANHO_PEQUENO)
        self._proximo()

    # --- tocar o roteiro ----------------------------------------------------

    def _proximo(self):
        """Executa os passos da fila até chegar num que espera o jogador."""
        self.botoes = []
        while self.fila:
            passo = self.fila.pop(0)
            tipo = passo["tipo"]
            if tipo == "fundo":
                novo = (passo["fundo"], passo.get("filtro", "noite"))
                if novo != self.fundo:
                    self.fundo_anterior = self.fundo
                    self.fundo = novo
                    self.tempo_troca = 0.0
            elif tipo == "visitante":
                self.visitante = passo["visitante"]
                self.tempo_chegada = 0.0
            elif tipo == "fala":
                self._mostrar_fala(passo["quem"], passo["texto"])
                return
            elif tipo == "sinal":
                self.estado.caderno.append(passo["texto"])
                self._mostrar_fala(DIA["caderno"], DIA["anotado"] + " " + passo["texto"])
                return
            elif tipo == "perguntas":
                self._mostrar_perguntas(passo)
                return
            elif tipo == "escolha":
                self._mostrar_escolha(passo)
                return
            else:
                raise ValueError("Tipo de passo desconhecido em dados/dias.py: %r" % tipo)
        self.terminar()

    def _mostrar_fala(self, quem, texto, pergunta=""):
        self.modo = "fala"
        self.quem = quem
        self.pergunta = pergunta
        self.caixa = ui.CaixaTexto(texto, LARGURA_FALA, POSICAO_FALA, ancora="baixo", max_linhas=2)
        self.caixa.comecar_digitacao()

    def _criar_botoes(self, opcoes):
        """opcoes: lista de (texto, função). Empilha os botões na coluna da direita."""
        self.botoes = []
        for i, (texto, acao) in enumerate(opcoes):
            botao = ui.Botao(texto, (X_BOTOES, Y_PRIMEIRO_BOTAO + i * ESPACO_ENTRE_BOTOES),
                             tamanho=TAMANHO_BOTAO_DIA, largura_minima=420, alinhamento="esquerda")
            self.botoes.append((botao, acao))

    def _mostrar_perguntas(self, passo):
        self.modo = "perguntas"
        opcoes = []
        for i, item in enumerate(passo["perguntas"]):
            if (id(passo), i) not in self.perguntas_feitas:
                opcoes.append((item["pergunta"], lambda i=i, item=item: self._perguntar(passo, i, item)))
        opcoes.append((DIA["decidir"], self._proximo))
        self._criar_botoes(opcoes)

    def _perguntar(self, passo, indice, item):
        self.perguntas_feitas.add((id(passo), indice))
        self._aplicar(item.get("efeitos"))
        # Depois da resposta, volta para as perguntas que sobraram.
        self.fila.insert(0, passo)
        self.botoes = []
        self._mostrar_fala(self.quem, item["resposta"], pergunta=item["pergunta"])

    def _mostrar_escolha(self, passo):
        self.modo = "escolha"
        self._criar_botoes([(opcao["texto"], lambda opcao=opcao: self._escolher(opcao))
                            for opcao in passo["opcoes"]])

    def _escolher(self, opcao):
        self._aplicar(opcao.get("efeitos"))
        if opcao.get("entra"):
            self.estado.dentro.append(opcao["entra"])
        self.fila[0:0] = opcao.get("passos", [])
        self._proximo()

    def _aplicar(self, efeitos_do_passo):
        for nome, valor in (efeitos_do_passo or {}).items():
            setattr(self.estado, nome, getattr(self.estado, nome) + valor)

    def avancar(self):
        """Clique ou Espaço numa fala: primeiro completa o texto; depois segue o roteiro."""
        if self.modo != "fala":
            return
        if not self.caixa.terminou():
            self.caixa.completar()
        else:
            self._proximo()

    def terminar(self):
        self.modo = None
        self.jogo.ir_para("em_construcao")

    # --- eventos e quadro ---------------------------------------------------

    def tratar_evento(self, evento):
        if self.botao_menu.clicado(evento):
            self.jogo.ir_para("menu")
            return
        for botao, acao in self.botoes:
            if botao.clicado(evento):
                acao()
                return
        if evento.type == pygame.KEYDOWN and evento.key in TECLAS_AVANCAR:
            self.avancar()
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.avancar()

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        self.tempo_troca += dt
        self.tempo_chegada += dt
        if self.caixa:
            self.caixa.atualizar(dt)
        self.botao_menu.atualizar(self.jogo.mouse)
        for botao, _ in self.botoes:
            botao.atualizar(self.jogo.mouse)

    # --- desenho ------------------------------------------------------------

    def desenhar_cena(self, tela):
        apelido, filtro = self.fundo
        if self.fundo_anterior and self.tempo_troca < DURACAO_TROCA_DE_FUNDO:
            desenhar_cenario(tela, *self.fundo_anterior, self.tempo)
            novo = imagens.cenario(apelido, filtro)
            novo.set_alpha(int(255 * self.tempo_troca / DURACAO_TROCA_DE_FUNDO))
            tela.blit(novo, (0, 0))
            novo.set_alpha(None)  # devolve a imagem do cache como estava
        else:
            desenhar_cenario(tela, apelido, filtro, self.tempo)

        if self.visitante:
            pessoa = imagens.personagem(self.visitante, filtro)
            progresso = min(1.0, self.tempo_chegada / DURACAO_CHEGADA)
            rect = pessoa.get_rect(midbottom=(CENTRO_VISITANTE_X,
                                              config.ALTURA + int(SUBIDA_CHEGADA * (1 - progresso))))
            if progresso < 1.0:
                pessoa.set_alpha(int(255 * progresso))
                tela.blit(pessoa, rect)
                # 255, e não None: None desligaria a transparência da imagem (fundo preto).
                pessoa.set_alpha(255)
            else:
                tela.blit(pessoa, rect)

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, self.roteiro["titulo"], (40, 60), config.TAMANHO_PEQUENO,
                         nome_fonte="mono", cor=config.BARRO, ancora="esquerda")
        self.botao_menu.desenhar(tela)

        if self.caixa:
            self.caixa.desenhar(tela)
            topo = self.caixa.rect.top
            # Quem fala, numa etiqueta logo acima da caixa.
            fonte_nome = fontes.fonte_escalada("serif_negrito", config.TAMANHO_PEQUENO + 4)
            nome = fonte_nome.render(self.quem, True, config.TABATINGA)
            etiqueta = pygame.Rect(self.caixa.rect.left, topo - nome.get_height() - 12,
                                   nome.get_width() + 2 * ui.CaixaTexto.MARGEM, nome.get_height() + 12)
            fundo = pygame.Surface(etiqueta.size, pygame.SRCALPHA)
            fundo.fill(config.PRETO + (215,))
            tela.blit(fundo, etiqueta.topleft)
            tela.blit(nome, (etiqueta.left + ui.CaixaTexto.MARGEM, etiqueta.top + 6))
            if self.pergunta:
                # A pergunta do jogador, discreta, ao lado do nome de quem responde.
                ui.texto_simples(tela, "— " + self.pergunta, (etiqueta.right + 16, etiqueta.centery),
                                 config.TAMANHO_PEQUENO, nome_fonte="serif_italico",
                                 cor=config.TABATINGA, ancora="esquerda")
            if self.modo == "fala" and self.caixa.terminou():
                ui.texto_simples(tela, "▸", (self.caixa.rect.right - 24, self.caixa.rect.bottom - 22),
                                 config.TAMANHO_PEQUENO, ancora="centro")

        for botao, _ in self.botoes:
            botao.desenhar(tela)
