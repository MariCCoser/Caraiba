# Tratamento visual da cena: filtros de noite (âmbar) e dia (frio), linhas, grão, vinheta, tremor e luz do fogo.
#
# REGRA DE OURO (Arte/PALETA E EXEMPLO.docx): o tratamento vai SÓ SOBRE A CENA.
# A interface (textos, botões) é desenhada DEPOIS, sem tratamento, para ficar legível.
# As cenas seguem isso sozinhas: veja Cena.desenhar() em motor/cenas.py.
#
# Desempenho: nada aqui mexe pixel por pixel a cada quadro. As texturas
# (linhas, grão, vinheta, brilho do fogo) são geradas UMA vez e depois só
# "carimbadas" por cima da tela com modos de mistura do pygame.

import math
import random

import pygame

import config

# ---------------------------------------------------------------------------
# Filtros (aplicados uma vez na imagem, quando ela é carregada)
# ---------------------------------------------------------------------------


def filtro_noite(imagem):
    """Noite: deixa a imagem monocromática âmbar, com o escuro virando preto de verdade.

    À noite, dentro da aldeia, a única luz é o fogo: não há azul nem verde.
    """
    resultado = pygame.transform.grayscale(imagem)
    # "Esmaga" o preto: tudo que é bem escuro vira preto absoluto.
    resultado.fill((26, 26, 26), special_flags=pygame.BLEND_RGB_SUB)
    # Aumenta o contraste (x1,5): soma à imagem metade dela mesma.
    metade = resultado.copy()
    metade.fill((128, 128, 128), special_flags=pygame.BLEND_RGB_MULT)
    resultado.blit(metade, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    # Pinta tudo com o tom do fogo (cinza -> âmbar).
    resultado.fill(config.TOM_FILTRO_NOITE, special_flags=pygame.BLEND_RGB_MULT)
    return resultado


def filtro_dia(imagem):
    """Dia: paleta fria e dessaturada (tira boa parte da cor e puxa para o azul-acinzentado)."""
    resultado = imagem.copy()
    cinza = pygame.transform.grayscale(imagem)
    cinza.set_alpha(165)  # quanto da cor some: 0 = nada, 255 = tudo
    resultado.blit(cinza, (0, 0))
    resultado.fill(config.TOM_FILTRO_DIA, special_flags=pygame.BLEND_RGB_MULT)
    # Clareia um pouco (x1,25): é dia, a luz é fraca e fria, mas não é noite.
    quarto = resultado.copy()
    quarto.fill((64, 64, 64), special_flags=pygame.BLEND_RGB_MULT)
    resultado.blit(quarto, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    return resultado


# ---------------------------------------------------------------------------
# Texturas pré-geradas (criadas na primeira vez que alguém usa)
# ---------------------------------------------------------------------------

TAMANHO_GRAO = 512          # lado de cada textura de grão (repetida pela tela)
QUANTIDADE_GRAOS = 4        # quantas texturas diferentes se alternam
TROCAS_DE_GRAO_POR_SEGUNDO = 18
NIVEIS_DE_BRILHO = 12       # quantas versões do brilho do fogo (para "pulsar" sem recalcular)

_texturas = {}


def _gerar_linhas():
    """Riscos horizontais finos: uma linha escura a cada 3 pixels."""
    linhas = pygame.Surface(config.TAMANHO_LOGICO, pygame.SRCALPHA)
    for y in range(0, config.ALTURA, 3):
        pygame.draw.line(linhas, (0, 0, 0, 55), (0, y), (config.LARGURA, y))
    return linhas


def _gerar_graos(intensidade):
    """Algumas texturas de ruído cinza. `intensidade` 0-255: o quanto o grão aparece."""
    sorteio = random.Random(1562)  # semente fixa: o grão é sempre o mesmo, jogo repetível
    graos = []
    for _ in range(QUANTIDADE_GRAOS):
        bytes_aleatorios = sorteio.randbytes(TAMANHO_GRAO * TAMANHO_GRAO * 3)
        ruido = pygame.image.frombytes(bytes_aleatorios, (TAMANHO_GRAO, TAMANHO_GRAO), "RGB")
        ruido = pygame.transform.grayscale(ruido).convert()
        ruido.fill((intensidade, intensidade, intensidade), special_flags=pygame.BLEND_RGB_MULT)
        graos.append(ruido)
    return graos


def _gerar_vinheta():
    """Escurece as bordas. Calculada pequena e depois ampliada (fica suave e é rápido)."""
    largura, altura = 64, 36
    pequena = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for y in range(altura):
        for x in range(largura):
            dx = (x + 0.5) / largura * 2 - 1
            dy = (y + 0.5) / altura * 2 - 1
            distancia = math.sqrt(dx * dx + dy * dy)
            forca = max(0.0, min(1.0, (distancia - 0.45) / 0.85))
            pequena.set_at((x, y), (0, 0, 0, int(235 * forca ** 1.6)))
    return pygame.transform.smoothscale(pequena, config.TAMANHO_LOGICO)


def _gerar_brilhos():
    """Brilho redondo do fogo em vários níveis de força (para somar à tela)."""
    lado = 64
    pequeno = pygame.Surface((lado, lado))
    for y in range(lado):
        for x in range(lado):
            dx = (x + 0.5) / lado * 2 - 1
            dy = (y + 0.5) / lado * 2 - 1
            forca = max(0.0, 1.0 - math.sqrt(dx * dx + dy * dy)) ** 2
            pequeno.set_at((x, y), (int(70 * forca), int(38 * forca), int(12 * forca)))
    grande = pygame.transform.smoothscale(pequeno, (1100, 800))
    niveis = []
    for i in range(NIVEIS_DE_BRILHO):
        copia = grande.copy()
        valor = int(255 * (i + 1) / NIVEIS_DE_BRILHO)
        copia.fill((valor, valor, valor), special_flags=pygame.BLEND_RGB_MULT)
        niveis.append(copia)
    return niveis


def _textura(nome):
    if nome not in _texturas:
        if nome == "linhas":
            _texturas[nome] = _gerar_linhas()
        elif nome == "grao_fraco":
            _texturas[nome] = _gerar_graos(22)
        elif nome == "grao_forte":
            _texturas[nome] = _gerar_graos(44)
        elif nome == "vinheta":
            _texturas[nome] = _gerar_vinheta()
        elif nome == "brilhos":
            _texturas[nome] = _gerar_brilhos()
    return _texturas[nome]


def preparar_texturas():
    """Gera todas as texturas de uma vez (chamado no início, para não engasgar no meio)."""
    for nome in ("linhas", "grao_fraco", "grao_forte", "vinheta", "brilhos"):
        _textura(nome)


# ---------------------------------------------------------------------------
# Tratamento: o que vai por cima da cena a cada quadro
# ---------------------------------------------------------------------------


class Tratamento:
    """Linhas + grão animado + vinheta (+ tremor quando a sanidade está baixa).

    Cada cena tem o seu. Use ajustar_pela_sanidade() quando a sanidade mudar.
    """

    def __init__(self, linhas=True, grao=True, vinheta=True):
        self.usar_linhas = linhas
        self.usar_grao = grao
        self.usar_vinheta = vinheta
        self.grao_forte = False
        self.tremor = 0          # pixels máximos que a cena "treme" para os lados
        self._tempo = 0.0
        self._indice_grao = 0
        self._deslocamento_grao = (0, 0)
        self._deslocamento_tremor = 0
        self._sorteio = random.Random(9)

    def ajustar_pela_sanidade(self, sanidade):
        """Documento de design: sanidade 6 ou menos -> a linha treme mais e o grão aumenta."""
        if sanidade <= 6:
            self.grao_forte = True
            self.tremor = 3
        else:
            self.grao_forte = False
            self.tremor = 0

    def atualizar(self, dt):
        self._tempo += dt
        # Troca de textura de grão ~18 vezes por segundo, como grão de filme.
        passo = int(self._tempo * TROCAS_DE_GRAO_POR_SEGUNDO)
        if passo != self._indice_grao:
            self._indice_grao = passo
            self._deslocamento_grao = (self._sorteio.randrange(TAMANHO_GRAO),
                                       self._sorteio.randrange(TAMANHO_GRAO))
            if self.tremor:
                self._deslocamento_tremor = self._sorteio.randint(-self.tremor, self.tremor)

    def aplicar(self, tela):
        """Desenha o tratamento por cima do que já está na tela (a cena)."""
        if self.tremor and self._deslocamento_tremor:
            tela.scroll(self._deslocamento_tremor, 0)
        if self.usar_linhas:
            tela.blit(_textura("linhas"), (0, 0))
        if self.usar_grao:
            self._aplicar_grao(tela)
        if self.usar_vinheta:
            tela.blit(_textura("vinheta"), (0, 0))

    def _aplicar_grao(self, tela):
        graos = _textura("grao_forte" if self.grao_forte else "grao_fraco")
        # Duas texturas diferentes: uma clareia pontos, a outra escurece.
        claro = graos[self._indice_grao % QUANTIDADE_GRAOS]
        escuro = graos[(self._indice_grao + 2) % QUANTIDADE_GRAOS]
        ox, oy = self._deslocamento_grao
        for y in range(-oy, config.ALTURA, TAMANHO_GRAO):
            for x in range(-ox, config.LARGURA, TAMANHO_GRAO):
                tela.blit(claro, (x, y), special_flags=pygame.BLEND_RGB_ADD)
                tela.blit(escuro, (x, y), special_flags=pygame.BLEND_RGB_SUB)


def luz_de_fogo(tela, tempo, centro):
    """Faz a luz da cena pulsar devagar, como chama de fogueira, e acende um brilho em volta do fogo.

    Use DEPOIS de desenhar o cenário e ANTES do tratamento.
    """
    # Soma de ondas lentas com velocidades diferentes: parece irregular, mas é suave.
    oscilacao = (math.sin(tempo * 1.3) * 0.5
                 + math.sin(tempo * 3.1 + 1.0) * 0.3
                 + math.sin(tempo * 7.3 + 2.0) * 0.2)          # entre -1 e 1
    brilho_geral = int(232 + 20 * oscilacao)                   # 212 a 252 (de 255)
    tela.fill((brilho_geral,) * 3, special_flags=pygame.BLEND_RGB_MULT)

    brilhos = _textura("brilhos")
    nivel = int((oscilacao + 1) / 2 * (NIVEIS_DE_BRILHO - 1))
    brilho = brilhos[nivel]
    tela.blit(brilho, brilho.get_rect(center=centro), special_flags=pygame.BLEND_RGB_ADD)


def escurecer(tela, quanto):
    """Escurece a tela inteira. quanto: 0 (nada) a 255 (preto). Útil para pôr texto sobre o cenário."""
    valor = 255 - quanto
    tela.fill((valor, valor, valor), special_flags=pygame.BLEND_RGB_MULT)


def limpar_cache():
    """Esquece as texturas geradas (necessário ao fechar o pygame)."""
    _texturas.clear()
