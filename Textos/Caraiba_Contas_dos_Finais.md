# Caraíba — As contas dos finais

O que o jogador precisa fazer para chegar a cada um dos dez finais, e **em que noite, no
mínimo, cada um pode acontecer**. Versão de 25/10/2026.

No jogo, as condições ficam em `Jogo/dados/finais.py` (dá para mudar os números lá), e o
cálculo em `Jogo/motor/finais.py`. As chances de cada final estão em
`Caraiba_Porcentagens_dos_Finais.md`.

## 1. Quando o jogo acaba

- **No fim de cada noite**, o jogo confere os finais que podem acontecer antes da hora, na
  ordem da fila: Guerra Justa, A Troca, A Loucura, A Água do Batismo e Anhangá. Se um deles já
  bate, a partida acaba ali. O Vazio também acaba o jogo antes, se a aldeia esvaziar.
- **Na manhã do dia 10**, antes de Araci chegar, o jogo confere a fila inteira e fica com o
  primeiro final que bater. O Vazio é o último e sempre bate. Nada do que o jogador faz com
  Araci muda o final.
- **Rio Acima** é a exceção: é a escolha "Ir com ele" na noite 10, quando Krenan volta. Ela vale
  mais que o final calculado de manhã.

## 2. As regras usadas nas contas

`vivos` conta só quem é de fora e está vivo na aldeia (no máximo 5: Yara, Mbaé, Potira,
Tamandaré-mirim e Iandé). O jogador e o pajé não contam.

| O que acontece | Efeito nas variáveis |
|---|---|
| Deixar alguém entrar | `vivos` +1 |
| Aceitar o machado de Yara (dia 1) | `proximidade_vila` +1; +1 olhar em toda noite |
| Comer a mandioca de Potira (dia 4) | +1 olhar em toda noite, da 4 à 10 |
| Aceitar a pulseira de Iandé (dia 7) | +1 olhar em toda noite, da 7 à 10 |
| Entregar alguém ao Aleixo (dias 3, 6 e 9) | `entregues` +1, `proximidade_vila` +1, `vivos` −1 |
| Negar o Aleixo | +1 olhar só naquela noite. Nos dias 6 e 9, ele leva alguém sorteado (`levados` +1) |
| No dia 9, "Deixar ir" quem o Aleixo leva | `entregues` +1 |
| No dia 9, "Pegar o arco" | `aleixo_morto` = 1, `mortos_por_sua_mao` +1, sanidade −2; a pessoa volta |
| Perguntar ao Aleixo sobre quem ele levou | `perguntou_levados` +1 (uma vez por visita; nenhum final usa ainda) |
| Matar alguém na fogueira | `mortos_por_sua_mao` +1, `mortos` +1, `vivos` −1, sanidade −3. Se a pessoa era sã, `mortos_saos_por_sua_mao` +1 |
| Levar ao tapiri um amaldiçoado | `tapiri_usos` +1 |
| Levar ao tapiri alguém são | `tapiri_saos` +1 |
| Ver o veado na mata (noites 2, 5 e 9) | `viu_anhanga` +1 |
| Deixar o padre entrar (dia 9) e aceitar o batismo (noite 9) | `converteu` = 1 |
| Ir com Krenan na noite 10 | `subiu_o_rio` = 1 |
| Ouvir a história de quem entrou | `memoria` +1 (uma por pessoa; hoje a Honra não pede) |

**A febre.** Se um amaldiçoado dorme na oca, a febre passa para alguns de fora que dormem nas
ocas. Quantos pegam é sorteado a cada partida (`Jogo/dados/febre.py`). Quem pega acorda
doente no dia seguinte e morre no 2º dia. O "Continuar" repete a mesma sorte.

**O tapiri.** Tem 1 vaga. Quem entra fica 3 noites, longe de todos, e o mal não passa para
ninguém. Quem era amaldiçoado sai curado.

## 3. Final por final

| Nº | Final | Condição | Acaba no mínimo na… |
|---|---|---|---|
| 1 | Guerra Justa | `aleixo_morto` = 1 (o arco no dia 9) | noite 9 |
| 2 | A Troca | `entregues` ≥ 2 **ou** `proximidade_vila` ≥ 3 | noite 6 |
| 3 | A Loucura | `mortos_por_sua_mao` ≥ 3 | noite 4 |
| 4 | A Água do Batismo | `converteu` = 1 | noite 9 |
| 5 | Rio Acima | `subiu_o_rio` = 1 | noite 10 |
| 6 | Anhangá | `viu_anhanga` ≥ 3 e nenhuma morte pela sua mão | noite 9 |
| 7 | O Tapiri | `tapiri_usos` ≥ 2, `tapiri_saos` = 0, `vivos` ≥ 2, nunca matar alguém são | dia 10 |
| 8 | A Honra | `vivos` ≥ 1, nunca matar ninguém, levar ao tapiri 1 amaldiçoado e nunca alguém são | dia 10 |
| 9 | Ferida | matou alguém são **ou** levou alguém são ao tapiri, com 1 vivo ou mais | dia 10 |
| 10 | O Vazio | nenhum dos anteriores; ou a aldeia esvaziou | dia 10 (ou antes, se esvaziar) |

