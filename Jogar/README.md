# ▶ Jogar Caraíba

## Jogue no navegador: **<https://mariccoser.github.io/Caraiba/>**

Não precisa baixar nem instalar nada. Funciona no computador, no Chrome, Edge ou Firefox.

- **A primeira vez demora um pouco para abrir.** O navegador baixa o Python e o jogo (algumas dezenas de MB) antes de mostrar o menu. Nas vezes seguintes, costuma abrir mais rápido.
- **Clique na tela** quando aparecer o aviso para começar: o som só toca depois do primeiro clique (regra dos navegadores).
- **Tela cheia:** em Opções, "Tela cheia" → "Ligada". Para sair, aperte Esc.
- **A partida fica guardada** no próprio navegador: para continuar, abra o mesmo link no mesmo navegador e clique em "Continuar". Numa aba anônima, ela se perde ao fechar.

## O que tem nesta pasta

`navegador/` é o jogo pronto para o navegador (o mesmo que vai para o itch.io). É ele que aparece no link acima. Não precisa abrir esses arquivos: o `index.html` só funciona servido pela internet, não clicando duas vezes nele.

## Para o grupo: atualizar o jogo daqui

Depois de gerar o zip do itch.io (veja `Jogo/README.md`, seção "Jogar no navegador"), copie os três arquivos de `.tmp/web/caraiba/build/web/` (`index.html`, `favicon.png` e `caraiba.apk`) para `Jogar/navegador/` e mande para o GitHub. O link se atualiza sozinho em um ou dois minutos (`.github/workflows/jogar.yml`).
