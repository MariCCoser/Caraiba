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
LARGURA_TEXTO = 1150
ESCURECER = 150             # o quanto o fundo escurece atrás do texto (0 a 255)
ESCURECER_COM_FUNDO = 80
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
        if not self.revendo:
            progresso.salvar("final", jogo.estado.para_dicionario())
            finais.marcar_visto(self.final["id"])
        # Cada tela: (título, texto).
        self.telas = [
            (self.final["nome"], self.final["cena"]),
            (self.final["povo"], TELA_FINAL["povo"] % self.final["povo"] + "\n\n" + self.final["fato"]),
            (TELA_FINAL["fonte"], self.final["fonte"]),
        ]
        self.linhas_chance = self._linhas_chance()
        self.indice = 0
        self.botao = ui.Botao(TELA_FINAL["seguir"], (800, 830), largura_minima=300)
        self._mostrar()

    def _linhas_chance(self):
        """"Final 5/8" e as chances, para a tela da fonte."""
        linhas = [TELA_FINAL["numero"] % finais.numero(self.final["id"])]
        chances = [TELA_FINAL["chance_acaso"] % porcentagem(self.final["chance_acaso"])]
        if self.final.get("chance_tentando") is not None:
            chances.append(TELA_FINAL["chance_tentando"] % porcentagem(self.final["chance_tentando"]))
        return linhas + [" · ".join(chances)]

    def _ultima(self):
        return self.indice == len(self.telas) - 1

    def _mostrar(self):
        _, texto = self.telas[self.indice]
        self.caixa = ui.CaixaTexto(texto, LARGURA_TEXTO, (800, 470), ancora="centro",
                                   tamanho=30, alinhamento="centro", max_linhas=10)
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
        desenhar_cenario(tela, self.final.get("fundo", TELA_FINAL["fundo"]), "noite", self.tempo)
        # Final com imagem própria (o veado do Anhangá) escurece menos, para ela aparecer.
        efeitos.escurecer(tela, ESCURECER_COM_FUNDO if "fundo" in self.final else ESCURECER)

    def desenhar_interface(self, tela):
        titulo, _ = self.telas[self.indice]
        self.caixa.desenhar(tela)
        ui.texto_simples(tela, titulo, (800, self.caixa.rect.top - 60),
                         config.TAMANHO_SUBTITULO + 8, nome_fonte="serif_negrito")
        if self._ultima() and self.caixa.terminou():
            numero, chance = self.linhas_chance
            y = self.caixa.rect.bottom + ESPACO_CHANCE
            ui.texto_simples(tela, numero, (800, y), config.TAMANHO_SUBTITULO,
                             nome_fonte="serif_negrito")
            ui.texto_simples(tela, chance, (800, y + 46), config.TAMANHO_PEQUENO,
                             cor=config.BARRO)
        self.botao.desenhar(tela)
