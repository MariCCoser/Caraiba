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

# Altura de todo personagem dentro do jogo (a largura acompanha a proporção da arte).
ALTURA_PERSONAGEM = 860

# Quão claro um pixel precisa ser (0-255, no canal mais escuro) para contar como fundo branco.
LIMIAR_FUNDO_BRANCO = 228

# Lista de personagens: (original dentro de Arte/, destino dentro de assets/, giro em graus).
# As artes de Arte/PP/ vieram desenhadas deitadas, com a cabeça para a direita:
# 90 gira no sentido anti-horário e deixa a pessoa de pé. Use 0 se a arte já estiver de pé.
PERSONAGENS = [
    ("PP/Yara.png", "personagens/yara.png", 90),
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
    alfa = claro.point(lambda v: 0 if v == 128 else 255)
    # Come 1 pixel da borda (tira o contorno claro) e suaviza o recorte.
    alfa = alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    imagem.putalpha(alfa)
    return imagem


def converter_personagem(origem, destino, giro):
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
    imagem = imagem.crop(imagem.getbbox())  # corta a sobra transparente em volta
    escala = ALTURA_PERSONAGEM / imagem.height
    imagem = imagem.resize((round(imagem.width * escala), ALTURA_PERSONAGEM), Image.LANCZOS)
    imagem.save(caminho_destino, optimize=True)
    tamanho_kb = os.path.getsize(caminho_destino) // 1024
    print("  ok  %-22s -> %-36s %4d KB" % (origem, destino, tamanho_kb))


def main():
    print("Convertendo cenários de", PASTA_ARTE)
    for origem, destino in CENARIOS:
        converter_cenario(origem, destino)
    print("Convertendo personagens")
    for origem, destino, giro in PERSONAGENS:
        converter_personagem(origem, destino, giro)
    print("Pronto.")


if __name__ == "__main__":
    main()
