# Preferências do jogador que valem para o jogo todo (não só para uma partida): tamanho do texto e tela cheia.

import config
from motor import salvamento


class Preferencias:
    def __init__(self):
        self.tamanho_texto = "normal"   # "normal" ou "grande" (veja config.ESCALAS_DE_TEXTO)
        self.tela_cheia = False

    def escala_texto(self):
        """Quanto multiplicar o tamanho de todo texto (1.0 no normal, maior no grande)."""
        return config.ESCALAS_DE_TEXTO.get(self.tamanho_texto, 1.0)

    def salvar(self):
        salvamento.salvar("preferencias", {
            "tamanho_texto": self.tamanho_texto,
            "tela_cheia": self.tela_cheia,
        })

    def carregar(self):
        dados = salvamento.carregar("preferencias")
        if not dados:
            return
        if dados.get("tamanho_texto") in config.ESCALAS_DE_TEXTO:
            self.tamanho_texto = dados["tamanho_texto"]
        self.tela_cheia = bool(dados.get("tela_cheia", False))


# Uma só cópia das preferências para o jogo todo. Qualquer parte do código
# lê daqui (ex.: preferencias.atual.escala_texto()).
atual = Preferencias()
