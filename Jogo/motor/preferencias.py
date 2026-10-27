# Preferências do jogador que valem para o jogo todo (não só para uma partida): tamanho do texto,
# tela cheia, som, efeitos visuais e a descrição dos sinais.

import config
from motor import salvamento


class Preferencias:
    def __init__(self):
        self.tamanho_texto = "normal"   # "normal" ou "grande" (veja config.ESCALAS_DE_TEXTO)
        self.tela_cheia = False
        self.som = True
        # Efeitos visuais (motor/efeitos.py): desligados, somem o grão, as linhas e o tremor,
        # e a luz da fogueira para de pulsar. Para quem se incomoda com imagem que mexe.
        self.efeitos = True
        # A descrição em palavras embaixo de cada imagem do exame (dados/arte.py, LEGENDAS).
        self.legendas = True

    def escala_texto(self):
        """Quanto multiplicar o tamanho de todo texto (1.0 no normal, maior no grande)."""
        return config.ESCALAS_DE_TEXTO.get(self.tamanho_texto, 1.0)

    def salvar(self):
        salvamento.salvar("preferencias", {
            "tamanho_texto": self.tamanho_texto,
            "tela_cheia": self.tela_cheia,
            "som": self.som,
            "efeitos": self.efeitos,
            "legendas": self.legendas,
        })

    def carregar(self):
        dados = salvamento.carregar("preferencias")
        if not dados:
            return
        if dados.get("tamanho_texto") in config.ESCALAS_DE_TEXTO:
            self.tamanho_texto = dados["tamanho_texto"]
        self.tela_cheia = bool(dados.get("tela_cheia", False))
        self.som = bool(dados.get("som", True))
        self.efeitos = bool(dados.get("efeitos", True))
        self.legendas = bool(dados.get("legendas", True))


# Uma só cópia das preferências para o jogo todo. Qualquer parte do código
# lê daqui (ex.: preferencias.atual.escala_texto()).
atual = Preferencias()
