# Caraíba — As porcentagens dos finais

## Atualização de 25/10/2026: os dez finais

400 partidas jogadas ao acaso pelo simulador (`Jogo/ferramentas/simular_finais.py`), com as
regras de hoje. Estes números são os que aparecem na tela da fonte de cada final.

| Nº | Final | Ao acaso | Em que noite acabou |
|---|---|---|---|
| 1 | Guerra Justa | 1,8% | noite 9 |
| 2 | A Troca | 13,8% | noite 6 (36), noite 9 (19) |
| 3 | A Loucura | 2,2% | noites 4 a 8 |
| 4 | A Água do Batismo | 8,2% | noite 9 |
| 5 | Rio Acima | 1,0% | noite 10 |
| 6 | Anhangá | 0,5% | noite 9 |
| 7 | O Tapiri | 0% | — |
| 8 | A Honra | 1,8% | noite 10 |
| 9 | Ferida | 5,8% | noite 10 |
| 10 | O Vazio | 65,0% | 146 no dia 10; o resto antes, quando a aldeia esvaziou |

Depois de facilitar A Honra (1 vivo ou mais, nenhuma morte pela sua mão, 1 amaldiçoado no
tapiri) e o Ferida (1 vivo ou mais), os dois já aparecem jogando ao acaso. O Tapiri continua
pedindo escolhas pensadas até o dia 10. O resto deste documento é a análise anterior (oito finais), guardada
como histórico.


Com que frequência cada um dos oito finais acontece e o que o jogador precisa fazer para chegar
a cada um. Versão de 17/10/2026, com o jogo como está hoje (dias e noites 1 a 10).

**De onde vêm os números.** Não são contas feitas à mão: um robô jogou milhares de partidas
inteiras no jogo de verdade (`Jogo/ferramentas/simular_finais.py`), sem janela, usando os
mesmos roteiros, a mesma febre sorteada e o mesmo cálculo dos finais. Se o grupo mudar o
roteiro ou as condições, é só rodar de novo, de dentro da pasta `Jogo`:

```
python -m ferramentas.simular_finais 2000            (ao acaso)
python -m ferramentas.simular_finais 300 tapiri      (quem tenta O Tapiri)
```

Como as partidas são sorteadas, os números variam um pouco de uma rodada para outra (cerca
de 1 a 3 pontos para cima ou para baixo).

## 1. Como o jogo escolhe o final

- **No fim de cada noite**, o jogo testa A Troca, A Loucura e Rio Acima, nessa ordem. Se um
  deles já bate, a partida acaba ali.
- Também no fim de cada noite: se **não sobrou ninguém de fora vivo na aldeia e já morreram
  2 ou mais**, a partida acaba em **O Vazio**.
- **Na manhã do dia 10**, antes de Araci chegar, o jogo testa a fila inteira e fica com o
  primeiro que bater. O final aparece no fim da noite 10, e nada do que se faz com Araci muda
  o resultado. O Vazio é o último da fila e sempre bate.

## 2. Jogando ao acaso

Um jogador que escolhe tudo ao acaso: cada botão tem a mesma chance, faz mais ou menos metade
das perguntas e conversa com metade das pessoas na aldeia.

2000 partidas:

| Final | Partidas | % | Em que noite acabou |
|---|---|---|---|
| A Troca | 254 | **12,7%** | noite 6: 153 · noite 9: 101 |
| A Loucura | 10 | **0,5%** | noite 5: 7 · noite 7: 1 · noite 8: 2 |
| A Água do Batismo | 0 | **0%** | — |
| Rio Acima | 0 | **0%** | — |
| Anhangá | 0 | **0%** | — |
| A Honra | 0 | **0%** | — |
| O Tapiri | 0 | **0%** | — |
| O Vazio | 1736 | **86,8%** | noite 2: 56 · noite 4: 116 · noite 5: 120 · noite 6: 68 · noite 7: 143 · noite 8: 43 · noite 9: 13 · noite 10: 1177 |

