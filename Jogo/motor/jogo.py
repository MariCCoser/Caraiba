# O Jogo: abre a janela, escala a tela 1600x900 para ela (com barras pretas), recebe cliques e teclas e roda a cena atual.

import pygame

import config
from estado import Estado
from motor import cursor, efeitos, febre, finais, fontes, imagens, preferencias, progresso, sons, teclado, ui
from motor.cena import GerenciadorCenas

# Todas as cenas do jogo, pelo nome. Para criar uma cena nova:
# 1) crie o arquivo em cenas/; 2) acrescente aqui; 3) use jogo.ir_para("nome").
# (Usar nomes evita que uma cena precise importar a outra.)
from cenas.menu import Menu
from cenas.opcoes import Opcoes
from cenas.introducao import Introducao
from cenas.dia import Dia
from cenas.tutorial import Tutorial
from cenas.aldeia import Aldeia
from cenas.oca import Oca
from cenas.final import Final
from cenas.finais import Finais
from cenas.testar import Testar

CENAS = {
    "menu": Menu,
    "opcoes": Opcoes,
    "introducao": Introducao,
    "dia": Dia,
    "tutorial": Tutorial,
    "aldeia": Aldeia,
    "oca": Oca,
    "final": Final,
    "finais": Finais,
    "testar": Testar,   # só com config.MODO_TESTE
}

# Tamanhos de janela tentados, do maior para o menor (todos 16:9).
TAMANHOS_DE_JANELA = [(1600, 900), (1280, 720), (1024, 576), (960, 540)]


