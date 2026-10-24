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
| Olhar a mata nas noites 2, 5 e 9 | `viu_anhanga` +1. Custa 1 de energia |
| Levar ao tapiri um doente de verdade | `tapiri_usos` +1. Gente sã não conta |
| Levar ao tapiri quem o pajé acusou | `seguiu_paje` +1. Se a pessoa era sã, `inocentes` +1 |

**A febre.** Se o doente dorme na oca, a febre passa para alguns moradores. **Quantos é
sorteado** a cada partida, entre um mínimo e um máximo (`Jogo/dados/febre.py`). Quem pega a
febre acorda doente no dia seguinte e **morre no 2º dia**. O doente que trouxe a febre não
morre dela.

| Doente | Noite | Se dormir na oca: moradores que pegam | Acordam doentes | Morrem |
|---|---|---|---|---|
| Mbaé | 2 | 1 a 3 | dia 3 | dia 4 |
| Tamandaré-mirim | 5 | 2 a 4 | dia 6 | dia 7 |
| Iandé | 7 | 3 a 5 | dia 8 | dia 9 |

- O sorteio usa a "semente" da partida: muda de uma partida para outra, mas o "Continuar" repete
  a mesma sorte.
- **Atenção:** a Proposta diz "Não há sorte; o mesmo caminho dá sempre o mesmo resultado". Com
  a febre sorteada, isso deixa de valer para o número de mortos.
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
| 3 | A Água do Batismo | `converteu` ≥ 1 (aceitou o batismo do padre novo) | noite 9 |
| 4 | Rio Acima | `rio_acima` ≥ 4 e `entregues` = 0 | **noite 9** |
| 5 | Anhangá | `viu_anhanga` ≥ 3, sem mortes pela mão (entregar ao Aleixo não impede) | noite 9 |
| 6 | A Honra | `memoria` ≥ 5, `vivos` ≥ 2, nunca matar alguém são, nunca levar alguém são ao tapiri | dia 10 |
| 7 | O Tapiri | `tapiri_usos` ≥ 2 e `tapiri_saos` = 0, `vivos` ≥ 2, sem mortes pela mão, sem entregas | dia 10 |
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

### 3. A Água do Batismo: noite 9

