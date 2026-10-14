# O Estado guarda todas as variáveis de uma partida (as do documento de design).
#
# As escolhas do Dia (dados/dias.py) mudam estas variáveis pelo nome,
# com "efeitos": {"memoria": 1} soma 1 em memoria.

import random


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
        self.tapiri_usos = 0           # doentes de verdade levados ao tapiri (final O Tapiri)
        self.viu_anhanga = 0           # noites em que olhou o veado na mata (final Anhangá)
        self.seguiu_paje = 0           # vezes que levou ao tapiri quem o pajé acusou (A Água do Batismo)
        self.inocentes = 0             # dessas vezes, quantas a pessoa era sã

        # Quem de fora entrou na aldeia (nomes), para a noite saber quem examinar
        self.dentro = []
        # Quem o jogador levou ao tapiri (o abrigo isolado): está na aldeia, mas fora da oca
        self.tapiri = []
        # Em que noite cada um entrou no tapiri (a vaga abre depois de TAPIRI["noites"] noites)
        self.tapiri_desde = {}
        # A febre que passou na oca: de quem, quantos pegaram e em que noite (motor/febre.py)
        self.febre = []
        # Moradores que morreram da febre (com nome): não voltam para a fogueira
        self.mortos_febre = []
        # Remédios do Irmão Aleixo guardados (cada um cura a febre de uma pessoa, na fogueira)
        self.remedios = 0
        # Quem foi curado com o remédio: não passa mais a febre nem pega de novo
        self.curados = []
        # Quem o jogador entregou ao Irmão Aleixo (nomes)
        self.entregues_nomes = []
        # As frases da manhã de hoje (quem acordou com febre, quem morreu dela)
        self.manha = []
        # A sorte desta partida: a febre é sorteada com ela (o "Continuar" repete a mesma sorte)
        self.semente = random.randrange(1_000_000_000)
        # Quem morreu pela mão do jogador (o corpo aparece com o nome no dia seguinte)
        self.mortos_nomes = []
        # Em que noite cada um morreu pela mão do jogador (o corpo aparece na manhã seguinte)
        self.mortos_quando = {}
        # Os sinais que o pajé contou, um por noite (a tábua de barro do jogador)
        self.tabua = []
        # O final da partida, quando ela acaba (o "id" de dados/finais.py), ou None
        self.final = None

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
