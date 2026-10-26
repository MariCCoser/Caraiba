# Converte as artes originais da pasta Arte/ para Jogo/assets/, no tamanho e no nome que o jogo usa.
#
# Por que existe: as artes do grupo vêm grandes (1672x940, até 1835 px de altura),
# com acento e espaço no nome. O jogo precisa de arquivos leves (abrem rápido no
# navegador) e de nomes sem acento (acento quebra em alguns navegadores).
# Os originais em Arte/ NUNCA são alterados: este script só lê de lá.
#
# Como rodar (de dentro da pasta Jogo, com o ambiente ativado):
#     python ferramentas/converter_arte.py
#     python ferramentas/converter_arte.py detalhes     (só os detalhes do exame)
#
# Chegou arte nova? Acrescente uma linha na lista CENARIOS (ou PERSONAGENS) abaixo e rode de novo.

import os
import random
import sys
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

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
    ("Ar_livre/Aldeia.png", "cenarios/cenario-aldeia.jpg"),
    ("Ar_livre/FogueiraLonge.png", "cenarios/cenario-fogueira-longe.jpg"),
    ("Ar_livre/FogueiraPerto.png", "cenarios/cenario-fogueira-perto.jpg"),
    # A mesma fogueira de perto, de dia (os troncos no mesmo lugar): a manhã depois de uma morte.
    ("Ar_livre/FogueiraDia.png", "cenarios/cenario-fogueira-dia.jpg"),
    ("Ar_livre/floresta_atras_personag.png", "cenarios/cenario-floresta.jpg"),
    # Por dentro das ocas (Arte/Ocas/). A oca 1 tem uma imagem só, para o dia e a noite.
    ("Ocas/Yorixiriamori_DN.png", "cenarios/cenario-oca1.jpg"),
    # A oca 2 (Yebá Bëló) tem uma imagem de dia e outra de noite.
    ("Ocas/Yebá Bëló_dia_2.png", "cenarios/cenario-oca2-dia.jpg"),
    ("Ocas/Yebá Bëló_noite_2.png", "cenarios/cenario-oca2-noite.jpg"),
    # A oca 3 (Wanadi) abre no dia 3: uma imagem de dia e outra de noite.
    ("Ocas/Wanadi_dia_3.png", "cenarios/cenario-oca3-dia.jpg"),
    ("Ocas/Wanadi_noite_3.png", "cenarios/cenario-oca3-noite.jpg"),
    # O tapiri por dentro: uma imagem só, para o dia e a noite.
    ("Ocas/Tabiri.png", "cenarios/cenario-tapiri.jpg"),
    # O Anhangá: a mata para onde o pajé aponta, a 1ª, a 2ª e a 3ª vez (o veado cada vez mais
    # à vista).
    ("Ar_livre/Anhanga_um.png", "cenarios/anhanga-1.jpg"),
    ("Ar_livre/Anhanga_dois.png", "cenarios/anhanga-2.jpg"),
    ("Ar_livre/Anhanga_tres.png", "cenarios/anhanga-3.jpg"),
    # As imagens atrás das telas de cada final (Arte/Ar_livre/Finais/).
    ("Ar_livre/Finais/Anhanga_final.png", "cenarios/anhanga-final.jpg"),
    ("Ar_livre/Finais/AguaDoBatismo.png", "cenarios/final-batismo.jpg"),
    ("Ar_livre/Finais/ATroca.png", "cenarios/final-troca.jpg"),
    ("Ar_livre/Finais/ALoucura.png", "cenarios/final-loucura.jpg"),
    ("Ar_livre/Finais/RioAcima.png", "cenarios/final-rio-acima.jpg"),
    ("Ar_livre/Finais/aHonra.png", "cenarios/final-honra.jpg"),
    ("Ar_livre/Finais/OVazio.png", "cenarios/final-vazio.jpg"),
    ("Ar_livre/Finais/OTapiri.png", "cenarios/final-tapiri.jpg"),
    ("Ar_livre/Finais/GuerraJusta.png", "cenarios/final-guerra-justa.jpg"),
    ("Ar_livre/Finais/Ferida.png", "cenarios/final-ferida.jpg"),
]