### 1. Guerra Justa: noite 9

- No dia 9, o jogador nega o padre novo e depois nega o pedido do Aleixo. O Aleixo leva alguém
  pela trilha, e aparecem "Pegar o arco" e "Deixar ir".
- "Pegar o arco" acaba o jogo no fim da noite 9. É o primeiro da fila: vence todos os outros.
- Com o padre lá dentro, o Aleixo não leva ninguém, e não há arco.

### 2. A Troca: a partir da noite 6

- Duas entregas: uma no dia 3 e outra no dia 6. O jogo acaba no fim da noite 6.
- A proximidade só sobe com o machado e com as entregas, então chegar a 3 também pede 2 entregas.
- No dia 9, "Deixar ir" conta como entrega: quem entregou uma vez antes chega a 2.

### 3. A Loucura: a partir da noite 4

- Matar 3 pessoas. Até a noite 3 entram no máximo 2 (Yara e Mbaé); a 3ª é Potira, na noite 4.
- O jeito mais rápido: Yara na noite 1, Mbaé na noite 2 e Potira na noite 4.

### 4. A Água do Batismo: noite 9

- No dia 9, deixar o padre novo entrar. Com ele lá dentro, o Aleixo não pede ninguém.
- Na noite 9, o padre tenta convencer o jogador. "Aceitar o batismo e batizar os outros" acaba o
  jogo no fim da noite 9.

### 5. Rio Acima: noite 10

- Na noite 8, deixar Krenan levar alguém rio acima. Assim ele volta na noite 10.
- Na noite 10, ele faz o mesmo pedido, e o jogador escolhe "Ir com ele".

### 6. Anhangá: noite 9

- Perguntar ao pajé "Que barulho é esse na mata?" nas três noites em que dá (2, 5 e 9).
- Nenhuma morte pela sua mão. Entregar alguém ao Aleixo não impede (com 2 entregas, A Troca vem
  antes).

### 7. O Tapiri: dia 10

- Levar ao tapiri 2 amaldiçoados (quem chegou com a maldição ou pegou a febre na oca) e nunca
  ninguém são. Quem já saiu curado do tapiri conta como são.
- O jeito mais simples: Mbaé na noite 2 (sai curado na noite 5) e Tamandaré-mirim na noite 5.
- Pelo menos 2 vivos no dia 10. Matar um amaldiçoado ou entregar alguém não impede; matar
  alguém são impede.
- Também não impedem: o Aleixo levar gente (sorteada, ou 1 entrega: com 2, é A Troca), ver o veado até 2 vezes
  (na 3ª, é Anhangá) e deixar Krenan levar alguém na noite 8 (só não pode ir com ele na noite 10,
  que é Rio Acima).

### 8. A Honra: dia 10

- Pelo menos 1 vivo no dia 10 (sem ninguém além do jogador e do pajé, é O Vazio).
- Nunca matar ninguém (nem amaldiçoado).
- Levar ao tapiri pelo menos 1 amaldiçoado, e nunca alguém são. O jeito mais simples: Mbaé na
  noite 2. Negar Tamandaré-mirim e Iandé (ou deixá-los entrar sem levar ao tapiri, correndo o
  risco da febre).
- Entregar 1 pessoa ao Aleixo, ver o veado até 2 vezes e deixar Krenan levar alguém não impedem.
- As 5 histórias estão desligadas (`HONRA_PEDE_HISTORIAS` em `dados/finais.py`; a palavra-chave
  para religar é "voltar a honra").
- O Tapiri vem antes na fila: com 2 amaldiçoados no tapiri (e 2 vivos ou mais), cai no Tapiri.

### 9. Ferida: dia 10

- A aldeia sobreviveu (pelo menos 1 vivo), mas o jogador matou alguém são ou levou alguém são
  ao tapiri. A cena diz o nome dessa pessoa.
- Quem matou 3 ou mais cai antes em A Loucura. Sem nenhum vivo, é O Vazio.

### 10. O Vazio

- No dia 10, é o que sobra quando nada mais bate.
- Antes disso, o jogo acaba no fim de uma noite em que não sobrou ninguém de fora vivo e pelo
  menos 2 já morreram.

## 4. Resumo: o jogo pode acabar antes da noite 10?

| Noite | Final | Como |
|---|---|---|
| 4 | A Loucura | matar Yara, Mbaé e Potira |
| 6 | A Troca | a 2ª entrega, na 2ª visita do Aleixo |
| qualquer | O Vazio | a aldeia esvaziou |
| 9 | Guerra Justa, A Água do Batismo ou Anhangá | o arco, o batismo ou a 3ª vez do veado |
| 10 | Rio Acima | ir com Krenan |
| 10 | os outros | o cálculo da manhã do dia 10 |

## 5. O que o grupo ainda precisa decidir

- [ ] Os Caeté são o povo de dois finais (A Água do Batismo e Guerra Justa). Trocar um deles?
- [ ] Algum final deve usar as perguntas ao Aleixo sobre quem ele levou (`perguntou_levados`)?
- [ ] Religar as 5 histórias na Honra ("voltar a honra")?
