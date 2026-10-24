# Teste de fumaça: joga sozinho, sem janela, menu -> opções -> introdução inteira -> Dia 1 -> aldeia e oca -> menu.
#
# Como rodar (de dentro da pasta Jogo, com o ambiente ativado):
#     python -m testes.teste_fluxo
# Para também salvar imagens das telas, diga em que pasta:
#     CARAIBA_CAPTURAS=/tmp/capturas python -m testes.teste_fluxo
#
# Se aparecer "TUDO CERTO" no fim, o fluxo funciona. Se der erro, o Python
# mostra a linha do problema.

import atexit
import os
import random
import shutil
import tempfile

# Sem janela e sem som: precisa vir ANTES de importar o pygame.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

import config  # noqa: E402

# Preferências do teste vão para uma pasta temporária (não estraga as suas), dentro do projeto
# (Caraiba/.tmp), e ela é apagada no fim.
os.makedirs(config.PASTA_TEMPORARIOS, exist_ok=True)
config.PASTA_SAVES = tempfile.mkdtemp(prefix="caraiba-teste-", dir=config.PASTA_TEMPORARIOS)
atexit.register(shutil.rmtree, config.PASTA_SAVES, True)

from dados.textos import INTRODUCAO  # noqa: E402
from estado import Estado  # noqa: E402
from motor import ui  # noqa: E402
from motor.jogo import Jogo  # noqa: E402

PASTA_CAPTURAS = os.environ.get("CARAIBA_CAPTURAS")
DT = 1 / 60


def rodar(jogo, quadros=1, eventos=None):
    """Roda alguns quadros. Os eventos (se houver) entram no primeiro."""
    jogo.passo(eventos or [], DT)
    for _ in range(quadros - 1):
        jogo.passo([], DT)


def esperar_transicao(jogo):
    """Roda quadros até o fade entre cenas acabar."""
    for _ in range(200):
        if not jogo.cenas.em_transicao():
            return
        rodar(jogo)
    raise AssertionError("o fade entre cenas nunca terminou")


def clicar(jogo, posicao_logica):
    """Simula um clique (apertar e soltar) num ponto da tela 1600x900."""
    posicao = jogo.logica_para_janela(posicao_logica)
    apertar = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": posicao, "button": 1})
    soltar = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": posicao, "button": 1})
    rodar(jogo, 1, [apertar, soltar])


def clicar_botao(jogo, botao):
    assert botao.visivel and botao.habilitado, "botão não clicável: " + botao.texto
    clicar(jogo, botao.retangulo().center)


def tecla(jogo, codigo):
    rodar(jogo, 1, [pygame.event.Event(pygame.KEYDOWN, {"key": codigo, "mod": 0, "unicode": ""})])


def capturar(jogo, nome):
    if PASTA_CAPTURAS:
        os.makedirs(PASTA_CAPTURAS, exist_ok=True)
        caminho = os.path.join(PASTA_CAPTURAS, nome + ".png")
        jogo.capturar_tela(caminho)
        print("   captura:", caminho)


def nome_cena(jogo):
    return type(jogo.cenas.atual).__name__


# ---------------------------------------------------------------------------


def testar_marcacao():
    palavras = ui.separar_marcacao("uma [maldição], [de dentro] fim")
    assert palavras[0] == [("uma", False)]
    assert palavras[1] == [("maldição", True), (",", False)]
    assert palavras[2] == [("de", True)] and palavras[3] == [("dentro", True)]
    assert palavras[4] == [("fim", False)]
    print("ok marcação de palavras [ ]")


def testar_estado_inicial():
    estado = Estado()
    esperado = {"dia": 1, "vivos": 0, "mortos": 0, "mortos_por_sua_mao": 0, "entregues": 0,
                "proximidade_vila": 0, "rio_acima": 0, "memoria": 0, "recusas_aleixo": 0, "levados": 0,
                "pistas": 0, "sanidade": 10, "tapiri_usos": 0, "viu_anhanga": 0, "seguiu_paje": 0, "converteu": 0,
                "entregou_ultima_visita": 0, "perguntou_levados": 0,
                "inocentes": 0, "machado": 0, "energia_hoje": 0, "krenan_volta": 0, "subiu_o_rio": 0, "rio_acima_nomes": [], "convidados": [], "dentro": [], "tapiri": [], "tapiri_desde": {}, "febre": [], "noites_na_oca": {}, "curados": [], "manha": [],
                "historias": [], "entregues_nomes": [],
                "mortos_nomes": [], "mortos_quando": {}, "corpos": [], "tabua": [], "tabua_noites": [],
                "final_calculado": None, "final": None}
    dados = estado.para_dicionario()
    assert isinstance(dados.pop("semente"), int), "cada partida tem a sua sorte"
    assert dados == esperado, dados
    print("ok Estado com os valores iniciais do documento")


def testar_sinais_no_rosto():
    """O olho e a boca de perto mudam com a doença (Textos/Caraiba_Sinais_dos_Personagens.md)."""
    from types import SimpleNamespace
    from cenas.dia import Dia
    from dados import noites

    def imagens(zonas, estado):
        dia = SimpleNamespace(estado=estado)
        return {zona["pergunta"]: zona.get("imagem") for zona in zonas if Dia._condicao(dia, zona)}

    estado = Estado()
    estado.dia = 3
    estado.dentro = ["Yara", "Mbaé"]
    # Yara: vermelho da fumaça nas noites 1 e 2; na 3, sã, o olho volta ao normal.
    assert imagens(noites.ZONAS_YARA, estado)["Olhos"] == "olho_yara_vermelho"
    assert imagens(noites.ZONAS_YARA_NOITE_3, estado) == {
        "Testa": None, "Olhos": "olho_yara", "Orelhas": "orelha_pescoco_yara", "Boca": "boca_yara",
        "Mãos": None, "Respiração": None}
    # Pegou a febre de Mbaé na noite 2 e mostra: o olho segue vermelho, a boca ferida.
    estado.febre = [{"nome": "Yara", "de": "Mbaé", "noite": 2, "visivel": True}]
    vistas = imagens(noites.ZONAS_YARA_NOITE_3, estado)
    assert vistas["Olhos"] == "olho_yara_vermelho" and vistas["Boca"] == "boca_yara_doente", vistas
    # Pegou sem mostrar: o rosto de sempre.
    estado.febre[0]["visivel"] = False
    assert imagens(noites.ZONAS_YARA_NOITE_3, estado)["Olhos"] == "olho_yara"
    # Mbaé: o olho piora depois de 3 noites dormindo na oca; a boca já chega ferida.
    vistas = imagens(noites.ZONAS_MBAE, estado)
    assert vistas["Olhos"] == "olho_mbae" and vistas["Boca"] == "boca_mbae_doente", vistas
    assert imagens(noites.ZONAS_MBAE_NOITE_9, estado)["Orelhas"] == "orelha_pescoco_mbae"
    estado.noites_na_oca = {"Mbaé": 3}
    assert imagens(noites.ZONAS_MBAE, estado)["Olhos"] == "olho_mbae_doente"
    vistas = imagens(noites.ZONAS_MBAE_NOITE_9, estado)
    assert vistas["Orelhas"] == "orelha_mbae_doente" and vistas["Pescoço"] == "pescoco_mbae_doente", vistas
    # Yara com febre: a orelha e o pescoço também.
    estado.febre = [{"nome": "Yara", "de": "Mbaé", "noite": 2, "visivel": True}]
    vistas = imagens(noites.com_pescoco(noites.ZONAS_YARA_NOITE_3, noites.PESCOCO_YARA), estado)
    assert vistas["Orelhas"] == "orelha_yara_doente" and vistas["Pescoço"] == "pescoco_yara_doente", vistas
    # Tamandaré-mirim: a orelha limpa na noite 5, doente da noite 6; o pescoço doente da 9.
    assert imagens(noites.ZONAS_TAMANDARE, estado)["Orelhas"] == "orelha_pescoco_tamandare"
    assert imagens(noites.ZONAS_TAMANDARE_NOITE_6, estado)["Orelhas"] == "orelha_tamandare_doente"
    assert imagens(noites.ZONAS_TAMANDARE_NOITE_9, estado)["Pescoço"] == "pescoco_tamandare_doente"
    # Iandé: limpa nas noites 7 e 8; orelha e pescoço doentes na 9.
    assert imagens(noites.ZONAS_IANDE_NOITE_8, estado)["Orelhas"] == "orelha_pescoco_iande"
    vistas = imagens(noites.ZONAS_IANDE_NOITE_9, estado)
    assert vistas["Orelhas"] == "orelha_iande_doente" and vistas["Pescoço"] == "pescoco_iande_doente", vistas
    # Potira com febre: orelha e pescoço doentes.
    estado.febre.append({"nome": "Potira", "de": "Mbaé", "noite": 2, "visivel": True})
    vistas = imagens(noites.com_pescoco(noites.ZONAS_POTIRA_DEPOIS, noites.PESCOCO_POTIRA), estado)
    assert vistas["Orelhas"] == "orelha_potira_doente" and vistas["Pescoço"] == "pescoco_potira_doente", vistas
    print("ok sinais no rosto: olho e boca mudam com a doença")


def testar_corpos():
    """Quem morre deixa o corpo coberto com a esteira no lugar onde estava."""
    from dados.aldeia import ONDE_DORME
    from motor import febre
    estado = Estado()
    estado.dia = 3
    estado.dentro = ["Yara", "Mbaé"]
    estado.vivos = 2
    # Yara pegou a febre na noite 2 e morre na noite 3, na oca dela: a esteira de amaldiçoado.
    estado.febre = [{"nome": "Yara", "de": "Mbaé", "noite": 2, "visivel": False}]
    febre.amanhecer(estado)
    assert estado.dia == 4 and "Yara" not in estado.dentro
    corpo = estado.corpos[0]
    assert (corpo["nome"], corpo["onde"], corpo["noite"], corpo["amaldicoado"]) == ("Yara", "oca1", 3, True), corpo
    assert tuple(corpo["posicao"]) == ONDE_DORME["Yara"]["posicao"]
    # De manhã, o corpo aparece também na fogueira, onde ela sentava na noite em que morreu.
    from dados.noites import NOITES
    assert tuple(corpo["fogueira"]["posicao"]) == NOITES[3]["pessoas"]["Yara"]["posicao"], corpo
    # Quem era são (sem DOENTES e sem febre) ganha a esteira comum; quem chegou doente, a outra.
    assert not febre.era_amaldicoado(Estado(), "Potira") and febre.era_amaldicoado(Estado(), "Mbaé")
    print("ok corpos: a esteira no lugar de quem morreu")


def testar_cura_no_tapiri():
    """Quem era amaldiçoado e completa as noites do tapiri sai curado."""
    from types import SimpleNamespace
    from cenas.dia import Dia
    from dados import noites
    from motor import febre
    estado = Estado()
    estado.dia = 5
    estado.dentro = ["Yara", "Mbaé"]
    estado.tapiri, estado.tapiri_desde = ["Mbaé"], {"Mbaé": 2}
    assert febre.amaldicoado(estado, "Mbaé")
    dia = SimpleNamespace(estado=estado)
    Dia._liberar_tapiri(dia)
    assert estado.tapiri == [] and estado.curados == ["Mbaé"]
    assert not febre.amaldicoado(estado, "Mbaé") and febre.quantos_amaldicoados(estado) == 0
    febre.pegar(estado, "Mbaé")
    assert estado.febre == [], "curado não passa a febre"
    vistas = {z["pergunta"]: z for z in noites.ZONAS_MBAE if Dia._condicao(dia, z)}
    assert vistas["Boca"]["imagem"] == "boca_mbae" and not vistas["Boca"].get("sinal")
    assert sum(1 for z in noites.ZONAS_MBAE if Dia._condicao(dia, z) and z["pergunta"] == "Olhos") == 1
    print("ok cura no tapiri: sai curado, não passa a febre e o rosto mostra")