# Cenários que saem mais claros que o original (1 = igual; 1.3 = 30% mais claro).
CLAREAR = {
    "cenarios/cenario-oca3-dia.jpg": 1.3,     # a oca Wanadi, onde Potira fica
    "cenarios/cenario-oca3-noite.jpg": 1.3,
    # O Anhangá veio muito escuro: com o filtro da noite por cima, o veado quase sumia.
    "cenarios/anhanga-1.jpg": 2.2,
    "cenarios/anhanga-2.jpg": 2.2,
    "cenarios/anhanga-3.jpg": 2.0,
    "cenarios/anhanga-final.jpg": 1.8,
    # As esteiras (o corpo coberto) se misturavam com o chão escuro da fogueira.
    "personagens/esteira.png": 2.1,
    "personagens/esteira-amaldicoado.png": 2.1,
}

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
# Arte com o fundo xadrez desenhado na imagem (cinza e branco, sem transparência de verdade):
# o xadrez preso entre o braço e o corpo forma manchas pequenas, que também saem.
ARTE_XADREZ = ["personagens_png/Potira_png.png", "Personagens_sentados_png/Potira_sentada_png.png",
               "personagens_png/esteira_amaldicoado.png", "personagens_png/Padre.png"]
AREA_MINIMA_BRANCO_CERCADO_XADREZ = 30
LIMIAR_BRANCO_CERCADO_XADREZ = 232   # o cinza do xadrez (238) também conta

# Arte que já vem transparente: o fundo é conhecido, então a limpeza perto da borda pode ser
# mais firme. A ferramenta que tira o fundo costuma deixar fios meio transparentes porém
# BRANCOS em volta do cabelo; esses somem, assim como o quase-branco colado na borda.
LIMIAR_BRANCO_PRESO_TRANSPARENTE = 215
DISTANCIA_BRANCO_PRESO_TRANSPARENTE = 10
LIMIAR_BRANCO_CERCADO_TRANSPARENTE = 228
LIMIAR_FIO_BRANCO = 190   # pixel meio transparente com o canal mais escuro acima disto: some
AREA_MINIMA_BRANCO_CERCADO_TRANSPARENTE = 600

# "Descascar" a borda (só para quem tem True no fim da linha em PERSONAGENS): tira, camada
# por camada, os pixels CLAROS e ACINZENTADOS encostados no transparente (fios brancos que
# sobram no cabelo). Cabelo escuro, pele e roupa bege (que têm cor) não saem.
CAMADAS_DESCASCAR = 6
CLARO_DESCASCAR = 140        # canal mais escuro acima disto = claro
NEUTRO_DESCASCAR = 30        # diferença entre o canal mais claro e o mais escuro abaixo disto = sem cor

