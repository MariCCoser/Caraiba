# Lista das imagens do jogo: apelido usado no código -> arquivo dentro de Jogo/assets/.
#
# Chegou arte nova? 1) converta com ferramentas/converter_arte.py;
# 2) coloque aqui o apelido e o arquivo. Se o arquivo ainda não existir,
# o jogo desenha um "provisório" com o nome escrito e continua funcionando.

CENARIOS = {
    "aldeia": "cenarios/cenario-aldeia.jpg",
    "fogueira_longe": "cenarios/cenario-fogueira-longe.jpg",
    "fogueira_perto": "cenarios/cenario-fogueira-perto.jpg",
    "fogueira_dia": "cenarios/cenario-fogueira-dia.jpg",   # a mesma, de dia (a manhã depois de uma morte)
    "floresta": "cenarios/cenario-floresta.jpg",   # a trilha na mata, atrás de quem chega
    "oca1": "cenarios/cenario-oca1.jpg",           # por dentro da oca 1 (Yorixiriamori), dia e noite
    "oca2_dia": "cenarios/cenario-oca2-dia.jpg",   # por dentro da oca 2 (Yebá Bëló), de dia
    "oca2_noite": "cenarios/cenario-oca2-noite.jpg",  # e de noite
    "oca3_dia": "cenarios/cenario-oca3-dia.jpg",   # por dentro da oca 3 (Wanadi), de dia
    "oca3_noite": "cenarios/cenario-oca3-noite.jpg",  # e de noite
    "tapiri": "cenarios/cenario-tapiri.jpg",       # por dentro do tapiri, dia e noite
    # O Anhangá: a mata para onde o pajé aponta, na 1ª, 2ª e 3ª vez, e o fundo do final Anhangá.
    "anhanga_um": "cenarios/anhanga-1.jpg",
    "anhanga_dois": "cenarios/anhanga-2.jpg",
    "anhanga_tres": "cenarios/anhanga-3.jpg",
    "anhanga_final": "cenarios/anhanga-final.jpg",
    "batismo_final": "cenarios/final-batismo.jpg",   # o fundo do final A Água do Batismo
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
    "padre": "personagens/padre.png",   # o padre novo da vila (noite 9, A Água do Batismo)

    # Sentados (a fogueira, de noite): o corpo inteiro, do topo da cabeça ao chão, 560 de altura.
    "yara_sentada": "personagens/sentados/yara.png",
    "mbae_sentado": "personagens/sentados/mbae.png",
    "paje_sentado": "personagens/sentados/paje.png",
    "tamandare_sentado": "personagens/sentados/tamandare.png",
    "krenan_sentado": "personagens/sentados/krenan.png",
    "iande_sentada": "personagens/sentados/iande.png",
    "araci_sentada": "personagens/sentados/araci.png",
    "potira_sentada": "personagens/sentados/potira.png",

    # O corpo coberto com a esteira, deitado, no lugar de quem morreu (a mesma altura dos sentados).
    "esteira": "personagens/esteira.png",                          # quem era são
    "esteira_amaldicoado": "personagens/esteira-amaldicoado.png",  # quem era amaldiçoado
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

# Detalhes do exame (Arte/Doenças/): o olho e a boca de perto, em cores.
# Quem mostra cada um e quando: Textos/Caraiba_Sinais_dos_Personagens.md.
DETALHES = {
    "olho_yara": "detalhes/olho-yara.png",                    # da noite 3 em diante, sem febre
    "olho_yara_vermelho": "detalhes/olho-yara-vermelho.png",  # fumaça (noites 1 e 2) ou febre
    "boca_yara": "detalhes/boca-yara.png",
    "boca_yara_doente": "detalhes/boca-yara-doente.png",
    "olho_mbae": "detalhes/olho-mbae.png",                    # até 3 noites na oca
    "olho_mbae_doente": "detalhes/olho-mbae-doente.png",      # depois de 3 noites na oca
    "boca_mbae": "detalhes/boca-mbae.png",                    # (sem uso: Mbaé já chega doente)
    "boca_mbae_doente": "detalhes/boca-mbae-doente.png",
    "olho_potira": "detalhes/olho-potira.png",
    "olho_potira_doente": "detalhes/olho-potira-doente.png",
    "boca_potira": "detalhes/boca-potira.png",
    "boca_potira_doente": "detalhes/boca-potira-doente.png",
    "olho_tamandare": "detalhes/olho-tamandare.png",          # até 3 noites na oca
    "olho_tamandare_doente": "detalhes/olho-tamandare-doente.png",
    "boca_tamandare": "detalhes/boca-tamandare.png",          # (sem uso: já chega doente)
    "boca_tamandare_doente": "detalhes/boca-tamandare-doente.png",
    "olho_iande": "detalhes/olho-iande.png",                  # noites 7 e 8
    "olho_iande_doente": "detalhes/olho-iande-doente.png",    # noites 9 e 10
    "boca_iande": "detalhes/boca-iande.png",
    "boca_iande_doente": "detalhes/boca-iande-doente.png",
    "olho_krenan": "detalhes/olho-krenan.png",                # (sem uso: Krenan não é examinado)
    "olho_krenan_doente": "detalhes/olho-krenan-doente.png",
    "olho_araci_doente": "detalhes/olho-araci-doente.png",
    "boca_araci": "detalhes/boca-araci.png",                  # (sem uso: Araci já chega doente)
    "boca_araci_doente": "detalhes/boca-araci-doente.png",
}

# Onde fica o fogo em cada cenário (x, y na tela 1600x900).
# Usado para o brilho que pulsa em volta da fogueira. Cenário sem fogo: não coloque aqui.
CENTRO_DO_FOGO = {
    "fogueira_longe": (880, 540),
    "fogueira_perto": (830, 560),
}