def testar_febre():
    """A febre na oca, entre quem é de fora (não há moradores): quem pega é sorteado; quem pega
    morre no 2º dia; o doente não morre; alguns não mostram nada; quem pegou passa adiante (os
    amaldiçoados); quem está no tapiri não pega."""
    from motor import febre

    estado = Estado()
    estado.semente = 7
    estado.dia = 2
    estado.dentro = ["Yara", "Mbaé", "Potira"]
    estado.vivos = 3
    febre.pegar(estado, "Mbaé")
    pegaram = [e["nome"] for e in estado.febre]
    assert 1 <= len(pegaram) <= 2 and set(pegaram) <= {"Yara", "Potira"}, estado.febre
    assert all(e["de"] == "Mbaé" and e["noite"] == 2 for e in estado.febre)
    febre.pegar(estado, "Yara")                   # Yara é sã: não passa nada
    assert len(estado.febre) == len(pegaram)
    assert febre.amaldicoado(estado, "Mbaé") and not febre.amaldicoado(estado, "Yara")

    visiveis = [e["nome"] for e in estado.febre if e["visivel"]]
    febre.amanhecer(estado)                        # dia 3: acordam com febre (só quem mostra)
    assert estado.dia == 3 and estado.vivos == 3
    if visiveis:
        assert len(estado.manha) == 1 and visiveis[0] in estado.manha[0], estado.manha
    else:
        assert estado.manha == [], "quem não mostra nada não aparece de manhã"
    febre.amanhecer(estado)                        # dia 4: morrem (o 2º dia com febre)
    assert estado.vivos == 3 - len(pegaram) and estado.mortos == len(pegaram) and estado.febre == []
    assert all("morreu" in frase or "morreram" in frase for frase in estado.manha)
    assert "Mbaé" in estado.dentro and not set(pegaram) & set(estado.dentro), "quem pegou sai da aldeia"
    febre.amanhecer(estado)                        # dia 5: nada de novo
    assert estado.manha == []

    # A mesma partida (semente) sorteia sempre igual; partidas diferentes variam.
    def sorteio(semente, tapiri=()):
        e = Estado()
        e.semente, e.dia = semente, 2
        e.dentro, e.tapiri = ["Yara", "Mbaé", "Potira"], list(tapiri)
        febre.pegar(e, "Mbaé")
        return tuple(sorted(x["nome"] for x in e.febre))
    assert sorteio(7) == tuple(sorted(pegaram))
    assert {len(sorteio(s)) for s in range(200)} == {1, 2}
    # Quem está no tapiri não pega; e Mbaé no tapiri não passa.
    assert all("Yara" not in sorteio(s, tapiri=["Yara"]) for s in range(50))
    assert all(sorteio(s, tapiri=["Mbaé"]) == () for s in range(50))
    # Sem ninguém de fora para pegar, não acontece nada.
    e = Estado()
    e.dia, e.dentro = 2, ["Mbaé"]
    febre.pegar(e, "Mbaé")
    assert e.febre == []

    # Quem não mostra nada morre do mesmo jeito, e a manhã diz que ele não tinha nada.
    e = Estado()
    e.dia, e.vivos, e.dentro = 3, 3, ["Yara", "Mbaé", "Potira"]
    e.febre = [{"nome": "Yara", "de": "Mbaé", "noite": 2, "visivel": False},
               {"nome": "Potira", "de": "Mbaé", "noite": 2, "visivel": True}]
    febre.amanhecer(e)
    assert e.manha == ["Potira morreu de febre esta noite.",
                       "Yara não tinha nada, e morreu de febre esta noite."], e.manha
    assert e.vivos == 1 and e.dentro == ["Mbaé"]

    # Quem pegou passa adiante (0 ou 1 por noite); quem pegou nesta noite, ainda não.
    def passa(semente, noite=2):
        e = Estado()
        e.semente, e.dia = semente, 3
        e.dentro = ["Yara", "Potira"]
        e.febre = [{"nome": "Yara", "de": "Mbaé", "noite": noite, "visivel": True}]
        febre.passar_na_oca(e)
        return len(e.febre) - 1
    assert {passa(s) for s in range(50)} == {0, 1}
    assert all(passa(s, noite=3) == 0 for s in range(50))

    # Mbaé passa a febre enquanto está na aldeia; levado pelo Aleixo (fora de "dentro"), não.
    e = Estado()
    e.dia, e.dentro = 3, ["Mbaé"]
    assert febre.amaldicoado(e, "Mbaé")
    e.dentro = []
    assert not febre.amaldicoado(e, "Mbaé")
    print("ok febre entre quem é de fora (sorteada), amaldiçoados com e sem sinal, tapiri isola")

    # A oferta do Aleixo: entregar só quem está dentro; negar sempre aparece, e ele fica mais
    # irritado a cada visita.
    from dados.dias import FALA_ALEIXO_NEGADO, oferta_aleixo
    assert [o["texto"] for o in oferta_aleixo(3)["opcoes"]] == [
        "Entregar Yara", "Entregar Mbaé", "Entregar Potira", "Entregar Tamandaré-mirim", "Entregar Iandé",
        "Negar"]
    assert sorted(FALA_ALEIXO_NEGADO) == [3, 6, 9]
    assert oferta_aleixo(9)["opcoes"][-1]["passos"][0]["texto"] == FALA_ALEIXO_NEGADO[9]


def testar_cartoes_introducao():
    # A Proposta pede: aviso de conteúdo primeiro (tela preta) e as regras por último.
    cartoes = INTRODUCAO["cartoes"]
    assert all(cartao.get("texto") for cartao in cartoes), "cartão sem texto"
    assert cartoes[0].get("titulo") and not cartoes[0].get("fundo"), "o 1º cartão deve ser o aviso"
    assert cartoes[-1].get("titulo") and cartoes[-1].get("fundo"), "o último cartão deve ser as regras"
    print("ok ordem dos cartões da introdução (aviso ... regras)")


def passar_falas(jogo, seguir_seta=True):
    """No Dia: clica nas falas (completar e seguir) até aparecerem botões ou a cena acabar.

    Se o roteiro levar à aldeia de dia, segue a seta e continua (ou para lá, com seguir_seta=False).
    """
    for _ in range(100):
        esperar_transicao(jogo)
        cena = jogo.cenas.atual
        if nome_cena(jogo) == "Aldeia" and cena.de_dia:
            if not seguir_seta:
                return
            clicar(jogo, cena.rect_seta.center)
            continue
        if nome_cena(jogo) != "Dia" or cena.modo != "fala":
            return
        rodar(jogo, 5)
        clicar(jogo, (800, 300))   # completa o texto
        clicar(jogo, (800, 300))   # segue o roteiro
    raise AssertionError("as falas do Dia nunca terminaram")


def ate_a_aldeia_de_dia(jogo):
    """Passa as falas do pajé até a aldeia de dia aparecer (sem seguir a seta)."""
    for _ in range(100):
        esperar_transicao(jogo)
        if nome_cena(jogo) == "Aldeia":
            return jogo.cenas.atual
        rodar(jogo, 5)
        clicar(jogo, (800, 300))
        clicar(jogo, (800, 300))
    raise AssertionError("a aldeia de dia nunca apareceu")


def testar_aldeia_de_dia(jogo):
    """Depois do pajé: a aldeia de dia, a oca 1 vazia, e a seta leva à entrada (Yara)."""
    jogo.nova_partida()
    jogo.ir_para("dia")
    aldeia = ate_a_aldeia_de_dia(jogo)
    assert aldeia.de_dia and aldeia.abertas == ["oca1", "tapiri"]
    assert jogo.cenas.atual.filtro == "dia"
    rodar(jogo, 20)
    capturar(jogo, "07b-dia1-aldeia")

    clicar(jogo, centro_da_oca("oca1"))
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Oca" and jogo.cenas.atual.de_dia and jogo.cenas.atual.pessoas == []
    rodar(jogo, 5)
    capturar(jogo, "07c-dia1-oca1")
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia" and jogo.cenas.atual.de_dia, "sair da oca de dia volta à aldeia de dia"

    # Menu e Continuar no meio da aldeia de dia: volta para a aldeia de dia.
    clicar_botao(jogo, jogo.cenas.atual.botao_menu)
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_continuar)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia" and jogo.cenas.atual.de_dia, nome_cena(jogo)

    # Seta: a entrada da aldeia, onde Yara chega.
    clicar(jogo, jogo.cenas.atual.rect_seta.center)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.visitante == "yara", (nome_cena(jogo), getattr(dia, "visitante", None))
    print("ok aldeia de dia: oca 1 vazia, Continuar e seta para a entrada")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def clicar_opcao(jogo, texto):
    """Clica no botão do Dia que tem esse texto."""
    for botao, _ in jogo.cenas.atual.botoes:
        if botao.texto == texto:
            clicar_botao(jogo, botao)
            return
    raise AssertionError("botão não encontrado: %s (há: %s)" % (
        texto, [b.texto for b, _ in jogo.cenas.atual.botoes]))


def testar_dia1(jogo):
    """Joga o Dia 1 duas vezes: deixando Yara entrar (com perguntas e machado) e sem deixar."""
    from dados.dias import DIAS
    perguntas = next(p for p in DIAS[1]["passos"] if p["tipo"] == "perguntas")["perguntas"]

    # 1ª vez: pergunta tudo, deixa entrar, aceita o machado.
    jogo.nova_partida()
    jogo.ir_para("dia")
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Dia"
    rodar(jogo, 20)
    capturar(jogo, "07-dia1-paje")
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "perguntas" and dia.visitante == "yara", (dia.modo, dia.visitante)
    rodar(jogo, 60)  # Yara termina de aparecer
    capturar(jogo, "08-dia1-yara-perguntas")
    for item in perguntas:
        clicar_opcao(jogo, item["pergunta"])
        if item is perguntas[1]:
            dia.caixa.completar()
            rodar(jogo, 2)
            capturar(jogo, "09-dia1-yara-resposta")
        passar_falas(jogo)
    assert [b.texto for b, _ in dia.botoes] == ["Decidir"], "as perguntas feitas deviam sumir"
    clicar_opcao(jogo, "Decidir")
    assert dia.modo == "escolha"
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo)
    capturar(jogo, "10-dia1-machado")
    clicar_opcao(jogo, "Aceitar o machado")
    passar_falas(jogo, seguir_seta=False)
    estado = jogo.estado
    assert estado.vivos == 1 and estado.dentro == ["Yara"], (estado.vivos, estado.dentro)
    assert estado.proximidade_vila == 1 and estado.machado == 1, (estado.proximidade_vila, estado.machado)
    testar_aldeia_com_yara(jogo)
    passar_falas(jogo)
    estado = jogo.estado   # o Continuar da aldeia recriou o Estado
    assert estado.memoria == 1, estado.memoria
    assert estado.tabua == ["Olho vermelho, com o branco raiado."], estado.tabua
    print("ok Dia 1 deixando Yara entrar (perguntas curtas, machado, aldeia, sinal na tábua)")
    testar_noite1_com_yara(jogo)
    testar_aldeia_e_oca(jogo, yara_dentro=True)

    # 2ª vez: decide direto, sem perguntar, e não deixa entrar. A noite não tem ninguém de fora.
    jogo.nova_partida()
    jogo.ir_para("dia")
    esperar_transicao(jogo)
    passar_falas(jogo)
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Não deixar entrar")
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "fogueira" and [p.nome for p in dia.na_fogueira] == ["Pajé"]
    assert dia.botao_dormir.visivel and dia.botao_dormir.texto == "Ir dormir"
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", nome_cena(jogo)
    estado = jogo.estado
    assert estado.vivos == 0 and estado.dentro == [] and estado.memoria == 0, estado.para_dicionario()
    assert len(estado.tabua) == 1
    print("ok Dia 1 sem deixar Yara entrar (noite sem ninguém de fora)")
    testar_aldeia_e_oca(jogo, yara_dentro=False)

    # 3ª vez: deixa entrar, recusa o machado e, na fogueira, leva Yara ao tapiri.
    jogo.nova_partida()
    jogo.ir_para("dia")
    esperar_transicao(jogo)
    passar_falas(jogo)
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo)
    clicar_opcao(jogo, "Recusar o machado")
    passar_falas(jogo)
    clicar_pessoa(jogo, "Yara")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Levar ao tapiri")
    passar_falas(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", nome_cena(jogo)
    estado = jogo.estado
    assert estado.dentro == ["Yara"] and estado.tapiri == ["Yara"] and estado.proximidade_vila == 0
    assert estado.tapiri_usos == 0, "Yara é sã: levar ao tapiri não conta para o final O Tapiri"
    print("ok Noite 1 levando Yara ao tapiri")
    testar_aldeia_e_oca(jogo, yara_dentro=False)

    # O tapiri, ao lado da Yebá Bëló: Yara está lá dentro.
    oca = entrar_na_oca(jogo, "tapiri")
    assert oca.no_tapiri and [quem for quem, _ in oca.pessoas] == ["Yara"], oca.pessoas
    assert oca.botao_sair.texto == "Sair do tapiri", oca.botao_sair.texto
    rodar(jogo, 5)
    capturar(jogo, "11c-noite1-tapiri-yara")
    clicar_botao(jogo, oca.botao_sair)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia"
    print("ok tapiri: Yara dorme lá, longe das ocas")

    # 4ª vez: mata Yara. Uma morte só: o jogo segue.
    jogar_ate_matar_yara(jogo)
    esperar_transicao(jogo)
    estado = jogo.estado
    assert nome_cena(jogo) == "Aldeia", nome_cena(jogo)
    assert estado.dentro == [] and estado.mortos_nomes == ["Yara"] and estado.vivos == 0
    assert estado.mortos_por_sua_mao == 1 and estado.sanidade == 7 and estado.final is None
    print("ok Noite 1 matando Yara (o jogo segue)")

    # 5ª vez: quem já matou duas pessoas mata a terceira: A Loucura, antes do dia 10.
    jogar_ate_matar_yara(jogo, mortes_antes=2)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Final" and jogo.estado.final == "loucura", nome_cena(jogo)
    final = jogo.cenas.atual
    rodar(jogo, 10)
    capturar(jogo, "16-final-loucura-cena")
    for _ in range(2):
        clicar_botao(jogo, final.botao)   # completa o texto
        clicar_botao(jogo, final.botao)   # próxima tela
    assert final.indice == 2 and final.botao.texto == "Voltar ao menu"
    final.caixa.completar()
    rodar(jogo, 3)
    capturar(jogo, "17-final-loucura-fonte")
    # Continuar, com a partida acabada, volta à tela do final.
    clicar_botao(jogo, final.botao)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Menu"
    clicar_botao(jogo, jogo.cenas.atual.botao_continuar)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Final" and jogo.cenas.atual.final["id"] == "loucura"
    print("ok fim antecipado: A Loucura na noite em que a 3ª pessoa morre (e Continuar)")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def jogar_ate_matar_yara(jogo, mortes_antes=0):
    """Joga o Dia 1 deixando Yara entrar e, na fogueira, mata Yara (sem examinar) e vai dormir."""
    jogo.nova_partida()
    jogo.estado.mortos_por_sua_mao = mortes_antes
    jogo.ir_para("dia")
    esperar_transicao(jogo)
    passar_falas(jogo)
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo)
    clicar_opcao(jogo, "Recusar o machado")
    passar_falas(jogo)
    clicar_pessoa(jogo, "Yara")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Matar")
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "fogueira" and [p.nome for p in dia.na_fogueira] == ["Pajé"]
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)


