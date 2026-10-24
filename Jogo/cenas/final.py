# O final da partida: três telas, uma depois da outra (clique, Espaço ou "Continuar"):
# 1) a cena: o que aconteceu com a aldeia; 2) o povo real e o fato; 3) a fonte, com a posição
# do final na fila ("Final 5/8") e a chance dele (dados/finais.py).
# Depois, "Voltar ao menu". Qual final é: jogo.estado.final (veja motor/finais.py).
#
# Ler de novo (tela "Finais" do menu): com jogo.final_revendo = id, mostra esse final sem mexer
# na partida, e o último botão volta para a lista.

import pygame

import config
from dados.finais import TELA_FINAL
from motor import efeitos, finais, progresso, ui
from motor.cena import Cena, desenhar_cenario

TECLAS_AVANCAR = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)
# O texto fica numa coluna à direita, para a imagem do final aparecer à esquerda.
CENTRO_COLUNA = 1180        # o meio da coluna (x)
LARGURA_TEXTO = 640
Y_TEXTO = 450               # o meio do texto (y)
TAMANHO_TEXTO = 27
ESCURECER = 150             # o quanto a imagem escurece inteira (0 a 255), no final sem imagem própria
ESCURECER_COM_FUNDO = 35    # no final com imagem própria: quase nada
PAINEL = (0, 0, 0, 110)     # o painel atrás da coluna: preto quase transparente
MARGEM_PAINEL = 28
ESPACO_CHANCE = 70   # da fonte até a linha "Final 5/8" (e, embaixo dela, a chance)


def porcentagem(valor):
    """12.7 -> "12,7%"; 100 -> "100%"; 0 -> "menos de 1%" (não aconteceu na simulação, mas
    aconteceu com quem está vendo a tela)."""
    if valor == 0:
        return "menos de 1%"
    texto = ("%.1f" % valor).rstrip("0").rstrip(".")
    return texto.replace(".", ",") + "%"


class Final(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.tratamento = efeitos.Tratamento()
        self.tempo = 0.0
        self.revendo = getattr(jogo, "final_revendo", None)
        jogo.final_revendo = None
        self.final = finais.por_id(self.revendo or jogo.estado.final)
        de_teste = getattr(jogo, "final_de_teste", False)
        jogo.final_de_teste = False
        if not self.revendo:
            if not de_teste:   # a noite de teste (motor/teste.py) não troca a partida guardada
                progresso.salvar("final", jogo.estado.para_dicionario())
            finais.marcar_visto(self.final["id"])
        # Cada tela: (título, texto).
        self.telas = [
            (self.final["nome"], finais.texto_da_cena(self.final, None if self.revendo else jogo.estado)),
            (self.final["povo"], TELA_FINAL["povo"] % self.final["povo"] + "\n\n" + self.final["fato"]),
            (TELA_FINAL["fonte"], self.final["fonte"]),
        ]
        self.linhas_chance = self._linhas_chance()
        self.indice = 0
        self.botao = ui.Botao(TELA_FINAL["seguir"], (CENTRO_COLUNA, 830), largura_minima=300)
        self._mostrar()

    def _linhas_chance(self):
        """"Final 5/8" e as chances, para a tela da fonte."""
        linhas = [TELA_FINAL["numero"] % finais.numero(self.final["id"])]
        chances = [TELA_FINAL["chance_acaso"] % porcentagem(self.final["chance_acaso"])]
        if self.final.get("chance_tentando") is not None:
            chances.append(TELA_FINAL["chance_tentando"] % porcentagem(self.final["chance_tentando"]))
        return linhas + chances

    def _ultima(self):
        return self.indice == len(self.telas) - 1

    def _mostrar(self):
        _, texto = self.telas[self.indice]
        self.caixa = ui.CaixaTexto(texto, LARGURA_TEXTO, (CENTRO_COLUNA, Y_TEXTO), ancora="centro",
                                   tamanho=TAMANHO_TEXTO, alinhamento="centro", max_linhas=12,
                                   fundo=False)
        self.caixa.comecar_digitacao()
        if not self._ultima():
            self.botao.texto = TELA_FINAL["seguir"]
        else:
            self.botao.texto = TELA_FINAL["voltar_finais"] if self.revendo else TELA_FINAL["menu"]

    def avancar(self):
        if not self.caixa.terminou():
            self.caixa.completar()
        elif not self._ultima():
            self.indice += 1
            self._mostrar()
        else:
            self.jogo.ir_para("finais" if self.revendo else "menu")

    def tratar_evento(self, evento):
        if self.botao.clicado(evento):
            self.avancar()
        elif evento.type == pygame.KEYDOWN and evento.key in TECLAS_AVANCAR:
            self.avancar()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE and self.revendo:
            self.jogo.ir_para("finais")

    def atualizar(self, dt):
        super().atualizar(dt)
        self.tempo += dt
        self.caixa.atualizar(dt)
        self.botao.atualizar(self.jogo.mouse)

    def desenhar_cena(self, tela):
        # Final com imagem própria aparece com as cores do desenho (sem o filtro da noite).
        filtro = None if "fundo" in self.final else "noite"
        desenhar_cenario(tela, self.final.get("fundo", TELA_FINAL["fundo"]), filtro, self.tempo)
        # Final com imagem própria (o veado do Anhangá) escurece menos, para ela aparecer.
        efeitos.escurecer(tela, ESCURECER_COM_FUNDO if "fundo" in self.final else ESCURECER)

    def desenhar_interface(self, tela):
        titulo, _ = self.telas[self.indice]
        self.caixa.numero_de_linhas()   # garante o layout (o tamanho do texto pode ter mudado)
        y_titulo = self.caixa.rect.top - 50
        # "Final 5/8" e as chances, embaixo da fonte (só na última tela, com o texto inteiro).
        chance = self._ultima() and self.caixa.terminou()
        fim = self.caixa.rect.bottom + (ESPACO_CHANCE + 46 * (len(self.linhas_chance) - 1) if chance else 0)
        # O painel quase transparente atrás da coluna inteira (título, texto e chances).
        painel = pygame.Rect(0, 0, LARGURA_TEXTO + 2 * MARGEM_PAINEL, 0)
        painel.top = y_titulo - 30 - MARGEM_PAINEL // 2
        painel.height = fim + 20 - painel.top
        painel.centerx = CENTRO_COLUNA
        ui.painel_arredondado(tela, painel, PAINEL)
        ui.texto_simples(tela, titulo, (CENTRO_COLUNA, y_titulo),
                         config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito")
        self.caixa.desenhar(tela)
        if chance:
            numero, *chances = self.linhas_chance
            y = self.caixa.rect.bottom + ESPACO_CHANCE
            ui.texto_simples(tela, numero, (CENTRO_COLUNA, y), config.TAMANHO_SUBTITULO,
                             nome_fonte="serif_negrito")
            for linha in chances:
                y += 46
                ui.texto_simples(tela, linha, (CENTRO_COLUNA, y), config.TAMANHO_PEQUENO,
                                 cor=config.TABATINGA)
        self.botao.desenhar(tela)
