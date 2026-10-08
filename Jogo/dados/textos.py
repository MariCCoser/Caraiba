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
    # Frase do título da Proposta, menor, embaixo do subtítulo.
    "chamada": "A entrada da aldeia, a febre e quem decide quem entra.",
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
            "texto": "Litoral do Brasil, 1562.",
            "fundo": "aldeia",
            "filtro": "dia",
        },
        {
            "texto": "Uma [febre] que veio com os estrangeiros está esvaziando as aldeias da costa.",
            "fundo": "aldeia",
            "filtro": "dia",
        },
        {
            "texto": "A sua aldeia, entre a mata e o rio, tinha cerca de quarenta pessoas. "
                     "[Restam doze].",
            "fundo": "aldeia",
            "filtro": "dia",
        },
        {
            "texto": "O cacique saiu para a mata. O [pajé] ficou, e é a única autoridade que resta.",
            "fundo": "fogueira_perto",
            "filtro": "noite",
        },
        {
            "texto": "A [entrada da aldeia] ficou sob a sua guarda. "
                     "A cada dia, alguém vai chegar.",
            "fundo": "aldeia",
            "filtro": "noite",
        },
        {
            "titulo": "Como se joga",
            "texto": "• [De dia], alguém chega à entrada. Converse e decida se a pessoa entra.\n"
                     "• Antes da noite, o [pajé] diz qual é o sinal da doença. Ele pode errar.\n"
                     "• [À noite], na fogueira, examine quem está dentro. Cada olhar gasta energia.\n"
                     "• Depois: deixar na [oca], levar ao [tapiri] ou [matar] (exige dois sinais).\n"
                     "• A doença só passa dentro da oca, nas redes. Na fogueira, ninguém pega nada.",
            "fundo": "fogueira_longe",
            "filtro": "noite",
            "largura": 1300,
            "tamanho": 30,
            "max_linhas": 12,
        },
    ],
}

# Textos fixos da cena do Dia (as falas de cada dia ficam em dados/dias.py).
DIA = {
    "menu": "Menu",
    "decidir": "Decidir",
    "caderno": "Caderno",
    "anotado": "Anotado:",
}

# Cena provisória: aparece no fim do Dia 1 até a Noite 1 ficar pronta.
EM_CONSTRUCAO = {
    "titulo": "Noite 1",
    "texto": "Em construção. Aqui começa a noite na fogueira.",
    "voltar": "Voltar ao menu",
    "fundo": "fogueira_perto",
}
