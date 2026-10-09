# Lista das imagens do jogo: apelido usado no código -> arquivo dentro de Jogo/assets/.
#
# Chegou arte nova? 1) converta com ferramentas/converter_arte.py;
# 2) coloque aqui o apelido e o arquivo. Se o arquivo ainda não existir,
# o jogo desenha um "provisório" com o nome escrito e continua funcionando.

CENARIOS = {
    "aldeia": "cenarios/cenario-aldeia.jpg",
    "fogueira_longe": "cenarios/cenario-fogueira-longe.jpg",
    "fogueira_perto": "cenarios/cenario-fogueira-perto.jpg",
    "floresta": "cenarios/cenario-floresta.jpg",   # a trilha na mata, atrás de quem chega
}

# Personagens gerados por ferramentas/converter_arte.py: PNG com fundo transparente,
# todos com o mesmo corte (do topo da cabeça ao meio das coxas, 860 de altura).
PERSONAGENS = {
    "yara": "personagens/yara.png",
    "mbae": "personagens/mbae.png",
    "potira": "personagens/potira.png",
    "tamandare": "personagens/tamandare.png",
    "iande": "personagens/iande.png",
    "krenan": "personagens/krenan.png",
    "araci": "personagens/araci.png",
    "aleixo": "personagens/aleixo.png",
    "paje": "personagens/paje.png",
}

# Onde fica o fogo em cada cenário (x, y na tela 1600x900).
# Usado para o brilho que pulsa em volta da fogueira. Cenário sem fogo: não coloque aqui.
CENTRO_DO_FOGO = {
    "fogueira_longe": (880, 540),
    "fogueira_perto": (830, 560),
}
