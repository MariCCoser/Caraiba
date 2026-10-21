# Joga muitas partidas sozinho, sem janela, e conta em que final cada uma acabou.
#
# Usa a cena Dia de verdade (cenas/dia.py) com os roteiros de dados/dias.py e dados/noites.py:
# se o roteiro ou as condições dos finais mudarem, é só rodar de novo.
#
# Como rodar (de dentro da pasta Jogo):
#     python -m ferramentas.simular_finais                  (2000 partidas, ao acaso)
#     python -m ferramentas.simular_finais 10000
#     python -m ferramentas.simular_finais 1000 tapiri      (quem tenta O Tapiri: ESTRATEGIAS)
#
# O "jogador" (sem estratégia) escolhe ao acaso: cada botão que aparece tem a mesma chance. Nas
# perguntas e no exame, a cada vez ele faz mais uma pergunta (ou olha mais uma zona) com chance
# CHANCE_DE_PERGUNTAR; senão segue. Na aldeia de dia, conversa com cada pessoa com chance
# CHANCE_DE_CONVERSAR. Na fogueira, conversa com quem ainda não conversou; quando já dá para
# dormir, dorme com chance CHANCE_DE_DORMIR. Com uma estratégia, ele prefere certas opções
# (ESTRATEGIAS) e, no resto, continua ao acaso.

import os
import random
import sys
import tempfile
from collections import Counter

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import config  # noqa: E402

config.PASTA_SAVES = tempfile.mkdtemp(prefix="caraiba-simulacao-")

from cenas.dia import Dia  # noqa: E402
from dados.aldeia import TAPIRI  # noqa: E402
from dados.dias import DIAS, PERGUNTAS_ALEIXO, PERGUNTOU_LEVADOS, perguntas_sobre_os_levados  # noqa: E402
from dados.febre import DOENTES  # noqa: E402
from dados.finais import FINAIS  # noqa: E402
from dados.noites import QUEM_SOBE  # noqa: E402
from estado import Estado  # noqa: E402
from motor import febre, finais  # noqa: E402
from motor.jogo import Jogo  # noqa: E402

CHANCE_DE_PERGUNTAR = 0.6
CHANCE_DE_CONVERSAR = 0.5
CHANCE_DE_DORMIR = 0.5
LIMITE_DE_ACOES = 5000   # por dia: se passar disso, o roteiro prendeu o jogador


def _onde_dorme_tapiri(dia):
    """Doente de verdade vai para o tapiri, se há vaga; o resto fica na oca."""
    quem = dia.passo_atual.get("quem")
    if quem in DOENTES and len(dia.estado.tapiri) < TAPIRI["vagas"]:
        return ["Levar ao tapiri"]
    return ["Deixar na oca"]


def _entregar(dia):
    return [bloco.texto for bloco, _ in dia.botoes if bloco.texto.startswith("Entregar")]


# Cada estratégia: "preferir" diz as opções preferidas da escolha que está na tela, em ordem
# (a primeira da lista que estiver habilitada ganha); "evitar": perguntas que ele nunca faz;
# "historias": True faz todas as perguntas das
# conversas (a memória da Honra); "perguntar" são as perguntas que ele sempre faz primeiro;
# "paje_primeiro": True, na fogueira, fala com o pajé antes de todos (antes de gastar os olhares).
# O que a estratégia não decide, o jogador escolhe ao acaso.
ESTRATEGIAS = {
    "troca": {"preferir": lambda dia: ["Deixar entrar", "Deixar na oca"] + _entregar(dia)},
    # Matar cedo esvazia a aldeia (O Vazio vem antes da 3ª morte): só mata da noite 5 em diante.
    "loucura": {"preferir": lambda dia: ["Deixar entrar", "Negar",
                                         "Matar" if dia.estado.dia >= 5 else "Deixar na oca"]},
    "tapiri": {"preferir": lambda dia: ["Deixar entrar", "Negar", "Não deixar", "Ficar na aldeia"]
               + _onde_dorme_tapiri(dia)},
    "honra": {"historias": True,
              "preferir": lambda dia: ["Deixar entrar", "Negar", "Não deixar", "Ficar na aldeia"]
              + _onde_dorme_tapiri(dia)},
    # A aldeia precisa chegar viva à noite 10: doentes no tapiri, um doente sobe com Krenan na noite 8
    # e, na noite 10, o jogador vai com ele.
    "rio_acima": {"preferir": lambda dia: ["Deixar entrar", "Negar", "Chamar para a fogueira",
                                           "Deixar levar alguém"]
                  + (["Ir com ele"] if dia.estado.dia >= 10 else DOENTES + QUEM_SOBE)
                  + _onde_dorme_tapiri(dia)},
    # Entrega 1 pessoa só no dia 9, nunca pergunta por quem o Aleixo levou e aceita o batismo.
    "batismo": {"evitar": [p["pergunta"] for p in PERGUNTAS_ALEIXO[9] + perguntas_sobre_os_levados()
                           if p.get("efeitos") == PERGUNTOU_LEVADOS],
                "preferir": lambda dia: (_entregar(dia)[:1] if dia.estado.dia == 9 else [])
                + ["Deixar entrar", "Negar", "Não deixar", "Aceitar o batismo", "Deixar na oca"]},
    "anhanga": {"perguntar": ["Que barulho é esse na mata?"], "paje_primeiro": True,
                "preferir": lambda dia: ["Deixar entrar", "Negar", "Não deixar", "Ficar na aldeia",
                                         "Deixar na oca"]},
}