def testar_finais():
    """As contas de cada final (Textos/Caraiba_Contas_dos_Finais.md), sem jogar."""
    from motor import finais

    def estado_com(**valores):
        estado = Estado()
        for nome, valor in valores.items():
            setattr(estado, nome, valor)
        return estado

    # O dia 10: cada caminho típico cai no seu final.
    casos = [
        ({"entregues": 2, "vivos": 5}, "troca"),
        ({"proximidade_vila": 3}, "troca"),
        ({"mortos_por_sua_mao": 3}, "loucura"),
        ({"entregues": 2, "mortos_por_sua_mao": 3}, "troca"),          # a fila: Troca vem antes
        ({"converteu": 1, "tapiri_usos": 3}, "batismo"),               # aceitou o padre novo
        ({"seguiu_paje": 3, "inocentes": 0, "tapiri_usos": 3, "vivos": 4}, "tapiri"),
        ({"subiu_o_rio": 1, "entregues": 1}, "rio_acima"),              # a escolha da noite 10
        ({"rio_acima": 4}, "vazio"),                                     # levar gente com Krenan não basta
        ({"viu_anhanga": 3, "memoria": 5, "vivos": 5}, "anhanga"),     # Anhangá antes da Honra
        ({"viu_anhanga": 3, "mortos_por_sua_mao": 1}, "vazio"),
        ({"memoria": 5, "vivos": 2}, "honra"),
        ({"memoria": 5, "vivos": 1}, "vazio"),
        ({"memoria": 4, "vivos": 5, "tapiri_usos": 3}, "tapiri"),
        ({"tapiri_usos": 3, "vivos": 1}, "vazio"),
        ({}, "vazio"),
    ]
    for valores, esperado in casos:
        estado = estado_com(dia=10, **valores)
        assert finais.escolher(estado)["id"] == esperado, (valores, finais.escolher(estado)["id"])
        assert finais.fim_da_noite(estado)["id"] == esperado

    # Antes do dia 10: só os finais antecipados (ou a aldeia vazia) acabam o jogo.
    antes = [
        ({"dia": 1, "mortos_por_sua_mao": 1}, None),
        ({"dia": 4, "mortos_por_sua_mao": 3}, "loucura"),
        ({"dia": 3, "proximidade_vila": 3}, "troca"),
        ({"dia": 6, "entregues": 2}, "troca"),
        ({"dia": 9, "rio_acima": 4}, None),                             # Rio Acima só na noite 10
        ({"dia": 9, "vivos": 0, "mortos": 2}, "vazio"),                 # ninguém de fora sobrou
        ({"dia": 9, "vivos": 0, "mortos": 1}, None),
        ({"dia": 2, "vivos": 0}, None),                                 # ninguém entrou ainda
        ({"dia": 9, "vivos": 1, "mortos": 4}, None),
        ({"dia": 5, "memoria": 5, "vivos": 5}, None),                   # A Honra só no dia 10
        ({"dia": 7, "tapiri_usos": 3}, None),                           # O Tapiri só no dia 10
        ({"dia": 8, "viu_anhanga": 3}, None),                           # Anhangá fecha na noite 9
        ({"dia": 9, "viu_anhanga": 3}, "anhanga"),
        ({"dia": 9, "viu_anhanga": 3, "entregues": 1}, "anhanga"),     # entregar não impede
        ({"dia": 9, "viu_anhanga": 3, "entregues": 2}, "troca"),        # 2 entregas: A Troca antes
        ({"dia": 9, "viu_anhanga": 3, "mortos_por_sua_mao": 1}, None),
        ({"dia": 9, "converteu": 1, "entregues": 1}, "batismo"),       # o padre novo, na noite 9
    ]
    for valores, esperado in antes:
        final = finais.fim_da_noite(estado_com(**valores))
        assert (final["id"] if final else None) == esperado, (valores, final and final["id"])
    # Na noite 10, subir o rio com Krenan vence o final calculado de manhã.
    estado = estado_com(dia=10, subiu_o_rio=1, final_calculado="vazio")
    assert finais.fim_da_noite(estado)["id"] == "rio_acima"
    assert finais.fim_da_noite(estado_com(dia=10, final_calculado="vazio"))["id"] == "vazio"
    print("ok contas dos finais (fila do dia 10 e fins antecipados)")


def textos_dos_botoes(jogo):
    return [b.texto for b, _ in jogo.cenas.atual.botoes]


def ponto_na_pessoa(pessoa):
    """Um ponto em cima da pessoa (não no fundo transparente): perto do meio do corpo."""
    rect = pessoa.mascara.get_bounding_rects()[0]
    x, y = rect.centerx, rect.top + rect.height // 3
    while not pessoa.mascara.get_at((x, y)):
        y += 1
    return (x + pessoa.rect.x, y + pessoa.rect.y)


def clicar_pessoa(jogo, nome):
    """Clica numa pessoa desenhada no cenário (na aldeia, numa oca de dia ou na fogueira)."""
    cena = jogo.cenas.atual
    pessoas = {"Aldeia": "pessoas", "Oca": "na_oca", "Dia": "na_fogueira"}[nome_cena(jogo)]
    pessoa = next(p for p in getattr(cena, pessoas) if p.nome == nome)
    ponto = ponto_na_pessoa(pessoa)
    rodar(jogo, 1, [pygame.event.Event(pygame.MOUSEMOTION, pos=jogo.logica_para_janela(ponto),
                                       rel=(0, 0), buttons=(0, 0, 0))])
    clicar(jogo, ponto)
    esperar_transicao(jogo)


def entrar_na_oca(jogo, nome):
    clicar(jogo, centro_da_oca(nome))
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Oca", nome_cena(jogo)
    return jogo.cenas.atual


def testar_aldeia_com_yara(jogo):
    """Depois de entrar, Yara espera dentro da oca: clicar nela abre a conversa sobre a aldeia antiga."""
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.de_dia, nome_cena(jogo)
    assert aldeia.pessoas == [], "Yara não fica do lado de fora: ela espera na oca"
    assert aldeia.texto_seta == "Esperar a noite"
    rodar(jogo, 20)
    capturar(jogo, "10b-dia1-aldeia-depois-de-yara")

    oca = entrar_na_oca(jogo, "oca1")
    assert oca.de_dia and [p.nome for p in oca.na_oca] == ["Yara"]
    rodar(jogo, 20)
    capturar(jogo, "10c-dia1-yara-na-oca")

    clicar_pessoa(jogo, "Yara")
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.visitante == "yara" and dia.fundo == ("oca1", "dia"), (
        nome_cena(jogo), getattr(dia, "visitante", None), getattr(dia, "fundo", None))
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Conte da sua aldeia.", "Por que saiu de lá?",
                                       "A maldição chegou lá?", "Terminar a conversa"]
    # A história da aldeia dela: três frases, e conta como história ouvida.
    clicar_opcao(jogo, "Conte da sua aldeia.")
    dia.caixa.completar()
    rodar(jogo, 2)
    capturar(jogo, "10d-dia1-aldeia-de-yara")
    passar_falas(jogo)
    assert jogo.estado.memoria == 1
    clicar_opcao(jogo, "Terminar a conversa")
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Oca" and jogo.cenas.atual.de_dia, "a conversa termina dentro da oca"
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia" and jogo.cenas.atual.de_dia

    # Menu e Continuar: volta à aldeia, e a pergunta feita não volta.
    clicar_botao(jogo, jogo.cenas.atual.botao_menu)
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_continuar)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia" and jogo.estado.memoria == 1, (nome_cena(jogo), jogo.estado.memoria)
    entrar_na_oca(jogo, "oca1")
    clicar_pessoa(jogo, "Yara")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Por que saiu de lá?", "A maldição chegou lá?", "Terminar a conversa"]
    clicar_opcao(jogo, "Terminar a conversa")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)
    print("ok Yara espera na oca de dia: conversa sobre a aldeia antiga dela (e Continuar)")


