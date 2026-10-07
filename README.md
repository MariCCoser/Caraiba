# Caraíba: Dez Dias, Dez Fogueiras

Jogo educativo de História sobre a epidemia de 1562-63 no litoral brasileiro, feito em **Python + pygame**.

> Por volta de 1562, numa pequena aldeia entre a mata e o rio, restam doze pessoas. O cacique foi para a mata e deixou a entrada sob a sua guarda. Gente chega pela trilha todos os dias: uns doentes, outros sãos, alguns sem saber. De dia, o Irmão Aleixo, um jesuíta, dá a leitura dele de cada visitante. De noite, na fogueira, o pajé conta o que sonhou. Em quem você acredita?

Inspirado em *No, I'm Not a Human*.

## Sobre o jogo

Durante **10 dias**, o jogador decide quem entra na aldeia. Cada dia tem quatro momentos:

1. **Manhã, na oca**: as consequências da noite (quem adoeceu, quem morreu, sempre com nome) e uma ação sobre os de dentro.
2. **Dia, na entrada**: o visitante chega de longe. Aleixo dá a leitura europeia (botica, lei e batismo). Você o chama para a fogueira ou o manda seguir.
3. **Noite, na fogueira**: você examina o rosto (olhos, boca, pele, pescoço e mãos), faz perguntas, ouve a história e o sonho do pajé. Depois decide: dormir na oca, dormir no tapiri, mandar seguir ou matar.
4. **Tela de fato**: um fato histórico ligado ao tema do dia, com a fonte.

As regras são fixas e sem sorte. A doença passa só dentro da oca, de noite. Os sintomas seguem as fases reais da varíola, do sarampo e da gripe, e os nomes das doenças nunca aparecem na tela, porque os povos indígenas não tinham nome para essas enfermidades novas.

### Os cinco finais

Cada final mostra um povo real que seguiu o mesmo caminho do jogador e o que aconteceu com ele depois:

| Final | Paralelo histórico |
|---|---|
| A Troca | Tupiniquim |
| A Loucura | Santidade de Jaguaripe |
| Rio Acima | Aimoré / Botocudo → Krenak |
| A Honra | Tupinambá |
| O Vazio | Goitacá |

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
├── Jogo/          Código do jogo (pygame)
├── Arte/          Artes desenhadas pelo grupo, paleta e guia de personagens
│   └── PP/        Personagens
├── Pesquisa/      Pesquisa histórica (doenças, epidemia, povos originários)
├── Textos/        Documento de design: "Dez Dias, Dez Fogueiras"
├── Proposta.docx  Proposta original do jogo
├── requisitos.docx Requisitos e rubrica do projeto
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
