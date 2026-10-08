# Converte as artes originais da pasta Arte/ para Jogo/assets/, no tamanho e no nome que o jogo usa.
#
# Por que existe: as artes do grupo vêm grandes (1672x940, até 1835 px de altura),
# com acento e espaço no nome. O jogo precisa de arquivos leves (abrem rápido no
# navegador) e de nomes sem acento (acento quebra em alguns navegadores).
# Os originais em Arte/ NUNCA são alterados: este script só lê de lá.
#
# Como rodar (de dentro da pasta Jogo, com o ambiente ativado):
#     python ferramentas/converter_arte.py
#
# Chegou arte nova? Acrescente uma linha na lista CENARIOS (ou PERSONAGENS) abaixo e rode de novo.

import os
from PIL import Image, ImageChops, ImageDraw, ImageFilter

# Pasta Jogo/ (este arquivo está em Jogo/ferramentas/)
PASTA_JOGO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ARTE = os.path.join(os.path.dirname(PASTA_JOGO), "Arte")
PASTA_ASSETS = os.path.join(PASTA_JOGO, "assets")

# Tamanho de todo cenário dentro do jogo (resolução lógica)
TAMANHO_CENARIO = (1600, 900)

# Qualidade do JPG: 80 deixa os cenários com cerca de 250-310 KB sem perder detalhe visível.
QUALIDADE_JPG = 80

# Lista de cenários: (arquivo original dentro de Arte/, arquivo de destino dentro de assets/)
CENARIOS = [
    ("Aldeia.png", "cenarios/cenario-aldeia.jpg"),
    ("FogueiraLonge.png", "cenarios/cenario-fogueira-longe.jpg"),
    ("FogueiraPerto.png", "cenarios/cenario-fogueira-perto.jpg"),
]

# CORTE PADRÃO DAS PESSOAS: do topo da cabeça até o meio das coxas, sempre com esta
# altura. Assim todo mundo aparece na mesma escala, com a cabeça no mesmo lugar da tela.
# (A largura acompanha a pose de cada um.)
ALTURA_PERSONAGEM = 860

# Quão claro um pixel precisa ser (0-255, no canal mais escuro) para contar como fundo branco.
LIMIAR_FUNDO_BRANCO = 228
# Branco "preso" entre fios de cabelo perto da borda: some se for bem branco e estiver
# a menos de DISTANCIA_BRANCO_PRESO pixels do fundo. (Dentes e olhos, longe da borda, ficam.)
LIMIAR_BRANCO_PRESO = 245
DISTANCIA_BRANCO_PRESO = 24
# Branco cercado pela pessoa (entre o braço e o corpo, entre o arco e o corpo): some se a
# mancha branca for grande. Mancha pequena (dente, brilho do olho) fica.
LIMIAR_BRANCO_CERCADO = 240
AREA_MINIMA_BRANCO_CERCADO = 1500   # pixels da arte original

# Lista de personagens: (original dentro de Arte/, destino dentro de assets/, giro, meio da coxa).
# - giro: as artes de Arte/PP/ vieram deitadas, com a cabeça para a direita; 90 gira no
#   sentido anti-horário e deixa a pessoa de pé. Use 0 se a arte já estiver de pé.
# - meio da coxa: a altura (em pixels da arte JÁ DE PÉ, contando de cima) onde fica o meio
#   das coxas. O topo da cabeça é achado sozinho. Se a arte acaba antes do meio da coxa
#   (Mbaé, Tamandaré-mirim e Iandé foram desenhados só até a cintura ou o quadril), coloque
#   onde a coxa estaria: o pedaço que falta fica transparente, escondido atrás da caixa de fala.
PERSONAGENS = [
    ("PP/Yara.png", "personagens/yara.png", 90, 830),
    ("PP/Mbaé.png", "personagens/mbae.png", 90, 1020),
    ("PP/Tama.png", "personagens/tamandare.png", 90, 965),
    ("PP/Iandé.png", "personagens/iande.png", 90, 880),
    ("PP/Krenan.png", "personagens/krenan.png", 90, 950),
    ("PP/Araci.png", "personagens/araci.png", 90, 960),
    ("PP/Irmão Aleixo.png", "personagens/aleixo.png", 0, 920),
]


def ajustar_ao_tamanho(imagem, tamanho):
    """Redimensiona cobrindo o tamanho inteiro e corta o que sobrar no meio.

    Assim a imagem nunca fica esticada: se a proporção for um pouco diferente
    de 16:9, perde-se uma faixa fina das bordas.
    """
    largura, altura = tamanho
    escala = max(largura / imagem.width, altura / imagem.height)
    nova = imagem.resize(
        (round(imagem.width * escala), round(imagem.height * escala)),
        Image.LANCZOS,
    )
    esquerda = (nova.width - largura) // 2
    topo = (nova.height - altura) // 2
    return nova.crop((esquerda, topo, esquerda + largura, topo + altura))


def converter_cenario(origem, destino):
    caminho_origem = os.path.join(PASTA_ARTE, origem)
    caminho_destino = os.path.join(PASTA_ASSETS, destino)
    if not os.path.exists(caminho_origem):
        print("  FALTA o original:", caminho_origem)
        return
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
    imagem = Image.open(caminho_origem).convert("RGB")
    imagem = ajustar_ao_tamanho(imagem, TAMANHO_CENARIO)
    imagem.save(caminho_destino, quality=QUALIDADE_JPG, optimize=True, progressive=True)
    tamanho_kb = os.path.getsize(caminho_destino) // 1024
    print("  ok  %-22s -> %-36s %4d KB" % (origem, destino, tamanho_kb))


