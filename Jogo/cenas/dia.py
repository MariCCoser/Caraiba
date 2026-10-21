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
import random

import pygame

import config
from dados.aldeia import TAPIRI
from dados.arte import EM_PE
from dados.dias import DIAS
from dados.febre import DOENTES
from dados.noites import NOITES
from dados.textos import DIA
from motor import efeitos, febre, finais, fontes, imagens, progresso, ui
from motor.pessoas import PessoaNoCenario, corpo_no_cenario
from motor.cena import Cena, desenhar_cenario
from motor.tabua import Tabua

DURACAO_TROCA_DE_FUNDO = 0.8   # segundos que um cenário leva para se misturar no outro
DURACAO_CHEGADA = 0.9          # segundos que o visitante leva para aparecer
SUBIDA_CHEGADA = 30            # pixels que o visitante sobe enquanto aparece
TECLAS_AVANCAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)

# Onde fica cada coisa na tela 1600x900
CENTRO_VISITANTE_X = 500       # a pessoa fica à esquerda
# Quem o Irmão Aleixo leva fica atrás dele, à esquerda (para quem olha) e menor (mais longe).
# O que importa é o rosto: ele fica inteiro, centralizado entre a borda da tela e o corpo do
# Aleixo, mesmo que o resto da pessoa (o cesto de Potira, o arco de Mbaé) saia pela borda.
MARGEM_ROSTO_ACOMPANHANTE = 16   # espaço mínimo entre o rosto e a borda (ou o Aleixo)
ESCALA_ACOMPANHANTE = 0.82
CENTRO_PAINEL_COM_VISITANTE = 1180
CENTRO_PAINEL_SOZINHO = 800    # sem ninguém na entrada, a fala fica no meio
TOPO_PAINEL = 150
LARGURA_PAINEL = 620
MARGEM_PAINEL = 24
TAMANHO_FALA_DIA = 32
ESPACO_PAINEL_OPCOES = 18      # entre a fala e os blocos de resposta
ESPACO_ENTRE_OPCOES = 14
POSICAO_BOTAO_MENU = (1420, 60)
CENTRO_DICA_FOGUEIRA = (800, 850)          # sem a seta de ir dormir, a dica fica embaixo
CENTRO_DICA_FOGUEIRA_SETA = (800, 730)     # com a seta, ela sobe
CENTRO_SETA_DORMIR = (800, 830)
LARGURA_DETALHE = 520          # o olho de perto, embaixo do painel
# Fala que mostra o olho de perto: a caixa de texto fica menor, para o olho caber grande.
LARGURA_PAINEL_DETALHE = 500
TAMANHO_FALA_DETALHE = 25