class Jogo:
    def __init__(self, tamanho_janela=None):
        pygame.mixer.pre_init(44100, -16, 2, config.BUFFER_DO_SOM)
        pygame.init()
        pygame.display.set_caption(config.TITULO_JANELA)

        self.preferencias = preferencias.atual
        self.preferencias.carregar()

        self.tamanho_janela = tamanho_janela or self._escolher_tamanho_janela()
        self.janela = None
        self._abrir_janela()

        # A "tela lógica": tudo é desenhado aqui em 1600x900 e só no fim vai para a janela.
        self.tela = pygame.Surface(config.TAMANHO_LOGICO).convert()
        self._tela_escalada = None
        self._area = pygame.Rect(0, 0, *config.TAMANHO_LOGICO)  # onde a tela lógica cai na janela

        self.estado = Estado()
        # Ações guardadas para a cena refazer ao "Continuar" (veja motor/progresso.py).
        self.acoes_para_refazer = None
        # Em que oca o jogador está entrando (a aldeia escolhe, a cena Oca lê).
        self.oca_atual = None
        # O Dia que está esperando o jogador andar pela aldeia (None = aldeia de noite).
        self.dia_pausado = None
        # O final que a tela "Finais" do menu pediu para ler de novo (cenas/final.py), ou None.
        self.final_revendo = None
        # Modo de teste: o próximo Dia começa direto na fogueira (motor/teste.py).
        self.testando_noite = False
        self.relogio = pygame.time.Clock()
        self.mouse = (0, 0)       # posição do mouse já em coordenadas 1600x900
        # Jogar sem mouse: setas/Tab escolhem, Enter/Espaço clicam (motor/teclado.py).
        self.teclado = teclado.Teclado()
        self.rodando = True
        self._cursor_mao = False
        cursor.usar()             # o cursor do mouse é uma tocha (motor/cursor.py)

        efeitos.preparar_texturas()
        imagens.ler_de_antemao()

        self.cenas = GerenciadorCenas()
        self.ir_para("menu", com_fade=False)

    # --- janela ------------------------------------------------------------

    def _escolher_tamanho_janela(self):
        """O maior tamanho 16:9 que cabe na tela do computador (com folga para a barra de tarefas)."""
        if config.NO_NAVEGADOR:
            return config.TAMANHO_LOGICO
        try:
            largura_monitor, altura_monitor = pygame.display.get_desktop_sizes()[0]
        except Exception:
            return (1280, 720)
        for largura, altura in TAMANHOS_DE_JANELA:
            if largura <= largura_monitor - 40 and altura <= altura_monitor - 100:
                return (largura, altura)
        return TAMANHOS_DE_JANELA[-1]

    def _abrir_janela(self):
        if config.NO_NAVEGADOR:
            # No navegador o pygbag cuida do tamanho: a "janela" é sempre 1600x900.
            self.janela = pygame.display.set_mode(config.TAMANHO_LOGICO)
        elif self.preferencias.tela_cheia:
            self.janela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.janela = pygame.display.set_mode(self.tamanho_janela, pygame.RESIZABLE)

    def em_tela_cheia(self):
        """No navegador, pergunta à página (o jogador pode sair com Esc a qualquer hora)."""
        if config.NO_NAVEGADOR:
            try:
                import platform  # no pygbag, "platform" dá acesso ao navegador
                return bool(platform.window.document.fullscreenElement)
            except Exception:
                return False
        return self.preferencias.tela_cheia

    def alternar_tela_cheia(self):
        if config.NO_NAVEGADOR:
            # O navegador só aceita entrar em tela cheia logo depois de um clique (o botão das
            # Opções). Se ele recusar, nada acontece: o jogo segue na página.
            try:
                import platform
                documento = platform.window.document
                if documento.fullscreenElement:
                    documento.exitFullscreen()
                else:
                    documento.documentElement.requestFullscreen()
            except Exception as erro:
                print("Aviso: o navegador não deixou mudar a tela cheia -", erro)
            return
        self.preferencias.tela_cheia = not self.preferencias.tela_cheia
        self.preferencias.salvar()
        self._abrir_janela()

    def _calcular_area(self):
        """Maior retângulo 16:9 que cabe na janela, centralizado (o resto vira barra preta)."""
        largura, altura = self.janela.get_size()
        escala = min(largura / config.LARGURA, altura / config.ALTURA)
        area = pygame.Rect(0, 0, int(config.LARGURA * escala), int(config.ALTURA * escala))
        area.center = (largura // 2, altura // 2)
        return area

    def janela_para_logica(self, posicao):
        """Converte um ponto da janela (pixels reais) para a tela lógica 1600x900."""
        x, y = posicao
        escala = self._area.width / config.LARGURA
        return (int((x - self._area.x) / escala), int((y - self._area.y) / escala))

    def logica_para_janela(self, posicao):
        """O contrário: ponto da tela 1600x900 -> pixel da janela (usado nos testes)."""
        x, y = posicao
        escala = self._area.width / config.LARGURA
        return (int(x * escala + self._area.x), int(y * escala + self._area.y))

    # --- cenas -------------------------------------------------------------

    def ir_para(self, nome_cena, com_fade=True):
        """Troca para a cena com esse nome (veja o dicionário CENAS no topo)."""
        nova = CENAS[nome_cena](self)
        self.cenas.trocar(nova, com_fade)

    def nova_partida(self):
        """Zera todas as variáveis para começar do Dia 1 (e esquece a partida guardada)."""
        self.estado = Estado()
        self.acoes_para_refazer = None
        self.dia_pausado = None
        progresso.apagar()

    def continuar(self):
        """Volta à partida guardada, exatamente no ponto em que o jogador parou."""
        dados = progresso.carregar()
        if not dados:
            return
        self.estado = Estado()
        self.estado.carregar_dicionario(dados["estado"])
        self.acoes_para_refazer = dados["acoes"]
        self.dia_pausado = None
        self.ir_para(dados["cena"])

    def voltar_ao_dia(self):
        """Da aldeia de dia para a entrada da aldeia: o Dia guardado continua de onde parou."""
        dia = self.dia_pausado
        self.dia_pausado = None
        dia.voltar_da_aldeia()
        self.cenas.trocar(dia)

    def conversar_no_dia(self, nome, voltar_para="aldeia"):
        """Da aldeia (ou de uma oca) de dia, clicando numa pessoa: o Dia guardado toca a conversa
        com ela e, no fim, volta para voltar_para ("aldeia" ou "oca")."""
        dia = self.dia_pausado
        self.dia_pausado = None
        dia.voltar_para = voltar_para
        dia.conversar_na_aldeia(nome)
        self.cenas.trocar(dia)

    def amanhecer(self):
        """Da aldeia de noite ("Dormir"): começa o dia seguinte (e a febre anda, motor/febre.py)."""
        febre.amanhecer(self.estado)
        # Na manhã do dia 10, depois das mortes e antes de Araci chegar, o final é calculado
        # (o jogador não vê): ele aparece no fim da noite 10 (motor/finais.py).
        finais.calcular_na_manha(self.estado)
        self.ir_para("dia")

    def sair(self):
        self.rodando = False

    # --- um quadro ---------------------------------------------------------

    def tratar_evento(self, evento):
        if evento.type == pygame.QUIT:
            self.sair()
            return
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
            self.alternar_tela_cheia()
            return
        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            # As cenas só conhecem 1600x900: trocamos a posição da janela pela posição lógica.
            dados = dict(evento.dict)
            dados["pos"] = self.janela_para_logica(evento.pos)
            evento = pygame.event.Event(evento.type, dados)
        if self.teclado.tratar_evento(evento, self.cenas):
            return
        self.cenas.tratar_evento(evento)

    def passo(self, eventos, dt):
        """Roda um quadro inteiro: eventos, atualização e desenho."""
        dt = min(dt, 0.1)  # se o computador engasgar, não deixa as animações "pularem"
        self._area = self._calcular_area()
        # Com o foco do teclado, o "mouse" do jogo fica nele: o destaque mostra onde está.
        if self.cenas.atual:
            self.teclado.conferir(self.cenas.atual)
        self.mouse = self.teclado.foco or self.janela_para_logica(pygame.mouse.get_pos())

        for evento in eventos:
            self.tratar_evento(evento)
            if not self.rodando:
                return

        ui.mouse_sobre_botao = False
        self.cenas.atualizar(dt)
        sons.ambiente(self.cenas.atual.som_ambiente(), self.cenas.atual.som_intensidade())
        sons.atualizar(dt)
        self._atualizar_cursor()

        self.cenas.desenhar(self.tela)
        self._mostrar_na_janela()

    def _atualizar_cursor(self):
        # Sobre o que é clicável, a chama da tocha cresce e clareia: deixa claro onde clicar.
        if ui.mouse_sobre_botao != self._cursor_mao:
            self._cursor_mao = ui.mouse_sobre_botao
            cursor.usar(acesa=self._cursor_mao)

    def _mostrar_na_janela(self):
        area = self._area
        if area.size != self.janela.get_size():
            self.janela.fill(config.PRETO)  # barras pretas onde a tela 16:9 não cobre
        if area.size == config.TAMANHO_LOGICO:
            # Janela do tamanho exato: não precisa escalar (mais rápido).
            self.janela.blit(self.tela, area.topleft)
        else:
            # Reaproveita a mesma Surface de destino enquanto o tamanho da janela não muda.
            if self._tela_escalada is None or self._tela_escalada.get_size() != area.size:
                self._tela_escalada = pygame.Surface(area.size).convert()
            pygame.transform.smoothscale(self.tela, area.size, self._tela_escalada)
            self.janela.blit(self._tela_escalada, area.topleft)
        pygame.display.flip()

    def capturar_tela(self, caminho):
        """Salva a tela lógica (1600x900) num arquivo de imagem."""
        pygame.image.save(self.tela, caminho)

    def encerrar(self):
        # Imagens e fontes guardadas deixam de valer depois do pygame.quit().
        fontes.limpar_cache()
        imagens.limpar_cache()
        efeitos.limpar_cache()
        sons.parar()
        pygame.quit()