def _clicar(dia, sorte, estrategia):
    """Perguntas, exame ou escolha: aperta um dos botões habilitados."""
    habilitados = [(bloco, acao) for bloco, acao in dia.botoes if bloco.habilitado]
    if dia.modo == "perguntas":
        perguntas, seguir = habilitados[:-1], habilitados[-1]
        perguntas = [(bloco, acao) for bloco, acao in perguntas if bloco.texto not in estrategia.get("evitar", [])]
        primeiro = [(bloco, acao) for bloco, acao in perguntas if bloco.texto in estrategia.get("perguntar", [])]
        if primeiro:
            primeiro[0][1]()
            return
        exame = dia.passo_atual["tipo"] == "exame"
        chance = 1 if estrategia.get("historias") and not exame else CHANCE_DE_PERGUNTAR
        if perguntas and sorte.random() < chance:
            sorte.choice(perguntas)[1]()
        else:
            seguir[1]()
        return
    if "preferir" in estrategia:
        por_texto = {bloco.texto: acao for bloco, acao in habilitados}
        for texto in estrategia["preferir"](dia):
            if texto in por_texto:
                por_texto[texto]()
                return
    sorte.choice(habilitados)[1]()


def _na_aldeia(dia, sorte, estrategia):
    """De dia, andando pela aldeia: conversa (ou não) com cada um, depois vai para a entrada."""
    conversou = dia.bot_conversou.setdefault(id(dia.passo_aldeia), set())
    chance = 1 if estrategia.get("historias") else CHANCE_DE_CONVERSAR
    for pessoa in dia.passo_aldeia.get("pessoas", []):
        if pessoa["nome"] not in conversou:
            conversou.add(pessoa["nome"])
            if sorte.random() < chance:
                dia.conversar_na_aldeia(pessoa["nome"])
                return
    dia.voltar_da_aldeia()


def _na_fogueira(dia, sorte, estrategia):
    faltam = [pessoa.nome for pessoa in dia.na_fogueira if pessoa.nome not in dia.conversados]
    if estrategia.get("paje_primeiro") and "Pajé" in faltam:
        dia._conversar_na_fogueira("Pajé")
    elif dia.botao_dormir.visivel and (not faltam or sorte.random() < CHANCE_DE_DORMIR):
        dia._dormir()
    elif faltam:
        dia._conversar_na_fogueira(sorte.choice(faltam))
    else:
        # Só sobrou quem pode conversar de novo (o pajé): conversa outra vez.
        dia._conversar_na_fogueira(sorte.choice([pessoa.nome for pessoa in dia.na_fogueira]))


def jogar_um_dia(jogo, sorte, estrategia):
    dia = Dia(jogo)
    dia.bot_conversou = {}
    for _ in range(LIMITE_DE_ACOES):
        if dia.modo == "fala":
            dia._proximo()
        elif dia.modo in ("perguntas", "escolha"):
            _clicar(dia, sorte, estrategia)
        elif dia.modo == "aldeia":
            _na_aldeia(dia, sorte, estrategia)
        elif dia.modo == "fogueira":
            _na_fogueira(dia, sorte, estrategia)
        else:
            return
    raise RuntimeError("o dia %d não terminou" % jogo.estado.dia)


def jogar_uma_partida(jogo, sorte, estrategia):
    """Devolve o estado no fim da partida (estado.final é o id do final)."""
    jogo.estado = Estado()
    jogo.estado.semente = sorte.randrange(1_000_000_000)
    while True:
        jogar_um_dia(jogo, sorte, estrategia)
        estado = jogo.estado
        if estado.final:
            return estado
        if estado.dia + 1 not in DIAS:
            raise RuntimeError("a partida passou do último dia sem final")
        febre.amanhecer(estado)
        finais.calcular_na_manha(estado)


def simular(partidas, estrategia=None, semente=1562):
    jogo = Jogo()
    # As cenas não trocam de verdade: o robô comanda o Dia direto.
    jogo.ir_para = lambda nome_cena, com_fade=True: None
    sorte = random.Random(semente)
    contagem, noites = Counter(), {}
    for _ in range(partidas):
        estado = jogar_uma_partida(jogo, sorte, ESTRATEGIAS.get(estrategia, {}))
        contagem[estado.final] += 1
        noites.setdefault(estado.final, Counter())[estado.dia] += 1
    return contagem, noites


def main():
    partidas = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    estrategia = sys.argv[2] if len(sys.argv) > 2 else None
    contagem, noites = simular(partidas, estrategia)
    print("%d partidas, %s" % (partidas, "estratégia " + estrategia if estrategia else "escolhendo ao acaso"))
    print()
    for final in FINAIS:
        vezes = contagem.get(final["id"], 0)
        quando = ", ".join("noite %d: %d" % (noite, n) for noite, n in sorted(noites.get(final["id"], {}).items()))
        print("%-20s %6.1f%%  (%d)  %s" % (final["nome"], 100 * vezes / partidas, vezes, quando))


if __name__ == "__main__":
    main()