def testar_noite1_com_yara(jogo):
    """A fogueira: escolher com quem falar (pajé, Yara), exame com energia, Continuar e a decisão."""
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.titulo == "Noite 1", (nome_cena(jogo), dia.titulo)
    assert dia.modo == "fogueira" and dia.fundo == ("fogueira_perto", "noite")
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Yara"]
    assert not dia.botao_dormir.visivel, "só dá para dormir depois de decidir sobre Yara"
    rodar(jogo, 60)
    capturar(jogo, "10d-noite1-fogueira")

    # O pajé: uma pergunta e volta para a fogueira.
    clicar_pessoa(jogo, "Pajé")
    assert dia.visitante == "paje"
    passar_falas(jogo)
    clicar_opcao(jogo, "Todo olho vermelho é o mal?")
    passar_falas(jogo)
    clicar_opcao(jogo, "Voltar para a fogueira")
    assert dia.modo == "fogueira" and dia.visitante is None

    # Yara: a conversa de sempre, a mesma da oca. A história já ouvida não soma memória de novo.
    clicar_pessoa(jogo, "Yara")
    assert dia.visitante == "yara"
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Conte da sua aldeia.", "Por que saiu de lá?",
                                       "A maldição chegou lá?", "Examinar o rosto"]
    clicar_opcao(jogo, "Conte da sua aldeia.")
    passar_falas(jogo)
    assert jogo.estado.memoria == 1 and jogo.estado.historias == ["aldeia_yara"]

    # O exame: na noite 1 só os olhos (1 de energia).
    clicar_opcao(jogo, "Examinar o rosto")
    assert dia.energia == 1 and textos_dos_botoes(jogo) == ["Olhos", "Terminar o exame"], (
        dia.energia, textos_dos_botoes(jogo))
    clicar_opcao(jogo, "Olhos")
    dia.caixa.completar()
    rodar(jogo, 5)
    capturar(jogo, "10f-noite1-olhos")
    passar_falas(jogo)
    assert dia.energia == 0 and dia.sinais == {"Yara": 1}
    assert textos_dos_botoes(jogo) == ["Terminar o exame"]

    # Continuar no meio do exame: a mesma energia, o mesmo sinal achado.
    clicar_botao(jogo, dia.botao_menu)
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_continuar)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.titulo == "Noite 1" and dia.modo == "perguntas"
    assert dia.energia == 0 and dia.sinais == {"Yara": 1} and jogo.estado.memoria == 1
    assert "Pajé" in dia.conversados and "Yara" in dia.conversados
    assert textos_dos_botoes(jogo) == ["Terminar o exame"]
    print("ok Continuar no meio do exame da Noite 1 (só os olhos)")
    clicar_opcao(jogo, "Terminar o exame")

    # A decisão: as três opções abertas (matar também).
    assert dia.modo == "escolha"
    assert textos_dos_botoes(jogo) == ["Deixar na oca", "Levar ao tapiri", "Matar"]
    assert all(bloco.habilitado for bloco, _ in dia.botoes)
    dia.caixa.completar()
    rodar(jogo, 5)
    capturar(jogo, "10e-noite1-decisao")
    clicar_opcao(jogo, "Deixar na oca")
    passar_falas(jogo)

    # De volta à fogueira: Yara foi dormir, só sobra o pajé, e agora dá para ir dormir.
    assert dia.modo == "fogueira" and [p.nome for p in dia.na_fogueira] == ["Pajé"]
    assert dia.botao_dormir.visivel
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", nome_cena(jogo)
    assert jogo.estado.tapiri == [] and jogo.estado.mortos_por_sua_mao == 0
    print("ok Noite 1 na fogueira (pajé e Yara, exame com energia, matar aberto, Yara na oca)")


def centro_da_oca(nome):
    from dados.aldeia import OCAS
    pontos = OCAS[nome]["contorno"]
    # Um ponto bem dentro do contorno: a média dos pontos. A seta do tapiri (/\) é oca no
    # meio: aí o ponto sobe até cair dentro dela.
    forma = pygame.Surface(config.TAMANHO_LOGICO, pygame.SRCALPHA)
    pygame.draw.polygon(forma, (255, 255, 255, 255), pontos)
    mascara = pygame.mask.from_surface(forma)
    x, y = (sum(x for x, _ in pontos) // len(pontos), sum(y for _, y in pontos) // len(pontos))
    while not mascara.get_at((x, y)):
        y -= 1
    return (x, y - 4) if mascara.get_at((x, y - 4)) else (x, y)


def testar_aldeia_e_oca(jogo, yara_dentro):
    """Na noite 1 só a oca 1 (e o tapiri) abre; Yara está nela se o jogador a deixou entrar."""
    aldeia = jogo.cenas.atual
    assert aldeia.abertas == ["oca1", "tapiri"], aldeia.abertas

    # Mouse em cima da oca 3 (fechada): acende, mas clicar não entra.
    clicar(jogo, centro_da_oca("oca3"))
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", "a oca 3 está fechada na noite 1"
    rodar(jogo, 20)
    capturar(jogo, "11-noite1-aldeia")

    # Oca 1: entra.
    clicar(jogo, centro_da_oca("oca1"))
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Oca", nome_cena(jogo)
    oca = jogo.cenas.atual
    assert oca.nome == "oca1"
    if yara_dentro:
        assert [quem for quem, _ in oca.pessoas] == ["Yara"], oca.pessoas
        rodar(jogo, 5)
        capturar(jogo, "11b-noite1-oca1-yara")
    else:
        assert oca.pessoas == [], oca.pessoas
    clicar_botao(jogo, oca.botao_sair)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia"
    print("ok aldeia de noite: só a oca 1 abre%s" % (" e Yara dorme nela" if yara_dentro else ", vazia"))


def comecar_noite_1_na_aldeia(jogo, **valores):
    """Uma partida parada na aldeia, no fim da noite 1 (sem jogar o Dia 1)."""
    jogo.nova_partida()
    estado = jogo.estado
    estado.dentro = ["Yara"]
    estado.vivos = 1
    estado.tabua = ["Olho vermelho, com o branco raiado."]
    for nome, valor in valores.items():
        setattr(estado, nome, valor)
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    return estado


def ate_mbae_entrar(jogo):
    """Do começo do Dia 2 até Mbaé entrar e esperar na oca (a aldeia de dia)."""
    passar_falas(jogo)                       # a aldeia (seta) até a entrada
    dia = jogo.cenas.atual
    assert dia.modo == "perguntas" and dia.visitante == "mbae", (dia.modo, dia.visitante)
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo, seguir_seta=False)
    assert nome_cena(jogo) == "Aldeia" and jogo.cenas.atual.de_dia


def examinar(jogo, zonas):
    for zona in zonas:
        clicar_opcao(jogo, zona)
        passar_falas(jogo)


