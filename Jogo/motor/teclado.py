# Jogar sem mouse: as setas (ou Tab) andam entre o que dá para clicar na tela, e Enter ou Espaço
# clicam. Cada cena diz o que dá para clicar em alvos() (motor/cena.py): uma lista de pontos.
#
# O "mouse" do jogo (jogo.mouse) vai para o ponto escolhido, então o destaque de sempre (o
# contorno aceso do botão, a pessoa iluminada, a oca com a etiqueta) mostra onde o teclado está.
# Mexeu o mouse de verdade? O teclado solta e o mouse volta a mandar.

import pygame

import config

SETAS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}
TECLAS_CLICAR = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)

# Na hora de escolher o alvo na direção da seta, andar de lado "custa" mais que andar para frente:
# assim a seta para baixo prefere o botão logo embaixo ao que está embaixo e muito para o lado.
PESO_DE_LADO = 2

# De quantos em quantos pixels procurar um ponto livre dentro de uma pessoa ou oca.
PASSO_DA_BUSCA = 12


class Teclado:
    def __init__(self):
        self.foco = None       # o ponto (x, y) escolhido pelo teclado, ou None (o mouse manda)
        self._cena = None      # a cena do foco: trocou de cena, o foco começa de novo

    def conferir(self, cena):
        """A cada quadro: se o alvo do foco sumiu (ou a cena mudou), o teclado solta."""
        if cena is not self._cena:
            self._cena = cena
            self.foco = None
        elif self.foco is not None and self.foco not in cena.alvos():
            self.foco = None

    def tratar_evento(self, evento, cenas):
        """Devolve True se o teclado usou o evento (aí ele não vai para a cena)."""
        if evento.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            self.foco = None
            return False
        if evento.type != pygame.KEYDOWN or cenas.em_transicao() or cenas.atual is None:
            return False
        alvos = cenas.atual.alvos()
        if evento.key in TECLAS_CLICAR:
            if self.foco is None or self.foco not in alvos:
                return False   # sem foco, Enter e Espaço fazem o de sempre (passar a fala, Começar)
            # Um clique de verdade, no ponto do foco: a cena não vê diferença.
            for tipo in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                cenas.tratar_evento(pygame.event.Event(tipo, pos=self.foco, button=1))
            return True
        if not alvos:
            return False
        if evento.key == pygame.K_TAB:
            passo = -1 if evento.mod & pygame.KMOD_SHIFT else 1
            if self.foco in alvos:
                self.foco = alvos[(alvos.index(self.foco) + passo) % len(alvos)]
            else:
                self.foco = alvos[0] if passo == 1 else alvos[-1]
            return True
        if evento.key in SETAS:
            if self.foco not in alvos:
                self.foco = alvos[0]
            else:
                self.foco = _na_direcao(self.foco, alvos, *SETAS[evento.key]) or self.foco
            return True
        return False


def _na_direcao(origem, alvos, dx, dy):
    """O alvo mais perto de `origem` na direção (dx, dy), ou None se não houver nenhum."""
    melhor, menor_custo = None, None
    for alvo in alvos:
        vx, vy = alvo[0] - origem[0], alvo[1] - origem[1]
        para_frente = vx * dx + vy * dy
        if para_frente <= 0:
            continue
        de_lado = abs(vx * dy - vy * dx)
        custo = para_frente + PESO_DE_LADO * de_lado
        if menor_custo is None or custo < menor_custo:
            melhor, menor_custo = alvo, custo
    return melhor


def ponto_dentro(mascara, deslocamento=(0, 0), livre=None):
    """Um ponto da tela dentro da máscara, o mais perto do meio dela.

    livre(ponto): se for dada, o ponto também precisa passar nela (ex.: não estar atrás de outra
    pessoa, senão o clique cairia na da frente). None se não achar nenhum.
    """
    meio_x, meio_y = mascara.centroid()
    largura, altura = mascara.get_size()
    dentro = [(x, y) for x in range(0, largura, PASSO_DA_BUSCA) for y in range(0, altura, PASSO_DA_BUSCA)
              if mascara.get_at((x, y))]
    dentro.sort(key=lambda p: (p[0] - meio_x) ** 2 + (p[1] - meio_y) ** 2)
    for x, y in dentro:
        ponto = (x + deslocamento[0], y + deslocamento[1])
        na_tela = 0 <= ponto[0] < config.LARGURA and 0 <= ponto[1] < config.ALTURA
        if na_tela and (livre is None or livre(ponto)):
            return ponto
    return None
