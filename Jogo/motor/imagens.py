# Carrega cada imagem do disco UMA vez só e guarda na memória (cache); se faltar arte, gera um provisório.

import os

import pygame

import config
from dados import arte
from motor import efeitos, fontes

# {caminho ou chave: Surface já convertida}
_cache = {}


def carregar(caminho_relativo, transparente=False):
    """Carrega assets/<caminho_relativo>. Se o arquivo não existir, devolve um provisório.

    `transparente=True` para imagens com fundo transparente (personagens);
    False para cenários (mais rápido de desenhar).
    """
    chave = ("arquivo", caminho_relativo, transparente)
    if chave in _cache:
        return _cache[chave]

    caminho = os.path.join(config.PASTA_ASSETS, caminho_relativo)
    if os.path.exists(caminho):
        imagem = pygame.image.load(caminho)
        # convert() deixa a imagem no formato da tela: desenha muito mais rápido.
        imagem = imagem.convert_alpha() if transparente else imagem.convert()
    else:
        print("Aviso: arte não encontrada, usando provisório:", caminho_relativo)
        imagem = provisorio(caminho_relativo, config.TAMANHO_LOGICO)

    _cache[chave] = imagem
    return imagem


def cenario(apelido, filtro=None):
    """Devolve o cenário `apelido` (veja dados/arte.py), já com o filtro pedido.

    filtro: None (original), "noite" (âmbar monocromático) ou "dia" (frio e sem cor).
    O filtro é aplicado uma vez e guardado, para não pesar a cada quadro.
    """
    chave = ("cenario", apelido, filtro)
    if chave in _cache:
        return _cache[chave]

    if apelido in arte.CENARIOS:
        imagem = carregar(arte.CENARIOS[apelido])
    else:
        print("Aviso: cenário sem entrada em dados/arte.py:", apelido)
        imagem = provisorio(apelido, config.TAMANHO_LOGICO)

    # Garante o tamanho lógico mesmo se alguém colocar uma arte de outro tamanho.
    if imagem.get_size() != config.TAMANHO_LOGICO:
        imagem = pygame.transform.smoothscale(imagem, config.TAMANHO_LOGICO)

    if filtro == "noite":
        imagem = efeitos.filtro_noite(imagem)
    elif filtro == "dia":
        imagem = efeitos.filtro_dia(imagem)

    _cache[chave] = imagem
    return imagem


def personagem(apelido, filtro=None):
    """Devolve a pessoa `apelido` (veja dados/arte.py) com o filtro pedido, como em cenario()."""
    chave = ("personagem", apelido, filtro)
    if chave in _cache:
        return _cache[chave]

    if apelido in arte.PERSONAGENS:
        caminho = arte.PERSONAGENS[apelido]
        if os.path.exists(os.path.join(config.PASTA_ASSETS, caminho)):
            imagem = carregar(caminho, transparente=True)
        else:
            print("Aviso: arte não encontrada, usando provisório:", caminho)
            imagem = provisorio(apelido, (600, 860), silhueta=True)
    else:
        print("Aviso: personagem sem entrada em dados/arte.py:", apelido)
        imagem = provisorio(apelido, (600, 860), silhueta=True)

    if filtro in ("noite", "dia"):
        imagem = _filtrar_mantendo_transparencia(imagem, filtro)

    _cache[chave] = imagem
    return imagem


def _filtrar_mantendo_transparencia(imagem, filtro):
    """Os filtros perdem a transparência (o fundo vira preto). Aqui o filtro é aplicado
    numa cópia opaca e depois a transparência original é devolvida."""
    opaca = imagem.convert()
    if filtro == "noite":
        filtrada = efeitos.filtro_noite(opaca)
    else:
        filtrada = efeitos.filtro_dia(opaca)
    resultado = filtrada.convert_alpha()
    # Máscara: a mesma imagem toda branca, só com a transparência original.
    mascara = imagem.copy()
    mascara.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
    resultado.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return resultado


def provisorio(nome, tamanho, silhueta=False):
    """Desenha uma imagem provisória com o nome escrito, para o jogo nunca travar esperando arte.

    silhueta=True desenha o contorno simples de uma pessoa (para personagens).
    """
    imagem = pygame.Surface(tamanho, pygame.SRCALPHA if silhueta else 0)
    largura, altura = tamanho
    if silhueta:
        imagem.fill((0, 0, 0, 0))
        cx = largura // 2
        # cabeça e corpo em Fumaça, o meio-tom da pele
        pygame.draw.circle(imagem, config.FUMACA, (cx, altura // 8), largura // 7)
        pygame.draw.ellipse(imagem, config.FUMACA,
                            (cx - largura // 3, altura // 5, 2 * largura // 3, altura * 3 // 4))
    else:
        imagem.fill(config.TERRA)
        pygame.draw.rect(imagem, config.FUMACA, imagem.get_rect(), 6)
    texto = fontes.fonte("sans", 40).render("[" + nome + "]", True, config.TABATINGA)
    imagem.blit(texto, texto.get_rect(center=(largura // 2, altura // 2)))
    return imagem


def limpar_cache():
    """Esquece as imagens carregadas (necessário ao fechar o pygame)."""
    _cache.clear()
