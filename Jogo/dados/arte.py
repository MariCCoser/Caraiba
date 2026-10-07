# Lista das imagens do jogo: apelido usado no código -> arquivo dentro de Jogo/assets/.
#
# Chegou arte nova? 1) converta com ferramentas/converter_arte.py;
# 2) coloque aqui o apelido e o arquivo. Se o arquivo ainda não existir,
# o jogo desenha um "provisório" com o nome escrito e continua funcionando.

CENARIOS = {
    "aldeia": "cenarios/cenario-aldeia.jpg",
    "fogueira_longe": "cenarios/cenario-fogueira-longe.jpg",
    "fogueira_perto": "cenarios/cenario-fogueira-perto.jpg",
}

# Personagens (700 x 1500, PNG com fundo transparente). Ainda não usados.
PERSONAGENS = {
}

# Onde fica o fogo em cada cenário (x, y na tela 1600x900).
# Usado para o brilho que pulsa em volta da fogueira. Cenário sem fogo: não coloque aqui.
CENTRO_DO_FOGO = {
    "fogueira_longe": (880, 540),
    "fogueira_perto": (830, 560),
}
