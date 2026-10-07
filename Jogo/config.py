# Configurações fixas do jogo: resolução, velocidade, cores da paleta e pastas.
#
# Tudo que é "número mágico" usado em vários lugares fica aqui, com nome,
# para que ninguém precise caçar valores espalhados pelo código.

import os
import sys

# ---------------------------------------------------------------------------
# Tela
# ---------------------------------------------------------------------------

# O jogo é sempre desenhado em 1600x900 (a "resolução lógica") e depois
# esticado para o tamanho da janela, mantendo a proporção 16:9.
# Assim todas as posições no código valem para qualquer monitor.
LARGURA = 1600
ALTURA = 900
TAMANHO_LOGICO = (LARGURA, ALTURA)

FPS = 60
TITULO_JANELA = "Caraíba — Dez Dias, Dez Fogueiras"

# Duração (em segundos) de cada metade do escurecimento entre cenas.
DURACAO_FADE = 0.25

# True quando o jogo roda no navegador (pygbag). Lá não existe "Sair",
# nem arquivos no disco, nem controle da janela.
NO_NAVEGADOR = sys.platform == "emscripten"

# ---------------------------------------------------------------------------
# Paleta (Arte/PALETA E EXEMPLO.docx). Use SEMPRE estes nomes, nunca números soltos.
# ---------------------------------------------------------------------------

# A rampa quente, do mais escuro ao mais claro
NOITE = (0x0F, 0x0B, 0x09)       # fundo de tudo, sombra mais profunda
TERRA = (0x24, 0x1A, 0x14)       # chão, cabelo, sombra na pele
FUMACA = (0x5A, 0x43, 0x32)      # meio-tom, coisas distantes
BARRO = (0x9C, 0x6B, 0x45)       # pele iluminada pelo fogo
TABATINGA = (0xE8, 0xDC, 0xC8)   # pintura branca, brilho, TEXTO

# Os três acentos: cada um significa UMA coisa só no jogo inteiro
URUCUM = (0xC1, 0x4A, 0x24)      # o fogo e a aldeia: o que é de dentro
GENIPAPO = (0x2E, 0x4A, 0x52)    # rio, vila, padre: o que é de fora
ICTERICA = (0xC9, 0xA2, 0x27)    # SÓ DOENÇA. Nunca usar na interface.

# Preto de verdade: a regra da noite é "o que a luz não toca vira preto absoluto".
PRETO = (0, 0, 0)

# Âmbar das palavras marcadas nas falas. Não é cor da paleta: é o tom claro
# da luz do fogo (o mesmo do filtro da noite). Escolhido bem diferente da
# Ictérica (mais laranja, mais claro) para o amarelo continuar sendo só doença,
# e com contraste alto sobre o preto para ser legível.
AMBAR = (0xF0, 0xA8, 0x58)

# Tom usado para "pintar" a cena da noite (preto -> este tom).
TOM_FILTRO_NOITE = (255, 170, 90)
# Tom frio do dia (multiplica a imagem já dessaturada).
TOM_FILTRO_DIA = (200, 214, 222)

# ---------------------------------------------------------------------------
# Texto
# ---------------------------------------------------------------------------

# Multiplicador do tamanho de todos os textos para cada opção do menu Opções.
ESCALAS_DE_TEXTO = {
    "normal": 1.0,
    "grande": 1.25,
}

# Tamanhos-base (em pixels da tela lógica 1600x900), antes da escala acima.
TAMANHO_TITULO = 150
TAMANHO_SUBTITULO = 40
TAMANHO_FALA = 36
TAMANHO_BOTAO = 34
TAMANHO_PEQUENO = 24

# Letras por segundo no efeito de "texto sendo escrito".
LETRAS_POR_SEGUNDO = 45

# ---------------------------------------------------------------------------
# Pastas
# ---------------------------------------------------------------------------

PASTA_JOGO = os.path.dirname(os.path.abspath(__file__))
PASTA_ASSETS = os.path.join(PASTA_JOGO, "assets")
PASTA_FONTES = os.path.join(PASTA_ASSETS, "fontes")
PASTA_SAVES = os.path.join(PASTA_JOGO, "saves")

# Arquivos de fonte. Sempre carregados do arquivo (no navegador não há fontes do sistema).
FONTES = {
    "serif": "dejavu-serif.ttf",
    "serif_negrito": "dejavu-serif-negrito.ttf",
    "serif_italico": "dejavu-serif-italico.ttf",
    "sans": "dejavu-sans.ttf",
    "mono": "dejavu-sans-mono.ttf",
}
