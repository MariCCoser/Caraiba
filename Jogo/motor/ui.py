# Componentes de interface reutilizáveis: Botao e CaixaTexto (com palavras marcadas em âmbar).
#
# MARCAÇÃO DE PALAVRAS: nos textos (pasta dados/), escreva a palavra entre
# colchetes para ela aparecer em âmbar e sublinhada:
#     "Eu tive [sorte]. Passei no meio de tudo e não peguei [nada]."
# Pode marcar várias palavras de uma vez: "[de dentro para fora]".
# Escolhemos colchetes (e não *asteriscos*) porque colchete quase nunca
# aparece numa fala de verdade, então não há risco de marcar sem querer.
# Além da cor, a palavra marcada é sublinhada: assim quem não distingue
# cores também percebe a marcação.

import pygame

import config
from motor import fontes, preferencias

# Fica True no quadro em que o mouse está sobre algum botão habilitado
# (o jogo usa isso para trocar o cursor para a "mãozinha").
mouse_sobre_botao = False


# ---------------------------------------------------------------------------
# Botão
# ---------------------------------------------------------------------------

class Botao:
    """Botão de texto com três aparências: normal, mouse em cima (hover) e desabilitado.

    Uso numa cena:
        self.botao = Botao("Começar", (800, 600))
        ... em atualizar:  self.botao.atualizar(self.jogo.mouse)
        ... em tratar_evento: if self.botao.clicado(evento): fazer_algo()
        ... em desenhar_interface: self.botao.desenhar(tela)

    Desabilitado: passe habilitado=False e um `motivo`, que aparece embaixo
    (ex.: "O pajé precisa ver dois sinais"). Assim o jogador sabe por quê.
    """

    MARGEM_X = 28
    MARGEM_Y = 12

    def __init__(self, texto, centro, tamanho=config.TAMANHO_BOTAO, largura_minima=0,
                 habilitado=True, motivo="", selecionado=False, alinhamento="centro"):
        self.texto = texto
        self.centro = centro              # (x, y) do meio do botão (ou da borda esquerda, ver alinhamento)
        self.tamanho = tamanho
        self.largura_minima = largura_minima
        self.habilitado = habilitado
        self.motivo = motivo
        self.selecionado = selecionado    # marcado como opção escolhida (ex.: "Grande")
        self.alinhamento = alinhamento    # "centro" ou "esquerda"
        self.mouse_em_cima = False
        self.visivel = True

    def retangulo(self):
        """Área clicável do botão (muda se o tamanho do texto mudar nas Opções)."""
        fonte = fontes.fonte_escalada("sans", self.tamanho)
        largura, altura = fonte.size(self._texto_exibido())
        largura = max(largura + 2 * self.MARGEM_X, self.largura_minima)
        altura = altura + 2 * self.MARGEM_Y
        rect = pygame.Rect(0, 0, largura, altura)
        if self.alinhamento == "esquerda":
            rect.midleft = self.centro
        else:
            rect.center = self.centro
        return rect

    def _texto_exibido(self):
        # O "●" mostra a opção escolhida por FORMA, não só por cor.
        return ("● " + self.texto) if self.selecionado else self.texto

    def atualizar(self, posicao_mouse):
        global mouse_sobre_botao
        self.mouse_em_cima = self.visivel and self.retangulo().collidepoint(posicao_mouse)
        if self.mouse_em_cima and self.habilitado:
            mouse_sobre_botao = True

    def clicado(self, evento):
        """True se este evento é um clique (botão esquerdo solto) em cima do botão habilitado."""
        if not self.visivel or not self.habilitado:
            return False
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            return self.retangulo().collidepoint(evento.pos)
        return False

    def desenhar(self, tela):
        if not self.visivel:
            return
        rect = self.retangulo()
        fonte = fontes.fonte_escalada("sans", self.tamanho)

        # Fundo preto semitransparente: o texto fica legível sobre qualquer cenário.
        fundo = pygame.Surface(rect.size, pygame.SRCALPHA)
        if self.habilitado and self.mouse_em_cima:
            fundo.fill(config.TERRA + (235,))
        else:
            fundo.fill(config.PRETO + (170,))
        tela.blit(fundo, rect.topleft)

        if not self.habilitado:
            cor_texto = config.BARRO
        else:
            cor_texto = config.TABATINGA

        # Contorno: aceso (Urucum) quando o mouse está em cima; claro quando selecionado.
        if self.habilitado and self.mouse_em_cima:
            pygame.draw.rect(tela, config.URUCUM, rect, 3)
        elif self.selecionado:
            pygame.draw.rect(tela, config.TABATINGA, rect, 2)

        imagem = fonte.render(self._texto_exibido(), True, cor_texto)
        if self.alinhamento == "esquerda":
            texto_rect = imagem.get_rect(midleft=(rect.left + self.MARGEM_X, rect.centery))
        else:
            texto_rect = imagem.get_rect(center=rect.center)
        tela.blit(imagem, texto_rect)

        if not self.habilitado:
            # Risco no meio do texto: mostra "indisponível" sem depender de cor.
            pygame.draw.line(tela, config.BARRO, (texto_rect.left, texto_rect.centery),
                             (texto_rect.right, texto_rect.centery), 2)
            if self.motivo:
                fonte_motivo = fontes.fonte_escalada("sans", config.TAMANHO_PEQUENO)
                motivo = fonte_motivo.render(self.motivo, True, config.TABATINGA)
                tela.blit(motivo, motivo.get_rect(midtop=(rect.centerx, rect.bottom + 6)))


