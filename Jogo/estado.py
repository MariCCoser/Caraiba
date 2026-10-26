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
        self.vivos = 0                 # quem é de fora e está vivo na aldeia (além do jogador e do pajé)
        self.mortos = 0                # doença sob o seu teto + mortos por sua mão + mortos na trilha
        self.mortos_por_sua_mao = 0    # quem você matou, doente ou não
        self.mortos_saos_por_sua_mao = 0   # desses, quem não era amaldiçoado (fecha A Honra)
        self.entregues = 0             # pessoas entregues a Aleixo numa oferta
        self.levados = 0               # pessoas que o Irmão Aleixo levou mesmo negando (sorteadas)
        self.proximidade_vila = 0      # machado, entregas, doente mandado seguir de dia
        self.rio_acima = 0             # pessoas mandadas para a cabeceira (com Krenan)
        self.krenan_volta = 0          # 1 se Krenan volta na noite 10 (levou alguém na noite 8)
        self.subiu_o_rio = 0           # 1 se, na noite 10, a aldeia inteira subiu o rio com Krenan
        self.memoria = 0               # histórias ouvidas
        self.recusas_aleixo = 0        # vezes que você recusou uma oferta
        self.perguntou_levados = 0     # visitas em que perguntou ao Aleixo sobre quem ele levou
        self.pistas = 0                # caderno de Aleixo, colar, notícia (máximo 3)
        self.sanidade = 10             # não decide final; muda a tela (tremor, grão, tábua)
        self.tapiri_usos = 0           # amaldiçoados levados ao tapiri (final O Tapiri)
        self.tapiri_saos = 0           # gente sã levada ao tapiri (fecha o final O Tapiri)
        self.viu_anhanga = 0           # noites em que olhou o veado na mata (final Anhangá)
        self.seguiu_paje = 0           # vezes que levou ao tapiri quem o pajé acusou
        self.converteu = 0             # 1 se aceitou o batismo do padre novo (A Água do Batismo)
        self.padre_entrou = 0          # 1 se deixou o padre novo entrar no dia 9 (A Água do Batismo)
        self.aleixo_morto = 0          # 1 se atirou no Irmão Aleixo na trilha, no dia 9 (Guerra Justa)
        self.inocentes = 0             # dessas vezes, quantas a pessoa era sã
        self.machado = 0               # 1 se aceitou o machado de Yara (+1 energia em toda noite)
        self.pulseira = 0              # 1 se aceitou a pulseira de Iandé (+1 energia das noites 7 a 10)
        self.mandioca = 0              # 1 se comeu a mandioca de Potira (+1 energia das noites 4 a 10)
        self.energia_hoje = 0          # energia a mais só na noite de hoje (negar o Aleixo); zera de manhã

        # Quem de fora entrou na aldeia (nomes), para a noite saber quem examinar
        self.dentro = []
        # Quem o jogador levou ao tapiri (o abrigo isolado): está na aldeia, mas fora da oca
        self.tapiri = []
        # Em que noite cada um entrou no tapiri (a vaga abre depois de TAPIRI["noites"] noites)
        self.tapiri_desde = {}
        # A febre que passou na oca: quem pegou, de quem e em que noite (motor/febre.py)
        self.febre = []
        # Quantas noites cada um de fora dormiu na oca (o olho dos amaldiçoados piora com elas)
        self.noites_na_oca = {}
        # Quem era amaldiçoado e saiu curado do tapiri (completou as noites lá): não passa mais a febre
        self.curados = []
        # As histórias já ouvidas (dados/conversas.py): a memória sobe uma vez por história
        self.historias = []
        # Quantas conversas da noite cada um já teve (dados/historias.py): a próxima fala é a seguinte
        self.conversas_oca = {}
        self.conversas_fogueira = {}
        # Com quem o jogador já conversou (fez uma pergunta), de dia na oca ou de noite na
        # fogueira; a conversa da entrada não conta (A Honra: conhecidos)
        self.conversou = []
        # Quem o jogador chamou para a fogueira sem deixar entrar na aldeia (ex.: Krenan)
        self.convidados = []
        # Quem subiu o rio com Krenan (nomes)
        self.rio_acima_nomes = []
        # Quem de fora foi com o Irmão Aleixo para a vila, entregue ou sorteado (nomes)
        self.entregues_nomes = []
        # As frases da manhã de hoje (quem acordou com febre, quem morreu dela)
        self.manha = []
        # A sorte desta partida: a febre é sorteada com ela (o "Continuar" repete a mesma sorte)
        self.semente = random.randrange(1_000_000_000)
        # Quem morreu pela mão do jogador (o corpo aparece com o nome no dia seguinte)
        self.mortos_nomes = []
        # Desses, quem era são; e quem era são e foi levado ao tapiri (o final Ferida diz o nome)
        self.saos_mortos_nomes = []
        self.tapiri_saos_nomes = []
        # Em que noite cada um morreu pela mão do jogador (o corpo aparece na manhã seguinte)
        self.mortos_quando = {}
        # Os corpos cobertos com a esteira, no lugar onde a pessoa estava (cenas/dia.py, cenas/oca.py):
        # {"nome", "noite" (em que morreu), "onde" ("fogueira", ou o nome da oca, ou "tapiri"),
        #  "posicao", "escala", "espelhar", "amaldicoado" (True: a esteira de amaldiçoado)}
        self.corpos = []
        # Os sinais que o pajé contou (a tábua de barro do jogador) e em que noite cada um
        self.tabua = []
        self.tabua_noites = []
        # O final calculado na manhã do dia 10, antes de Araci chegar (motor/finais.py), ou None
        self.final_calculado = None
        # O final da partida, quando ela acaba (o "id" de dados/finais.py), ou None
        self.final = None

    @property
    def conhecidos(self):
        """Quantas pessoas o jogador conheceu (A Honra): com quem conversou, mais quem foi levado
        (pelo Irmão Aleixo ou por Krenan) antes de dar tempo de conversar."""
        return len(set(self.conversou) | set(self.entregues_nomes) | set(self.rio_acima_nomes))

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
