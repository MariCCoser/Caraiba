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
    # Os fundos das telas de cada final (dados/finais.py, "fundo").
    "batismo_final": "cenarios/final-batismo.jpg",
    "troca_final": "cenarios/final-troca.jpg",
    "loucura_final": "cenarios/final-loucura.jpg",
    "rio_acima_final": "cenarios/final-rio-acima.jpg",
    "honra_final": "cenarios/final-honra.jpg",
    "vazio_final": "cenarios/final-vazio.jpg",
    "tapiri_final": "cenarios/final-tapiri.jpg",
    "guerra_justa_final": "cenarios/final-guerra-justa.jpg",
    "ferida_final": "cenarios/final-ferida.jpg",
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
    "padre_sentado": "personagens/sentados/padre.png",

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
    "olho_yara": "detalhes/olho-yara.jpg",                    # da noite 3 em diante, sem febre
    "olho_yara_vermelho": "detalhes/olho-yara-vermelho.jpg",  # fumaça (noites 1 e 2) ou febre
    "boca_yara": "detalhes/boca-yara.jpg",
    "boca_yara_doente": "detalhes/boca-yara-doente.jpg",
    "olho_mbae": "detalhes/olho-mbae.jpg",                    # até 3 noites na oca
    "olho_mbae_doente": "detalhes/olho-mbae-doente.jpg",      # depois de 3 noites na oca
    "boca_mbae": "detalhes/boca-mbae.jpg",                    # (sem uso: Mbaé já chega doente)
    "boca_mbae_doente": "detalhes/boca-mbae-doente.jpg",
    "olho_potira": "detalhes/olho-potira.jpg",
    "olho_potira_doente": "detalhes/olho-potira-doente.jpg",
    "boca_potira": "detalhes/boca-potira.jpg",
    "boca_potira_doente": "detalhes/boca-potira-doente.jpg",
    "olho_tamandare": "detalhes/olho-tamandare.jpg",          # até 3 noites na oca
    "olho_tamandare_doente": "detalhes/olho-tamandare-doente.jpg",
    "boca_tamandare": "detalhes/boca-tamandare.jpg",          # (sem uso: já chega doente)
    "boca_tamandare_doente": "detalhes/boca-tamandare-doente.jpg",
    "olho_iande": "detalhes/olho-iande.jpg",                  # noites 7 e 8
    "olho_iande_doente": "detalhes/olho-iande-doente.jpg",    # noites 9 e 10
    "boca_iande": "detalhes/boca-iande.jpg",
    "boca_iande_doente": "detalhes/boca-iande-doente.jpg",
    "olho_araci_doente": "detalhes/olho-araci-doente.jpg",
    "boca_araci_doente": "detalhes/boca-araci-doente.jpg",
    # Atrás da orelha e o pescoço: uma imagem saudável para as duas zonas; a doente, uma de cada.
    "orelha_pescoco_yara": "detalhes/orelha-pescoco-yara.jpg",
    "orelha_yara_doente": "detalhes/orelha-yara-doente.jpg",
    "pescoco_yara_doente": "detalhes/pescoco-yara-doente.jpg",
    "orelha_pescoco_mbae": "detalhes/orelha-pescoco-mbae.jpg",                 # até 3 noites na oca
    "orelha_mbae_doente": "detalhes/orelha-mbae-doente.jpg",                   # depois de 3 noites
    "pescoco_mbae_doente": "detalhes/pescoco-mbae-doente.jpg",
    "orelha_pescoco_araci_doente": "detalhes/orelha-pescoco-araci-doente.jpg",
    "orelha_pescoco_potira": "detalhes/orelha-pescoco-potira.jpg",
    "orelha_potira_doente": "detalhes/orelha-potira-doente.jpg",
    "pescoco_potira_doente": "detalhes/pescoco-potira-doente.jpg",
    "orelha_pescoco_tamandare": "detalhes/orelha-pescoco-tamandare.jpg",
    "orelha_tamandare_doente": "detalhes/orelha-tamandare-doente.jpg",
    "pescoco_tamandare_doente": "detalhes/pescoco-tamandare-doente.jpg",
    "orelha_pescoco_iande": "detalhes/orelha-pescoco-iande.jpg",
    "orelha_iande_doente": "detalhes/orelha-iande-doente.jpg",
    "pescoco_iande_doente": "detalhes/pescoco-iande-doente.jpg",
}

