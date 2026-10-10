# Teste de fumaça: joga sozinho, sem janela, menu -> opções -> introdução inteira -> Dia 1 -> aldeia e oca -> menu.
#
# Como rodar (de dentro da pasta Jogo, com o ambiente ativado):
#     python -m testes.teste_fluxo
# Para também salvar imagens das telas, diga em que pasta:
#     CARAIBA_CAPTURAS=/tmp/capturas python -m testes.teste_fluxo
#
# Se aparecer "TUDO CERTO" no fim, o fluxo funciona. Se der erro, o Python
# mostra a linha do problema.

import os
import tempfile

# Sem janela e sem som: precisa vir ANTES de importar o pygame.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

import config  # noqa: E402

# Preferências do teste vão para uma pasta temporária (não estraga as suas).
config.PASTA_SAVES = tempfile.mkdtemp(prefix="caraiba-teste-")

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
    esperado = {"dia": 1, "vivos": 12, "mortos": 0, "mortos_por_sua_mao": 0, "entregues": 0,
                "proximidade_vila": 0, "rio_acima": 0, "memoria": 0, "recusas_aleixo": 0,
                "pistas": 0, "sanidade": 10, "dentro": [], "tapiri": [], "mortos_nomes": [], "tabua": []}
    assert estado.para_dicionario() == esperado, estado.para_dicionario()
    print("ok Estado com os valores iniciais do documento")


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
    assert aldeia.de_dia and aldeia.abertas == ["oca1"]
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
    assert estado.vivos == 13 and estado.dentro == ["Yara"], (estado.vivos, estado.dentro)
    assert estado.proximidade_vila == 1, estado.proximidade_vila
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
    assert dia.botao_dormir.habilitado and dia.botao_dormir.texto == "Ir dormir"
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", nome_cena(jogo)
    estado = jogo.estado
    assert estado.vivos == 12 and estado.dentro == [] and estado.memoria == 0, estado.para_dicionario()
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
    print("ok Noite 1 levando Yara ao tapiri")
    testar_aldeia_e_oca(jogo, yara_dentro=False)
    jogo.ir_para("menu")
    esperar_transicao(jogo)


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
    """Clica numa pessoa desenhada no cenário (na aldeia de dia ou na fogueira)."""
    cena = jogo.cenas.atual
    pessoas = cena.pessoas if nome_cena(jogo) == "Aldeia" else cena.na_fogueira
    pessoa = next(p for p in pessoas if p.nome == nome)
    ponto = ponto_na_pessoa(pessoa)
    rodar(jogo, 1, [pygame.event.Event(pygame.MOUSEMOTION, pos=jogo.logica_para_janela(ponto),
                                       rel=(0, 0), buttons=(0, 0, 0))])
    clicar(jogo, ponto)
    esperar_transicao(jogo)


