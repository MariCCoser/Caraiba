# Caraíba: Dez Dias, Dez Fogueiras

Jogo educativo de História sobre a epidemia de 1562-63 no litoral brasileiro, feito em **Python + pygame**.

> Por volta de 1562, numa pequena aldeia entre a mata e o rio, restam só você e o pajé. O cacique foi para a mata e deixou a entrada sob a sua guarda. Gente chega pela trilha todos os dias: uns doentes, outros sãos, alguns sem saber. De dia, o Irmão Aleixo, um jesuíta, dá a leitura dele de cada visitante. De noite, na fogueira, o pajé conta o que sonhou. Em quem você acredita?

Inspirado em *No, I'm Not a Human*.

## Sobre o jogo

Durante **10 dias**, o jogador guarda a entrada da aldeia. Cada dia tem dois momentos:

1. **Dia, na entrada**: alguém chega pela trilha e pede para entrar. Nos dias 3, 6 e 9, o Irmão Aleixo, um jesuíta, vem pedir gente para levar à vila. Entre uma visita e outra, dá para andar pela aldeia e conversar nas ocas.
2. **Noite, na fogueira**: o pajé conta o que sonhou e risca o sinal na tábua de barro. Com poucos olhares (a energia da noite), você examina o rosto de quem entrou (olhos, orelhas, boca e pescoço), conversa e decide: deixar dormir na oca, levar ao tapiri (o abrigo isolado, onde o mal não passa e quem é amaldiçoado sai curado) ou matar.

A doença passa só dentro da oca, de noite. Os sinais seguem as fases reais da varíola e do sarampo, e os nomes das doenças nunca aparecem na tela: para a aldeia, é uma maldição.

### Os dez finais

Cada final mostra um povo real que seguiu um caminho parecido com o do jogador e o que aconteceu com ele depois. A ordem é a da fila: vale o primeiro que bater.

| Final | Povo |
|---|---|
| Guerra Justa | Caeté |
| A Troca | Tupiniquim |
| A Loucura | Tupinambá (Santidade de Jaguaripe) |
| A Água do Batismo | Caeté |
| Rio Acima | Aimoré, hoje Krenak |
| Anhangá | Tremembé |
| O Tapiri | Korubo |
| A Honra | Tupinambá |
| Ferida | Potiguara |
| O Vazio | Goitacá |

As condições de cada um estão em [`Textos/Caraíba — Os Finais.pdf`](Textos/Cara%C3%ADba%20%E2%80%94%20Os%20Finais.pdf).

## Como rodar

> O jogo está em desenvolvimento. As instruções completas estarão em [`Jogo/README.md`](Jogo/README.md).

Requisitos: Python 3.12 ou mais recente.

```bash
cd Jogo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Estrutura do repositório

```
Caraiba/
├── Jogo/          Código do jogo (pygame); instruções em Jogo/README.md
├── Arte/          Artes originais do grupo (o jogo usa as cópias leves em Jogo/assets/)
│   ├── Ar_livre/          Cenários ao ar livre e fundos dos finais
│   ├── Ocas/              O dentro das ocas e do tapiri
│   ├── Doenças/           Os detalhes do exame (olhos, boca, orelha, pescoço)
│   ├── personagens_png/   Personagens em pé
│   └── Personagens_sentados_png/  Personagens sentados na fogueira
├── Pesquisa/      Pesquisa histórica (doenças, epidemia, povos originários)
├── Textos/        Documentos de design: história, noites, finais, sinais e conversas
├── Documentos/    Proposta original e requisitos do projeto
└── .claude/agents/ Agentes de IA usados no desenvolvimento
```

## Paleta

| Nome | Cor | Uso |
|---|---|---|
| Noite | `#0F0B09` | Fundo, sombra mais profunda |
| Terra | `#241A14` | Chão, cabelo, sombra na pele |
| Fumaça | `#5A4332` | Meio-tom, pele na sombra |
| Barro | `#9C6B45` | Pele iluminada pelo fogo |
| Tabatinga | `#E8DCC8` | Pintura corporal, brilho, texto |
| Urucum | `#C14A24` | O fogo e a aldeia: o que é de dentro |
| Genipapo | `#2E4A52` | Rio, vila, padre: o que é de fora |
| Ictérica | `#C9A227` | Só doença |

## Equipe

Projeto semestral de História, Prof. Felipe Asbahr Pedoneze, turma 2º DSN.

- Marina Calchi Coser
- Júlia Chiarotto Filippini
- Laura Cristina Buosi
- Emanuelle Bonai Rodrigues
- Júlia Dafny da Silva
- Nycollas Eduardo de Souza Sena

## Aviso

Este é um trabalho escolar com finalidade educativa. Ele trata de epidemias, morte e violência colonial contra povos indígenas, e procura retratar esses povos com respeito, como sujeitos históricos. As fontes usadas estão na pasta `Pesquisa/` e nas telas de fato do jogo.
