# Todos os textos do menu, das opções e da introdução. Edite à vontade: aqui não há lógica.
#
# Dicas para editar:
# - Mantenha as aspas "..." em volta de cada texto e a vírgula no fim da linha.
# - Palavras entre [colchetes] aparecem em âmbar e sublinhadas (palavra marcada).
# - Cada cartão da introdução deve ter no máximo umas 3 linhas na tela.
# - "fundo" é o apelido de um cenário (veja dados/arte.py).
# - "filtro" é "noite" (âmbar, luz de fogo) ou "dia" (frio e sem cor).

# As regras do jogo, em poucas frases. Aparecem no último cartão da introdução e no
# botão "Como se joga" das Opções (o mesmo texto nos dois lugares).
# O que é o tapiri, o que é matar e onde a maldição passa ficam de fora de propósito:
# o jogador descobre conversando com o pajé.
REGRAS = ("• [De dia], alguém chega à entrada. Converse e decida se a pessoa entra.\n"
          "• Antes da noite, o [pajé] diz o sinal da maldição. Será que ele sempre acerta?\n"
          "• Os sinais ficam riscados na [tábua de barro], no canto de cima da tela.\n"
          "• [À noite], na fogueira, examine quem está dentro. Cada olhar gasta energia.\n"
          "• Depois: deixar na [oca], levar ao [tapiri] ou [matar].\n"
          "• Uma [brasa] acima da cabeça: alguém com quem você ainda não conversou.\n"
          "• Sem mouse: [setas] ou Tab escolhem, [Enter] confirma, T abre a tábua, Esc volta.")

MENU = {
    "titulo": "CARAÍBA",
    "subtitulo": "Dez Dias, Dez Fogueiras",
    # Frase do título da Proposta, menor, embaixo do subtítulo.
    "chamada": "A entrada da aldeia, a maldição e quem decide quem entra.",
    "continuar": "Continuar",
    "comecar": "Começar",
    "tutorial": "Como se joga",
    "finais": "Finais",   # só aparece depois do primeiro final visto
    "opcoes": "Opções",
    "sair": "Sair",
    "rodape": "Projeto de História · 2º DSN",
    "fundo": "fogueira_longe",
}

OPCOES = {
    "titulo": "Opções",
    "tamanho_texto": "Tamanho do texto",
    "normal": "Normal",
    "grande": "Grande",
    "tela_cheia": "Tela cheia (atalho: F11)",
    "ligada": "Ligada",
    "desligada": "Desligada",
    "tela_cheia_navegador": "Tela cheia (Esc para sair)",
    "som": "Som",
    "som_ligado": "Ligado",
    "som_desligado": "Desligado",
    "exemplo": "Exemplo de fala: as palavras [marcadas] merecem atenção. "
               "Elas mostram o que a pessoa diz e você não tem como [verificar].",
    "voltar": "Voltar",
}

INTRODUCAO = {
    "pular": "Pular",
    "continuar": "Clique ou aperte Espaço para continuar",
    # A ordem segue a Proposta (seção "O jogo abre com..."): aviso de conteúdo,
    # a explicação do nome Caraíba, onde o jogador está e, por último, as regras.
    #
    # Campos de cada cartão:
    #   "texto"   obrigatório. "\n" força uma quebra de linha.
    #   "fundo"   apelido do cenário. Sem "fundo": tela preta, sem filtros.
    #   "filtro"  "noite" ou "dia" (padrão: "noite").
    #   "titulo"  opcional. Cartão com título fica no meio da tela, com o título em cima.
    #   "largura", "tamanho", "max_linhas", "alinhamento": opcionais, para cartões maiores.
    "cartoes": [
        {
            "titulo": "Aviso de conteúdo",
            "texto": "Este jogo fala de epidemias, doença e morte entre os povos indígenas "
                     "do litoral do Brasil no século XVI. "
                     "Os povos citados existiram e [têm descendentes vivos].",
            "largura": 1300,
            "alinhamento": "centro",
        },
        {
            "texto": "Em tupi, [caraíba] era o nome dos grandes pajés e profetas, "
                     "os que andavam de aldeia em aldeia.",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "Os missionários usaram a mesma palavra para dizer “santo”. "
                     "Depois, ela passou a nomear o [homem branco].",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "A mesma palavra servia para o [profeta] e para o [invasor].",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "Litoral do Brasil, por volta de 1562.",
            "fundo": "aldeia",
            "filtro": "dia",
        },
        {
            "texto": "Um dia, no horizonte, você vê eles vindo junto ao [deus sol].",
            "fundo": "aldeia",
            "filtro": "dia",
        },
        {
            "texto": "Depois de chegarem, uma [maldição] se iniciou.",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "Alguns de nós, que não gostaram muito dos novos escolhidos, "
                     "começaram a [apodrecer de dentro para fora], igual às lendas…",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "Vi muitos amigos serem expulsos por pensarem como os [amaldiçoados], "
                     "restando o cacique, o pajé e eu.",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "Mas o cacique está certo de tudo. Afinal, ele é o mais próximo dos deuses; "
                     "não devemos questioná-lo.",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "Ele precisou ir à mata e deixou sob meu comando a [entrada da aldeia].",
            "fundo": "aldeia",
            "filtro": "noite",
        },
        {
            "texto": "Assim, ele foi, e eu fiquei com meu arco e flecha, guardando quem entraria…",
            "fundo": "aldeia",
            "filtro": "noite",
        },
        {
            "titulo": "Como se joga",
            "texto": REGRAS,
            "fundo": "fogueira_longe",
            "filtro": "noite",
            "largura": 1300,
            "tamanho": 30,
            "max_linhas": 13,   # com o texto grande, as 7 regras ocupam 13 linhas (e cabem)
        },
    ],
}

# Textos fixos da cena do Dia (as falas de cada dia ficam em dados/dias.py).
DIA = {
    "menu": "Menu",
    "decidir": "Decidir",
    "terminar_exame": "Terminar o exame",
    "tapiri_cheio": "Levar ao tapiri · não há lugar",
    "energia": "Energia",
    "tabua": "Tábua de barro",
    "anotado": "Riscado na tábua:",
}

# A tábua de barro: onde ficam riscados os sinais que o pajé contou (ícone no canto de cima).
TABUA = {
    "titulo": "Tábua de barro",
    "subtitulo": "Os sinais que o pajé sonhou",
    "noite": "Noite %d",
    "vazia": "Nada riscado ainda. O pajé conta um sinal ao fim de cada dia.",
    "fechar": "Fechar",
    "dica": "Tábua de barro",
}

# Tela "Como se joga", aberta pelas Opções.
# Modo de teste (config.MODO_TESTE): pular direto para uma noite.
TESTE = {
    "menu": "Testar uma noite",
    "titulo": "Testar uma noite",
    "aviso": "Todos que chegam até essa noite estão na aldeia. A partida guardada só muda se você seguir jogando depois.",
    "noite": "Noite %d",
    "voltar": "Voltar",
    "fundo": "fogueira_longe",
}

TUTORIAL = {
    "titulo": "Como se joga",
    "texto": REGRAS,
    "fundo": "fogueira_longe",
    "voltar": "Voltar",
}
