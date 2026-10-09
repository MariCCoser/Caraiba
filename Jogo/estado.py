# O Estado guarda todas as variáveis de uma partida (as do documento de design).
#
# As escolhas do Dia (dados/dias.py) mudam estas variáveis pelo nome,
# com "efeitos": {"memoria": 1} soma 1 em memoria.


class Estado:
    def __init__(self):
        # Em que dia da história estamos (1 a 10)
        self.dia = 1

        # Variáveis da tabela "As variáveis" do documento de design
        self.vivos = 12                # pessoas vivas na aldeia (a Proposta: eram quarenta, restam doze)
        self.mortos = 0                # doença sob o seu teto + mortos por sua mão + mortos na trilha
        self.mortos_por_sua_mao = 0    # quem você matou, doente ou não
        self.entregues = 0             # pessoas entregues a Aleixo numa oferta
        self.proximidade_vila = 0      # machado, remédio aceito, entregas, doente mandado seguir de dia
        self.rio_acima = 0             # pessoas mandadas para a cabeceira
        self.memoria = 0               # histórias ouvidas
        self.recusas_aleixo = 0        # vezes que você recusou uma oferta
        self.pistas = 0                # caderno de Aleixo, colar, notícia (máximo 3)
        self.sanidade = 10             # não decide final; muda a tela (tremor, grão, tábua)

        # Quem de fora entrou na aldeia (nomes), para a noite saber quem examinar
        self.dentro = []
        # Os sinais que o pajé contou, um por noite (a tábua de barro do jogador)
        self.tabua = []

    def para_dicionario(self):
        """Copia as variáveis num dicionário simples (para salvar a partida)."""
        return dict(self.__dict__)

    def carregar_dicionario(self, dados):
        """Recoloca no Estado as variáveis de um dicionário salvo antes.

        Só aceita nomes que o Estado já conhece, para um save antigo ou
        estragado não criar variáveis estranhas.
        """
        for nome, valor in dados.items():
            if nome in self.__dict__:
                setattr(self, nome, valor)
