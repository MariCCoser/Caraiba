# O Dia: a fala do pajé, a chegada do visitante na entrada, a conversa, a decisão e o sinal da noite.
#
# A cena só "toca" o roteiro de dados/dias.py, passo a passo. Para mudar o que acontece
# num dia, edite lá; aqui fica só o jeito de mostrar cada tipo de passo.
#
# Como a tela é montada (modelo: Arte/Exemplo/): a pessoa à esquerda; a fala num painel
# escuro de cantos arredondados ao lado dela; as respostas do jogador em blocos menores,
# logo abaixo da fala. Quando ninguém está na entrada (o pajé falando), o painel fica no meio.
#
# Cada clique do jogador fica guardado (motor/progresso.py), para o botão "Continuar".

import copy

import pygame

import config
from dados.dias import DIAS
from dados.textos import DIA
from motor import efeitos, fontes, imagens, progresso, ui
from motor.cena import Cena, desenhar_cenario
from motor.tabua import Tabua

DURACAO_TROCA_DE_FUNDO = 0.8   # segundos que um cenário leva para se misturar no outro
DURACAO_CHEGADA = 0.9          # segundos que o visitante leva para aparecer
SUBIDA_CHEGADA = 30            # pixels que o visitante sobe enquanto aparece
TECLAS_AVANCAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)

