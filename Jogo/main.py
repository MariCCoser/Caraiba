# Ponto de partida do jogo Caraíba. Rode com:  python main.py
#
# O laço principal é "async" para o jogo também rodar no navegador (pygbag):
# a cada quadro devolvemos o controle ao navegador com "await asyncio.sleep(0)".
# Por isso NUNCA use input(), time.sleep() ou laços que esperam algo sem fim.

import asyncio

import pygame

import config
from motor.jogo import Jogo


async def main():
    jogo = Jogo()
    while jogo.rodando:
        dt = jogo.relogio.tick(config.FPS) / 1000  # segundos desde o último quadro
        jogo.passo(pygame.event.get(), dt)
        await asyncio.sleep(0)
    jogo.encerrar()


asyncio.run(main())