def testar_dia2_e_noite2(jogo):
    """Da noite 1 ao Dia 2 (Mbaé) e à Noite 2: o tapiri tem lugar para um só."""
    # A aldeia de noite tem a seta "Dormir", que leva ao Dia 2.
    estado = comecar_noite_1_na_aldeia(jogo)
    aldeia = jogo.cenas.atual
    assert aldeia.tem_seta and aldeia.texto_seta == "Dormir"
    rodar(jogo, 20)
    capturar(jogo, "18-noite1-aldeia-dormir")
    clicar(jogo, aldeia.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    estado = jogo.estado
    # O Dia 2 começa na aldeia de dia, com a seta para a entrada.
    assert estado.dia == 2 and nome_cena(jogo) == "Aldeia" and jogo.cenas.atual.de_dia, nome_cena(jogo)
    assert jogo.dia_pausado.titulo == "Dia 2" and jogo.cenas.atual.texto_seta == "Entrada da aldeia"

    # De dia, Yara dorme na oca Yorixiriamori (parada, sem conversa nova).
    oca = entrar_na_oca(jogo, "oca1")
    assert oca.de_dia and oca.pessoas == [("Yara", "yara_sentada")] and oca.na_oca == []
    clicar_botao(jogo, oca.botao_sair)
    esperar_transicao(jogo)

    # A entrada: Mbaé. Pergunta se está doente e deixa entrar.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    rodar(jogo, 60)
    capturar(jogo, "19-dia2-mbae")
    clicar_opcao(jogo, "Você está amaldiçoado?")
    passar_falas(jogo)
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo, seguir_seta=False)
    assert estado.dentro == ["Yara", "Mbaé"] and estado.vivos == 2

    # Mbaé espera na oca Yebá Bëló: a história de antes conta como história ouvida.
    oca = entrar_na_oca(jogo, "oca2")
    assert [p.nome for p in oca.na_oca] == ["Mbaé"]
    rodar(jogo, 20)
    capturar(jogo, "20-dia2-mbae-na-oca")
    clicar_pessoa(jogo, "Mbaé")
    assert jogo.cenas.atual.fundo == ("oca2_dia", "dia")
    passar_falas(jogo)
    clicar_opcao(jogo, "Conte de antes.")
    passar_falas(jogo)
    assert estado.memoria == 1
    clicar_opcao(jogo, "Terminar a conversa")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)

    # O sinal do pajé e a fogueira: pajé, Yara e Mbaé. Só Mbaé é obrigatório.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert estado.tabua[-1] == "Boca com feridas."
    assert dia.titulo == "Noite 2" and dia.modo == "fogueira" and dia.energia == 1
    # Quem aceitou o machado de Yara tem 2 olhares já na noite 2.
    estado.machado = 1
    dia._comecar_noite()
    assert dia.energia == dia.energia_max == 2
    estado.machado = 0
    dia._comecar_noite()
    assert dia.energia == 1
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Yara", "Mbaé"]
    assert not dia.botao_dormir.visivel
    rodar(jogo, 40)
    capturar(jogo, "21-noite2-fogueira")

    # O pajé fala do que a aldeia diz de Mbaé (só porque ele entrou).
    clicar_pessoa(jogo, "Pajé")
    passar_falas(jogo)
    assert "Por que olham torto para Mbaé?" in textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Por que olham torto para Mbaé?")
    passar_falas(jogo)
    clicar_opcao(jogo, "Voltar para a fogueira")

    # Mbaé: a conversa de sempre, a mesma da oca (e a história não soma memória de novo).
    # Na noite 2, 1 olhar só, e só os olhos ou a boca (a tosse).
    clicar_pessoa(jogo, "Mbaé")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Conte de antes.", "Por que olham torto para você?",
                                       "Examinar o rosto"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Conte de antes.")
    passar_falas(jogo)
    assert estado.memoria == 1
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Boca", "Terminar o exame"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Boca")
    dia.caixa.completar()
    assert "tosse" in dia.caixa.texto, dia.caixa.texto
    passar_falas(jogo)
    assert dia.energia == 0 and dia.sinais == {"Mbaé": 1}
    assert [b.habilitado for b, _ in dia.botoes] == [False, True], "sem energia, os olhos ficam fechados"
    rodar(jogo, 5)
    capturar(jogo, "22-noite2-exame-mbae")
    clicar_opcao(jogo, "Terminar o exame")

    # Deixar Mbaé na oca: no fim da noite, a febre passa para quem é de fora e dorme nas ocas.
    # Só Yara: ela pega (Mbaé passa para 1 a 3, e só há ela), e morre no dia 4.
    assert textos_dos_botoes(jogo) == ["Deixar na oca", "Levar ao tapiri", "Matar"]
    clicar_opcao(jogo, "Deixar na oca")
    passar_falas(jogo)
    assert estado.febre == [], "a febre só passa no fim da noite"
    assert dia.botao_dormir.visivel
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert [(e["nome"], e["de"], e["noite"]) for e in estado.febre] == [("Yara", "Mbaé", 2)], estado.febre

    # A aldeia de noite 2: as duas ocas abertas, e a seta "Dormir" leva ao Dia 3.
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.abertas == ["oca1", "oca2", "tapiri"] and aldeia.tem_seta
    oca = entrar_na_oca(jogo, "oca2")
    assert oca.pessoas == [("Mbaé", "mbae_sentado")]
    rodar(jogo, 5)
    capturar(jogo, "23-noite2-oca2-mbae")
    print("ok Dia 2 e Noite 2 (Mbaé na oca, 1 olhar: a tosse na boca, febre sorteada)")
    jogo.ir_para("menu")
    esperar_transicao(jogo)

    # Yara ficou no tapiri na noite 1: na noite 2 ela não vem à fogueira, e não há lugar para Mbaé.
    comecar_noite_1_na_aldeia(jogo, tapiri=["Yara"], tapiri_desde={"Yara": 1})
    jogo.amanhecer()
    esperar_transicao(jogo)
    ate_mbae_entrar(jogo)
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Mbaé"], [p.nome for p in dia.na_fogueira]
    clicar_pessoa(jogo, "Mbaé")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    clicar_opcao(jogo, "Terminar o exame")
    assert textos_dos_botoes(jogo) == ["Deixar na oca", "Levar ao tapiri · não há lugar", "Matar"]
    assert not dia.botoes[1][0].habilitado
    dia.caixa.completar()
    rodar(jogo, 5)
    capturar(jogo, "24-noite2-tapiri-cheio")
    clicar_opcao(jogo, "Matar")
    passar_falas(jogo)
    assert jogo.estado.mortos_nomes == ["Mbaé"] and jogo.estado.febre == []
    # Na noite 4, Yara já passou três noites lá: a vaga abre.
    jogo.estado.dia = 4
    dia._liberar_tapiri()
    assert jogo.estado.tapiri == [] and jogo.estado.tapiri_desde == {}
    print("ok Noite 2 com o tapiri cheio (Yara lá desde a noite 1); a vaga abre na noite 4")
    jogo.ir_para("menu")
    esperar_transicao(jogo)

    # De manhã: primeiro a febre, depois o corpo de quem o jogador matou, com o nome.
    comecar_noite_1_na_aldeia(jogo, dentro=["Potira"], vivos=1, mortos=1, mortos_por_sua_mao=1,
                              mortos_nomes=["Yara"],
                              febre=[{"nome": "Potira", "de": "Mbaé", "noite": 1, "visivel": True}])
    jogo.amanhecer()
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "fala" and dia.caixa.texto == "Potira acordou com febre.", dia.caixa.texto
    rodar(jogo, 5)
    capturar(jogo, "25-dia2-manha-febre")
    dia.caixa.completar()
    clicar(jogo, (800, 300))
    assert dia.caixa.texto.startswith("O corpo de Yara"), dia.caixa.texto
    assert jogo.estado.vivos == 1 and len(jogo.estado.febre) == 1   # morre no dia 3
    print("ok manhã do Dia 2: a febre e o corpo com o nome")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_dia3_e_noite3(jogo):
    """Dia 3 (a primeira visita do Irmão Aleixo, que leva alguém) e a Noite 3 (os amaldiçoados)."""
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 2
    estado.dentro = ["Yara", "Mbaé", "Potira"]
    estado.vivos = 3
    # A semente faz o sorteio do Aleixo cair em Mbaé.
    estado.semente = next(n for n in range(1000)
                          if random.Random("%s:aleixo:3" % n).choice(estado.dentro) == "Mbaé")
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas."]
    # Mbaé dormiu na oca na noite 2 e Yara pegou dele.
    estado.febre = [{"nome": "Yara", "de": "Mbaé", "noite": 2, "visivel": True}]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    aldeia = jogo.cenas.atual
    assert aldeia.tem_seta and aldeia.texto_seta == "Dormir"
    clicar(jogo, aldeia.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)

    # A manhã: Yara acordou com febre (com o nome); e Mbaé tossiu a noite toda.
    dia = jogo.cenas.atual
    assert estado.dia == 3 and dia.titulo == "Dia 3"
    assert dia.modo == "fala" and dia.caixa.texto == "Yara acordou com febre.", dia.caixa.texto
    dia.caixa.completar()
    clicar(jogo, (800, 300))
    assert dia.caixa.texto.startswith("Mbaé tossiu"), dia.caixa.texto

    # A entrada: ninguém chega; o Irmão Aleixo finca a cruz, responde e pede alguém.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "perguntas" and dia.visitante == "aleixo", (dia.modo, dia.visitante)
    rodar(jogo, 60)
    capturar(jogo, "26-dia3-aleixo")
    assert textos_dos_botoes(jogo) == ["O que você quer?", "Por que a cruz?", "Seguir"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "O que você quer?")
    passar_falas(jogo)
    clicar_opcao(jogo, "Seguir")
    assert textos_dos_botoes(jogo) == ["Entregar Yara", "Entregar Mbaé", "Entregar Potira", "Negar"], (
        textos_dos_botoes(jogo))
    clicar_opcao(jogo, "Negar")
    dia.caixa.completar()
    # Na 1ª visita, negar não faz ele levar ninguém (A Honra precisa de gente viva no dia 10).
    assert dia.caixa.texto == "Ninguém? Desta vez eu vou sozinho.", dia.caixa.texto
    clicar(jogo, (800, 300))
    assert dia.caixa.texto == "Volto daqui a alguns dias.", dia.caixa.texto
    assert dia.acompanhante is None
    passar_falas(jogo)
    assert estado.dentro == ["Yara", "Mbaé", "Potira"] and estado.entregues_nomes == [], (
        estado.dentro, estado.entregues_nomes)
    assert estado.vivos == 3 and estado.levados == 0 and estado.entregues == 0 and estado.recusas_aleixo == 1
    assert estado.proximidade_vila == 0 and estado.pistas == 0
    # O resto do teste é a noite só com Yara: Mbaé sai da aldeia (como se o Aleixo o levasse).
    estado.dentro.remove("Mbaé")
    estado.entregues_nomes.append("Mbaé")
    estado.vivos -= 1
    print("ok Dia 3: o Irmão Aleixo (negar, e na 1ª visita ele vai embora sozinho)")

    # O sinal do pajé e a fogueira: sem Mbaé (foi com Aleixo).
    passar_falas(jogo)
    assert len(estado.tabua) == 2, "no Dia 3 o pajé não conta sinal novo"
    # 1 olhar, e mais 1 por ter negado o Aleixo; quem aceitou o machado de Yara tem mais 1.
    assert estado.energia_hoje == 1
    assert dia.titulo == "Noite 3" and dia.modo == "fogueira" and dia.energia == 2, dia.energia
    estado.machado = 1
    dia._comecar_noite()
    assert dia.energia == dia.energia_max == 3
    estado.energia_hoje = 0
    dia._comecar_noite()
    assert dia.energia == dia.energia_max == 2
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Yara"]
    assert not dia.botao_dormir.visivel, "ainda há energia e alguém para examinar"
    rodar(jogo, 40)
    capturar(jogo, "27-noite3-fogueira")

    # O pajé só desconfia do Irmão Aleixo.
    clicar_pessoa(jogo, "Pajé")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo)[0] == "O que você acha do Irmão Aleixo?", textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Ele vai voltar?")
    dia.caixa.completar()
    assert dia.caixa.texto.startswith("Volta."), dia.caixa.texto
    passar_falas(jogo)
    clicar_opcao(jogo, "Voltar para a fogueira")

    # Yara: os 2 olhares (com o machado). Ela pegou a febre, mas o rosto ainda não mostra.
    clicar_pessoa(jogo, "Yara")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Boca", "Terminar o exame"], textos_dos_botoes(jogo)
    examinar(jogo, ["Olhos", "Boca"])
    assert dia.energia == 0
    clicar_opcao(jogo, "Terminar o exame")
    assert textos_dos_botoes(jogo) == ["Deixar na oca", "Levar ao tapiri", "Matar"], textos_dos_botoes(jogo)
    rodar(jogo, 5)
    capturar(jogo, "28-noite3-yara-escolha")
    clicar_opcao(jogo, "Deixar na oca")
    passar_falas(jogo)
    assert dia.botao_dormir.visivel

    # Ir dormir: Yara, que pegou na noite 2, passa adiante (0 ou 1): só pode ser para Potira.
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    novos = [e for e in estado.febre if e["noite"] == 3]
    assert len(novos) <= 1 and all(e["nome"] == "Potira" and e["de"] == "Yara" for e in novos), novos

    # A aldeia de noite 3: as três ocas abertas, e a seta "Dormir" leva ao Dia 4.
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.abertas == ["oca1", "oca2", "oca3", "tapiri"] and aldeia.tem_seta
    entrar_na_oca(jogo, "oca3")
    rodar(jogo, 5)
    capturar(jogo, "29-noite3-oca3")
    print("ok Noite 3: amaldiçoados (quem pegou passa adiante, entre quem é de fora)")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_dia4_e_noite4(jogo):
    """Dia 4 (Potira chega: conversa curta na entrada, longa na oca Wanadi; o 3º sinal) e a Noite 4."""
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 3
    estado.dentro = ["Mbaé"]
    estado.vivos = 1
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas."]
    estado.tabua_noites = [1, 2]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    aldeia = jogo.cenas.atual
    assert aldeia.tem_seta and aldeia.texto_seta == "Dormir"
    clicar(jogo, aldeia.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert estado.dia == 4 and dia.titulo == "Dia 4"
    assert dia.caixa.texto.startswith("Mbaé tossiu"), dia.caixa.texto

    # Na entrada: Potira, e uma pergunta só.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "perguntas" and dia.visitante == "potira", (dia.modo, dia.visitante)
    assert textos_dos_botoes(jogo) == ["Onde você estava?", "Decidir"], textos_dos_botoes(jogo)
    rodar(jogo, 60)
    capturar(jogo, "30-dia4-potira")
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo, seguir_seta=False)
    assert estado.dentro == ["Mbaé", "Potira"] and estado.vivos == 2

    # Na oca Wanadi, a conversa inteira (mais longa que a da entrada).
    oca = entrar_na_oca(jogo, "oca3")
    assert [p.nome for p in oca.na_oca] == ["Potira"]
    rodar(jogo, 20)
    capturar(jogo, "31-dia4-potira-na-oca")
    clicar_pessoa(jogo, "Potira")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Viu gente amaldiçoada?", "Por que foi sozinha?",
                                       "Conte de antes.", "Terminar a conversa"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Conte de antes.")
    passar_falas(jogo)
    assert estado.memoria == 1 and "antes_potira" in estado.historias
    clicar_opcao(jogo, "Terminar a conversa")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)

    # O sinal do pajé: o 3º risco da tábua (III), contado na noite 4.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert estado.tabua[-1] == "Pontos brancos por dentro da bochecha." and len(estado.tabua) == 3
    assert estado.tabua_noites == [1, 2, 4], estado.tabua_noites
    dia.tabua.aberta = True
    rodar(jogo, 5)
    capturar(jogo, "32-dia4-tabua-III")
    dia.tabua.aberta = False
    print("ok Dia 4: Potira (curta na entrada, longa na oca) e o 3º sinal na tábua")

    # A fogueira: pajé, Mbaé e Potira. Os dois de fora são obrigatórios.
    assert dia.titulo == "Noite 4" and dia.modo == "fogueira" and dia.energia == 1
    # Potira senta no chão, à esquerda do pajé, e o pajé chega para o lado.
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Mbaé", "Potira"]
    from dados.noites import POSICAO_PAJE_COM_POTIRA
    assert dia.na_fogueira[0].rect.midbottom[0] == POSICAO_PAJE_COM_POTIRA[0]
    assert not dia.botao_dormir.visivel, "a seta de ir dormir só aparece sem energia"
    rodar(jogo, 40)
    capturar(jogo, "33-noite4-fogueira")
    clicar_pessoa(jogo, "Pajé")
    passar_falas(jogo)
    assert "E a Potira?" in textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Voltar para a fogueira")

    # Potira é sã: nada bate com a tábua. Na fogueira, a conversa dela é curta.
    clicar_pessoa(jogo, "Potira")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Viu gente amaldiçoada?", "Examinar o rosto"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Boca", "Terminar o exame"], textos_dos_botoes(jogo)
    # A boca: os lábios rachados, e ela se justifica (o frio, longe da fogueira).
    clicar_opcao(jogo, "Boca")
    dia.caixa.completar()
    clicar(jogo, (800, 300))
    assert "frio" in dia.caixa.texto, dia.caixa.texto
    passar_falas(jogo)
    assert dia.sinais.get("Potira", 0) == 0 and dia.energia == 0
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Deixar na oca")
    passar_falas(jogo)
    # Sem energia, já dá para dormir, mesmo sem ter falado com Mbaé (ele dormiria na oca).
    assert dia.energia == 0 and dia.botao_dormir.visivel, "sem energia, a seta de dormir aparece"

    clicar_pessoa(jogo, "Mbaé")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Levar ao tapiri")
    passar_falas(jogo)
    assert estado.tapiri == ["Mbaé"]
    assert dia.botao_dormir.visivel
    rodar(jogo, 10)
    capturar(jogo, "33b-noite4-seta-dormir")

    # Ir dormir: a aldeia de noite 4, e a seta "Dormir" leva ao Dia 5.
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.tem_seta
    oca = entrar_na_oca(jogo, "oca3")
    assert [quem for quem, _ in oca.pessoas] == ["Potira"], oca.pessoas
    rodar(jogo, 5)
    capturar(jogo, "34-noite4-oca3-potira")
    print("ok Noite 4: Potira sã, Mbaé ao tapiri")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_dia5_e_noite5(jogo):
    """Dia 5 (Tamandaré-mirim: curto na entrada, longo na oca Yebá Bëló; o pajé e os deuses) e a
    Noite 5."""
    from motor import febre
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 4
    estado.dentro = ["Mbaé", "Potira"]
    estado.vivos = 2
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas.",
                    "Pontos brancos por dentro da bochecha."]
    estado.tabua_noites = [1, 2, 4]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    aldeia = jogo.cenas.atual
    clicar(jogo, aldeia.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert estado.dia == 5 and dia.titulo == "Dia 5"
    assert dia.caixa.texto.startswith("Mbaé tossiu"), dia.caixa.texto

    # Na entrada: só "de onde vem" e "está amaldiçoado".
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "perguntas" and dia.visitante == "tamandare", (dia.modo, dia.visitante)
    assert textos_dos_botoes(jogo) == ["De onde você vem?", "Você está amaldiçoado?", "Decidir"], (
        textos_dos_botoes(jogo))
    clicar_opcao(jogo, "De onde você vem?")
    dia.caixa.completar()
    assert dia.caixa.texto.startswith("Dos caraíbas."), dia.caixa.texto
    rodar(jogo, 60)
    capturar(jogo, "35-dia5-tamandare")
    passar_falas(jogo)
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo, seguir_seta=False)
    assert estado.dentro == ["Mbaé", "Potira", "Tamandaré-mirim"] and estado.vivos == 3

    # Na oca Yebá Bëló, à esquerda da porta: a conversa inteira.
    oca = entrar_na_oca(jogo, "oca2")
    assert [p.nome for p in oca.na_oca] == ["Tamandaré-mirim"]
    assert [p.nome for p in oca.paradas] == ["Mbaé"], "Mbaé dorme na mesma oca"
    rodar(jogo, 20)
    capturar(jogo, "36-dia5-tamandare-na-oca")
    clicar_pessoa(jogo, "Tamandaré-mirim")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Conte do que você prega.", "Por que tosse?", "Por que essa cruz?",
                                       "Terminar a conversa"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Conte do que você prega.")
    passar_falas(jogo)
    assert estado.memoria == 1 and "prega_tamandare" in estado.historias
    clicar_opcao(jogo, "Terminar a conversa")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)

    # O pajé: Mbaé e Tamandaré-mirim na aldeia são 2 amaldiçoados: os deuses estão infelizes.
    # Nenhum sinal novo na tábua.
    assert febre.quantos_amaldicoados(estado) == 2
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert len(estado.tabua) == 3, "no Dia 5 o pajé não conta sinal novo"
    assert dia.titulo == "Noite 5" and dia.modo == "fogueira"
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Mbaé", "Potira", "Tamandaré-mirim"]
    rodar(jogo, 40)
    capturar(jogo, "37-noite5-fogueira")
    clicar_pessoa(jogo, "Pajé")
    dia.caixa.completar()
    assert "infelizes" in dia.caixa.texto, dia.caixa.texto
    passar_falas(jogo)
    # A acusação e o barulho na mata (a 2ª vez do Anhangá) são com o pajé, não com Potira.
    assert textos_dos_botoes(jogo) == ["De quem você desconfia?", "Que barulho é esse na mata?",
                                       "Voltar para a fogueira"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Voltar para a fogueira")
    assert dia.modo == "fogueira"
    # Com poucos amaldiçoados, os deuses estão felizes.
    assert dia._condicao({"amaldicoados_menos_de": 2}) is False
    estado.dentro.remove("Mbaé")
    assert dia._condicao({"amaldicoados_menos_de": 2}) and not dia._condicao({"amaldicoados_ao_menos": 2})
    estado.dentro.insert(0, "Mbaé")

    # Tamandaré-mirim: a boca mostra os pontos brancos (o sinal III).
    clicar_pessoa(jogo, "Tamandaré-mirim")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Boca", "Terminar o exame"], textos_dos_botoes(jogo)
    examinar(jogo, ["Boca"])
    assert dia.sinais["Tamandaré-mirim"] == 1 and dia.energia == 0
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Levar ao tapiri")
    passar_falas(jogo)
    assert estado.tapiri == ["Tamandaré-mirim"] and estado.tapiri_usos == 1

    clicar_pessoa(jogo, "Mbaé")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Deixar na oca")
    passar_falas(jogo)
    assert dia.botao_dormir.visivel
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.tem_seta, "a seta Dormir leva ao Dia 6"
    oca = entrar_na_oca(jogo, "tapiri")
    assert [quem for quem, _ in oca.pessoas] == ["Tamandaré-mirim"]
    rodar(jogo, 5)
    capturar(jogo, "38-noite5-tapiri-tamandare")
    print("ok Dia 5 e Noite 5: Tamandaré-mirim (dois sinais), o pajé e os deuses")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_dia6_e_noite6(jogo):
    """Dia 6 (a 2ª visita do Irmão Aleixo: o caderno, o que mudou, entregar ou negar) e a Noite 6
    (o 4º sinal: manchas pelo corpo, atrás das orelhas)."""
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 5
    estado.dentro = ["Mbaé", "Potira", "Tamandaré-mirim"]
    estado.entregues_nomes = ["Yara"]
    estado.levados = 1
    estado.vivos = 3
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas.",
                    "Pontos brancos por dentro da bochecha."]
    estado.tabua_noites = [1, 2, 4]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    clicar(jogo, jogo.cenas.atual.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert estado.dia == 6 and dia.titulo == "Dia 6"

    # A entrada: Aleixo veio sozinho (quem ele levou não voltou).
    passar_falas(jogo, seguir_seta=False)
    clicar(jogo, jogo.cenas.atual.rect_seta.center)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert dia.caixa.texto.startswith("Ninguém chega pela trilha"), dia.caixa.texto
    dia.caixa.completar()
    clicar(jogo, (800, 300))
    assert dia.caixa.texto.startswith("Ele veio sozinho"), dia.caixa.texto
    passar_falas(jogo)
    assert dia.visitante == "aleixo"
    # Ele levou Yara no dia 3: dá para perguntar se ela está curada e onde está (só dela).
    assert textos_dos_botoes(jogo) == ["O que tem nesse caderno?", "O que mudou?",
                                       "Yara está curada da maldição?", "Onde Yara está?",
                                       "Seguir"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "O que tem nesse caderno?")
    passar_falas(jogo)
    assert estado.pistas == 1
    clicar_opcao(jogo, "Yara está curada da maldição?")
    dia.caixa.completar()
    assert dia.caixa.texto.startswith("Ela reza todos os dias"), dia.caixa.texto
    passar_falas(jogo)
    clicar_opcao(jogo, "Onde Yara está?")
    dia.caixa.completar()
    assert dia.caixa.texto.startswith("Na casa da botica"), dia.caixa.texto
    passar_falas(jogo)
    rodar(jogo, 60)
    capturar(jogo, "39-dia6-aleixo")
    clicar_opcao(jogo, "Seguir")
    assert textos_dos_botoes(jogo) == ["Entregar Mbaé", "Entregar Potira", "Entregar Tamandaré-mirim",
                                       "Negar"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Entregar Mbaé")
    dia.caixa.completar()
    assert dia.acompanhante == "mbae"
    passar_falas(jogo)
    assert estado.dentro == ["Potira", "Tamandaré-mirim"] and estado.entregues == 1
    assert estado.entregues_nomes == ["Yara", "Mbaé"] and estado.proximidade_vila == 1 and estado.vivos == 2

    # O sinal do pajé: o 4º risco da tábua, na noite 6.
    assert estado.tabua[-1] == "Manchas avermelhadas atrás da orelha." and estado.tabua_noites == [1, 2, 4, 6]
    print("ok Dia 6: o Irmão Aleixo volta sozinho (caderno, o que mudou, onde está Yara, entregar) e o 4º sinal")

    # A fogueira: pajé, Potira e Tamandaré-mirim. Agora dá para olhar atrás das orelhas.
    assert dia.titulo == "Noite 6" and dia.modo == "fogueira"
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Potira", "Tamandaré-mirim"]
    rodar(jogo, 40)
    capturar(jogo, "40-noite6-fogueira")
    clicar_pessoa(jogo, "Tamandaré-mirim")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Orelhas", "Boca", "Terminar o exame"], textos_dos_botoes(jogo)
    examinar(jogo, ["Orelhas"])
    assert dia.sinais["Tamandaré-mirim"] == 1 and dia.energia == 0
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Levar ao tapiri")
    passar_falas(jogo)
    assert dia.botao_dormir.visivel
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.tem_seta, "a seta Dormir leva ao Dia 7"
    print("ok Noite 6: manchas atrás das orelhas, Tamandaré-mirim ao tapiri")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_dia7_e_noite7(jogo):
    """Dia 7 (Iandé: curta na entrada, longa na oca Yorixiriamori, com Yara) e a Noite 7."""
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 6
    estado.dentro = ["Yara"]
    estado.vivos = 1
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas.",
                    "Pontos brancos por dentro da bochecha.", "Manchas avermelhadas atrás da orelha."]
    estado.tabua_noites = [1, 2, 4, 6]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    clicar(jogo, jogo.cenas.atual.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    # Sem manhã para contar, o Dia 7 já começa andando pela aldeia.
    assert estado.dia == 7 and nome_cena(jogo) == "Aldeia", nome_cena(jogo)

    # Na entrada: uma pergunta só.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.modo == "perguntas" and dia.visitante == "iande", (dia.modo, dia.visitante)
    assert textos_dos_botoes(jogo) == ["Como estava a vila?", "Decidir"], textos_dos_botoes(jogo)
    rodar(jogo, 60)
    capturar(jogo, "41-dia7-iande")
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo, seguir_seta=False)
    assert estado.dentro == ["Yara", "Iandé"] and estado.vivos == 2

    # Na oca Yorixiriamori, com Yara: a conversa inteira.
    oca = entrar_na_oca(jogo, "oca1")
    assert [p.nome for p in oca.na_oca] == ["Iandé"] and [p.nome for p in oca.paradas] == ["Yara"]
    rodar(jogo, 20)
    capturar(jogo, "42-dia7-iande-na-oca")
    clicar_pessoa(jogo, "Iandé")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Como estava a vila?", "Viu alguém amaldiçoado?", "Que conta é essa no pulso?",
                                       "Conte da viagem.", "Terminar a conversa"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Viu alguém amaldiçoado?")
    dia = jogo.cenas.atual
    dia.caixa.completar()
    assert dia.caixa.texto == "Vi uma casa fechada, com uma cruz na porta.", dia.caixa.texto
    passar_falas(jogo)
    clicar_opcao(jogo, "Conte da viagem.")
    passar_falas(jogo)
    assert estado.memoria == 1 and "viagem_iande" in estado.historias
    clicar_opcao(jogo, "Terminar a conversa")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)

    # O pajé não conta sinal novo; na fogueira, Iandé é obrigatória e nada nela bate com a tábua.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert len(estado.tabua) == 4, "no Dia 7 o pajé não conta sinal novo"
    print("ok Dia 7: Iandé (curta na entrada, longa na oca com Yara)")
    assert dia.titulo == "Noite 7" and dia.modo == "fogueira"
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Yara", "Iandé"]
    rodar(jogo, 40)
    capturar(jogo, "43-noite7-fogueira")
    clicar_pessoa(jogo, "Pajé")
    passar_falas(jogo)
    clicar_opcao(jogo, "E a Iandé?")
    dia.caixa.completar()
    assert dia.caixa.texto == "Ela é nossa.", dia.caixa.texto
    passar_falas(jogo)
    clicar_opcao(jogo, "Voltar para a fogueira")
    clicar_pessoa(jogo, "Iandé")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Viu alguém amaldiçoado?", "Examinar o rosto"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Orelhas", "Boca", "Terminar o exame"], textos_dos_botoes(jogo)
    examinar(jogo, ["Orelhas"])
    assert dia.sinais.get("Iandé", 0) == 0 and dia.energia == 0
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Deixar na oca")
    passar_falas(jogo)
    assert dia.botao_dormir.visivel
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    # Iandé dormiu na oca: ela é amaldiçoada, e Yara (na mesma aldeia) pode pegar.
    assert all(e["de"] == "Iandé" and e["nome"] == "Yara" for e in estado.febre), estado.febre
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.tem_seta, "a seta Dormir leva ao Dia 8"
    print("ok Noite 7: Iandé sem nenhum sinal, e mesmo assim amaldiçoada")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_dia8_e_noite8(jogo):
    """Dia 8 (Krenan chega e é chamado para a fogueira) e a Noite 8 (a oferta de subir o rio)."""
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 7
    estado.dentro = ["Yara", "Iandé"]
    estado.vivos = 2
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas.",
                    "Pontos brancos por dentro da bochecha.", "Manchas avermelhadas atrás da orelha."]
    estado.tabua_noites = [1, 2, 4, 6]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    clicar(jogo, jogo.cenas.atual.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    assert estado.dia == 8

    # Na entrada: Krenan não pede teto. Só dá para chamá-lo para a fogueira.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.visitante == "krenan" and textos_dos_botoes(jogo) == ["Chamar para a fogueira",
                                                                      "Não deixar entrar"], (
        dia.visitante, textos_dos_botoes(jogo))
    rodar(jogo, 60)
    capturar(jogo, "44-dia8-krenan")
    clicar_opcao(jogo, "Chamar para a fogueira")
    passar_falas(jogo)
    assert estado.dentro == ["Yara", "Iandé"] and len(estado.tabua) == 4 and estado.convidados == ["Krenan"]
    print("ok Dia 8: Krenan chega e é chamado para a fogueira")

    # A fogueira: Krenan é obrigatório e não é examinado.
    assert dia.titulo == "Noite 8" and dia.modo == "fogueira"
    assert [p.nome for p in dia.na_fogueira] == ["Krenan", "Pajé", "Yara", "Iandé"]
    rodar(jogo, 40)
    capturar(jogo, "45-noite8-fogueira")
    clicar_pessoa(jogo, "Krenan")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Avisar sobre o quê?", "Ouvir o pedido"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Avisar sobre o quê?")
    passar_falas(jogo)
    clicar_opcao(jogo, "Ouvir o pedido")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Deixar levar alguém", "Não deixar"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Deixar levar alguém")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Yara", "Iandé", "Ninguém, afinal"], textos_dos_botoes(jogo)
    # Krenan levou alguém: volta na noite 10 para levar mais.
    clicar_opcao(jogo, "Yara")
    passar_falas(jogo)
    assert estado.dentro == ["Iandé"] and estado.rio_acima == 1 and estado.rio_acima_nomes == ["Yara"]
    assert estado.vivos == 1 and estado.krenan_volta == 1
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Iandé"]

    # Mesmo se quem sobe é amaldiçoado (Iandé traz a febre), Krenan volta.
    estado.krenan_volta = 0
    dia._subir_o_rio("Iandé")
    assert estado.krenan_volta == 1 and estado.dentro == [] and estado.rio_acima == 2
    estado.dentro, estado.rio_acima, estado.vivos = ["Iandé"], 1, 1
    estado.rio_acima_nomes = ["Yara"]
    estado.krenan_volta = 1
    # Sem o convite (o jogador não deixou entrar), Krenan não aparece na fogueira.
    estado.convidados = []
    dia._comecar_noite()
    assert "Krenan" not in [p.nome for p in dia.na_fogueira]
    print("ok Noite 8: Krenan leva quem o jogador escolhe rio acima (e volta na noite 10)")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_dia9_e_noite9(jogo):
    """Dia 9 (a última visita do Irmão Aleixo: tudo o que faltava, o cordão de Iandé, entregar ou
    negar) e a Noite 9 (o 5º sinal: manchas avermelhadas no pescoço; Krenan não está)."""
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 8
    estado.dentro = ["Tamandaré-mirim", "Iandé"]
    estado.vivos = 2
    estado.krenan_volta = 1
    estado.rio_acima, estado.rio_acima_nomes = 1, ["Yara"]
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas.",
                    "Pontos brancos por dentro da bochecha.", "Manchas avermelhadas atrás da orelha."]
    estado.tabua_noites = [1, 2, 4, 6]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    clicar(jogo, jogo.cenas.atual.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    assert estado.dia == 9

    # Na entrada: Aleixo, pela última vez, com tudo o que faltava dizer.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.visitante == "aleixo"
    assert textos_dos_botoes(jogo) == ["Os que você levou voltam?", "Isso é ameaça?", "Quem são os outros?",
                                       "Que cordão é esse no seu pescoço?", "Seguir"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Que cordão é esse no seu pescoço?")
    dia.caixa.completar()
    assert "Iandé" in dia.caixa.texto, dia.caixa.texto
    passar_falas(jogo)
    assert estado.pistas == 1
    rodar(jogo, 60)
    capturar(jogo, "46-dia9-aleixo")
    clicar_opcao(jogo, "Seguir")
    assert textos_dos_botoes(jogo) == ["Entregar Tamandaré-mirim", "Entregar Iandé", "Negar"], textos_dos_botoes(jogo)
    estado.semente = next(n for n in range(1000)
                          if random.Random("%s:aleixo:9" % n).choice(estado.dentro) == "Tamandaré-mirim")
    clicar_opcao(jogo, "Negar")
    dia.caixa.completar()
    assert dia.caixa.texto == "Chega. Eu levo quem eu quiser.", dia.caixa.texto
    passar_falas(jogo)
    assert estado.dentro == ["Iandé"] and estado.energia_hoje == 1

    # O sinal do pajé: o 5º risco da tábua.
    assert estado.tabua[-1] == "Manchas avermelhadas no pescoço." and estado.tabua_noites[-1] == 9
    print("ok Dia 9: a última visita do Irmão Aleixo (tudo o que faltava, o cordão) e o 5º sinal")

    # A fogueira: Krenan não está (volta só na noite 10). Iandé, que parecia perfeita, tem as
    # manchas no pescoço.
    assert dia.titulo == "Noite 9" and dia.modo == "fogueira" and dia.energia == 2
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Iandé"], [p.nome for p in dia.na_fogueira]
    rodar(jogo, 40)
    capturar(jogo, "47-noite9-fogueira")
    clicar_pessoa(jogo, "Iandé")
    passar_falas(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Orelhas", "Boca", "Pescoço", "Terminar o exame"], (
        textos_dos_botoes(jogo))
    examinar(jogo, ["Pescoço"])
    assert dia.sinais["Iandé"] == 1
    clicar_opcao(jogo, "Terminar o exame")
    clicar_opcao(jogo, "Levar ao tapiri")
    passar_falas(jogo)
    assert dia.botao_dormir.visivel
    print("ok Noite 9: manchas no pescoço de Iandé, e Krenan fora da aldeia")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_rever_finais(jogo):
    """Depois do primeiro final visto, o menu tem "Finais": ler de novo, com "Final N/8" e a chance."""
    from motor import finais
    vistos = finais.vistos()
    assert vistos, "a noite 10 acabou num final: ele fica guardado como visto"
    menu = jogo.cenas.atual
    assert nome_cena(jogo) == "Menu" and menu.botao_finais.visivel
    clicar_botao(jogo, menu.botao_finais)
    esperar_transicao(jogo)
    lista = jogo.cenas.atual
    assert nome_cena(jogo) == "Finais" and [i for _, i in lista.linhas] == vistos
    assert len(lista.linhas) + len(lista.escondidos) == 8
    clicar_botao(jogo, lista.linhas[0][0])
    esperar_transicao(jogo)
    fim = jogo.cenas.atual
    numero, total = finais.numero(vistos[0])
    assert nome_cena(jogo) == "Final" and fim.revendo == vistos[0]
    assert fim.linhas_chance[0] == "Final %d/%d" % (numero, total), fim.linhas_chance
    assert "%" in fim.linhas_chance[1], fim.linhas_chance
    for _ in range(5):
        fim.avancar()
    assert fim.indice == 2 and fim.botao.texto == "Voltar aos finais"
    rodar(jogo, 10)
    capturar(jogo, "51-final-fonte-e-chance")
    clicar_botao(jogo, fim.botao)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Finais"
    clicar_botao(jogo, jogo.cenas.atual.botao_voltar)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Menu"
    print("ok Finais: ler de novo um final já visto (Final N/8 e a chance)")


def testar_dia10_e_noite10(jogo):
    """Dia 10 (Araci: duas perguntas na entrada, a conversa inteira na oca Wanadi, no meio da
    cama) e a Noite 10 (o pajé e Araci na fogueira; o final calculado de manhã não muda)."""
    from motor import finais
    jogo.nova_partida()
    estado = jogo.estado
    estado.dia = 9
    estado.dentro = ["Potira"]
    estado.vivos = 1
    estado.krenan_volta = 1
    # Já matou dois: se o final fosse calculado depois de matar Araci, seria A Loucura.
    estado.mortos = estado.mortos_por_sua_mao = 2
    estado.tabua = ["Olho vermelho, com o branco raiado.", "Boca com feridas.",
                    "Pontos brancos por dentro da bochecha.", "Manchas avermelhadas atrás da orelha.",
                    "Manchas avermelhadas no pescoço."]
    estado.tabua_noites = [1, 2, 4, 6, 9]
    jogo.ir_para("aldeia")
    esperar_transicao(jogo)
    assert jogo.cenas.atual.tem_seta, "a noite 9 tem a seta de dormir: existe o Dia 10"
    clicar(jogo, jogo.cenas.atual.rect_seta.center)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    assert estado.dia == 10
    assert estado.final_calculado == finais.escolher(estado)["id"] != "loucura", estado.final_calculado

    # Na entrada: a cruz sem o Aleixo, e Araci com só duas perguntas.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.titulo == "Dia 10" and dia.visitante == "araci"
    assert textos_dos_botoes(jogo) == ["De onde você vem?", "Desde quando as manchas?", "Decidir"], (
        textos_dos_botoes(jogo))
    rodar(jogo, 60)
    capturar(jogo, "48-dia10-araci")
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Deixar entrar")
    passar_falas(jogo, seguir_seta=False)
    assert estado.dentro == ["Potira", "Araci"] and estado.vivos == 2

    # Na oca Wanadi: Araci no meio da cama; Potira desce para a esteira ao lado.
    oca = entrar_na_oca(jogo, "oca3")
    assert [p.nome for p in oca.na_oca] == ["Araci"] and oca.na_oca[0].rect.centerx == 1240
    assert oca.pessoas == [("Potira", "potira_sentada")] and oca.paradas[0].rect.centerx == 1075
    rodar(jogo, 20)
    capturar(jogo, "49-dia10-araci-na-oca")
    clicar_pessoa(jogo, "Araci")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["De onde você vem?", "Desde quando as manchas?",
                                       "Como ela vai se chamar?", "Onde está o pai da criança?",
                                       "Você sente dor?",
                                       "Terminar a conversa"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Como ela vai se chamar?")
    passar_falas(jogo)
    assert estado.memoria == 1
    clicar_opcao(jogo, "Terminar a conversa")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    esperar_transicao(jogo)
    print("ok Dia 10: Araci (duas perguntas na entrada, a conversa inteira na oca Wanadi)")

    # A fogueira: o pajé e Araci, em cima do tronco de baixo, à esquerda. 2 olhares.
    passar_falas(jogo)
    dia = jogo.cenas.atual
    assert dia.titulo == "Noite 10" and dia.modo == "fogueira" and dia.energia == 2
    # Krenan levou alguém na noite 8: volta e faz o mesmo pedido. Aqui, ninguém vai.
    # Quem o jogador deixou entrar (Potira) também está no fogo.
    assert [p.nome for p in dia.na_fogueira] == ["Krenan", "Pajé", "Potira", "Araci"], [p.nome for p in dia.na_fogueira]
    assert not dia.botao_dormir.visivel, "antes, é preciso falar com Araci e com Krenan"
    clicar_pessoa(jogo, "Krenan")
    passar_falas(jogo)
    # O mesmo pedido da noite 8, e agora o jogador também pode ir com ele (Rio Acima).
    assert textos_dos_botoes(jogo) == ["Deixar levar alguém", "Não deixar"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Deixar levar alguém")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo)[-2:] == ["Ir com ele", "Ninguém, afinal"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Ninguém, afinal")
    passar_falas(jogo)
    assert estado.subiu_o_rio == 0
    rodar(jogo, 40)
    capturar(jogo, "50-noite10-fogueira")
    clicar_pessoa(jogo, "Araci")
    passar_falas(jogo)
    # Na fogueira, sem as perguntas da criança (só na oca).
    assert textos_dos_botoes(jogo) == ["De onde você vem?", "Desde quando as manchas?",
                                       "Você sente dor?", "Examinar o rosto"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Examinar o rosto")
    assert textos_dos_botoes(jogo) == ["Olhos", "Orelhas", "Boca", "Pescoço",
                                       "Terminar o exame"], textos_dos_botoes(jogo)
    examinar(jogo, ["Olhos", "Boca"])
    assert dia.sinais["Araci"] == 2 and dia.energia == 0
    clicar_opcao(jogo, "Terminar o exame")
    assert textos_dos_botoes(jogo) == ["Deixar na oca", "Levar ao tapiri", "Matar"], textos_dos_botoes(jogo)
    clicar_opcao(jogo, "Matar")
    dia.caixa.completar()
    assert dia.caixa.texto == "Araci. Duas.", dia.caixa.texto
    passar_falas(jogo)
    assert dia.botao_dormir.visivel and estado.mortos_por_sua_mao == 3
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Final" and estado.final == estado.final_calculado != "loucura", (
        nome_cena(jogo), estado.final)
    print("ok Noite 10: o pajé e Araci na fogueira; o final é o da manhã, mesmo matando Araci")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


def testar_continuar_tabua_tutorial(jogo):
    from dados.dias import DIAS
    perguntas = next(p for p in DIAS[1]["passos"] if p["tipo"] == "perguntas")["perguntas"]

    # Joga um pedaço do Dia 1: faz a 1ª pergunta e sai pelo botão Menu.
    jogo.nova_partida()
    jogo.ir_para("menu", com_fade=False)
    rodar(jogo, 2)
    assert not jogo.cenas.atual.botao_continuar.visivel, "sem partida guardada, Continuar não aparece"
    jogo.ir_para("dia")
    esperar_transicao(jogo)
    passar_falas(jogo)
    clicar_opcao(jogo, perguntas[1]["pergunta"])   # os olhos: a resposta de Yara é "[Fumaça]"
    passar_falas(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_menu)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Menu"
    menu = jogo.cenas.atual
    assert menu.botao_continuar.visivel, "com partida guardada, Continuar aparece"
    rodar(jogo, 5)
    capturar(jogo, "12-menu-continuar")

    # Continuar: volta exatamente às perguntas, sem a que já foi feita.
    clicar_botao(jogo, menu.botao_continuar)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.modo == "perguntas", (nome_cena(jogo), dia.modo)
    textos = [b.texto for b, _ in dia.botoes]
    assert textos == [perguntas[0]["pergunta"], "Decidir"], textos
    assert dia.visitante == "yara"
    print("ok Continuar volta ao ponto exato do Dia 1")

    # Segue até o sinal: a tábua ganha o sinal e o ícone avisa que há coisa nova.
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Não deixar entrar")
    passar_falas_ate_sinal = 0
    while not jogo.estado.tabua and passar_falas_ate_sinal < 20:
        clicar(jogo, (800, 300))
        passar_falas_ate_sinal += 1
    assert jogo.estado.tabua and dia.tabua.nova
    rodar(jogo, 30)
    capturar(jogo, "13-dia1-sinal-tabua")
    clicar(jogo, dia.tabua.rect_icone.center)
    assert dia.tabua.aberta and not dia.tabua.nova
    rodar(jogo, 3)
    capturar(jogo, "14-tabua-aberta")
    modo_antes = dia.modo
    clicar(jogo, (800, 450))                       # clique dentro da tábua: o jogo não avança
    assert dia.tabua.aberta and dia.modo == modo_antes
    clicar_botao(jogo, dia.tabua.botao_fechar)
    assert not dia.tabua.aberta
    print("ok tábua de barro (sinal novo, abrir, fechar)")

    passar_falas(jogo)
    clicar_botao(jogo, dia.botao_dormir)   # a fogueira, só com o pajé
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", nome_cena(jogo)
    jogo.ir_para("menu")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_continuar)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", "depois do Dia 1, Continuar leva à aldeia, de noite"
    print("ok Continuar depois do fim do Dia 1")

    # Como se joga: fica dentro das Opções (o menu principal não tem mais o botão).
    jogo.ir_para("menu")
    esperar_transicao(jogo)
    assert not hasattr(jogo.cenas.atual, "botao_tutorial")
    clicar_botao(jogo, jogo.cenas.atual.botao_opcoes)
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_tutorial)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Tutorial"
    rodar(jogo, 5)
    capturar(jogo, "15-como-se-joga")
    tecla(jogo, pygame.K_ESCAPE)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Opcoes", nome_cena(jogo)
    print("ok Como se joga, pelas Opções")


def testar_escala(jogo):
    # Janela 1280x720: a tela 1600x900 é reduzida a 80%, sem barras.
    area = jogo._calcular_area()
    assert area.size == (1280, 720), area
    # Ida e volta janela <-> lógica.
    for ponto in [(0, 0), (800, 450), (1599, 899)]:
        volta = jogo.janela_para_logica(jogo.logica_para_janela(ponto))
        assert abs(volta[0] - ponto[0]) <= 2 and abs(volta[1] - ponto[1]) <= 2, (ponto, volta)
    print("ok escala da tela e conversão do mouse")


def testar_fluxo():
    jogo = Jogo(tamanho_janela=(1280, 720))
    testar_escala(jogo)

    # 1. Menu
    rodar(jogo, 40)
    assert nome_cena(jogo) == "Menu"
    capturar(jogo, "01-menu")
    print("ok menu abriu")

    # 2. Opções: trocar tamanho do texto e voltar com Esc
    clicar_botao(jogo, jogo.cenas.atual.botao_opcoes)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Opcoes"
    rodar(jogo, 5)
    capturar(jogo, "02-opcoes")
    clicar_botao(jogo, jogo.cenas.atual.botao_grande)
    assert jogo.preferencias.tamanho_texto == "grande"
    rodar(jogo, 5)
    capturar(jogo, "03-opcoes-texto-grande")
    clicar_botao(jogo, jogo.cenas.atual.botao_normal)
    assert jogo.preferencias.tamanho_texto == "normal"
    tecla(jogo, pygame.K_ESCAPE)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Menu"
    print("ok opções (texto normal/grande, Esc volta)")

    # 3. Começar -> introdução, avançando cada cartão
    clicar_botao(jogo, jogo.cenas.atual.botao_comecar)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Introducao"
    intro = jogo.cenas.atual
    total = len(INTRODUCAO["cartoes"])
    vistos = set()
    for _ in range(4 * total):
        if nome_cena(jogo) != "Introducao" or jogo.cenas.em_transicao():
            break
        vistos.add(intro.indice)
        rodar(jogo, 20)  # deixa algumas letras aparecerem
        assert not intro.caixa.terminou(), (intro.indice, intro.caixa.letras_visiveis, intro.caixa.total_letras)
        clicar(jogo, (800, 300))            # 1º clique: completa o texto
        assert intro.caixa.terminou()
        rodar(jogo, 50)                     # termina a mistura de cenários, se houver
        if intro.indice == 3:
            capturar(jogo, "04-introducao-cartao")
        if intro.indice % 2:
            tecla(jogo, pygame.K_SPACE)     # avança com Espaço...
        else:
            clicar(jogo, (800, 300))        # ...ou com clique
    esperar_transicao(jogo)
    assert vistos == set(range(total)), vistos
    assert nome_cena(jogo) == "Dia", nome_cena(jogo)
    print("ok introdução inteira (%d cartões) -> Dia 1" % total)

    # 4. Botão Menu do Dia volta ao menu
    clicar_botao(jogo, jogo.cenas.atual.botao_menu)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Menu"
    print("ok voltar ao menu")

    # 5. Começar de novo e usar "Pular"
    tecla(jogo, pygame.K_RETURN)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Introducao"
    clicar_botao(jogo, jogo.cenas.atual.botao_pular)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Dia"
    print("ok botão Pular")

    # 5b. O Dia 1 inteiro, pelos dois caminhos, e a aldeia de dia
    testar_dia1(jogo)
    testar_dia2_e_noite2(jogo)
    testar_dia3_e_noite3(jogo)
    testar_dia4_e_noite4(jogo)
    testar_dia5_e_noite5(jogo)
    testar_dia6_e_noite6(jogo)
    testar_dia7_e_noite7(jogo)
    testar_dia8_e_noite8(jogo)
    testar_dia9_e_noite9(jogo)
    testar_dia10_e_noite10(jogo)
    testar_rever_finais(jogo)
    testar_aldeia_de_dia(jogo)

    # 5c. Continuar de onde parou, a tábua de barro e o "Como se joga" do menu
    testar_continuar_tabua_tutorial(jogo)

    # 6. Texto grande não quebra a introdução
    jogo.preferencias.tamanho_texto = "grande"
    jogo.ir_para("introducao")
    esperar_transicao(jogo)
    jogo.cenas.atual.caixa.completar()
    rodar(jogo, 3)
    capturar(jogo, "06-introducao-texto-grande")
    jogo.preferencias.tamanho_texto = "normal"
    print("ok texto grande")

    # 7. Sanidade baixa: tratamento mais forte não quebra nada
    jogo.cenas.atual.tratamento.ajustar_pela_sanidade(3)
    rodar(jogo, 30)
    print("ok tratamento com sanidade baixa")

    # 8. Sair
    jogo.ir_para("menu", com_fade=False)
    rodar(jogo, 2)
    clicar_botao(jogo, jogo.cenas.atual.botao_sair)
    assert not jogo.rodando
    jogo.encerrar()
    print("ok sair")


def testar_modo_teste():
    """Testar uma noite (config.MODO_TESTE): cada noite abre direto na fogueira, sem mexer na
    partida guardada."""
    from motor import progresso, teste
    progresso.salvar("aldeia", {"dia": 3})
    jogo = Jogo(tamanho_janela=(1280, 720))
    for noite in range(1, 11):
        teste.ir_para_noite(jogo, noite)
        esperar_transicao(jogo)
        dia = jogo.cenas.atual
        assert nome_cena(jogo) == "Dia" and dia.titulo == "Noite %d" % noite and dia.modo == "fogueira", (
            noite, nome_cena(jogo), getattr(dia, "titulo", None))
        assert len(jogo.estado.dentro) == {1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 5, 10: 6}[noite]
    assert "Krenan" not in [p.nome for p in dia.na_fogueira] or noite in (8, 10)
    assert progresso.carregar()["estado"] == {"dia": 3}, "a partida guardada não muda"
    jogo.encerrar()
    print("ok testar uma noite: as 10 noites abrem na fogueira, e a partida guardada fica")


def testar_desempenho():
    """Mede quanto tempo um quadro leva (meta: bem menos que 16 ms para 60 FPS)."""
    import time
    jogo = Jogo(tamanho_janela=(1280, 720))
    rodar(jogo, 10)
    inicio = time.perf_counter()
    quadros = 120
    rodar(jogo, quadros)
    ms = (time.perf_counter() - inicio) / quadros * 1000
    print("ok desempenho do menu: %.1f ms por quadro (janela 1280x720)" % ms)
    jogo.encerrar()


if __name__ == "__main__":
    testar_marcacao()
    testar_estado_inicial()
    testar_finais()
    testar_febre()
    testar_sinais_no_rosto()
    testar_corpos()
    testar_cura_no_tapiri()
    testar_cartoes_introducao()
    testar_fluxo()
    testar_modo_teste()
    testar_desempenho()
    print("TUDO CERTO")
