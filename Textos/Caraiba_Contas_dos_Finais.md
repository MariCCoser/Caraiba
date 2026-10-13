# Caraíba — As contas dos finais

O que o jogador precisa fazer para chegar a cada um dos oito finais, e **em que noite, no
mínimo, cada um pode acontecer**. Baseado em `Caraiba_Os_Finais.pdf` e `A_Febre_Caraiba.pdf`.
Versão de 13/10/2026.

No jogo, as condições ficam em `Jogo/dados/finais.py` (dá para mudar os números lá), e o
cálculo em `Jogo/motor/finais.py`.

## 1. Quando o jogo acaba

- **No fim de cada noite**, o jogo confere os finais que podem acontecer antes da hora:
  **A Troca**, **A Loucura**, **Rio Acima** e **O Vazio**, se a aldeia esvaziar. Se um deles já
  bate, a partida acaba ali, na noite 3, na 4, na 6…
- **Na manhã do dia 10**, antes de Araci chegar, o jogo confere a fila inteira, na ordem, e
  fica com o primeiro final que bater. O Vazio é o último e sempre bate.

Os outros quatro finais (A Água do Batismo, Anhangá, A Honra e O Tapiri) só são conferidos
no dia 10, porque dependem de escolhas feitas até o fim do jogo.

## 2. As regras usadas nas contas

Algumas destas regras ainda não estavam escritas nos documentos. **As marcadas com (proposta)
precisam ser confirmadas pelo grupo.**

| O que acontece | Efeito nas variáveis |
|---|---|
| Deixar alguém entrar | `vivos` +1 |
| Aceitar o machado (dia 1) | `proximidade_vila` +1 |
| Entregar alguém ao Aleixo (dias 3, 6 e 9) | `entregues` +1, `proximidade_vila` +1, `vivos` −1 |
| Matar alguém na fogueira | `mortos_por_sua_mao` +1, `mortos` +1, `vivos` −1, `sanidade` −3 |
| Krenan leva alguém rio acima (dias 8 a 10) | `rio_acima` +1, `vivos` −1. Ele leva até 2 por dia (proposta) |
| Ouvir a história de quem entrou | `memoria` +1 (uma história por visitante) |
| Olhar a mata nas noites 2, 5 e 8 | `viu_anhanga` +1. Custa 1 de energia |
| Levar ao tapiri um doente de verdade | `tapiri_usos` +1. Gente sã não conta |
| Levar ao tapiri quem o pajé acusou | `seguiu_paje` +1. Se a pessoa era sã, `inocentes` +1 |

**A febre (de `A_Febre_Caraiba.pdf`).** Se o doente dorme na oca, a doença passa:

| Doente | Noite | Se dormir na oca |
|---|---|---|
| Mbaé | 2 | 2 moradores, dia 4 |
| Tamandaré-mirim | 5 | 3 moradores, dia 8 |
| Iandé | 7 | ela e mais 4 moradores, dia 9 |

- **(proposta)** Quem pega a febre morre naquele dia: `vivos` −1 por pessoa.
- **(proposta)** No tapiri, a doença não passa. A pessoa fica lá **3 noites** e depois a vaga
  abre.
- O tapiri tem **1 vaga**. Se Potira entrou no dia 4, ela ergue a 2ª vaga no dia 5.

**Os números de partida.** São 12 vivos. Se o jogador deixar entrar os cinco que podem ficar
(Yara, Mbaé, Potira, Tamandaré-mirim e Iandé), são **17 no máximo**. O Aleixo e o Krenan não
entram, e Araci chega depois do cálculo.

## 3. Final por final