def testar_aldeia_com_yara(jogo):
    """Depois de entrar, Yara está na aldeia: clicar nela abre a conversa sobre a aldeia antiga."""
    aldeia = jogo.cenas.atual
    assert nome_cena(jogo) == "Aldeia" and aldeia.de_dia, nome_cena(jogo)
    assert [p.nome for p in aldeia.pessoas] == ["Yara"] and aldeia.texto_seta == "Esperar a noite"
    rodar(jogo, 20)
    capturar(jogo, "10b-dia1-aldeia-com-yara")

    clicar_pessoa(jogo, "Yara")
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.visitante == "yara" and dia.fundo == ("aldeia", "dia"), (nome_cena(jogo), getattr(dia, "visitante", None), getattr(dia, "fundo", None))
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Conte da sua aldeia.", "Por que saiu de lá?",
                                       "A febre chegou lá?", "Voltar à aldeia"]
    # A história da aldeia dela: três frases, e conta como história ouvida.
    clicar_opcao(jogo, "Conte da sua aldeia.")
    dia.caixa.completar()
    rodar(jogo, 2)
    capturar(jogo, "10c-dia1-aldeia-de-yara")
    passar_falas(jogo)
    assert jogo.estado.memoria == 1
    clicar_opcao(jogo, "Voltar à aldeia")
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia" and jogo.cenas.atual.de_dia

    # Menu e Continuar: volta à aldeia, e a pergunta feita não volta.
    clicar_botao(jogo, jogo.cenas.atual.botao_menu)
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_continuar)
    esperar_transicao(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia" and jogo.estado.memoria == 1, (nome_cena(jogo), jogo.estado.memoria)
    clicar_pessoa(jogo, "Yara")
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Por que saiu de lá?", "A febre chegou lá?", "Voltar à aldeia"]
    clicar_opcao(jogo, "Voltar à aldeia")
    esperar_transicao(jogo)
    print("ok aldeia de dia com Yara: conversa sobre a aldeia antiga dela (e Continuar)")


def testar_noite1_com_yara(jogo):
    """A fogueira: escolher com quem falar (pajé, Yara), exame com energia, Continuar e a decisão."""
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.titulo == "Noite 1", (nome_cena(jogo), dia.titulo)
    assert dia.modo == "fogueira" and dia.fundo == ("fogueira_perto", "noite")
    assert [p.nome for p in dia.na_fogueira] == ["Pajé", "Yara"]
    assert not dia.botao_dormir.habilitado, "só dá para dormir depois de decidir sobre Yara"
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

    # Yara: a conversa é só sobre o que se vê nela.
    clicar_pessoa(jogo, "Yara")
    assert dia.visitante == "yara"
    passar_falas(jogo)
    assert textos_dos_botoes(jogo) == ["Seus olhos ainda estão vermelhos.", "Que terra é essa nas suas unhas?",
                                       "Esse pano é dos estrangeiros?", "Examinar o rosto"]
    clicar_opcao(jogo, "Seus olhos ainda estão vermelhos.")
    passar_falas(jogo)

    # O exame: 3 de energia para 5 zonas.
    clicar_opcao(jogo, "Examinar o rosto")
    assert dia.energia == 3 and textos_dos_botoes(jogo)[-1] == "Terminar o exame"
    clicar_opcao(jogo, "Olhos")
    passar_falas(jogo)
    assert dia.energia == 2 and dia.sinais == {"Yara": 1}

    # Continuar no meio do exame: a mesma energia, o mesmo sinal achado.
    clicar_botao(jogo, dia.botao_menu)
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_continuar)
    esperar_transicao(jogo)
    dia = jogo.cenas.atual
    assert nome_cena(jogo) == "Dia" and dia.titulo == "Noite 1" and dia.modo == "perguntas"
    assert dia.energia == 2 and dia.sinais == {"Yara": 1} and jogo.estado.memoria == 1
    assert "Pajé" in dia.conversados and "Yara" in dia.conversados
    assert textos_dos_botoes(jogo) == ["Boca", "Pele", "Pescoço", "Mãos", "Terminar o exame"]
    print("ok Continuar no meio do exame da Noite 1")

    for zona in ["Boca", "Mãos"]:
        clicar_opcao(jogo, zona)
        passar_falas(jogo)
    assert dia.energia == 0
    # Sem energia: as zonas que sobraram ficam fechadas, só dá para terminar.
    assert [b.habilitado for b, _ in dia.botoes] == [False, False, True]
    clicar(jogo, dia.botoes[0][0].rect.center)     # clique em "Pele", fechada
    assert dia.modo == "perguntas" and dia.energia == 0, "zona sem energia não pode abrir"
    rodar(jogo, 5)
    capturar(jogo, "10d-noite1-sem-energia")
    clicar_opcao(jogo, "Terminar o exame")

    # A decisão: só um sinal achado, então matar está fechado.
    assert dia.modo == "escolha"
    assert textos_dos_botoes(jogo) == ["Deixar na oca", "Levar ao tapiri", "Matar · só com dois sinais"]
    assert not dia.botoes[2][0].habilitado
    clicar(jogo, dia.botoes[2][0].rect.center)     # clique em "Matar", fechado
    assert dia.modo == "escolha" and jogo.estado.dentro == ["Yara"], "matar exige dois sinais"
    dia.caixa.completar()
    rodar(jogo, 5)
    capturar(jogo, "10e-noite1-decisao")
    clicar_opcao(jogo, "Deixar na oca")
    passar_falas(jogo)

    # De volta à fogueira: Yara foi dormir, só sobra o pajé, e agora dá para ir dormir.
    assert dia.modo == "fogueira" and [p.nome for p in dia.na_fogueira] == ["Pajé"]
    assert dia.botao_dormir.habilitado
    clicar_botao(jogo, dia.botao_dormir)
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Aldeia", nome_cena(jogo)
    assert jogo.estado.tapiri == [] and jogo.estado.mortos_por_sua_mao == 0
    print("ok Noite 1 na fogueira (pajé e Yara, exame com energia, matar fechado, Yara na oca)")


def centro_da_oca(nome):
    from dados.aldeia import OCAS
    pontos = OCAS[nome]["contorno"]
    # Um ponto bem dentro do contorno: a média dos pontos.
    return (sum(x for x, _ in pontos) // len(pontos), sum(y for _, y in pontos) // len(pontos))


def testar_aldeia_e_oca(jogo, yara_dentro):
    """Na noite 1 só a oca 1 abre; Yara está nela se o jogador a deixou entrar."""
    aldeia = jogo.cenas.atual
    assert aldeia.abertas == ["oca1"], aldeia.abertas

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

    # Como se joga, pelo menu.
    jogo.ir_para("menu")
    esperar_transicao(jogo)
    clicar_botao(jogo, jogo.cenas.atual.botao_tutorial)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Tutorial"
    rodar(jogo, 5)
    capturar(jogo, "15-como-se-joga")
    tecla(jogo, pygame.K_ESCAPE)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "Menu"
    print("ok Como se joga, pelo menu")


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
    testar_cartoes_introducao()
    testar_fluxo()
    testar_desempenho()
    print("TUDO CERTO")
