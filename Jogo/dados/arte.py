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
    "oca1": "cenarios/cenario-oca1.jpg",           # por dentro da oca 1 (Yorixiriamori), dia e noite
    "oca2_dia": "cenarios/cenario-oca2-dia.jpg",   # por dentro da oca 2 (Yebá Bëló), de dia
    "oca2_noite": "cenarios/cenario-oca2-noite.jpg",  # e de noite
    "oca3_dia": "cenarios/cenario-oca3-dia.jpg",   # por dentro da oca 3 (Wanadi), de dia
    "oca3_noite": "cenarios/cenario-oca3-noite.jpg",  # e de noite
    "tapiri": "cenarios/cenario-tapiri.jpg",       # por dentro do tapiri, dia e noite
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

    # Sentados (a fogueira, de noite): o corpo inteiro, do topo da cabeça ao chão, 560 de altura.
    "yara_sentada": "personagens/sentados/yara.png",
    "mbae_sentado": "personagens/sentados/mbae.png",
    "paje_sentado": "personagens/sentados/paje.png",
    "tamandare_sentado": "personagens/sentados/tamandare.png",
    "krenan_sentado": "personagens/sentados/krenan.png",
    "iande_sentada": "personagens/sentados/iande.png",
    "araci_sentada": "personagens/sentados/araci.png",
    "potira_sentada": "personagens/sentados/potira.png",
}

# Quem é de fora, pelo nome, e o apelido da arte em pé (em PERSONAGENS). Usado quando o Irmão
# Aleixo leva alguém: a pessoa fica atrás dele, em pé, até os dois irem embora.
EM_PE = {
    "Yara": "yara",
    "Mbaé": "mbae",
    "Potira": "potira",
    "Tamandaré-mirim": "tamandare",
    "Iandé": "iande",
    "Krenan": "krenan",
    "Araci": "araci",
}

# Detalhes do exame (Arte/Doenças/): o olho de perto, em cores, à direita da tela.
DETALHES = {
    "olho_yara": "detalhes/olho-yara.png",          # vermelho da fumaça (noites 1 e 2)
    "olho_mbae": "detalhes/olho-mbae.png",          # até o 3º dia na oca
    "olho_potira": "detalhes/olho-potira.png",
    "olho_tamandare": "detalhes/olho-tamandare.png",
    "olho_iande": "detalhes/olho-iande.png",
    "olho_iande_doente": "detalhes/olho-iande-doente.png",
    "olho_krenan": "detalhes/olho-krenan.png",
    "olho_krenan_doente": "detalhes/olho-krenan-doente.png",
}

# Onde fica o fogo em cada cenário (x, y na tela 1600x900).
# Usado para o brilho que pulsa em volta da fogueira. Cenário sem fogo: não coloque aqui.
CENTRO_DO_FOGO = {
    "fogueira_longe": (880, 540),
    "fogueira_perto": (830, 560),
}
