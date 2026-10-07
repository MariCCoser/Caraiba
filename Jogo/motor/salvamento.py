# Guarda e lê dados pequenos (preferências, e depois o progresso) no computador ou no navegador.
#
# Por que assim: no computador o jeito simples é um arquivo .json na pasta saves/.
# No navegador (pygbag) não existe pasta de verdade que sobreviva ao fechar a
# aba; lá usamos o localStorage do navegador. Qualquer erro aqui é ignorado de
# propósito: perder uma preferência é ruim, mas o jogo travar é muito pior.

import json
import os

import config


def salvar(nome, dados):
    """Salva um dicionário com o nome dado (ex.: "preferencias"). Devolve True se deu certo."""
    try:
        texto = json.dumps(dados, ensure_ascii=False, indent=2)
        if config.NO_NAVEGADOR:
            import platform  # no pygbag, "platform" dá acesso ao navegador
            platform.window.localStorage.setItem("caraiba-" + nome, texto)
        else:
            os.makedirs(config.PASTA_SAVES, exist_ok=True)
            caminho = os.path.join(config.PASTA_SAVES, nome + ".json")
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(texto)
        return True
    except Exception as erro:
        print("Aviso: não consegui salvar", nome, "-", erro)
        return False


def carregar(nome):
    """Lê o que foi salvo com esse nome. Devolve None se não houver nada (ou se der erro)."""
    try:
        if config.NO_NAVEGADOR:
            import platform
            texto = platform.window.localStorage.getItem("caraiba-" + nome)
            if not texto:
                return None
        else:
            caminho = os.path.join(config.PASTA_SAVES, nome + ".json")
            if not os.path.exists(caminho):
                return None
            with open(caminho, encoding="utf-8") as arquivo:
                texto = arquivo.read()
        return json.loads(texto)
    except Exception as erro:
        print("Aviso: não consegui ler", nome, "-", erro)
        return None
