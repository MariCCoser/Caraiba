# Os sons: o ambiente em loop de cada lugar e os efeitos curtos (a lista fica em dados/sons.py).
#
# - ambiente(nome): a cada quadro, o Jogo passa o ambiente da cena atual (Cena.som_ambiente).
#   Só faz algo quando ele muda: o que sai some devagar, o que entra aparece devagar.
# - efeito(nome): toca um som curto uma vez (ex.: os passos de quem chega).
# - atualizar_volume(): liga ou desliga tudo, conforme as Opções (preferencias.som).
#
# Sem placa de som (ou se o áudio falhar), tudo continua funcionando, só que em silêncio.
# No navegador, o som só começa depois do primeiro clique na página (regra dos navegadores).

import os

import pygame

import config
from dados.sons import AMBIENTES, EFEITOS, SONS, TROCA_MS
from motor import preferencias

_sons = {}          # nome -> pygame.mixer.Sound, carregado na primeira vez
_tocando = {}       # nome do som do ambiente -> Channel em que ele está tocando
_ambiente = None    # o ambiente que está tocando agora
_ligado = None      # None = ainda não tentou abrir o áudio


def _audio_ok():
    global _ligado
    if _ligado is None:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.set_num_channels(16)
            _ligado = True
        except pygame.error:
            _ligado = False
    return _ligado


def _som(nome):
    if nome not in _sons:
        try:
            _sons[nome] = pygame.mixer.Sound(os.path.join(config.PASTA_ASSETS, SONS[nome]))
        except (pygame.error, FileNotFoundError):
            _sons[nome] = None   # arquivo faltando: fica sem esse som
    return _sons[nome]


def ambiente(nome):
    """Troca o ambiente (um nome de AMBIENTES, ou None para silêncio). Com o som desligado,
    só guarda o nome: ele começa a tocar quando o som for ligado (atualizar_volume)."""
    global _ambiente
    if nome == _ambiente or not _audio_ok():
        return
    _ambiente = nome
    if not preferencias.atual.som:
        return
    camadas = AMBIENTES.get(nome, {})
    for som, canal in list(_tocando.items()):
        if som not in camadas:
            canal.fadeout(TROCA_MS)
            del _tocando[som]
    for som, volume in camadas.items():
        if som in _tocando:
            _tocando[som].set_volume(volume)
            continue
        arquivo = _som(som)
        if arquivo is None:
            continue
        canal = arquivo.play(loops=-1, fade_ms=TROCA_MS)
        if canal is not None:
            canal.set_volume(volume)
            _tocando[som] = canal


def efeito(nome):
    """Toca um som curto uma vez."""
    if not _audio_ok() or not preferencias.atual.som:
        return
    arquivo = _som(nome)
    if arquivo is None:
        return
    jeito = EFEITOS.get(nome, {})
    canal = arquivo.play()
    if canal is not None:
        canal.set_volume(jeito.get("volume", 1.0))
        if jeito.get("some_em_ms"):
            canal.fadeout(jeito["some_em_ms"])


def atualizar_volume():
    """Depois de ligar ou desligar o som nas Opções. Desligar para tudo; ligar começa de novo
    o ambiente do lugar onde o jogador está."""
    global _ambiente
    if not _audio_ok():
        return
    pygame.mixer.stop()
    _tocando.clear()
    nome, _ambiente = _ambiente, None
    ambiente(nome)


def parar():
    """Silêncio imediato (ao fechar o jogo)."""
    global _ambiente
    if _audio_ok():
        pygame.mixer.stop()
    _tocando.clear()
    _ambiente = None