# Lista de personagens: (original dentro de Arte/, destino dentro de assets/, giro, meio da coxa).
# Todas as artes vêm de Arte/personagens_png/personagens_em_png/, com fundo transparente.
# - giro: as artes vieram deitadas, com a cabeça para a direita; 90 gira no
#   sentido anti-horário e deixa a pessoa de pé. Use 0 se a arte já estiver de pé.
# - meio da coxa: a altura (em pixels da arte JÁ DE PÉ, contando de cima) onde fica o meio
#   das coxas. O topo da cabeça é achado sozinho. Se a arte acaba antes do meio da coxa
#   (Mbaé, Tamandaré-mirim e Iandé foram desenhados só até a cintura ou o quadril), coloque
#   onde a coxa estaria: o pedaço que falta fica transparente, escondido atrás da caixa de fala.
PNG = "personagens_png/"
PERSONAGENS = [
    (PNG + "Yara.png", "personagens/yara.png", 90, 1675, True),
    (PNG + "Mbaé.png", "personagens/mbae.png", 90, 1920),
    # Potira veio de novo (Potira_png.png): já de pé, com o fundo xadrez desenhado na própria
    # imagem (cinza e branco, sem transparência de verdade), que sai como fundo branco.
    (PNG + "Potira_png.png", "personagens/potira.png", 0, 950),
    (PNG + "Tama.png", "personagens/tamandare.png", 90, 1950),
    (PNG + "Iandé.png", "personagens/iande.png", 90, 1785),
    (PNG + "Krenan.png", "personagens/krenan.png", 90, 1590),
    (PNG + "Araci.png", "personagens/araci.png", 90, 1550),
    (PNG + "Irmão Aleixo.png", "personagens/aleixo.png", 0, 1520),
    # O pajé já veio de pé. O topo é o do cocar de penas, então a cabeça fica um pouco menor.
    (PNG + "Pajé.png", "personagens/paje.png", 0, 920),
    # O padre novo da vila (noite 9, A Água do Batismo): já de pé, com o fundo xadrez desenhado.
    ("personagens_png/Padre.png", "personagens/padre.png", 0, 1200),
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
    if destino in CLAREAR:
        imagem = ImageEnhance.Brightness(imagem).enhance(CLAREAR[destino])
    imagem.save(caminho_destino, quality=QUALIDADE_JPG, optimize=True, progressive=True)
    tamanho_kb = os.path.getsize(caminho_destino) // 1024
    print("  ok  %-22s -> %-36s %4d KB" % (origem, destino, tamanho_kb))


def tirar_fundo_branco(imagem, limiar_preso=LIMIAR_BRANCO_PRESO, distancia=DISTANCIA_BRANCO_PRESO,
                       limiar_cercado=LIMIAR_BRANCO_CERCADO, area_cercado=AREA_MINIMA_BRANCO_CERCADO):
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
    for _ in range(distancia // 2):
        perto_do_fundo = perto_do_fundo.filter(ImageFilter.MaxFilter(5))
    bem_branco = mais_escuro.point(lambda v: 255 if v >= limiar_preso else 0)
    fundo = ImageChops.lighter(fundo, ImageChops.multiply(perto_do_fundo, bem_branco))
    fundo = _juntar_brancos_grandes(fundo, mais_escuro, limiar_cercado, area_cercado)
    alfa = ImageChops.invert(fundo)
    # Come 1 pixel da borda (tira o contorno claro) e suaviza o recorte.
    alfa = alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    imagem.putalpha(alfa)
    return imagem


def _juntar_brancos_grandes(fundo, mais_escuro, limiar_cercado=LIMIAR_BRANCO_CERCADO,
                            area_minima=AREA_MINIMA_BRANCO_CERCADO):
    """Marca como fundo as manchas brancas grandes que o balde de tinta da borda não alcançou."""
    branco = mais_escuro.point(lambda v: 255 if v >= limiar_cercado else 0)
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
            novo = 50 if area >= area_minima else 200
            marcas = marcas.point(lambda v, novo=novo: novo if v == 100 else v)
            pixels = marcas.load()
    grandes = marcas.point(lambda v: 255 if v == 50 else 0)
    return ImageChops.lighter(fundo, grandes)


def descascar_borda(imagem):
    """Tira os fios claros e sem cor da borda, uma camada de pixels por vez."""
    r, g, b, alfa = imagem.split()
    mais_escuro = ImageChops.darker(ImageChops.darker(r, g), b)
    mais_claro = ImageChops.lighter(ImageChops.lighter(r, g), b)
    claro = mais_escuro.point(lambda v: 255 if v >= CLARO_DESCASCAR else 0)
    neutro = ImageChops.subtract(mais_claro, mais_escuro).point(lambda v: 255 if v <= NEUTRO_DESCASCAR else 0)
    fio = ImageChops.multiply(claro, neutro)
    for _ in range(CAMADAS_DESCASCAR):
        vazio = alfa.point(lambda a: 255 if a < 20 else 0)
        borda = vazio.filter(ImageFilter.MaxFilter(3))          # encosta no transparente
        tirar = ImageChops.multiply(borda, fio)
        alfa = ImageChops.subtract(alfa, tirar)
    imagem.putalpha(alfa)
    return imagem


def converter_personagem(origem, destino, giro, meio_da_coxa, descascar=False):
    caminho_origem = os.path.join(PASTA_ARTE, origem)
    caminho_destino = os.path.join(PASTA_ASSETS, destino)
    if not os.path.exists(caminho_origem):
        print("  FALTA o original:", caminho_origem)
        return
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
    imagem = Image.open(caminho_origem).convert("RGBA")
    if giro:
        imagem = imagem.rotate(giro, expand=True, fillcolor=(0, 0, 0, 0))
    if imagem.getchannel("A").getextrema()[0] < 255:
        # Arte que já vem com fundo transparente: o recorte de fora feito por quem desenhou
        # é mantido. Mas o branco PRESO (entre o braço e o corpo, entre o arco e o corpo) e
        # o contorno branco que às vezes sobra no cabelo ainda saem, como na arte de fundo branco.
        alfa_original = imagem.getchannel("A")
        sobre_branco = Image.new("RGBA", imagem.size, (255, 255, 255, 255))
        sobre_branco.alpha_composite(imagem)
        alfa_limpo = tirar_fundo_branco(sobre_branco, LIMIAR_BRANCO_PRESO_TRANSPARENTE,
                                        DISTANCIA_BRANCO_PRESO_TRANSPARENTE,
                                        LIMIAR_BRANCO_CERCADO_TRANSPARENTE,
                                        AREA_MINIMA_BRANCO_CERCADO_TRANSPARENTE).getchannel("A")
        # Fios brancos meio transparentes (sobra da ferramenta que tirou o fundo).
        r, g, b, _ = imagem.split()
        claro = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: 255 if v >= LIMIAR_FIO_BRANCO else 0)
        meio_transparente = alfa_original.point(lambda a: 255 if 0 < a < 250 else 0)
        fio_branco = ImageChops.multiply(claro, meio_transparente).filter(ImageFilter.MaxFilter(3))
        alfa = ImageChops.darker(alfa_original, alfa_limpo)
        imagem.putalpha(ImageChops.subtract(alfa, fio_branco))
        if descascar:
            imagem = descascar_borda(imagem)
    elif origem in ARTE_XADREZ:
        imagem = tirar_fundo_branco(imagem, limiar_cercado=LIMIAR_BRANCO_CERCADO_XADREZ,
                                    area_cercado=AREA_MINIMA_BRANCO_CERCADO_XADREZ)
        imagem = descascar_borda(imagem)   # os fios claros do xadrez que sobram na borda
    else:
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


# PESSOAS SENTADAS (a fogueira, de noite): o corpo inteiro, do topo da cabeça ao chão, já de pé
# na arte (sem giro) e com fundo transparente. Saem todas com a mesma altura; o tamanho na
# fogueira se ajusta em dados/noites.py ("escala").
ALTURA_SENTADO = 560
SENTADOS_PNG = "Personagens_sentados_png/Personagens_sentados/"
SENTADOS = [
    (SENTADOS_PNG + "Yara_sentada.png", "personagens/sentados/yara.png"),
    (SENTADOS_PNG + "Mbaé_sentado.png", "personagens/sentados/mbae.png"),
    (SENTADOS_PNG + "Pajé_sentado.png", "personagens/sentados/paje.png"),
    (SENTADOS_PNG + "Tama_sentado.png", "personagens/sentados/tamandare.png"),
    (SENTADOS_PNG + "Krenan_sentado.png", "personagens/sentados/krenan.png"),
    # Os dois nomes vieram trocados: a moça grávida (Araci) está no arquivo "Iandé_sentada",
    # e a moça abraçando os joelhos (Iandé) no arquivo "Araci_sentada".
    (SENTADOS_PNG + "Iandé_sentada.png", "personagens/sentados/araci.png"),
    (SENTADOS_PNG + "Araci_sentada.png", "personagens/sentados/iande.png"),
    # Potira veio fora da pasta dos sentados, com o fundo xadrez desenhado na imagem.
    ("Personagens_sentados_png/Potira_sentada_png.png", "personagens/sentados/potira.png"),
]

# O corpo coberto com a esteira, deitado (no lugar de quem morreu: na fogueira, na oca ou no
# tapiri). Sai com a mesma altura dos sentados; quem desenha diminui (cenas/dia.py, ESCALA_ESTEIRA).
# A esteira de quem era amaldiçoado veio com o fundo xadrez desenhado (ARTE_XADREZ).
ESTEIRAS = [
    ("personagens_png/esteira.png", "personagens/esteira.png"),
    ("personagens_png/esteira_amaldicoado.png", "personagens/esteira-amaldicoado.png"),
]


def converter_sentado(origem, destino):
    caminho_origem = os.path.join(PASTA_ARTE, origem)
    caminho_destino = os.path.join(PASTA_ASSETS, destino)
    if not os.path.exists(caminho_origem):
        print("  FALTA o original:", caminho_origem)
        return
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
    imagem = Image.open(caminho_origem).convert("RGBA")
    if imagem.getchannel("A").getextrema()[0] == 255:
        # Sem transparência (fundo branco, ou o xadrez claro desenhado na imagem): tira o fundo.
        area = AREA_MINIMA_BRANCO_CERCADO_XADREZ if origem in ARTE_XADREZ else AREA_MINIMA_BRANCO_CERCADO
        imagem = tirar_fundo_branco(imagem, limiar_cercado=LIMIAR_BRANCO_CERCADO_XADREZ if origem in ARTE_XADREZ
                                    else LIMIAR_BRANCO_CERCADO, area_cercado=area)
        if origem in ARTE_XADREZ:
            imagem = descascar_borda(imagem)   # os fios claros do xadrez que sobram na borda
    imagem = imagem.crop(imagem.getchannel("A").getbbox())   # só a pessoa, sem a sobra em volta
    escala = ALTURA_SENTADO / imagem.height
    imagem = imagem.resize((round(imagem.width * escala), ALTURA_SENTADO), Image.LANCZOS)
    if destino in CLAREAR:
        # Clareia só a cor: a transparência fica como estava.
        alfa = imagem.getchannel("A")
        imagem = ImageEnhance.Brightness(imagem.convert("RGB")).enhance(CLAREAR[destino])
        imagem.putalpha(alfa)
    imagem.save(caminho_destino, optimize=True)
    tamanho_kb = os.path.getsize(caminho_destino) // 1024
    print("  ok  %-22s -> %-36s %4d KB" % (origem.split("/")[-1], destino, tamanho_kb))


# DETALHES DO EXAME (Arte/Doenças/): o olho e a boca de perto, que aparecem no exame da noite
# em vez de uma descrição. Saem em cores (a interface não passa pelo filtro da noite), com a
# borda "comida" (rasgada) de cada arte. Cada detalhe vira dois arquivos: o .jpg com a pintura
# (leve) e o -borda.png com a forma da borda (a transparência). O jogo junta os dois
# (motor/imagens.py). A arte que vem sem borda rasgada, ou com uma borda quase reta (que entra
# menos que BORDA_MINIMA), ganha uma parecida com a do olho vermelho da Yara (borda_rasgada).
# Quem mostra cada um e quando: Textos/Caraiba_Sinais_dos_Personagens.md.
TAMANHO_DETALHE = 420
QUALIDADE_DETALHE = 88
DOENCAS = "Doenças/"
DETALHES = [
    # Yara: o olho vermelho da fumaça nas noites 1 e 2 (e se pegar a febre); depois, o normal.
    (DOENCAS + "Yara/OlhoYara_Doente.png", "detalhes/olho-yara-vermelho.jpg"),
    (DOENCAS + "Yara/OlhoYara.png", "detalhes/olho-yara.jpg"),
    (DOENCAS + "Yara/BocaYara.png", "detalhes/boca-yara.jpg"),
    (DOENCAS + "Yara/BocaYaraDoente.png", "detalhes/boca-yara-doente.jpg"),
    # Mbaé: o olho até o 3º dia na oca; depois, o doente. A boca já chega ferida.
    (DOENCAS + "Mbaé/OlhoMbaé.png", "detalhes/olho-mbae.jpg"),
    (DOENCAS + "Mbaé/OlhoDoenteMbaé.png", "detalhes/olho-mbae-doente.jpg"),
    (DOENCAS + "Mbaé/BocaMbaé.png", "detalhes/boca-mbae.jpg"),
    (DOENCAS + "Mbaé/BocaMbaéDoente.png", "detalhes/boca-mbae-doente.jpg"),
    (DOENCAS + "Potira/OlhoPotira.png", "detalhes/olho-potira.jpg"),
    (DOENCAS + "Potira/OlharPotiraDoente.png", "detalhes/olho-potira-doente.jpg"),
    (DOENCAS + "Potira/BocaPotira.png", "detalhes/boca-potira.jpg"),
    (DOENCAS + "Potira/BocaPotiraDoente.png", "detalhes/boca-potira-doente.jpg"),
    (DOENCAS + "Tama/OlhoTama.png", "detalhes/olho-tamandare.jpg"),
    (DOENCAS + "Tama/OlhoTamaDoente.png", "detalhes/olho-tamandare-doente.jpg"),
    (DOENCAS + "Tama/BocaTama.png", "detalhes/boca-tamandare.jpg"),
    (DOENCAS + "Tama/BocaTamaDoente.png", "detalhes/boca-tamandare-doente.jpg"),
    (DOENCAS + "Iandé/OlhoIandé.png", "detalhes/olho-iande.jpg"),
    (DOENCAS + "Iandé/OlhoIandé_Doente.png", "detalhes/olho-iande-doente.jpg"),
    (DOENCAS + "Iandé/BocaIandé.png", "detalhes/boca-iande.jpg"),
    (DOENCAS + "Iandé/BocaIandéDoente.png", "detalhes/boca-iande-doente.jpg"),
    (DOENCAS + "Araci/OlhoDoenteAraci.png", "detalhes/olho-araci-doente.jpg"),
    (DOENCAS + "Araci/BocaAraciDoente.png", "detalhes/boca-araci-doente.jpg"),
    # Atrás da orelha e o pescoço: a saudável vale para as duas zonas (PessoaOrelhaPescoco);
    # a doente é uma para cada (PessoaOrelhaDoente, PessoaPescocoDoente).
    (DOENCAS + "Yara/YaraOrelhaPescoco.png", "detalhes/orelha-pescoco-yara.jpg"),
    (DOENCAS + "Yara/YaraOrelhaDoente.png", "detalhes/orelha-yara-doente.jpg"),
    (DOENCAS + "Yara/YaraPescocoDoenete.png", "detalhes/pescoco-yara-doente.jpg"),
    (DOENCAS + "Mbaé/MbaeOrelhaPescoco.png", "detalhes/orelha-pescoco-mbae.jpg"),
    (DOENCAS + "Mbaé/MbaeOrelhaDoente.png", "detalhes/orelha-mbae-doente.jpg"),
    (DOENCAS + "Mbaé/MbaePescocoDoente.png", "detalhes/pescoco-mbae-doente.jpg"),
    # O nome diz "saudável", mas a arte já tem as manchas: Araci sempre chega doente.
    (DOENCAS + "Araci/AraciOrelhaPescoco.png", "detalhes/orelha-pescoco-araci-doente.jpg"),
    (DOENCAS + "Potira/PotiraOrelhaPescoco.png", "detalhes/orelha-pescoco-potira.jpg"),
    (DOENCAS + "Potira/PotiraOrelhaDoente.png", "detalhes/orelha-potira-doente.jpg"),
    (DOENCAS + "Potira/PotiraPescocoDoente.png", "detalhes/pescoco-potira-doente.jpg"),
    (DOENCAS + "Tama/TamaOrelhaPescoco.png", "detalhes/orelha-pescoco-tamandare.jpg"),
    (DOENCAS + "Tama/TamaOrelhaDoente.png", "detalhes/orelha-tamandare-doente.jpg"),
    (DOENCAS + "Tama/TamaPescocoDoente.png", "detalhes/pescoco-tamandare-doente.jpg"),
    (DOENCAS + "Iandé/IandeOrelhaPescoco.png", "detalhes/orelha-pescoco-iande.jpg"),
    (DOENCAS + "Iandé/IandeOrelhaDoente.png", "detalhes/orelha-iande-doente.jpg"),
    (DOENCAS + "Iandé/IandePescocoDoente.png", "detalhes/pescoco-iande-doente.jpg"),
]
# Detalhes com o fundo xadrez desenhado na imagem (sem transparência de verdade).
DETALHES_XADREZ = [DOENCAS + "Mbaé/OlhoDoenteMbaé.png", DOENCAS + "Tama/OlhoTamaDoente.png",
                   DOENCAS + "Tama/BocaTama.png", DOENCAS + "Tama/BocaTamaDoente.png"]
# Detalhes com a borda rasgada sobre um fundo preto pintado na imagem (sem transparência).
DETALHES_FUNDO_PRETO = [DOENCAS + "Potira/OlhoPotira.png", DOENCAS + "Tama/OlhoTama.png",
                        DOENCAS + "Yara/OlhoYara.png"]
LIMIAR_FUNDO_PRETO = 4   # canal mais claro abaixo disto, ligado à borda, é o fundo preto
OPACO = 250   # alfa a partir do qual o pixel conta como pintura (e não como borda rasgada)


def tirar_fundo_preto(imagem):
    """Deixa transparente o preto que encosta na borda da imagem (o fundo)."""
    r, g, b, _ = imagem.split()
    mais_claro = ImageChops.lighter(ImageChops.lighter(r, g), b)
    escuro = mais_claro.point(lambda v: 255 if v < LIMIAR_FUNDO_PRETO else 0)
    largura, altura = escuro.size
    for ponto in [(0, 0), (largura - 1, 0), (0, altura - 1), (largura - 1, altura - 1)]:
        if escuro.getpixel(ponto) == 255:
            ImageDraw.floodfill(escuro, ponto, 128)
    imagem.putalpha(escuro.point(lambda v: 0 if v == 128 else 255))
    return imagem


PROFUNDIDADE_BORDA = 0.04   # o quanto a borda gerada "come" para dentro (fração do lado)
BORDA_MINIMA = 0.08         # borda mais rasa que isto (fração do lado, em média) ganha a gerada


def profundidade_da_borda(imagem):
    """Quanto a parte transparente entra, em média, vindo de cada lado (fração do lado)."""
    alfa = imagem.getchannel("A")
    alfa = alfa.crop(alfa.getbbox())
    largura, altura = alfa.size
    pixels = alfa.load()
    total = vezes = 0
    for fixo, comprimento, ponto in [(altura, largura, lambda a, b: (b, a)),
                                     (largura, altura, lambda a, b: (a, b))]:
        for a in range(0, fixo, 6):
            for caminho in (range(comprimento), range(comprimento - 1, -1, -1)):
                entra = 0
                for b in caminho:
                    if pixels[ponto(a, b)] >= 128:
                        break
                    entra += 1
                total += entra
                vezes += 1
    return total / vezes / min(largura, altura)


def borda_rasgada(imagem, semente):
    """Come a borda de uma arte que veio com o canto reto, parecida com as outras (cada arte
    tem o seu desenho, sorteado pela semente: rodar de novo dá a mesma borda)."""
    sorte = random.Random(semente)
    largura, altura = imagem.size
    fundo = round(min(largura, altura) * PROFUNDIDADE_BORDA)
    passo = max(3, min(largura, altura) // 150)

    def recuos(quantos):
        """Quanto cada ponto do lado entra: ondulado, com umas mordidas mais fundas."""
        valores = [sorte.uniform(0.1, 1.0) for _ in range(quantos)]
        valores = [(valores[i - 1] + 2 * valores[i] + valores[(i + 1) % quantos]) / 4
                   for i in range(quantos)]
        # Umas pinceladas que entram mais fundo, como na borda do olho da Yara.
        return [fundo * (v * sorte.uniform(1.6, 2.4) if sorte.random() < 0.08 else v)
                for v in valores]

    pontos = []
    xs = list(range(0, largura, passo)) + [largura]
    ys = list(range(0, altura, passo)) + [altura]
    pontos += [(x, r) for x, r in zip(xs, recuos(len(xs)))]                       # em cima
    pontos += [(largura - r, y) for y, r in zip(ys, recuos(len(ys)))]             # direita
    pontos += [(x, altura - r) for x, r in zip(reversed(xs), recuos(len(xs)))]    # embaixo
    pontos += [(r, y) for y, r in zip(reversed(ys), recuos(len(ys)))]             # esquerda
    forma = Image.new("L", imagem.size, 0)
    ImageDraw.Draw(forma).polygon(pontos, fill=255)
    forma = forma.filter(ImageFilter.GaussianBlur(1))
    imagem.putalpha(ImageChops.darker(imagem.getchannel("A"), forma))
    return imagem


def so_a_pintura(imagem):
    """Tira os pedaços soltos fora da borda (os pontinhos do xadrez que sobram): fica só o
    que está ligado ao meio da pintura."""
    alfa = imagem.getchannel("A")
    pintura = alfa.point(lambda v: 255 if v >= 128 else 0)
    ImageDraw.floodfill(pintura, (pintura.width // 2, pintura.height // 2), 128)
    ligado = pintura.point(lambda v: 255 if v == 128 else 0).filter(ImageFilter.MaxFilter(3))
    imagem.putalpha(ImageChops.darker(alfa, ligado))
    return imagem


def caminho_borda(caminho_jpg):
    """detalhes/olho-yara.jpg -> detalhes/olho-yara-borda.png (motor/imagens.py usa o mesmo nome)."""
    return caminho_jpg[:-len(".jpg")] + "-borda.png"


def quadrado_com_borda(imagem):
    """Só a pintura (sem a sobra transparente em volta), no meio de um quadrado transparente."""
    imagem = imagem.crop(imagem.getchannel("A").getbbox())
    lado = max(imagem.size)
    quadrado = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    quadrado.paste(imagem, ((lado - imagem.width) // 2, (lado - imagem.height) // 2))
    return quadrado


def converter_detalhe(origem, destino):
    caminho_origem = os.path.join(PASTA_ARTE, origem)
    caminho_destino = os.path.join(PASTA_ASSETS, destino)
    if not os.path.exists(caminho_origem):
        print("  FALTA o original:", caminho_origem)
        return
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
    imagem = Image.open(caminho_origem).convert("RGBA")
    if origem in DETALHES_XADREZ:
        imagem = tirar_fundo_branco(imagem, limiar_cercado=LIMIAR_BRANCO_CERCADO_XADREZ,
                                    area_cercado=AREA_MINIMA_BRANCO_CERCADO_XADREZ)
    elif origem in DETALHES_FUNDO_PRETO:
        imagem = tirar_fundo_preto(imagem)
    imagem = so_a_pintura(imagem)
    if profundidade_da_borda(imagem) < BORDA_MINIMA:
        imagem = borda_rasgada(imagem, origem)   # veio com o canto reto, ou quase
    imagem = quadrado_com_borda(imagem)
    imagem = imagem.resize((TAMANHO_DETALHE, TAMANHO_DETALHE), Image.LANCZOS)
    alfa = imagem.getchannel("A")
    # A pintura em JPG (bem menor que PNG), com preto onde é transparente...
    pintura = Image.new("RGB", imagem.size, (0, 0, 0))
    pintura.paste(imagem.convert("RGB"), mask=alfa)
    pintura.save(caminho_destino, quality=QUALIDADE_DETALHE, optimize=True)
    # ...e a borda num PNG branco, só com a transparência (fica pequeno).
    borda = Image.new("RGBA", imagem.size, (255, 255, 255, 0))
    borda.putalpha(alfa)
    borda.save(caminho_borda(caminho_destino), optimize=True)
    tamanho_kb = (os.path.getsize(caminho_destino) + os.path.getsize(caminho_borda(caminho_destino))) // 1024
    print("  ok  %-22s -> %-36s %4d KB" % (origem.split("/")[-1], destino, tamanho_kb))


def main():
    if sys.argv[1:] == ["detalhes"]:   # só os detalhes do exame
        print("Convertendo detalhes do exame")
        for origem, destino in DETALHES:
            converter_detalhe(origem, destino)
        return
    print("Convertendo cenários de", PASTA_ARTE)
    for origem, destino in CENARIOS:
        converter_cenario(origem, destino)
    print("Convertendo personagens")
    for linha in PERSONAGENS:
        converter_personagem(*linha)
    print("Convertendo personagens sentados")
    for origem, destino in SENTADOS + ESTEIRAS:
        converter_sentado(origem, destino)
    print("Convertendo detalhes do exame")
    for origem, destino in DETALHES:
        converter_detalhe(origem, destino)
    print("Pronto.")


if __name__ == "__main__":
    main()