| Nº | Final | Condição | Acaba no mínimo na… |
|---|---|---|---|
| 1 | A Troca | `entregues` ≥ 2 **ou** `proximidade_vila` ≥ 3 | **noite 3** |
| 2 | A Loucura | `mortos_por_sua_mao` ≥ 3 | **noite 4** |
| 3 | A Água do Batismo | `seguiu_paje` ≥ 3 e `inocentes` ≥ 1 | dia 10 |
| 4 | Rio Acima | `rio_acima` ≥ 4 e `entregues` = 0 | **noite 9** |
| 5 | Anhangá | `viu_anhanga` ≥ 3, sem mortes pela mão, sem entregas | dia 10 |
| 6 | A Honra | `vivos` ≥ 9, `memoria` ≥ 5, sem mortes pela mão, sem entregas | dia 10 |
| 7 | O Tapiri | `tapiri_usos` ≥ 3, `vivos` ≥ 7, sem mortes pela mão, sem entregas | dia 10 |
| 8 | O Vazio | nenhuma das anteriores; ou `vivos` ≤ 7 no fim de uma noite | **noite 9** (ou dia 10) |

### 1. A Troca: a partir da noite 3

- **Mais rápido:** deixar Yara entrar no dia 1 e Mbaé no dia 2, e entregar os dois na
  primeira visita do Aleixo (dia 3). São 2 entregas, e o jogo acaba na **noite 3**.
- **Caminho típico:** aceitar o machado (+1) e entregar 1 pessoa no dia 3 e 1 no dia 6. São
  2 entregas e proximidade 3, e o jogo acaba na **noite 6**.
- Conta: com as regras de hoje, a proximidade só sobe com o machado (+1) e com entregas (+1
  cada). Então proximidade ≥ 3 só acontece junto com 2 entregas. Se o grupo usar também
  "remédio aceito" ou "doente mandado seguir de dia" (como diz o `estado.py`), dá para chegar
  a 3 sem entregar ninguém. Por exemplo: machado + recusar Mbaé + aceitar o remédio = 3 já na
  noite 3.

### 2. A Loucura: a partir da noite 4

- Precisa de 3 pessoas diferentes dentro da aldeia para matar. Até a noite 3 entram no
  máximo 2 (Yara e Mbaé; o Aleixo não entra). A 3ª é Potira, na noite 4.
- **Mais rápido:** matar Yara (noite 1), Mbaé (noite 2) e Potira (noite 4). Acaba na
  **noite 4**.
- **Caminho do PDF:** matar Mbaé (noite 2), Tamandaré-mirim (noite 5) e Iandé (noite 7). Acaba
  na **noite 7**.
- Cada morte tira 3 de sanidade: com 3 mortes, a sanidade cai de 10 para 1.

### 3. A Água do Batismo: dia 10

- O pajé precisa acusar alguém **pelo nome** em pelo menos 3 noites em que o tapiri tenha vaga
  livre, e pelo menos um dos acusados precisa ser são.
- Exemplo com 1 vaga só: Yara na noite 1 (inocente; fica até a 3), Potira na noite 4
  (inocente; fica até a 6) e Iandé na noite 7 (doente). São 3 acusações seguidas e 2 inocentes.
- **Falta no jogo:** hoje o pajé diz o sinal ("olho vermelho") mas não diz nomes. As falas dele
  precisam ser reescritas, como o PDF já indica.

### 4. Rio Acima: a partir da noite 9

- Krenan chega no dia 8 e leva até 2 moradores sãos por dia: 2 no dia 8 e mais 2 no dia 9 dão
  4, e o jogo acaba na **noite 9**.
- Precisa recusar o Aleixo nas três visitas (nenhuma entrega).

### 5. Anhangá: dia 10

- Precisa olhar a mata nas três noites (2, 5 e 8). Perder uma já tira o final, porque o máximo
  é 3.
- Cada olhar custa 1 de energia: é um olhar a menos no exame daquela noite.
- **Falta no jogo:** o desenho do veado e o botão "Olhar a mata".

### 6. A Honra: dia 10

- `memoria` ≥ 5 é a parte difícil: como há **uma história por visitante**, o jogador precisa
  deixar entrar **os cinco** (inclusive os três doentes) e ouvir a história de todos.