**Leitura:** quem joga sem plano cai em O Vazio quase 9 vezes em 10. Somando todos os finais,
41% das partidas acabam antes da noite 10. Em 28% do total, o motivo é a aldeia ter
esvaziado. A Troca aparece quando o
jogador entrega duas pessoas ao Aleixo. A Loucura e O Tapiri são possíveis, mas quase nunca
acontecem por acaso.

## 3. Final por final: como alcançar

As porcentagens desta seção são de **quem tenta** o final, seguindo o caminho descrito
(300 partidas para cada um).

| Final | Condição (`Jogo/dados/finais.py`) | Tentando, dá certo em | Acaba na |
|---|---|---|---|
| A Troca | 2 entregas ao Aleixo, **ou** proximidade da vila ≥ 3 | **100%** | noite 6 |
| A Loucura | 3 mortes pela sua mão | **44%** | noite 5 |
| A Água do Batismo | seguiu o pajé ≥ 3 e ≥ 1 inocente | **0%: impossível hoje** | — |
| Rio Acima | ≥ 4 levados por Krenan, sem entregas | **0%: impossível hoje** | — |
| Anhangá | viu o Anhangá ≥ 3, sem mortes pela mão, sem entregas | **0%: impossível hoje** | — |
| A Honra | ≥ 3 vivos, memória ≥ 5, sem mortes pela mão, sem entregas | **0%: impossível hoje** | — |
| O Tapiri | tapiri usado ≥ 3 vezes com doentes, ≥ 2 vivos, sem mortes pela mão, sem entregas | **35%** | noite 10 |
| O Vazio | o que sobra; ou a aldeia esvaziou | sempre que nada mais bate | noite 2 em diante |

### A Troca: 100%, na noite 6

- **Como:** deixar entrar quem chega e **entregar alguém ao Irmão Aleixo** na 1ª visita
  (dia 3) e na 2ª (dia 6). Com 2 entregas, o jogo acaba no fim da noite 6.
- O Aleixo só leva uma pessoa por visita, então não dá para acabar antes da noite 6.
- O machado de Yara soma 1 de proximidade, e cada entrega também. Mas a proximidade só chega
  a 3 com o machado mais 2 entregas, e aí as 2 entregas já bastam. **Na prática, A Troca é
  "entregar 2 pessoas".**
- Nada atrapalha: é o primeiro da fila, e a febre não tira as entregas.

### A Loucura: 44%, na noite 5

- **Como:** deixar entrar todo mundo, negar o Aleixo e **matar 3 pessoas na fogueira**.
- **A pegadinha:** matar cedo demais leva a O Vazio. Se ninguém de fora sobra vivo na aldeia
  e já morreram 2, o jogo acaba ali, antes da 3ª morte. Por exemplo, matar Yara na noite 1 e
  Mbaé na noite 2 acaba em O Vazio na noite 2.
- **O jeito que funciona:** esperar a noite 5. Nela podem estar na fogueira Potira,
  Tamandaré-mirim e quem sobrou de Yara e Mbaé depois do Aleixo. Matar os 3 na mesma noite
  dá A Loucura na **noite 5**, a mais cedo possível.
- **Por que só 44%:** o Aleixo leva alguém no dia 3 e a febre de Mbaé pode matar Yara. Às
  vezes chegam só 2 pessoas à noite 5, e aí a 2ª morte esvazia a aldeia (O Vazio).

### A Água do Batismo: impossível hoje

- A condição pede `seguiu_paje` ≥ 3, mas **nada no jogo soma `seguiu_paje` nem `inocentes`**.
  O pajé dá os sinais na tábua, mas não acusa ninguém pelo nome.
- **Para funcionar:** o pajé precisa acusar alguém pelo nome, e levar ao tapiri quem ele
  acusou precisa somar `seguiu_paje` (e `inocentes`, se a pessoa era sã).

### Rio Acima: impossível hoje

- A condição pede **4 pessoas** levadas por Krenan. Mas Krenan leva **1 por noite**: 1 na
  noite 8 e, se voltar, 1 na noite 10.