def tirar_fundo_branco(imagem):
    """Deixa transparente o branco que encosta na borda da imagem (o fundo).

    Só some o branco ligado à borda: o branco da pintura do corpo, dos olhos e
    dos dentes fica, porque está cercado pela pessoa.
    """
    r, g, b, _ = imagem.split()
    mais_escuro = ImageChops.darker(ImageChops.darker(r, g), b)
    claro = mais_escuro.point(lambda v: 255 if v >= LIMIAR_FUNDO_BRANCO else 0)
    # "Balde de tinta" a partir de cada ponto claro da borda: marca o fundo com 128.
    largura, altura = claro.size
    borda = ([(x, 0) for x in range(largura)] + [(x, altura - 1) for x in range(largura)]
             + [(0, y) for y in range(altura)] + [(largura - 1, y) for y in range(altura)])
    for ponto in borda:
        if claro.getpixel(ponto) == 255:
            ImageDraw.floodfill(claro, ponto, 128)
    fundo = claro.point(lambda v: 255 if v == 128 else 0)
    # Branco preso perto da borda (entre fios de cabelo): também vira fundo.
    perto_do_fundo = fundo
    for _ in range(DISTANCIA_BRANCO_PRESO // 2):
        perto_do_fundo = perto_do_fundo.filter(ImageFilter.MaxFilter(5))
    bem_branco = mais_escuro.point(lambda v: 255 if v >= LIMIAR_BRANCO_PRESO else 0)
    fundo = ImageChops.lighter(fundo, ImageChops.multiply(perto_do_fundo, bem_branco))
    fundo = _juntar_brancos_grandes(fundo, mais_escuro)
    alfa = ImageChops.invert(fundo)
    # Come 1 pixel da borda (tira o contorno claro) e suaviza o recorte.
    alfa = alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    imagem.putalpha(alfa)
    return imagem


def _juntar_brancos_grandes(fundo, mais_escuro):
    """Marca como fundo as manchas brancas grandes que o balde de tinta da borda não alcançou."""
    branco = mais_escuro.point(lambda v: 255 if v >= LIMIAR_BRANCO_CERCADO else 0)
    # Só o branco que ainda não é fundo.
    marcas = ImageChops.subtract(branco, fundo)       # 255 = branco cercado ainda não visto
    largura, altura = marcas.size
    pixels = marcas.load()
    for y in range(0, altura, 3):
        for x in range(0, largura, 3):
            if pixels[x, y] != 255:
                continue
            ImageDraw.floodfill(marcas, (x, y), 100)  # pinta a mancha toda com 100
            area = marcas.histogram()[100]
            # Mancha grande vira 50 (sai); pequena vira 200 (fica).
            novo = 50 if area >= AREA_MINIMA_BRANCO_CERCADO else 200
            marcas = marcas.point(lambda v, novo=novo: novo if v == 100 else v)
            pixels = marcas.load()
    grandes = marcas.point(lambda v: 255 if v == 50 else 0)
    return ImageChops.lighter(fundo, grandes)


def converter_personagem(origem, destino, giro, meio_da_coxa):
    caminho_origem = os.path.join(PASTA_ARTE, origem)
    caminho_destino = os.path.join(PASTA_ASSETS, destino)
    if not os.path.exists(caminho_origem):
        print("  FALTA o original:", caminho_origem)
        return
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
    imagem = Image.open(caminho_origem).convert("RGBA")
    if giro:
        imagem = imagem.rotate(giro, expand=True, fillcolor=(255, 255, 255, 255))
    imagem = tirar_fundo_branco(imagem)
    # Corte padrão: do topo da cabeça até o meio da coxa. Se a arte acabar antes,
    # crop() completa com transparente embaixo.
    esquerda, topo, direita, _ = imagem.getbbox()
    imagem = imagem.crop((esquerda, topo, direita, meio_da_coxa))
    escala = ALTURA_PERSONAGEM / imagem.height
    imagem = imagem.resize((round(imagem.width * escala), ALTURA_PERSONAGEM), Image.LANCZOS)
    imagem = imagem.crop(imagem.getbbox())  # tira colunas vazias dos lados (a altura fica)
    if imagem.height != ALTURA_PERSONAGEM:  # a arte acabou antes do meio da coxa
        completa = Image.new("RGBA", (imagem.width, ALTURA_PERSONAGEM), (0, 0, 0, 0))
        completa.paste(imagem, (0, 0))
        imagem = completa
    imagem.save(caminho_destino, optimize=True)
    tamanho_kb = os.path.getsize(caminho_destino) // 1024
    print("  ok  %-22s -> %-36s %4d KB" % (origem, destino, tamanho_kb))


def main():
    print("Convertendo cenários de", PASTA_ARTE)
    for origem, destino in CENARIOS:
        converter_cenario(origem, destino)
    print("Convertendo personagens")
    for origem, destino, giro, meio_da_coxa in PERSONAGENS:
        converter_personagem(origem, destino, giro, meio_da_coxa)
    print("Pronto.")


if __name__ == "__main__":
    main()