# O que cada detalhe mostra, em palavras: aparece numa faixa embaixo da imagem, para quem não
# distingue bem as cores (o vermelho do olho, as manchas) também ver o sinal. Só descreve o que
# está desenhado: quem decide se é doença continua sendo o jogador.
LEGENDAS = {
    "olho_yara": "O branco do olho está limpo.",
    "olho_yara_vermelho": "O branco do olho está vermelho, cheio de veias.",
    "boca_yara": "Lábios e língua lisos, sem feridas.",
    "boca_yara_doente": "Feridas no lábio, na língua e no fundo da boca.",
    "olho_mbae": "O branco do olho está um pouco avermelhado.",
    "olho_mbae_doente": "O olho está vermelho e inchado, cheio de veias.",
    "boca_mbae": "Lábios e língua lisos, sem feridas.",
    "boca_mbae_doente": "Pontos brancos no fundo da boca e uma ferida no lábio.",
    "olho_potira": "O branco do olho está limpo.",
    "olho_potira_doente": "O branco do olho está vermelho, cheio de veias.",
    "boca_potira": "Lábios secos, sem feridas.",
    "boca_potira_doente": "Feridas nos lábios.",
    "olho_tamandare": "O branco do olho está levemente avermelhado.",
    "olho_tamandare_doente": "O olho está muito vermelho, cheio de veias.",
    "boca_tamandare": "Lábios e língua lisos, sem feridas.",
    "boca_tamandare_doente": "Feridas nos lábios e pontos brancos na língua.",
    "olho_iande": "O branco do olho está limpo.",
    "olho_iande_doente": "O canto do olho está vermelho, com veias.",
    "boca_iande": "Lábios e língua lisos, sem feridas.",
    "boca_iande_doente": "Feridas nos lábios e na língua.",
    "olho_araci_doente": "O olho está vermelho e cansado, cheio de veias.",
    "boca_araci_doente": "A língua está coberta de feridas; uma ferida no lábio.",
    "orelha_pescoco_yara": "A pele atrás da orelha e no pescoço está lisa.",
    "orelha_yara_doente": "Manchas vermelhas atrás da orelha.",
    "pescoco_yara_doente": "Manchas vermelhas descendo pelo pescoço.",
    "orelha_pescoco_mbae": "A pele atrás da orelha e no pescoço está lisa.",
    "orelha_mbae_doente": "Manchas vermelhas atrás da orelha.",
    "pescoco_mbae_doente": "Manchas vermelhas descendo pelo pescoço.",
    "orelha_pescoco_araci_doente": "Manchas atrás da orelha e por todo o pescoço.",
    "orelha_pescoco_potira": "A pele atrás da orelha e no pescoço está lisa.",
    "orelha_potira_doente": "Manchas vermelhas atrás da orelha.",
    "pescoco_potira_doente": "Manchas vermelhas descendo pelo pescoço.",
    "orelha_pescoco_tamandare": "A pele atrás da orelha e no pescoço está lisa.",
    "orelha_tamandare_doente": "Manchas vermelhas atrás da orelha.",
    "pescoco_tamandare_doente": "Manchas vermelhas descendo pelo pescoço.",
    "orelha_pescoco_iande": "A pele atrás da orelha e no pescoço está lisa.",
    "orelha_iande_doente": "Manchas vermelhas atrás da orelha.",
    "pescoco_iande_doente": "Manchas vermelhas descendo pelo pescoço.",
}

# Onde fica o fogo em cada cenário (x, y na tela 1600x900).
# Usado para o brilho que pulsa em volta da fogueira. Cenário sem fogo: não coloque aqui.
CENTRO_DO_FOGO = {
    "fogueira_longe": (880, 540),
    "fogueira_perto": (830, 560),
}
