# Converte sons (mp3, wav, m4a, flac...) para .ogg, o formato que funciona no computador e no
# navegador, e deixa os arquivos menores.
#
# Como rodar (de dentro da pasta Jogo, com o ambiente ativado):
#     python -m ferramentas.converter_sons                     (todos os sons de assets/sons)
#     python -m ferramentas.converter_sons Floresta.mp3        (um arquivo, de qualquer pasta)
#     python -m ferramentas.converter_sons Floresta.mp3 40     (só os primeiros 40 segundos)
#
# O .ogg vai para assets/sons, com o mesmo nome. O original sai de assets/sons (para não ir
# junto no zip do itch.io) e fica guardado em Arte/Sons_originais.
# Os sons saem em mono e com qualidade média (QUALIDADE): para efeitos e ambiente, não se nota
# diferença, e o arquivo fica bem menor. Todos saem em 44100 Hz, o mesmo do jogo (motor/jogo.py):
# um som em outra frequência precisa ser convertido na hora de carregar, o que no navegador é
# lento e faz o som falhar. Com um tempo em segundos, o som é cortado e ganha um
# fade de 1 segundo no fim, para o loop não dar um estalo.
#
# Precisa do imageio-ffmpeg (requirements-ferramentas.txt): ele traz o ffmpeg junto.

import os
import shutil
import subprocess
import sys

import imageio_ffmpeg

import config

PASTA_SONS = os.path.join(config.PASTA_JOGO, "assets", "sons")
PASTA_ORIGINAIS = os.path.join(os.path.dirname(config.PASTA_JOGO), "Arte", "Sons_originais")
FORMATOS = (".mp3", ".wav", ".m4a", ".flac", ".aac", ".wma", ".opus")
QUALIDADE = "3"   # 0 a 10 no ogg vorbis; 3 dá uns 80 kbps em mono
FREQUENCIA = 44100


def converter(origem, segundos=None):
    nome = os.path.splitext(os.path.basename(origem))[0] + ".ogg"
    destino = os.path.join(PASTA_SONS, nome)
    comando = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", origem]
    if segundos:
        comando += ["-t", str(segundos), "-af", "afade=t=out:st=%s:d=1" % (segundos - 1)]
    comando += ["-vn", "-ac", "1", "-ar", str(FREQUENCIA), "-c:a", "libvorbis", "-q:a", QUALIDADE, destino]
    subprocess.run(comando, check=True)
    antes, depois = os.path.getsize(origem), os.path.getsize(destino)

    # O original sai de assets/sons e fica guardado fora do jogo.
    if os.path.dirname(os.path.abspath(origem)) == os.path.abspath(PASTA_SONS):
        os.makedirs(PASTA_ORIGINAIS, exist_ok=True)
        shutil.move(origem, os.path.join(PASTA_ORIGINAIS, os.path.basename(origem)))
    print("%-28s %7.0f KB -> %6.0f KB  (%s)" % (os.path.basename(origem), antes / 1024,
                                                 depois / 1024, nome))


def main():
    argumentos = sys.argv[1:]
    if argumentos:
        segundos = int(argumentos[1]) if len(argumentos) > 1 else None
        converter(argumentos[0], segundos)
        return
    arquivos = [os.path.join(PASTA_SONS, nome) for nome in sorted(os.listdir(PASTA_SONS))
                if nome.lower().endswith(FORMATOS)]
    if not arquivos:
        print("Nenhum som para converter em", PASTA_SONS)
    for arquivo in arquivos:
        converter(arquivo)


if __name__ == "__main__":
    main()