class Dia(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.estado = jogo.estado
        self.roteiro = DIAS[self.estado.dia]
        # Passos que ainda vão acontecer. O dia começa com as notícias da manhã (a febre).
        manha = [{"tipo": "fala", "quem": "", "texto": frase} for frase in self.estado.manha]
        self.fila = manha + list(self.roteiro["passos"])
        self.titulo = self.roteiro["titulo"]
        self.tempo = 0.0
        self.energia = None       # olhares que sobram na noite (None durante o dia)
        self.energia_max = 0      # olhares da noite inteira (os pontos da tela)
        self.sinais = {}          # quantos sinais o exame achou em cada pessoa, nesta noite
        self.acusado = None       # quem o pajé acusou pelo nome nesta noite (A Água do Batismo)

        self.fundo = ("aldeia", "dia")
        self.fundo_anterior = None
        self.tempo_troca = DURACAO_TROCA_DE_FUNDO
        self.visitante = None
        self.tempo_chegada = DURACAO_CHEGADA
        self.acompanhante = None   # quem o Irmão Aleixo leva: em pé, atrás dele, até ele ir embora
        self.tempo_acompanhante = 0.0

        self.modo = None          # "fala", "perguntas" (também o exame) ou "escolha"
        self.passo_atual = None   # o passo de perguntas, exame ou escolha que está na tela
        self.caixa = None         # a fala que está na tela
        self.quem = ""            # quem está falando
        self.pergunta = ""        # a pergunta que o jogador fez (aparece em cima da resposta)
        self.imagem_fala = None   # o detalhe que a fala mostra (dados/arte.py, DETALHES), ou None
        self.rect_imagem = pygame.Rect(0, 0, 0, 0)
        self.botoes = []          # [(BlocoOpcao, o que fazer ao clicar)]
        self.perguntas_feitas = set()
        self.apresentados = set()  # exames e escolhas que já mostraram o "texto" de abertura
        self.passo_aldeia = None   # o passo "aldeia" em que o jogador está andando
        self.voltar_para = None    # depois de uma conversa de dia: "aldeia" ou "oca" (onde ela começou)
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
        self.construindo = True    # o roteiro começa a tocar antes de a cena aparecer
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
        self.construindo = False
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
                if self.visitante is None:
                    self.acompanhante = None   # quem ia com o visitante some com ele
                self.tempo_chegada = 0.0
            elif tipo == "fala":
                self._mostrar_fala(passo["quem"], passo["texto"])
                return
            elif tipo == "sinal":
                self.estado.tabua.append(passo["texto"])
                self.estado.tabua_noites.append(self.estado.dia)
                self.tabua.marcar_nova()
                self._mostrar_fala(DIA["tabua"], DIA["anotado"] + " " + passo["texto"])
                return
            elif tipo == "aldeia":
                self._ir_para_aldeia(passo)
                return
            elif tipo == "se":
                if self._condicao(passo):
                    self.fila[0:0] = passo["passos"]
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
            elif tipo == "aleixo_leva":
                self._aleixo_leva(passo)
                return
            else:
                raise ValueError("Tipo de passo desconhecido em dados/dias.py: %r" % tipo)
        self.terminar()

    def _condicao(self, item):
        """Passo "se", pergunta, zona do exame ou "condicao" de uma opção: só aparece se bate.

        "dentro", "se_dentro", "morto", "morto_ontem" (morto na noite passada), "tapiri" e
        "na_oca" levam o nome de quem é de fora;
        "amaldicoado" e "sao" levam o nome de um doente de fora (motor/febre.py);
        "amaldicoados_ao_menos": 2 e "amaldicoados_menos_de": 2 contam quantos amaldiçoados há
        na aldeia (motor/febre.py, quantos_amaldicoados); "levou_alguem": True (o Irmão Aleixo já
        levou alguém); "entregue": "Yara" (o Irmão Aleixo levou essa pessoa, entregue ou não);
        "ao_menos": {"krenan_volta": 1} (variáveis do estado.py com pelo menos esse valor);
        "no_maximo": {"recusas_aleixo": 1} (variáveis do estado.py com no máximo esse valor);
        "com_febre" e "sem_febre" levam o nome de quem pegou a febre na oca e mostra
        (motor/febre.py, mostra_febre); "noites_na_oca_ao_menos": {"Mbaé": 3} e
        "noites_na_oca_menos_de": {"Mbaé": 3} contam as noites que a pessoa dormiu na oca.
        """
        estado = self.estado
        if "morto_ontem" in item and estado.mortos_quando.get(item["morto_ontem"]) != estado.dia - 1:
            return False
        if "na_oca" in item and (item["na_oca"] not in estado.dentro or item["na_oca"] in estado.tapiri):
            return False
        if "amaldicoado" in item and not febre.amaldicoado(estado, item["amaldicoado"]):
            return False
        if "sao" in item and febre.amaldicoado(estado, item["sao"]):
            return False
        if "com_febre" in item and not febre.mostra_febre(estado, item["com_febre"]):
            return False
        if "sem_febre" in item and febre.mostra_febre(estado, item["sem_febre"]):
            return False
        for nome, minimo in item.get("noites_na_oca_ao_menos", {}).items():
            if estado.noites_na_oca.get(nome, 0) < minimo:
                return False
        for nome, minimo in item.get("noites_na_oca_menos_de", {}).items():
            if estado.noites_na_oca.get(nome, 0) >= minimo:
                return False
        if item.get("levou_alguem") and not estado.entregues_nomes:
            return False
        if "entregue" in item and item["entregue"] not in estado.entregues_nomes:
            return False
        for nome, valor in item.get("ao_menos", {}).items():
            if getattr(estado, nome) < valor:
                return False
        for nome, valor in item.get("no_maximo", {}).items():
            if getattr(estado, nome) > valor:
                return False
        if "amaldicoados_ao_menos" in item and febre.quantos_amaldicoados(estado) < item["amaldicoados_ao_menos"]:
            return False
        if "amaldicoados_menos_de" in item and febre.quantos_amaldicoados(estado) >= item["amaldicoados_menos_de"]:
            return False
        if "dentro" in item and item["dentro"] not in estado.dentro:
            return False
        if "se_dentro" in item and item["se_dentro"] not in estado.dentro:
            return False
        if "morto" in item and item["morto"] not in estado.mortos_nomes:
            return False
        if "tapiri" in item and item["tapiri"] not in estado.tapiri:
            return False
        return True

    # --- a noite na fogueira ----------------------------------------------------

    def _comecar_noite(self):
        """A noite de dados/noites.py: todos sentam em volta do fogo e o jogador escolhe com quem falar."""
        self.noite = NOITES[self.estado.dia]
        self.acusado = None
        self._liberar_tapiri()
        self.titulo = self.noite["titulo"]
        # "energia_extra": +1 olhar para cada variável do estado.py que já chegou ao valor pedido.
        extra = sum(1 for nome, valor in self.noite.get("energia_extra", {}).items()
                    if getattr(self.estado, nome) >= valor)
        # "energia_hoje": a mais só nesta noite (negar o pedido do Irmão Aleixo, dados/dias.py).
        self.energia_max = self.noite["energia"] + extra + self.estado.energia_hoje
        self.energia = self.energia_max
        self._mostrar_fogueira()

    def _pessoas_da_noite(self):
        """Quem está em volta do fogo: o pessoal da aldeia e quem de fora entrou (na ordem do
        dicionário). Quem está no tapiri fica lá, isolado: não vem para a fogueira."""
        estado = self.estado
        for nome, pessoa in self.noite["pessoas"].items():
            if pessoa.get("de_fora") and (nome not in estado.dentro or nome in estado.tapiri):
                continue
            # Quem só vem se o jogador o chamou para a fogueira (Krenan).
            if pessoa.get("convidado") and nome not in estado.convidados:
                continue
            # Quem só vem se a "condicao" bate (ex.: Krenan volta na noite 10).
            if "condicao" in pessoa and not self._condicao(pessoa["condicao"]):
                continue
            # Quem morreu ou foi levado pelo Aleixo também não vem.
            if nome in estado.mortos_nomes or nome in estado.entregues_nomes:
                continue
            yield nome, pessoa

    def _liberar_tapiri(self):
        """Quem já passou TAPIRI["noites"] noites no tapiri volta para a oca: a vaga abre."""
        for nome in list(self.estado.tapiri):
            desde = self.estado.tapiri_desde.get(nome, 0)
            if self.estado.dia - desde >= TAPIRI["noites"]:
                self.estado.tapiri.remove(nome)
                self.estado.tapiri_desde.pop(nome, None)

    def _tapiri_cheio(self):
        return len(self.estado.tapiri) >= TAPIRI["vagas"]

    def _lugar_na_fogueira(self, nome):
        """Onde a pessoa senta na fogueira desta noite: {"posicao", "escala", "espelhar"}.
        "posicao_com": ela muda de lugar se outra está na fogueira nesta noite (mesmo que já
        tenha ido dormir: o lugar não muda no meio da noite)."""
        pessoa = self.noite["pessoas"][nome]
        da_noite = [outro for outro, _ in self._pessoas_da_noite()]
        posicao = next((lugar for outro, lugar in pessoa.get("posicao_com", {}).items() if outro in da_noite),
                       pessoa["posicao"])
        return {"posicao": posicao, "escala": pessoa["escala"], "espelhar": pessoa.get("espelhar", False)}

    def _corpos_na_fogueira(self):
        """De noite, quem o jogador matou nesta fogueira; de manhã, na fogueira, o da noite passada."""
        noite = self.estado.dia if self.modo == "fogueira" else self.estado.dia - 1
        filtro = "noite" if self.modo == "fogueira" else self.fundo[1]
        corpos = [corpo for corpo in self.estado.corpos if corpo["onde"] == "fogueira" and corpo["noite"] == noite]
        chave = (noite, filtro, tuple(corpo["nome"] for corpo in corpos))
        if getattr(self, "_chave_corpos", None) != chave:   # monta as imagens só quando muda
            self._chave_corpos = chave
            self._corpos = [corpo_no_cenario(corpo, filtro) for corpo in corpos]
        return self._corpos

    def _mostrar_fogueira(self):
        self.modo = "fogueira"
        self.caixa = None
        self.botoes = []
        self.visitante = None
        self._trocar_fundo((self.noite["fundo"], "noite"))
        # Quem tem "atras": True senta mais longe: é desenhado antes (os outros ficam na frente).
        pessoas = [(nome, pessoa) for nome, pessoa in self._pessoas_da_noite()
                   if not (pessoa.get("uma_vez") and nome in self.conversados)]
        pessoas.sort(key=lambda item: 0 if item[1].get("atras") else 1)
        # "posicao_com": a pessoa muda de lugar se outra está na fogueira nesta noite (mesmo que
        # já tenha ido dormir: o lugar não muda no meio da noite).
        self.na_fogueira = [
            PessoaNoCenario(nome, pessoa["imagem"], self._lugar_na_fogueira(nome)["posicao"],
                            pessoa["escala"], "noite", espelhar=pessoa.get("espelhar", False))
            for nome, pessoa in pessoas]
        # A seta "Ir dormir" só aparece depois de falar com quem é obrigatório (quem é de fora:
        # decidir onde dorme) e de gastar toda a energia. Se não sobrou ninguém para examinar,
        # ela aparece mesmo com energia (senão o jogador ficaria preso na fogueira).
        faltam = [nome for nome, pessoa in self._pessoas_da_noite()
                  if pessoa.get("obrigatorio") and nome not in self.conversados]
        da_para_examinar = any(passo["tipo"] == "exame"
                               for pessoa in self.na_fogueira
                               for passo in self.noite["pessoas"][pessoa.nome]["passos"])
        self.botao_dormir = ui.Seta(self.noite["dormir"], CENTRO_SETA_DORMIR)
        self.botao_dormir.visivel = not faltam and (self.energia <= 0 or not da_para_examinar)

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
        # A febre passa no fim da noite, entre quem dorme nas ocas (motor/febre.py): primeiro
        # quem pegou numa noite anterior (nas noites com amaldiçoados), depois os doentes de fora.
        if self.noite.get("amaldicoados"):
            febre.passar_na_oca(self.estado)
        # Quem é de fora e não está no tapiri dormiu na oca (o olho de Mbaé piora com as noites).
        for nome in self.estado.dentro:
            if nome not in self.estado.tapiri:
                self.estado.noites_na_oca[nome] = self.estado.noites_na_oca.get(nome, 0) + 1
        for nome in list(self.estado.dentro):
            febre.pegar(self.estado, nome)
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
        destino = self.voltar_para or "aldeia"
        self.voltar_para = None
        # Se o dia já começa na aldeia, a cena ainda nem apareceu: ao_entrar leva até lá.
        if not self.refazendo and not self.construindo:
            self.jogo.dia_pausado = self
            self.jogo.ir_para(destino)

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
        # "Continuar" parado na aldeia de dia (ou um dia que começa na aldeia): volta direto para ela.
        if self.modo == "aldeia" and self.jogo.dia_pausado is None:
            self.jogo.dia_pausado = self
            self.jogo.ir_para("aldeia")

    def _mostrar_fala(self, quem, texto, pergunta="", imagem=None):
        self.modo = "fala"
        self.quem = quem
        self.pergunta = pergunta
        self.imagem_fala = imagem
        largura = LARGURA_PAINEL_DETALHE if imagem else LARGURA_PAINEL
        tamanho = TAMANHO_FALA_DETALHE if imagem else TAMANHO_FALA_DIA
        self.caixa = ui.CaixaTexto(texto, largura, (0, 0), ancora="topo",
                                   tamanho=tamanho, alinhamento="centro", fundo=False,
                                   max_linhas=4, margem=MARGEM_PAINEL)
        self.caixa.comecar_digitacao()

    def _criar_blocos(self, opcoes):
        """opcoes: lista de (texto, função). Dois blocos por linha; se sobrar um, ele ocupa a linha toda."""
        self.botoes = []
        # O olho de perto é grande: quando os botões aparecem, ele sai (já foi visto durante a fala)
        # e a fala volta ao tamanho de sempre, alinhada com os botões.
        if self.imagem_fala:
            self.imagem_fala = None
            self.caixa = ui.CaixaTexto(self.caixa.texto, LARGURA_PAINEL, (0, 0), ancora="topo",
                                       tamanho=TAMANHO_FALA_DIA, alinhamento="centro", fundo=False,
                                       max_linhas=4, margem=MARGEM_PAINEL)
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
        liberadas = passo.get("liberadas")   # exame: só estas zonas (sem a lista, todas)
        for i, item in enumerate(_itens(passo)):
            if liberadas is not None and item["pergunta"] not in liberadas:
                continue
            if not self._condicao(item):
                continue
            if "acusa" in item and not self._acusado_da_pergunta(item):
                continue
            if (id(passo), i) not in self.perguntas_feitas:
                opcoes.append((item["pergunta"], lambda i=i, item=item: self._perguntar(passo, i, item)))
        botao = passo.get("botao", DIA["terminar_exame"] if exame else DIA["decidir"])
        opcoes.append((botao, self._decidir))
        self._criar_blocos(opcoes)
        # Zona (ou pergunta com "custo") que custa mais energia do que sobrou fica apagada.
        itens = {item["pergunta"]: item for item in _itens(passo)}
        for bloco, _ in self.botoes[:-1]:
            if _custo(passo, itens[bloco.texto]) > (self.energia or 0):
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
        # Uma "historia" soma os efeitos só na primeira vez (dados/conversas.py).
        historia = item.get("historia")
        if historia not in self.estado.historias:
            self._aplicar(item.get("efeitos"))
            if historia:
                self.estado.historias.append(historia)
        if _custo(passo, item):
            self.energia -= _custo(passo, item)
        if passo["tipo"] == "exame" and item.get("sinal"):
            self.sinais[passo["quem"]] = self.sinais.get(passo["quem"], 0) + 1
        resposta = item.get("resposta")
        if "acusa" in item:
            # O pajé acusa pelo nome: levar essa pessoa ao tapiri nesta noite é seguir o pajé.
            self.acusado, resposta = self._acusado_da_pergunta(item)
        # Uma resposta pode ter várias frases: a primeira aparece agora, as outras em seguida.
        # Depois da resposta, volta para as perguntas que sobraram.
        frases = [resposta] if isinstance(resposta, str) else list(resposta)
        quem = passo.get("quem", self.quem)
        self.fila[0:0] = [{"tipo": "fala", "quem": quem, "texto": frase} for frase in frases[1:]] + [passo]
        if "por_vez" in item:
            self.fila[0:0] = self._passos_da_vez(item["por_vez"])
        self.botoes = []
        # Zona com "imagem": o jogador vê (o olho de perto), em vez de ler uma descrição.
        self._mostrar_fala(quem, frases[0], pergunta=item["pergunta"], imagem=item.get("imagem"))

    def _passos_da_vez(self, por_vez):
        """Pergunta com "por_vez" (o Anhangá, dados/noites.py): a imagem e a frase da vez (o valor
        da variável, já com os efeitos), na tela inteira, sem ninguém na frente. Depois, o
        cenário e quem estava na tela voltam."""
        vezes = por_vez["vezes"]
        vez = vezes[max(0, min(getattr(self.estado, por_vez["variavel"]), len(vezes)) - 1)]
        apelido, filtro = self.fundo
        return [
            {"tipo": "visitante", "visitante": None},
            {"tipo": "fundo", "fundo": vez["fundo"], "filtro": "noite"},
            {"tipo": "fala", "quem": "", "texto": vez["resposta"]},
            {"tipo": "fundo", "fundo": apelido, "filtro": filtro},
            {"tipo": "visitante", "visitante": self.visitante},
        ]

    def _acusado_da_pergunta(self, item):
        """Pergunta com "acusa": [(nome, resposta), ...]: o pajé acusa o primeiro da lista que
        está na fogueira (na aldeia, fora do tapiri). Devolve (nome, resposta), ou None."""
        for nome, resposta in item["acusa"]:
            if nome in self.estado.dentro and nome not in self.estado.tapiri:
                return nome, resposta
        return None

    def _decidir(self):
        self._registrar(["decidir"])
        self._proximo()

    def _mostrar_escolha(self, passo):
        self.passo_atual = passo
        self._apresentar(passo)
        self.modo = "escolha"
        # Opção com "condicao" (ex.: {"dentro": "Yara"}) só aparece se ela bate.
        visiveis = [(i, opcao) for i, opcao in enumerate(passo["opcoes"])
                    if self._condicao(opcao.get("condicao", {}))]
        self._criar_blocos([(opcao["texto"], lambda i=i: self._escolher(i)) for i, opcao in visiveis])
        # Opção que exige sinais (matar): fica apagada até o exame achar o bastante.
        achados = self.sinais.get(passo.get("quem"), 0)
        for (bloco, _), (_, opcao) in zip(self.botoes, visiveis):
            if achados < opcao.get("requer_sinais", 0):
                bloco.habilitado = False
                bloco.definir_texto(opcao.get("texto_bloqueado", opcao["texto"]))
            if opcao.get("tapiri") and self._tapiri_cheio():
                bloco.habilitado = False
                bloco.definir_texto(DIA["tapiri_cheio"])
        self._posicionar()

    def _escolher(self, indice):
        self._registrar(["escolher", indice])
        opcao = self.passo_atual["opcoes"][indice]
        self._aplicar(opcao.get("efeitos"))
        if opcao.get("entra"):
            self.estado.dentro.append(opcao["entra"])
        if opcao.get("tapiri"):
            nome = opcao["tapiri"]
            if nome in DOENTES:
                self.estado.tapiri_usos += 1
            if nome == self.acusado:
                # Seguiu o pajé (A Água do Batismo). Se a pessoa era sã, é um inocente.
                self.estado.seguiu_paje += 1
                if nome not in DOENTES:
                    self.estado.inocentes += 1
            self.estado.tapiri.append(nome)
            self.estado.tapiri_desde[nome] = self.estado.dia
        if opcao.get("convida"):
            self.estado.convidados.append(opcao["convida"])
        if opcao.get("rio_acima"):
            self._subir_o_rio(opcao["rio_acima"])
        if opcao.get("entrega"):
            # Entregue ao Aleixo: sai da aldeia (da oca ou do tapiri) e vai para a vila.
            nome = opcao["entrega"]
            self._sair_da_aldeia(nome)
            self.estado.entregues_nomes.append(nome)
            self._acompanhar(nome)
        if opcao.get("morre"):
            nome = opcao["morre"]
            # O corpo fica coberto com a esteira onde a pessoa sentava, na fogueira.
            if self.noite and nome in self.noite["pessoas"]:
                febre.deixar_corpo(self.estado, nome, self.estado.dia, "fogueira",
                                   self._lugar_na_fogueira(nome), febre.era_amaldicoado(self.estado, nome))
            self._sair_da_aldeia(nome)
            self.estado.mortos_nomes.append(nome)
            self.estado.mortos_quando[nome] = self.estado.dia
        self.fila[0:0] = opcao.get("passos", [])
        self._proximo()

    def _aleixo_leva(self, passo):
        """O Irmão Aleixo leva uma pessoa de fora (na oca ou no tapiri), sorteada: o jogador não
        escolhe. Sem ninguém de fora, ele não leva ninguém. O sorteio usa a semente da partida,
        e o "Continuar" refaz o mesmo."""
        estado = self.estado
        if not estado.dentro:
            self._mostrar_fala("", passo["ninguem"])
            return
        sorte = random.Random("%s:aleixo:%d" % (estado.semente, estado.dia))
        nome = sorte.choice(estado.dentro)
        estado.vivos -= 1
        estado.levados += 1
        self._sair_da_aldeia(nome)
        estado.entregues_nomes.append(nome)
        self._acompanhar(nome)
        self._mostrar_fala("", passo["de_fora"] % nome)

    def _subir_o_rio(self, nome):
        """Krenan leva a pessoa rio acima: ela sai da aldeia, viva. Sã ou amaldiçoada, ele volta
        na noite 10 para levar mais."""
        estado = self.estado
        self._sair_da_aldeia(nome)
        estado.febre = [e for e in estado.febre if e.get("nome") != nome]
        estado.rio_acima_nomes.append(nome)
        estado.rio_acima += 1
        estado.vivos -= 1
        estado.krenan_volta = 1

    def _acompanhar(self, nome):
        """A pessoa que o Irmão Aleixo leva aparece em pé, atrás dele."""
        self.acompanhante = EM_PE.get(nome)
        self.tempo_acompanhante = 0.0

    def _sair_da_aldeia(self, nome):
        if nome in self.estado.dentro:
            self.estado.dentro.remove(nome)
        if nome in self.estado.tapiri:
            self.estado.tapiri.remove(nome)
            self.estado.tapiri_desde.pop(nome, None)

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
        # Fim da noite: a partida pode acabar aqui, antes do dia 10 (motor/finais.py).
        final = finais.fim_da_noite(self.estado) if self.noite else None
        if final:
            self.estado.final = final["id"]
            progresso.salvar("final", self.estado.para_dicionario())
            if not self.refazendo:
                self.jogo.ir_para("final")
            return
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
        self.painel = pygame.Rect(centro_x - self.caixa.largura // 2, TOPO_PAINEL,
                                  self.caixa.largura, self.caixa.rect.bottom - TOPO_PAINEL)

        # O detalhe do exame (o olho de perto) fica logo embaixo do painel; os blocos, embaixo dele.
        y = self.painel.bottom + ESPACO_PAINEL_OPCOES
        if self.imagem_fala:
            imagem = imagens.detalhe(self.imagem_fala, LARGURA_DETALHE)
            self.rect_imagem = imagem.get_rect(midtop=(self.painel.centerx, y))
            y = self.rect_imagem.bottom + ESPACO_PAINEL_OPCOES

        # Blocos de resposta: duas colunas, embaixo do painel; cada linha com a altura do maior.
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
        self.tempo_acompanhante += dt
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
                self.sobre = None if self.botao_dormir.mouse_em_cima else self._pessoa_no_ponto(self.jogo.mouse)
                if self.sobre:
                    ui.mouse_sobre_botao = True   # a tocha do cursor acende (motor/cursor.py)

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

        if self.modo == "fogueira" or apelido == "fogueira_perto":
            # Os corpos ficam no chão, atrás de quem está sentado.
            for corpo in self._corpos_na_fogueira():
                corpo.desenhar(tela)
        if self.modo == "fogueira":
            for pessoa in self.na_fogueira:
                pessoa.desenhar(tela)

        if self.visitante and self.acompanhante:
            self._desenhar_acompanhante(tela, filtro)

        if self.visitante:
            pessoa = imagens.personagem(self.visitante, filtro)
            progresso_chegada = min(1.0, self.tempo_chegada / DURACAO_CHEGADA)
            rect = pessoa.get_rect(midbottom=(CENTRO_VISITANTE_X,
                                              config.ALTURA + imagens.vazio_embaixo(self.visitante)
                                              + int(SUBIDA_CHEGADA * (1 - progresso_chegada))))
            if progresso_chegada < 1.0:
                pessoa.set_alpha(int(255 * progresso_chegada))
                tela.blit(pessoa, rect)
                # 255, e não None: None desligaria a transparência da imagem (fundo preto).
                pessoa.set_alpha(255)
            else:
                tela.blit(pessoa, rect)

    def _desenhar_acompanhante(self, tela, filtro):
        """Quem o Irmão Aleixo leva: atrás dele, menor, aparecendo aos poucos."""
        chave = (self.acompanhante, self.visitante, filtro)
        if getattr(self, "_imagem_acompanhante", (None, None, None))[0] != chave:
            original = imagens.personagem(self.acompanhante, filtro)
            tamanho = (round(original.get_width() * ESCALA_ACOMPANHANTE),
                       round(original.get_height() * ESCALA_ACOMPANHANTE))
            imagem = pygame.transform.smoothscale(original, tamanho)
            vazio = round(imagens.vazio_embaixo(self.acompanhante) * ESCALA_ACOMPANHANTE)
            rect = imagem.get_rect(bottom=config.ALTURA + vazio)
            # O rosto (na tela) fica no meio do espaço livre entre a borda e o corpo do visitante.
            esquerda, direita, topo, baixo = _caixa_do_rosto(imagem)
            limite = self._borda_esquerda_visitante(rect.top + topo, rect.top + baixo, filtro)
            livre_esquerda = MARGEM_ROSTO_ACOMPANHANTE
            livre_direita = limite - MARGEM_ROSTO_ACOMPANHANTE
            rect.x = (livre_esquerda + livre_direita) // 2 - (esquerda + direita) // 2
            # Se o rosto não couber no espaço, ele nunca sai pela borda da tela.
            rect.x = max(rect.x, livre_esquerda - esquerda)
            self._imagem_acompanhante = (chave, imagem, rect)
        _, imagem, rect = self._imagem_acompanhante
        imagem.set_alpha(int(255 * min(1.0, self.tempo_acompanhante / DURACAO_CHEGADA)))
        tela.blit(imagem, rect)

    def _borda_esquerda_visitante(self, topo, baixo, filtro):
        """O x mais à esquerda do corpo do visitante (já parado) entre as alturas topo e baixo."""
        pessoa = imagens.personagem(self.visitante, filtro)
        rect = pessoa.get_rect(midbottom=(CENTRO_VISITANTE_X,
                                          config.ALTURA + imagens.vazio_embaixo(self.visitante)))
        mascara = pygame.mask.from_surface(pessoa).connected_component()
        menor = rect.right
        for y in range(max(topo, rect.top), min(baixo, rect.bottom)):
            for x in range(pessoa.get_width()):
                if mascara.get_at((x, y - rect.top)):
                    menor = min(menor, rect.left + x)
                    break
        return menor

    def desenhar_interface(self, tela):
        ui.texto_simples(tela, self.titulo, (40, 60), config.TAMANHO_PEQUENO,
                         nome_fonte="mono", cor=config.BARRO, ancora="esquerda")
        if self.energia is not None:
            # A energia da noite, logo abaixo do título: um ponto por olhar.
            pontos = "●" * self.energia + "○" * (self.energia_max - self.energia)
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

        if self.caixa and self.imagem_fala:
            # Em cores (a interface não passa pelo filtro da noite): o vermelho do olho aparece.
            tela.blit(imagens.detalhe(self.imagem_fala, LARGURA_DETALHE), self.rect_imagem)
            pygame.draw.rect(tela, config.FUMACA, self.rect_imagem, 2, border_radius=6)

        for bloco, _ in self.botoes:
            bloco.desenhar(tela)

        if self.modo == "fogueira":
            if self.sobre:
                self.sobre.desenhar_destaque(tela)
            # A dica, sobre um fundo escuro arredondado, e a seta de ir dormir (quando ela aparece).
            fonte = fontes.fonte_escalada("sans", config.TAMANHO_PEQUENO + 2)
            rect_dica = pygame.Rect((0, 0), fonte.size(self.noite["dica"]))
            rect_dica.center = CENTRO_DICA_FOGUEIRA_SETA if self.botao_dormir.visivel else CENTRO_DICA_FOGUEIRA
            ui.painel_arredondado(tela, rect_dica.inflate(36, 18), config.PRETO + (190,), raio=14)
            ui.texto_simples(tela, self.noite["dica"], rect_dica.center, config.TAMANHO_PEQUENO + 2)
            self.botao_dormir.desenhar(tela, self.tempo)

        # A tábua por último: aberta, ela fica por cima de tudo.
        self.tabua.desenhar(tela)


def _caixa_do_rosto(imagem):
    """Onde fica a cabeça na imagem: (esquerda, direita, topo, baixo).

    Só conta a parte principal do desenho (fiapos soltos do recorte ficam de fora). O meio da
    cabeça é a faixa mais cheia do alto da pessoa: um arco ou um cesto é fino perto dela. A
    largura é a parte desenhada em volta desse meio, linha a linha, até o queixo."""
    mascara = pygame.mask.from_surface(imagem).connected_component()
    caixa = mascara.get_bounding_rects()[0]
    topo, baixo = caixa.top, caixa.top + caixa.height // 6
    limite = caixa.height // 9       # a cabeça nunca é mais larga que isso para cada lado
    colunas = [sum(mascara.get_at((x, y)) for y in range(topo, baixo, 2))
               for x in range(imagem.get_width())]
    janela = limite
    somas = [sum(colunas[x - janela:x + janela]) for x in range(janela, imagem.get_width() - janela)]
    meio = janela + somas.index(max(somas)) if somas else imagem.get_width() // 2
    esquerda, direita = meio, meio
    for y in range(topo, baixo):
        if not mascara.get_at((meio, y)):
            continue
        x = meio
        while x > max(meio - limite, 0) and mascara.get_at((x - 1, y)):
            x -= 1
        esquerda = min(esquerda, x)
        x = meio
        while x < min(meio + limite, imagem.get_width() - 1) and mascara.get_at((x + 1, y)):
            x += 1
        direita = max(direita, x)
    return esquerda, direita, topo, baixo


def _custo(passo, item):
    """Olhares que a pergunta gasta: cada zona do exame gasta 1 (ou o seu "custo"); uma
    pergunta da conversa só gasta se tiver "custo" (ex.: o barulho na mata, Anhangá)."""
    return item.get("custo", 1 if passo["tipo"] == "exame" else 0)


def _itens(passo):
    """As perguntas de uma conversa ou as zonas de um exame."""
    return passo["zonas"] if passo["tipo"] == "exame" else passo["perguntas"]
