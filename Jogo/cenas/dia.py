# O Dia: a fala do pajé, a chegada do visitante na entrada, a conversa, a decisão, o sinal
# do pajé e, depois dele, a noite na fogueira: o jogador clica em quem está sentado em volta
# do fogo para conversar (e, com quem é de fora, examinar o rosto e decidir onde dorme).
#
# A cena só "toca" o roteiro de dados/dias.py (e o da noite, em dados/noites.py), passo a
# passo. Para mudar o que acontece, edite lá; aqui fica só o jeito de mostrar cada tipo de passo.
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
from dados.noites import NOITES
from dados.textos import DIA
from motor import efeitos, fontes, imagens, progresso, ui
from motor.pessoas import PessoaNoCenario
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
CENTRO_DICA_FOGUEIRA = (800, 770)
TOPO_BOTAO_DORMIR = 815
LARGURA_BOTAO_DORMIR = 520


class Dia(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.estado = jogo.estado
        self.roteiro = DIAS[self.estado.dia]
        self.fila = list(self.roteiro["passos"])   # passos que ainda vão acontecer
        self.titulo = self.roteiro["titulo"]
        self.tempo = 0.0
        self.energia = None       # olhares que sobram na noite (None durante o dia)
        self.sinais = {}          # quantos sinais o exame achou em cada pessoa, nesta noite

        self.fundo = ("aldeia", "dia")
        self.fundo_anterior = None
        self.tempo_troca = DURACAO_TROCA_DE_FUNDO
        self.visitante = None
        self.tempo_chegada = DURACAO_CHEGADA

        self.modo = None          # "fala", "perguntas" (também o exame) ou "escolha"
        self.passo_atual = None   # o passo de perguntas, exame ou escolha que está na tela
        self.caixa = None         # a fala que está na tela
        self.quem = ""            # quem está falando
        self.pergunta = ""        # a pergunta que o jogador fez (aparece em cima da resposta)
        self.botoes = []          # [(BlocoOpcao, o que fazer ao clicar)]
        self.perguntas_feitas = set()
        self.apresentados = set()  # exames e escolhas que já mostraram o "texto" de abertura
        self.passo_aldeia = None   # o passo "aldeia" em que o jogador está andando
        self.noite = None          # a noite de dados/noites.py, depois do sinal do pajé
        self.na_fogueira = []      # [PessoaNoCenario] sentados em volta do fogo
        self.conversados = set()   # com quem o jogador já conversou na fogueira, nesta noite
        self.sobre = None          # a pessoa da fogueira embaixo do mouse
        self.botao_dormir = None
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
            self._perguntar(self.passo_atual, indice, _itens(self.passo_atual)[indice])
        elif tipo == "entrada" and self.modo == "aldeia":
            self.voltar_da_aldeia()
        elif tipo == "conversar" and self.modo == "aldeia":
            self.conversar_na_aldeia(acao[1])
        elif tipo == "pessoa" and self.modo == "fogueira":
            self._conversar_na_fogueira(acao[1])
        elif tipo == "dormir" and self.modo == "fogueira":
            self._dormir()
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
                self._trocar_fundo((passo["fundo"], passo.get("filtro", "noite")))
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
            elif tipo == "aldeia":
                self._ir_para_aldeia(passo)
                return
            elif tipo == "noite":
                self._comecar_noite()
                return
            elif tipo == "fogueira":
                self._mostrar_fogueira()
                return
            elif tipo in ("perguntas", "exame"):
                self._mostrar_perguntas(passo)
                return
            elif tipo == "escolha":
                self._mostrar_escolha(passo)
                return
            else:
                raise ValueError("Tipo de passo desconhecido em dados/dias.py: %r" % tipo)
        self.terminar()

    # --- a noite na fogueira ----------------------------------------------------

    def _comecar_noite(self):
        """A noite de dados/noites.py: todos sentam em volta do fogo e o jogador escolhe com quem falar."""
        self.noite = NOITES[self.estado.dia]
        self.titulo = self.noite["titulo"]
        self.energia = self.noite["energia"]
        self._mostrar_fogueira()

    def _pessoas_da_noite(self):
        """Quem está em volta do fogo: o pessoal da aldeia e quem de fora entrou (na ordem do dicionário)."""
        for nome, pessoa in self.noite["pessoas"].items():
            if not pessoa.get("de_fora") or nome in self.estado.dentro:
                yield nome, pessoa

    def _mostrar_fogueira(self):
        self.modo = "fogueira"
        self.caixa = None
        self.botoes = []
        self.visitante = None
        self._trocar_fundo((self.noite["fundo"], "noite"))
        self.na_fogueira = [
            PessoaNoCenario(nome, pessoa["imagem"], pessoa["posicao"], pessoa["escala"], "noite")
            for nome, pessoa in self._pessoas_da_noite()
            if not (pessoa.get("uma_vez") and nome in self.conversados)]
        # "Ir dormir" só abre depois de falar com quem é obrigatório (quem é de fora: decidir onde dorme).
        faltam = [nome for nome, pessoa in self._pessoas_da_noite()
                  if pessoa.get("obrigatorio") and nome not in self.conversados]
        texto = self.noite["dormir_bloqueado"] % " e ".join(faltam) if faltam else self.noite["dormir"]
        self.botao_dormir = ui.BlocoOpcao(texto, LARGURA_BOTAO_DORMIR)
        self.botao_dormir.habilitado = not faltam
        self.botao_dormir.posicionar((config.LARGURA // 2 - LARGURA_BOTAO_DORMIR // 2, TOPO_BOTAO_DORMIR))

    def _conversar_na_fogueira(self, nome):
        self._registrar(["pessoa", nome])
        self.conversados.add(nome)
        self.sobre = None
        # Depois da conversa, volta para a fogueira.
        self.fila[0:0] = self.noite["pessoas"][nome]["passos"] + [{"tipo": "fogueira"}]
        self._proximo()

    def _dormir(self):
        self._registrar(["dormir"])
        self.na_fogueira = []
        self.botao_dormir = None
        self.fila[0:0] = self.noite.get("fim", [])
        self._proximo()

    def _trocar_fundo(self, novo):
        if novo != self.fundo:
            self.fundo_anterior = self.fundo
            self.fundo = novo
            self.tempo_troca = 0.0

    # --- a aldeia de dia --------------------------------------------------------

    def _ir_para_aldeia(self, passo):
        """O jogador anda pela aldeia; esta cena fica guardada e volta pela seta da entrada."""
        self.passo_aldeia = passo
        self.modo = "aldeia"
        self.caixa = None
        self.botoes = []
        if not self.refazendo:
            self.jogo.dia_pausado = self
            self.jogo.ir_para("aldeia")

    def voltar_da_aldeia(self):
        """Chamado pela aldeia (seta da entrada): o roteiro continua na entrada."""
        self._registrar(["entrada"])
        self._proximo()

    def conversar_na_aldeia(self, nome):
        """Chamado pela aldeia (clique numa pessoa): a conversa dela e, depois, a aldeia de novo."""
        self._registrar(["conversar", nome])
        pessoa = next(p for p in self.passo_aldeia["pessoas"] if p["nome"] == nome)
        self.fila[0:0] = pessoa["passos"] + [self.passo_aldeia]
        self._proximo()

    def ao_entrar(self):
        # "Continuar" parado na aldeia de dia: refeito o roteiro, volta direto para a aldeia.
        if self.modo == "aldeia" and self.jogo.dia_pausado is None:
            self.jogo.dia_pausado = self
            self.jogo.ir_para("aldeia")

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
        """Perguntas da conversa ou zonas do exame: cada uma uma vez, e um botão para seguir."""
        self.modo = "perguntas"
        self.passo_atual = passo
        exame = passo["tipo"] == "exame"
        self._apresentar(passo)
        opcoes = []
        for i, item in enumerate(_itens(passo)):
            if (id(passo), i) not in self.perguntas_feitas:
                opcoes.append((item["pergunta"], lambda i=i, item=item: self._perguntar(passo, i, item)))
        botao = passo.get("botao", DIA["terminar_exame"] if exame else DIA["decidir"])
        opcoes.append((botao, self._decidir))
        self._criar_blocos(opcoes)
        if exame and not self.energia:
            # Sem energia, as zonas ficam apagadas: só dá para terminar o exame.
            for bloco, _ in self.botoes[:-1]:
                bloco.habilitado = False

    def _apresentar(self, passo):
        """Exame ou escolha com "texto": na primeira vez, ele aparece no painel (sem nome em cima)."""
        if passo.get("texto") and id(passo) not in self.apresentados:
            self.apresentados.add(id(passo))
            modo = self.modo
            self._mostrar_fala("", passo["texto"])
            self.modo = modo

    def _perguntar(self, passo, indice, item):
        self._registrar(["perguntar", indice])
        self.perguntas_feitas.add((id(passo), indice))
        self._aplicar(item.get("efeitos"))
        if passo["tipo"] == "exame":
            self.energia -= 1
            if item.get("sinal"):
                self.sinais[passo["quem"]] = self.sinais.get(passo["quem"], 0) + 1
        # Uma resposta pode ter várias frases: a primeira aparece agora, as outras em seguida.
        # Depois da resposta, volta para as perguntas que sobraram.
        resposta = item["resposta"]
        frases = [resposta] if isinstance(resposta, str) else list(resposta)
        quem = passo.get("quem", self.quem)
        self.fila[0:0] = [{"tipo": "fala", "quem": quem, "texto": frase} for frase in frases[1:]] + [passo]
        self.botoes = []
        self._mostrar_fala(quem, frases[0], pergunta=item["pergunta"])

    def _decidir(self):
        self._registrar(["decidir"])
        self._proximo()

    def _mostrar_escolha(self, passo):
        self.passo_atual = passo
        self._apresentar(passo)
        self.modo = "escolha"
        self._criar_blocos([(opcao["texto"], lambda i=i: self._escolher(i))
                            for i, opcao in enumerate(passo["opcoes"])])
        # Opção que exige sinais (matar): fica apagada até o exame achar o bastante.
        achados = self.sinais.get(passo.get("quem"), 0)
        for (bloco, _), opcao in zip(self.botoes, passo["opcoes"]):
            if achados < opcao.get("requer_sinais", 0):
                bloco.habilitado = False
                bloco.definir_texto(opcao.get("texto_bloqueado", opcao["texto"]))
        self._posicionar()

    def _escolher(self, indice):
        self._registrar(["escolher", indice])
        opcao = self.passo_atual["opcoes"][indice]
        self._aplicar(opcao.get("efeitos"))
        if opcao.get("entra"):
            self.estado.dentro.append(opcao["entra"])
        if opcao.get("tapiri"):
            self.estado.tapiri.append(opcao["tapiri"])
        if opcao.get("morre"):
            self.estado.dentro.remove(opcao["morre"])
            self.estado.mortos_nomes.append(opcao["morre"])
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
        progresso.salvar("aldeia", self.estado.para_dicionario())
        if not self.refazendo:
            # Depois do sinal do pajé, a noite: o jogador anda pela aldeia e entra nas ocas.
            self.jogo.ir_para("aldeia")

    # --- layout ---------------------------------------------------------------

    def _posicionar(self):
        """Calcula onde ficam o painel da fala e os blocos (muda com o tamanho do texto)."""
        if not self.caixa:
            return
        centro_x = CENTRO_PAINEL_COM_VISITANTE if self.visitante else CENTRO_PAINEL_SOZINHO
        y = TOPO_PAINEL + 16
        if self.quem:   # narração (sem nome) não guarda lugar para o nome
            y += fontes.fonte_escalada("serif_negrito", config.TAMANHO_PEQUENO + 2).get_linesize()
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
        if self.modo == "fogueira":
            if self.botao_dormir.clicado(evento):
                self._dormir()
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                pessoa = self._pessoa_no_ponto(evento.pos)
                if pessoa:
                    self._conversar_na_fogueira(pessoa.nome)
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
        self.sobre = None
        if not self.tabua.aberta:
            self.botao_menu.atualizar(self.jogo.mouse)
            for bloco, _ in self.botoes:
                bloco.atualizar(self.jogo.mouse)
            if self.modo == "fogueira":
                self.botao_dormir.atualizar(self.jogo.mouse)
                self.sobre = self._pessoa_no_ponto(self.jogo.mouse)
                if self.sobre:
                    ui.mouse_sobre_botao = True   # cursor de "mãozinha"

    def _pessoa_no_ponto(self, ponto):
        # A da frente (a última desenhada) ganha.
        for pessoa in reversed(self.na_fogueira):
            if pessoa.contem(ponto):
                return pessoa
        return None

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

        if self.modo == "fogueira":
            for pessoa in self.na_fogueira:
                pessoa.desenhar(tela)

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
        ui.texto_simples(tela, self.titulo, (40, 60), config.TAMANHO_PEQUENO,
                         nome_fonte="mono", cor=config.BARRO, ancora="esquerda")
        if self.energia is not None:
            # A energia da noite, logo abaixo do título: um ponto por olhar.
            pontos = "●" * self.energia + "○" * (NOITES[self.estado.dia]["energia"] - self.energia)
            ui.texto_simples(tela, DIA["energia"] + " " + pontos, (40, 100), config.TAMANHO_PEQUENO,
                             nome_fonte="mono", cor=config.TABATINGA, ancora="esquerda")
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

        if self.modo == "fogueira":
            if self.sobre:
                self.sobre.desenhar_destaque(tela)
            # A dica, sobre um fundo escuro arredondado, e o botão de ir dormir.
            fonte = fontes.fonte_escalada("sans", config.TAMANHO_PEQUENO + 2)
            rect_dica = pygame.Rect((0, 0), fonte.size(self.noite["dica"]))
            rect_dica.center = CENTRO_DICA_FOGUEIRA
            ui.painel_arredondado(tela, rect_dica.inflate(36, 18), config.PRETO + (190,), raio=14)
            ui.texto_simples(tela, self.noite["dica"], rect_dica.center, config.TAMANHO_PEQUENO + 2)
            self.botao_dormir.desenhar(tela)

        # A tábua por último: aberta, ela fica por cima de tudo.
        self.tabua.desenhar(tela)


def _itens(passo):
    """As perguntas de uma conversa ou as zonas de um exame."""
    return passo["zonas"] if passo["tipo"] == "exame" else passo["perguntas"]
