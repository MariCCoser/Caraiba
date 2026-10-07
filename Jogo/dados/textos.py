# Todos os textos do menu, das opções e da introdução. Edite à vontade: aqui não há lógica.
#
# Dicas para editar:
# - Mantenha as aspas "..." em volta de cada texto e a vírgula no fim da linha.
# - Palavras entre [colchetes] aparecem em âmbar e sublinhadas (palavra marcada).
# - Cada cartão da introdução deve ter no máximo umas 3 linhas na tela.
# - "fundo" é o apelido de um cenário (veja dados/arte.py).
# - "filtro" é "noite" (âmbar, luz de fogo) ou "dia" (frio e sem cor).

MENU = {
    "titulo": "CARAÍBA",
    "subtitulo": "Dez Dias, Dez Fogueiras",
    "comecar": "Começar",
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
    "motivo_navegador": "No navegador, use o botão de tela cheia da página",
    "exemplo": "Exemplo de fala: as palavras [marcadas] merecem atenção. "
               "Elas mostram o que a pessoa diz e você não tem como [verificar].",
    "voltar": "Voltar",
}

INTRODUCAO = {
    "pular": "Pular",
    "continuar": "Clique ou aperte Espaço para continuar",
    # O texto vem da Proposta do grupo (seção "História / introdução"),
    # só com a ortografia e a pontuação corrigidas.
    "cartoes": [
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
    ],
}

# Cena provisória: aparece no fim da introdução até o Dia 1 ficar pronto.
EM_CONSTRUCAO = {
    "titulo": "Dia 1",
    "texto": "Em construção. Aqui começa a manhã na oca.",
    "voltar": "Voltar ao menu",
    "fundo": "aldeia",
}