# ---------------------------------------------------------------------------
# Texto com palavras marcadas
# ---------------------------------------------------------------------------

def separar_marcacao(texto):
    """Transforma o texto em palavras; cada palavra é uma lista de pedaços (trecho, marcado).

    Ex.: "uma [maldição], enfim" ->
         [[("uma", False)], [("maldição", True), (",", False)], [("enfim", False)]]
    """
    palavras = []
    palavra_atual = []
    trecho = ""
    marcado = False

    def fechar_trecho():
        nonlocal trecho
        if trecho:
            palavra_atual.append((trecho, marcado))
            trecho = ""

    for letra in texto:
        if letra == "[":
            fechar_trecho()
            marcado = True
        elif letra == "]":
            fechar_trecho()
            marcado = False
        elif letra == " " or letra == "\n":
            fechar_trecho()
            if palavra_atual:
                palavras.append(palavra_atual)
                palavra_atual = []
            if letra == "\n":
                palavras.append("QUEBRA")  # quebra de linha forçada
        else:
            trecho += letra
    fechar_trecho()
    if palavra_atual:
        palavras.append(palavra_atual)
    return palavras


class CaixaTexto:
    """Caixa preta simples (sem moldura) com texto que quebra linha sozinho.

    - Palavras entre [colchetes] saem em âmbar e sublinhadas.
    - Efeito de digitação: chame comecar_digitacao(); a cada quadro, atualizar(dt).
      completar() mostra o texto inteiro de uma vez (ex.: quando o jogador clica).
    - posicao + ancora dizem onde a caixa fica:
        ancora="centro": posicao é o meio da caixa
        ancora="baixo":  posicao é o meio da borda de baixo (bom para falas)
        ancora="topo":   posicao é o meio da borda de cima
    - max_linhas: se o texto passar disso, aparece um aviso no terminal
      (as falas do jogo têm no máximo 2 linhas). O texto NÃO é cortado.
    """

    MARGEM = 28

    def __init__(self, texto, largura, posicao, ancora="centro", tamanho=config.TAMANHO_FALA,
                 nome_fonte="serif", cor=config.TABATINGA, alinhamento="esquerda",
                 fundo=True, max_linhas=None):
        self.largura = largura
        self.posicao = posicao
        self.ancora = ancora
        self.tamanho = tamanho
        self.nome_fonte = nome_fonte
        self.cor = cor
        self.alinhamento = alinhamento   # "esquerda" ou "centro"
        self.fundo = fundo
        self.max_linhas = max_linhas
        self.letras_visiveis = None      # None = texto inteiro
        self._tempo_digitacao = 0.0
        self._escala_usada = None
        self.definir_texto(texto)

    # --- texto e digitação -------------------------------------------------

    def definir_texto(self, texto):
        self.texto = texto
        self.palavras = separar_marcacao(texto)
        self.total_letras = 0
        for palavra in self.palavras:
            if palavra != "QUEBRA":
                self.total_letras += sum(len(trecho) for trecho, _ in palavra) + 1
        self._escala_usada = None  # força refazer o layout
        self.letras_visiveis = None

    def comecar_digitacao(self):
        self.letras_visiveis = 0
        self._tempo_digitacao = 0.0

    def completar(self):
        self.letras_visiveis = None

    def terminou(self):
        return self.letras_visiveis is None or self.letras_visiveis >= self.total_letras

    def atualizar(self, dt):
        if self.letras_visiveis is None:
            return
        self._tempo_digitacao += dt
        self.letras_visiveis = int(self._tempo_digitacao * config.LETRAS_POR_SEGUNDO)
        if self.letras_visiveis >= self.total_letras:
            self.letras_visiveis = None

    # --- layout ------------------------------------------------------------

    def _montar_layout(self):
        """Decide em que linha e posição vai cada palavra (refeito se o tamanho do texto mudar)."""
        escala = preferencias.atual.escala_texto()
        self._escala_usada = escala
        self.fonte = fontes.fonte_escalada(self.nome_fonte, self.tamanho)
        largura_util = self.largura - 2 * self.MARGEM
        espaco = self.fonte.size(" ")[0]

        linhas = [[]]          # cada linha: lista de palavras (listas de pedaços)
        largura_linha = 0
        for palavra in self.palavras:
            if palavra == "QUEBRA":
                linhas.append([])
                largura_linha = 0
                continue
            largura_palavra = sum(self.fonte.size(trecho)[0] for trecho, _ in palavra)
            extra = largura_palavra if not linhas[-1] else espaco + largura_palavra
            if linhas[-1] and largura_linha + extra > largura_util:
                linhas.append([])
                largura_linha = 0
                extra = largura_palavra
            linhas[-1].append(palavra)
            largura_linha += extra
        self.linhas = linhas
        self.espaco = espaco
        # Largura de cada linha, guardada para não recalcular a cada quadro
        self.larguras_linhas = []
        for linha in linhas:
            largura = sum(sum(self.fonte.size(t)[0] for t, _ in p) for p in linha)
            self.larguras_linhas.append(largura + espaco * max(0, len(linha) - 1))
        # Imagens de texto já desenhadas (cache): {(trecho, marcado): Surface}
        self._imagens = {}

        if self.max_linhas and len(linhas) > self.max_linhas:
            print("Aviso: texto com %d linhas (máximo %d): %s"
                  % (len(linhas), self.max_linhas, self.texto[:60]))

        altura = len(linhas) * self.fonte.get_linesize() + 2 * self.MARGEM
        self.rect = pygame.Rect(0, 0, self.largura, altura)
        if self.ancora == "baixo":
            self.rect.midbottom = self.posicao
        elif self.ancora == "topo":
            self.rect.midtop = self.posicao
        else:
            self.rect.center = self.posicao

    def numero_de_linhas(self):
        if self._escala_usada != preferencias.atual.escala_texto():
            self._montar_layout()
        return len(self.linhas)

    # --- desenho -----------------------------------------------------------

    def desenhar(self, tela):
        if self._escala_usada != preferencias.atual.escala_texto():
            self._montar_layout()

        if self.fundo:
            caixa = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            caixa.fill(config.PRETO + (215,))
            tela.blit(caixa, self.rect.topleft)

        altura_linha = self.fonte.get_linesize()
        restantes = self.total_letras if self.letras_visiveis is None else self.letras_visiveis
        y = self.rect.top + self.MARGEM
        for linha, largura_linha in zip(self.linhas, self.larguras_linhas):
            if self.alinhamento == "centro":
                x = self.rect.centerx - largura_linha // 2
            else:
                x = self.rect.left + self.MARGEM
            for palavra in linha:
                for trecho, marcado in palavra:
                    if restantes <= 0:
                        return
                    visivel = trecho[:restantes]
                    restantes -= len(visivel)
                    cor = config.AMBAR if marcado else self.cor
                    if visivel == trecho:
                        chave = (trecho, marcado)
                        if chave not in self._imagens:
                            self._imagens[chave] = self.fonte.render(trecho, True, cor)
                        imagem = self._imagens[chave]
                    else:
                        # pedaço ainda sendo "digitado": desenha só as letras que já apareceram
                        imagem = self.fonte.render(visivel, True, cor)
                    tela.blit(imagem, (x, y))
                    if marcado:
                        base = y + self.fonte.get_ascent() + 4
                        pygame.draw.line(tela, config.AMBAR, (x, base), (x + imagem.get_width(), base), 2)
                    x += imagem.get_width()
                x += self.espaco
                restantes -= 1  # o espaço entre palavras também "conta" na digitação
            y += altura_linha


def texto_simples(tela, texto, posicao, tamanho, nome_fonte="sans", cor=config.TABATINGA,
                  ancora="centro"):
    """Escreve uma linha de texto sem caixa. Devolve o retângulo ocupado."""
    fonte = fontes.fonte_escalada(nome_fonte, tamanho)
    imagem = fonte.render(texto, True, cor)
    if ancora == "esquerda":
        rect = imagem.get_rect(midleft=posicao)
    elif ancora == "direita":
        rect = imagem.get_rect(midright=posicao)
    else:
        rect = imagem.get_rect(center=posicao)
    tela.blit(imagem, rect)
    return rect