# Onde fica cada coisa na tela 1600x900
CENTRO_VISITANTE_X = 500       # a pessoa fica à esquerda
CENTRO_PAINEL_COM_VISITANTE = 1180
CENTRO_PAINEL_SOZINHO = 800    # sem ninguém na entrada, a fala fica no meio
TOPO_PAINEL = 150
LARGURA_PAINEL = 620
MARGEM_PAINEL = 24
TAMANHO_FALA_DIA = 32
ESPACO_PAINEL_OPCOES = 18      # entre a fala e os blocos de resposta
ESPACO_ENTRE_OPCOES = 14
POSICAO_BOTAO_MENU = (1420, 60)


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
        self.passo_atual = None   # o passo de perguntas ou de escolha que está na tela
        self.caixa = None         # a fala que está na tela
        self.quem = ""            # quem está falando
        self.pergunta = ""        # a pergunta que o jogador fez (aparece em cima da resposta)
        self.botoes = []          # [(BlocoOpcao, o que fazer ao clicar)]
        self.perguntas_feitas = set()
        self.painel = pygame.Rect(0, 0, 0, 0)

        self.botao_menu = ui.Botao(DIA["menu"], POSICAO_BOTAO_MENU, tamanho=config.TAMANHO_PEQUENO)
        self.tabua = Tabua(jogo)

        # Progresso: o Estado no começo do dia + cada ação do jogador, na ordem.
        self.estado_inicio = copy.deepcopy(self.estado.para_dicionario())
        self.acoes = []
        self.refazendo = False
        self._proximo()

        # "Continuar": refaz as ações guardadas, sem animação, até o ponto em que o jogador parou.
        acoes_guardadas = jogo.acoes_para_refazer or []
        jogo.acoes_para_refazer = None
        if acoes_guardadas:
            self.refazendo = True
            for acao in acoes_guardadas:
                self._refazer(acao)
            self.refazendo = False
            if self.caixa:
                self.caixa.completar()
            self.tempo_chegada = DURACAO_CHEGADA
            self.tempo_troca = DURACAO_TROCA_DE_FUNDO
        self._salvar()

    # --- progresso ----------------------------------------------------------

    def _salvar(self):
        progresso.salvar("dia", self.estado_inicio, self.acoes)

    def _registrar(self, acao):
        """Guarda a ação ANTES de executá-la (se ela terminar o dia, o fim do dia salva por cima)."""
        self.acoes.append(acao)
        if not self.refazendo:
            self._salvar()

    def _refazer(self, acao):
        tipo = acao[0]
        if tipo == "seguir" and self.modo == "fala":
            self.acoes.append(acao)
            self._proximo()
        elif tipo == "perguntar" and self.modo == "perguntas":
            indice = acao[1]
            self._perguntar(self.passo_atual, indice, self.passo_atual["perguntas"][indice])
        elif tipo == "decidir" and self.modo == "perguntas":
            self._decidir()
        elif tipo == "escolher" and self.modo == "escolha":
            self._escolher(acao[1])
        else:
            print("Aviso: ação guardada que não cabe mais no roteiro (ignorada):", acao)

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
                self.estado.tabua.append(passo["texto"])
                self.tabua.marcar_nova()
                self._mostrar_fala(DIA["tabua"], DIA["anotado"] + " " + passo["texto"])
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
        self.caixa = ui.CaixaTexto(texto, LARGURA_PAINEL, (0, 0), ancora="topo",
                                   tamanho=TAMANHO_FALA_DIA, alinhamento="centro", fundo=False,
                                   max_linhas=4, margem=MARGEM_PAINEL)
        self.caixa.comecar_digitacao()

    def _criar_blocos(self, opcoes):
        """opcoes: lista de (texto, função). Dois blocos por linha; se sobrar um, ele ocupa a linha toda."""
        self.botoes = []
        meia_largura = (LARGURA_PAINEL - ESPACO_ENTRE_OPCOES) // 2
        for i, (texto, acao) in enumerate(opcoes):
            sozinho_na_linha = (i == len(opcoes) - 1 and i % 2 == 0)
            largura = LARGURA_PAINEL if sozinho_na_linha else meia_largura
            self.botoes.append((ui.BlocoOpcao(texto, largura), acao))
        self._posicionar()

    def _mostrar_perguntas(self, passo):
        self.modo = "perguntas"
        self.passo_atual = passo
        opcoes = []
        for i, item in enumerate(passo["perguntas"]):
            if (id(passo), i) not in self.perguntas_feitas:
                opcoes.append((item["pergunta"], lambda i=i, item=item: self._perguntar(passo, i, item)))
        opcoes.append((DIA["decidir"], self._decidir))
        self._criar_blocos(opcoes)

    def _perguntar(self, passo, indice, item):
        self._registrar(["perguntar", indice])
        self.perguntas_feitas.add((id(passo), indice))
        self._aplicar(item.get("efeitos"))
        # Depois da resposta, volta para as perguntas que sobraram.
        self.fila.insert(0, passo)
        self.botoes = []
        self._mostrar_fala(self.quem, item["resposta"], pergunta=item["pergunta"])

    def _decidir(self):
        self._registrar(["decidir"])
        self._proximo()

    def _mostrar_escolha(self, passo):
        self.modo = "escolha"
        self.passo_atual = passo
        self._criar_blocos([(opcao["texto"], lambda i=i: self._escolher(i))
                            for i, opcao in enumerate(passo["opcoes"])])

    def _escolher(self, indice):
        self._registrar(["escolher", indice])
        opcao = self.passo_atual["opcoes"][indice]
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
            self._registrar(["seguir"])
            self._proximo()

    def terminar(self):
        self.modo = None
        progresso.salvar("em_construcao", self.estado.para_dicionario())
        if not self.refazendo:
            self.jogo.ir_para("em_construcao")

    # --- layout ---------------------------------------------------------------

    def _posicionar(self):
        """Calcula onde ficam o painel da fala e os blocos (muda com o tamanho do texto)."""
        if not self.caixa:
            return
        centro_x = CENTRO_PAINEL_COM_VISITANTE if self.visitante else CENTRO_PAINEL_SOZINHO
        y = TOPO_PAINEL + 16 + fontes.fonte_escalada("serif_negrito", config.TAMANHO_PEQUENO + 2).get_linesize()
        if self.pergunta:
            y += fontes.fonte_escalada("serif_italico", config.TAMANHO_PEQUENO).get_linesize()
        self.caixa.posicao = (centro_x, y - 10)
        self.caixa.numero_de_linhas()            # garante o layout do texto
        self.caixa.rect.midtop = self.caixa.posicao
        self.painel = pygame.Rect(centro_x - LARGURA_PAINEL // 2, TOPO_PAINEL,
                                  LARGURA_PAINEL, self.caixa.rect.bottom - TOPO_PAINEL)

        # Blocos de resposta: duas colunas, embaixo do painel; cada linha com a altura do maior.
        y = self.painel.bottom + ESPACO_PAINEL_OPCOES
        for i in range(0, len(self.botoes), 2):
            linha = [bloco for bloco, _ in self.botoes[i:i + 2]]
            altura = max(bloco.altura() for bloco in linha)
            x = self.painel.left
            for bloco in linha:
                bloco.posicionar((x, y), altura)
                x += bloco.largura + ESPACO_ENTRE_OPCOES
            y += altura + ESPACO_ENTRE_OPCOES

    # --- eventos e quadro ---------------------------------------------------

    def tratar_evento(self, evento):
        if self.tabua.tratar_evento(evento):
            return
        if self.botao_menu.clicado(evento):
            self.jogo.ir_para("menu")
            return
        for bloco, acao in self.botoes:
            if bloco.clicado(evento):
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
        self._posicionar()
        self.tabua.atualizar(dt, self.jogo.mouse)
        if not self.tabua.aberta:
            self.botao_menu.atualizar(self.jogo.mouse)
            for bloco, _ in self.botoes:
                bloco.atualizar(self.jogo.mouse)

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
            progresso_chegada = min(1.0, self.tempo_chegada / DURACAO_CHEGADA)
            rect = pessoa.get_rect(midbottom=(CENTRO_VISITANTE_X,
                                              config.ALTURA + int(SUBIDA_CHEGADA * (1 - progresso_chegada))))
            if progresso_chegada < 1.0:
                pessoa.set_alpha(int(255 * progresso_chegada))
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
            self._posicionar()
            ui.painel_arredondado(tela, self.painel, config.PRETO + (205,), contorno=config.FUMACA)
            # Quem fala, discreto, no alto do painel.
            fonte_nome = fontes.fonte_escalada("serif_negrito", config.TAMANHO_PEQUENO + 2)
            nome = fonte_nome.render(self.quem, True, config.BARRO)
            tela.blit(nome, nome.get_rect(midtop=(self.painel.centerx, self.painel.top + 14)))
            if self.pergunta:
                # A pergunta do jogador, logo abaixo do nome de quem responde.
                ui.texto_simples(tela, "— " + self.pergunta,
                                 (self.painel.centerx, self.painel.top + 18 + nome.get_height()
                                  + fontes.fonte_escalada("serif_italico", config.TAMANHO_PEQUENO).get_linesize() // 2),
                                 config.TAMANHO_PEQUENO, nome_fonte="serif_italico", cor=config.TABATINGA)
            self.caixa.desenhar(tela)
            if self.modo == "fala" and self.caixa.terminou():
                ui.texto_simples(tela, "▸", (self.painel.right - 24, self.painel.bottom - 22),
                                 config.TAMANHO_PEQUENO)

        for bloco, _ in self.botoes:
            bloco.desenhar(tela)

        # A tábua por último: aberta, ela fica por cima de tudo.
        self.tabua.desenhar(tela)
