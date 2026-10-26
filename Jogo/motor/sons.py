# Os sons: o ambiente em loop de cada lugar e os efeitos curtos (a lista fica em dados/sons.py).
#
# - ambiente(nome, intensidade): a cada quadro, o Jogo passa o ambiente da cena atual
#   (Cena.som_ambiente) e o quanto os sons que crescem já cresceram (Cena.som_intensidade, de
#   0 a 1: a introdução). Cada som tem um volume "alvo"; atualizar(dt) leva o volume até ele aos
#   poucos. Assim o que sai some devagar, o que entra aparece devagar, e um som que só muda de
#   volume (ex.: a mata, ao entrar na oca) também muda devagar, sem pulo.
# - efeito(nome): toca um som curto uma vez (ex.: os passos de quem chega).
# - atualizar_volume(): liga ou desliga tudo, conforme as Opções (preferencias.som).
#
# Sem placa de som (ou se o áudio falhar), tudo continua funcionando, só que em silêncio.
# No navegador, o som só começa depois do primeiro clique na página (regra dos navegadores).

import os

import pygame

import config
from dados.sons import AMBIENTES, CRESCEM, EFEITOS, SONS, TROCA_MS
from motor import preferencias

_sons = {}          # nome -> pygame.mixer.Sound, carregado na primeira vez
_tocando = {}       # nome do som do ambiente -> {"canal", "volume" (o de agora), "alvo"}
_ambiente = None    # o ambiente que está tocando agora
_intensidade = 1.0  # o quanto os sons de CRESCEM já cresceram (0 a 1)
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


def _alvos(nome, intensidade):
    """O volume final de cada som do ambiente (os de CRESCEM, vezes a intensidade)."""
    crescem = CRESCEM.get(nome, [])
    return {som: volume * (intensidade if som in crescem else 1.0)
            for som, volume in AMBIENTES.get(nome, {}).items()}


def ambiente(nome, intensidade=1.0):
    """Troca o ambiente (um nome de AMBIENTES, ou None para silêncio). Com o som desligado,
    só guarda o nome: ele começa a tocar quando o som for ligado (atualizar_volume)."""
    global _ambiente, _intensidade
    if (nome, intensidade) == (_ambiente, _intensidade) or not _audio_ok():
        return
    _ambiente, _intensidade = nome, intensidade
    if not preferencias.atual.som:
        return
    alvos = _alvos(nome, intensidade)
    for som, tocando in _tocando.items():
        tocando["alvo"] = alvos.get(som, 0.0)   # o que não está no ambiente novo some devagar
    for som, alvo in alvos.items():
        if som in _tocando:
            continue
        arquivo = _som(som)
        canal = arquivo.play(loops=-1) if arquivo else None
        if canal is not None:
            canal.set_volume(0.0)
            _tocando[som] = {"canal": canal, "volume": 0.0, "alvo": alvo}


def atualizar(dt):
    """A cada quadro: cada som anda um pouco até o volume alvo. O que chegou a zero para."""
    passo = dt * 1000 / TROCA_MS
    for som, tocando in list(_tocando.items()):
        volume, alvo = tocando["volume"], tocando["alvo"]
        if volume == alvo:
            continue
        volume = min(alvo, volume + passo) if volume < alvo else max(alvo, volume - passo)
        tocando["volume"] = volume
        tocando["canal"].set_volume(volume)
        if volume == 0.0 and alvo == 0.0:
            tocando["canal"].stop()
            del _tocando[som]


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
    ambiente(nome, _intensidade)


def parar():
    """Silêncio imediato (ao fechar o jogo)."""
    global _ambiente
    if _audio_ok():
        pygame.mixer.stop()
    _tocando.clear()
    _ambiente = None
