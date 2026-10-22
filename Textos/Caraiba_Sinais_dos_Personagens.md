# Caraíba — Os sinais de cada personagem (com e sem a maldição)

Este arquivo diz **o que o jogador vê de perto no exame da noite** (o olho e a boca) para cada
pessoa, com a maldição e sem ela, e **quando** a imagem muda.

- Artes originais: `Arte/Doenças/<pessoa>/`. Cópias do jogo: `Jogo/assets/detalhes/`
  (feitas por `Jogo/ferramentas/converter_arte.py`).
- Onde isso está no jogo: `Jogo/dados/noites.py` (as zonas do exame de cada noite) e
  `Jogo/dados/arte.py` (lista `DETALHES`).
- Os **olhos** e a **boca** têm imagem para todos. **Atrás da orelha** e o **pescoço** têm
  imagem para Yara, Mbaé e Araci (a saudável vale para as duas zonas). Para os outros, e para
  testa, mãos e respiração, o exame ainda descreve em texto.
- **O tapiri cura:** quem era amaldiçoado e completa as 3 noites lá volta com o rosto saudável.

## As regras

1. **Quem chega amaldiçoado** (Mbaé, Tamandaré-mirim, Iandé, Araci) traz a maldição desde o
   primeiro dia. Mas nem todo sinal aparece logo: alguns pioram com as noites.
2. **Quem chega são** (Yara, Potira) tem o rosto normal. Só fica doente se **pegar a febre na
   oca**, dormindo perto de um amaldiçoado.
3. Quem pega a febre e **mostra** acorda com febre no dia seguinte e, nessa noite, o exame já
   mostra o **olho e a boca doentes**. Morre na manhã depois.
4. Quem pega a febre e **não mostra** (metade das vezes, `CHANCE_DE_MOSTRAR` em
   `dados/febre.py`) segue com o rosto **normal** até morrer. O jogador não tem como ver.
5. **"Noites na oca"**: conta só as noites em que a pessoa dormiu na oca (não no tapiri). É com
   elas que o olho de Mbaé e o de Tamandaré-mirim pioram: depois de **3 noites**
   (`NOITES_ATE_O_OLHO_PIORAR` em `dados/noites.py`).

## Pessoa por pessoa

| Pessoa | Chega | Maldição? | Olho | Boca |
|---|---|---|---|---|
| **Yara** | Dia 1 | Não (pode pegar na oca) | Noites 1 e 2: **vermelho** (fumaça, não é doença). Da noite 3 em diante: **normal**. Se pegou a febre e mostra: **vermelho** de novo | **Normal**. Se pegou a febre e mostra: **doente** |
| **Mbaé** | Dia 2 | **Sim** (desde o início) | Até 3 noites na oca: o olho de **até o 3º dia**. Depois: **doente** | **Doente** desde o início (as feridas: sinal da noite 2) |
| **Potira** | Dia 4 | Não (pode pegar na oca) | **Normal** (cansado de sono). Se pegou a febre e mostra: **doente** | **Normal** (lábios secos do frio). Se pegou a febre e mostra: **doente** |
| **Tamandaré-mirim** | Dia 5 | **Sim** (desde o início) | Até 3 noites na oca: **levemente vermelho** (já é sinal). Depois: **doente** | **Doente** desde o início (os pontos brancos: sinal da noite 5) |
| **Iandé** | Dia 7 | **Sim**, mas escondida | Noites 7 e 8: **normal** (parece perfeita). Noites 9 e 10: **doente** | Noites 7 e 8: **normal**. Noites 9 e 10: **doente** |
| **Araci** | Dia 10 | **Sim**, tudo à vista | **Doente** | **Doente** |
| **Krenan** | Noite 8 | — | Não é examinado | Não é examinado |

### As imagens de cada um

| Pessoa | Sem a maldição (são) | Com a maldição (doente) |
|---|---|---|
| Yara | `OlhoYara.png`, `BocaYara.png` | `OlhoYara_Doente.png` (também o da fumaça), `BocaYaraDoente.png` |
| Mbaé | `OlhoMbaé_ate3.png` (até 3 noites na oca) | `OlhoDoenteMbaé.png`, `BocaMbaéDoente.png` |
| Potira | `OlhoPotira.png`, `BocaPotira.png` | `OlharPotiraDoente.png`, `BocaPotiraDoente.png` |
| Tamandaré-mirim | `OlhoTama.png` (até 3 noites na oca; já levemente vermelho) | `OlhoTamaDoente.png`, `BocaTamaDoente.png` |
| Iandé | `OlhoIandé.png`, `BocaIandé.png` (noites 7 e 8) | `OlhoIandé_Doente.png`, `BocaIandéDoente.png` (noites 9 e 10) |
| Araci | — | `OlhoDoenteAraci.png`, `BocaAraciDoente.png` |

**Convertidas, mas sem uso no jogo** (a pessoa já chega doente, ou não é examinada):
`BocaMbaé.png`, `BocaTama.png`, `BocaAraci.png`, `OlhoKrenan.png`, `OlhoKrenan_Doente.png`,
`OlhoMbaé.png` (igual ao `OlhoMbaé_ate3.png`).

## O que a pessoa diz quando o jogador olha

Com a imagem na tela, o texto fica só com o que a pessoa diz (em âmbar, o que ela afirma e o
jogador não tem como conferir).

| Pessoa | Olho (são) | Olho (doente) | Boca (são) | Boca (doente) |
|---|---|---|---|---|
| Yara | "Dormi perto do fogo." / "Viu? Era a fumaça." | "(treme) É frio, só isso." | "Pode olhar. Não tenho nada." | "(tosse) Dói para engolir." |
| Mbaé | "(tosse) É o vento do rio." | "(tosse) É o vento do rio. De noite arde mais." | — | "(tosse) Mordi a língua comendo peixe." |
| Potira | "É sono. Andei desde antes do sol." | "(treme) Dormi mal, só isso." | "Os lábios? Estão secos. / É do frio…" | "(tosse) Arde por dentro." |
| Tamandaré-mirim | "É o sol da estrada." | "É o sol da estrada. Agora arde." | — | "Rouco de pregar. Só isso." |
| Iandé | "Dormi bem na vila." | "Não dormi. É a dor nas costas." | "Pode olhar. Está tudo bem." | "(tosse) Comi farinha velha na vila." |
| Araci | — | "Não durmo. A criança não deixa." | — | "É sede. Andei o dia inteiro." |

## Atrás da orelha e pescoço (noite 6 em diante a orelha; noite 9 em diante o pescoço)

| Pessoa | Saudável (orelha e pescoço) | Doente |
|---|---|---|
| Yara | `YaraOrelhaPescoco.png` | se pegou a febre e mostra: `YaraOrelhaDoente.png` e `YaraPescocoDoenete.png` |
| Mbaé | `MbaeOrelhaPescoco.png` (até 3 noites na oca, ou curado no tapiri) | depois de 3 noites na oca: `MbaeOrelhaDoente.png` e `MbaePescocoDoente.png` |
| Araci | — | `AraciOrelhaPescoco.png` (o nome diz saudável, mas a arte tem as manchas: ela sempre chega doente) |
| Potira, Tamandaré-mirim, Iandé | ainda sem imagem (texto) | ainda sem imagem (texto) |
