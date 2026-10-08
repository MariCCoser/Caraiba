# Teste de fumaça: joga sozinho, sem janela, menu -> opções -> introdução inteira -> Dia 1 -> cena provisória -> menu.
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
                "pistas": 0, "sanidade": 10, "dentro": [], "caderno": []}
    assert estado.para_dicionario() == esperado, estado.para_dicionario()
    print("ok Estado com os valores iniciais do documento")


def testar_cartoes_introducao():
    # A Proposta pede: aviso de conteúdo primeiro (tela preta) e as regras por último.
    cartoes = INTRODUCAO["cartoes"]
    assert all(cartao.get("texto") for cartao in cartoes), "cartão sem texto"
    assert cartoes[0].get("titulo") and not cartoes[0].get("fundo"), "o 1º cartão deve ser o aviso"
    assert cartoes[-1].get("titulo") and cartoes[-1].get("fundo"), "o último cartão deve ser as regras"
    print("ok ordem dos cartões da introdução (aviso ... regras)")


def passar_falas(jogo):
    """No Dia: clica nas falas (completar e seguir) até aparecerem botões ou a cena acabar."""
    for _ in range(100):
        if nome_cena(jogo) != "Dia" or jogo.cenas.em_transicao() or jogo.cenas.atual.modo != "fala":
            return
        rodar(jogo, 5)
        clicar(jogo, (800, 300))   # completa o texto
        clicar(jogo, (800, 300))   # segue o roteiro
    raise AssertionError("as falas do Dia nunca terminaram")


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
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "EmConstrucao", nome_cena(jogo)
    estado = jogo.estado
    assert estado.vivos == 13 and estado.dentro == ["Yara"], (estado.vivos, estado.dentro)
    assert estado.memoria == 1 and estado.proximidade_vila == 1, (estado.memoria, estado.proximidade_vila)
    assert estado.caderno == ["Olho vermelho, com o branco raiado."], estado.caderno
    rodar(jogo, 5)
    capturar(jogo, "11-noite1-em-construcao")
    print("ok Dia 1 deixando Yara entrar (perguntas, machado, sinal no caderno)")

    # 2ª vez: decide direto, sem perguntar, e não deixa entrar.
    jogo.nova_partida()
    jogo.ir_para("dia")
    esperar_transicao(jogo)
    passar_falas(jogo)
    clicar_opcao(jogo, "Decidir")
    clicar_opcao(jogo, "Não deixar entrar")
    passar_falas(jogo)
    esperar_transicao(jogo)
    assert nome_cena(jogo) == "EmConstrucao", nome_cena(jogo)
    estado = jogo.estado
    assert estado.vivos == 12 and estado.dentro == [] and estado.memoria == 0, estado.para_dicionario()
    assert len(estado.caderno) == 1
    print("ok Dia 1 sem deixar Yara entrar")
    jogo.ir_para("menu")
    esperar_transicao(jogo)


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

    # 5b. O Dia 1 inteiro, pelos dois caminhos
    testar_dia1(jogo)

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