- E o final é calculado **na manhã do dia 10**, antes da noite 10. Então, na hora da conta,
  o máximo é **1**.
- **Para funcionar:** baixar a condição para 1 (`rio_acima >= 1`), ou deixar Krenan levar
  mais gente por noite. Lembrete: Rio Acima também exige nenhuma entrega ao Aleixo.

### Anhangá: impossível hoje

- A condição pede `viu_anhanga` ≥ 3, mas **ainda não existe o "Olhar a mata"** nas noites,
  e nada soma `viu_anhanga`.
- **Para funcionar:** criar o veado branco e o botão de olhar a mata (a ideia era nas noites
  2, 5 e 9, gastando 1 olhar).

### A Honra: impossível hoje

- Pede **memória ≥ 5**: ouvir as histórias de Yara, Mbaé, Potira, Tamandaré-mirim e Iandé.
  A de Araci não conta, porque ela chega depois do cálculo. Então é preciso deixar **os
  cinco** entrarem.
- Pede também **3 vivos ou mais** na manhã do dia 10, sem entregas.
- **A conta não fecha:** o Aleixo vem nos dias 3, 6 e 9. Se o jogador entrega alguém, perde
  a Honra; se nega, **ele leva alguém mesmo assim**, e sempre há alguém para levar. São 3
  pessoas a menos: dos 5, sobram **no máximo 2**.
- A única saída seria não ter ninguém na aldeia no dia do Aleixo, mas aí não dá para ouvir
  as cinco histórias.
- **Para funcionar** (o grupo escolhe): baixar para 2 vivos; ou fazer o Aleixo não levar
  ninguém quando o jogador nega (pelo menos numa das visitas); ou baixar a memória para 4.

### O Tapiri: 35%, na noite 10

- **Como:** deixar entrar todo mundo, negar o Aleixo, não deixar Krenan levar ninguém e
  **levar ao tapiri os doentes de verdade** sempre que houver vaga.
- O tapiri tem **1 vaga** e cada pessoa fica **3 noites**. Os doentes que contam são Mbaé,
  Tamandaré-mirim e Iandé (Araci chega tarde). Um caminho que fecha:
  Mbaé na noite 2 (sai na 5), Tamandaré-mirim na noite 5 (sai na 8), Iandé na noite 8.
- Levar o **mesmo** doente de novo, depois que ele sai, também conta.
- Precisa de **2 vivos** na manhã do dia 10. O Aleixo leva 3 (um por visita), então dos 5
  sobram 2, e **qualquer morte de febre derruba o final**. Por isso só dá certo em cerca de
  1 em cada 3 tentativas: depende do sorteio da febre e de quem o Aleixo leva.
- Dica: com os doentes no tapiri, a febre não passa. O risco maior é Tamandaré-mirim e Iandé
  dormirem na oca nas noites em que a vaga está ocupada.

### O Vazio: o que sobra

- Na manhã do dia 10, se nenhum outro final bateu, é O Vazio.
- **Antes do dia 10:** se, no fim de uma noite, não sobrou ninguém de fora vivo na aldeia e
  já morreram 2 ou mais (de febre ou pela sua mão), o jogo acaba ali. Pode ser já na
  **noite 2** (matar Yara e Mbaé).
- É de longe o final mais comum: quase tudo que dá errado nos outros cai aqui.

## 4. Resumo para o grupo

- **Hoje, só 4 dos 8 finais podem acontecer:** A Troca, A Loucura, O Tapiri e O Vazio.
- **Faltam no jogo** as peças de A Água do Batismo (acusações do pajé pelo nome) e de Anhangá
  (olhar a mata).
- **Rio Acima e A Honra** já têm tudo, mas as contas não fecham com as regras de hoje: Krenan
  leva gente de menos, e o Aleixo tira gente demais. Veja as sugestões em cada um.
- O **Vazio** domina quem joga sem plano. Se o grupo quiser que outros finais apareçam mais
  vezes por acaso, vale rever o quanto a febre mata e o quanto o Aleixo leva.