- Os vivos são a parte fácil: com os cinco dentro são 17. Para cair abaixo de 9, os três
  doentes teriam de dormir na oca (17 − 2 − 3 − 5 = 7). Basta pôr no tapiri **qualquer um**
  dos três: o pior caso fica em 17 − 3 − 5 = 9.
- **Atenção:** a Proposta fala em "não deixar ninguém morrer sob o seu teto", mas a condição só
  pede 9 vivos. Se Mbaé dormir na oca, 2 morrem e mesmo assim dá A Honra. O grupo decide se a
  condição deve exigir `mortos` = 0.

### 7. O Tapiri: dia 10

- Precisa levar ao tapiri **os três doentes**, Mbaé (noite 2), Tamandaré-mirim (noite 5) e
  Iandé (noite 7), porque só eles contam.
- Conta das vagas: Mbaé ocupa a vaga das noites 2 a 4. Tamandaré-mirim ocupa a mesma vaga das
  noites 5 a 7. Na noite 7 ela ainda está ocupada, então Iandé só cabe na **2ª vaga, que só
  existe se Potira entrou**. Ou seja, O Tapiri também exige deixar Potira entrar.
- Vivos: sem contágio nenhum, ficam pelo menos 16. O "≥ 7" quase nunca impede.
- Quem também ouviu as cinco histórias cai antes em A Honra.

### 8. O Vazio: a partir da noite 9 (ou no dia 10)

- No dia 10, é o que sobra quando nada mais bate.
- Antes disso, o jogo acaba se, no fim de uma noite, sobrarem **7 vivos ou menos**.
- Conta: o pior caso sem matar nem entregar é deixar os cinco entrarem e os três doentes
  dormirem na oca. São 17 − 2 (dia 4) − 3 (dia 8) − 5 (dia 9) = **7 na noite 9**. Antes disso
  a aldeia nunca chega a 7.

## 4. Resumo: o jogo pode acabar antes da noite 10?

Sim. Os fins mais cedo possíveis são:

| Noite | Final | Como |
|---|---|---|
| 3 | A Troca | entregar Yara e Mbaé ao Aleixo no dia 3 |
| 4 | A Loucura | matar Yara, Mbaé e Potira |
| 6 | A Troca | 2ª entrega na 2ª visita do Aleixo |
| 9 | Rio Acima | 4 moradores com Krenan (2 no dia 8, 2 no dia 9) |
| 9 | O Vazio | a aldeia ficou com 7 ou menos |
| 10 | os outros | a fila inteira, antes de Araci |

## 5. O que o grupo precisa decidir

- [ ] Quem pega a febre morre no mesmo dia? (As contas acima consideram que sim.)
- [ ] Quanto tempo o doente fica no tapiri? (Contas: 3 noites.)
- [ ] Krenan leva até quantas pessoas por dia? (Contas: 2.)
- [ ] "Remédio aceito" e "doente mandado seguir de dia" somam proximidade? Se sim, A Troca
      fica bem mais fácil.
- [ ] A Honra pede as **cinco** histórias. Baixar para 4, ou dar histórias também ao pajé?
- [ ] A Honra deve exigir `mortos` = 0 ("ninguém morreu sob o seu teto")?
- [ ] Reescrever as falas do pajé com acusações pelo nome (A Água do Batismo).
- [ ] Energia: o PDF fala em 4 por noite; a noite 1 está com 1, porque só os olhos podem ser
      examinados.

## 6. O que já funciona no jogo

- A fila dos oito finais, com as condições de `dados/finais.py`.
- A checagem no fim de cada noite: o jogo acaba antes do dia 10 quando um final antecipado
  bate.
- A tela de final, com três telas: a cena, o povo e o fato, e a fonte.
- Na noite 1: matar Yara conta para A Loucura, e levar um doente ao tapiri conta para O Tapiri
  (Yara é sã, então não conta).
- As outras variáveis (entregas, rio acima, Anhangá e acusações do pajé) passam a contar quando
  os dias 2 a 10 forem construídos.