- No dia 9 (a última visita do Aleixo), **entregar 1 pessoa** a ele.
- **Nunca perguntar por quem ele levou:** nem as perguntas do dia 6 sobre cada levado ("Yara
  está curada?", "Onde Yara está?"…), nem as do dia 9 ("Os que você levou voltam?", "Os meus
  estão curados?", "Onde os meus estão?"). Qualquer uma delas fecha o caminho.
- Ao cair da noite 9, o padre novo da vila sobe a trilha e oferece o batismo. **Aceitar** acaba
  o jogo no fim da noite 9. Recusar segue o jogo.
- Quem já entregou alguém no dia 3 ou no dia 6 chega a 2 entregas e cai antes em A Troca.

### 4. Rio Acima: a partir da noite 9

- Krenan chega no dia 8 e leva até 2 moradores sãos por dia: 2 no dia 8 e mais 2 no dia 9 dão
  4, e o jogo acaba na **noite 9**.
- Precisa recusar o Aleixo nas três visitas (nenhuma entrega).

### 5. Anhangá: noite 9

- Precisa perguntar ao pajé "Que barulho é esse na mata?" nas três noites em que dá (2, 5 e 9). No fim da noite 9, a da 3ª vez, o jogo vai para o final.
  Perder uma já tira o final, porque o máximo é 3.
- A mata aparece na tela inteira, na ordem das vezes: na 1ª, só o escuro (`Anhanga_um`); na 2ª,
  uma sombra clara (`Anhanga_dois`); na 3ª, o veado branco (`Anhanga_tres`).
- Cada olhar custa 1 de energia: é um olhar a menos no exame daquela noite.
- Sem mortes pela sua mão. Entregar alguém ao Aleixo não impede (mas com 2 entregas A Troca vem antes, e quem aceita o batismo na noite 9 cai em A Água do Batismo). O jogo acaba no fim da **noite 9**, com
  `Anhanga_final` atrás das telas do final.

### 6. A Honra: dia 10

- Ouvir **as 5 histórias** (`memoria` ≥ 5): uma por visitante, então é preciso deixar entrar
  **os cinco** (Yara, Mbaé, Potira, Tamandaré-mirim e Iandé) e perguntar a história de cada um.
- Chegar ao dia 10 com **pelo menos 2** pessoas de fora vivas na aldeia.
- **Nunca matar alguém são** (`mortos_saos_por_sua_mao` = 0). Matar um amaldiçoado não impede.
- **Nunca levar alguém são ao tapiri** (`tapiri_saos` = 0).
- Entregar alguém ao Irmão Aleixo **não impede** (com 2 entregas, A Troca vem antes na fila).
- A Honra vem antes d'O Tapiri: quem cumpre as duas cai na Honra.

### 7. O Tapiri: dia 10

- Precisa levar ao tapiri **2 amaldiçoados**: quem chegou com a maldição (Mbaé, Tamandaré-mirim,
  Iandé) ou quem pegou a febre na oca, mesmo sem mostrar.
- **Não pode levar ninguém são, em nenhuma noite** (`tapiri_saos`). Quem já saiu curado do
  tapiri conta como são.
- **O tapiri cura:** quem era amaldiçoado e completa as 3 noites lá volta curado. Não passa
  mais a febre, não conta como amaldiçoado para os deuses do pajé, e o rosto (olho, boca,
  manchas secando) e a fala mostram que sarou.
- O jeito mais simples: Mbaé na noite 2 (sai curado na noite 5) e Tamandaré-mirim na noite 5
  (sai curado na noite 8). O tapiri tem 1 vaga, e cada um fica 3 noites.
- Também: sem mortes pela sua mão, sem entregas ao Aleixo, e pelo menos 2 vivos de fora no dia 10.
- Quem também ouviu as cinco histórias cai antes em A Honra.

### 8. O Vazio: a partir da noite 9 (ou no dia 10)

- No dia 10, é o que sobra quando nada mais bate.
- Antes disso, o jogo acaba se, no fim de uma noite, sobrarem **7 vivos ou menos**.
- Com a febre sorteada, isso depende da sorte: no pior caso (os cinco dentro, os três doentes na
  oca e o maior sorteio) sobram 17 − 3 − 4 − 5 = **5 na noite 9**; no melhor, 11, e o jogo segue.
- Antes da noite 9 a aldeia nunca chega a 7: no pior sorteio, ficam 17 − 3 (dia 4) = 14 e
  depois 14 − 4 (dia 7) = 10.

## 4. Resumo: o jogo pode acabar antes da noite 10?

Sim. Os fins mais cedo possíveis são:

| Noite | Final | Como |
|---|---|---|
| 3 | A Troca | entregar Yara e Mbaé ao Aleixo no dia 3 |
| 4 | A Loucura | matar Yara, Mbaé e Potira |
| 6 | A Troca | 2ª entrega na 2ª visita do Aleixo |
| 9 | Rio Acima | 4 moradores com Krenan (2 no dia 8, 2 no dia 9) |
| 9 | O Vazio | a aldeia ficou com 7 ou menos (depende do sorteio da febre) |
| 10 | os outros | a fila inteira, antes de Araci |

## 5. O que o grupo precisa decidir

- [x] Quem pega a febre morre no 2º dia; o doente que a trouxe não morre dela. Quantos pegam
      é sorteado (decidido em 13/10/2026).
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
- Noites 1 e 2: matar conta para A Loucura, e levar um doente ao tapiri conta para O Tapiri
  (Yara é sã, então não conta; Mbaé conta).
- O tapiri com 1 vaga e 3 noites: se Yara foi para o tapiri na noite 1, na noite 2 não há
  lugar para Mbaé, e a vaga abre na noite 4.
- A febre sorteada: Mbaé dormindo na oca passa a febre para 1 a 3 moradores, que acordam
  doentes no dia 3 e morrem no dia 4. As notícias aparecem de manhã.
- As outras variáveis (entregas, rio acima, Anhangá e acusações do pajé) passam a contar quando
  os dias 3 a 10 forem construídos.
