# Caraíba — o código do jogo

Este é o jogo em Python + pygame. Este guia foi escrito para quem **nunca usou Python**.
Siga os passos na ordem. Todos os comandos são digitados no **terminal**
(no Windows: "Prompt de Comando" ou "PowerShell"; no Linux/Mac: "Terminal").

---

## 1. Instalar (só na primeira vez)

1. Instale o **Python 3.12** (ou mais novo) em <https://www.python.org/downloads/>.
   No Windows, marque a caixa **"Add Python to PATH"** na instalação.
2. Abra o terminal **dentro da pasta `Jogo`**. Exemplo:
   ```
   cd Caraiba/Jogo
   ```
3. Crie o "ambiente virtual" (uma pasta `.venv` com o pygame só para este projeto):
   ```
   python -m venv .venv
   ```
   (No Linux pode ser `python3` em vez de `python`.)
4. Ative o ambiente. Você precisa fazer isso **toda vez** que abrir um terminal novo:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

   Deu certo se aparecer `(.venv)` no começo da linha do terminal.
5. Instale o pygame:
   ```
   pip install -r requirements.txt
   ```

## 2. Rodar o jogo

Com o ambiente ativado (passo 4), dentro da pasta `Jogo`:
```
python main.py
```

Controles: tudo funciona **só com o mouse**. Atalhos: **Enter** começa,
**Espaço/Enter** avança o texto, **Esc** volta ou pula, **F11** liga/desliga a tela cheia.

## 3. Editar o conteúdo (sem mexer na lógica)

Todo o texto do jogo fica na pasta **`dados/`**. Abra com qualquer editor de texto
(o Bloco de Notas serve, mas o VS Code é melhor).

| Quero mudar... | Arquivo |
|---|---|
| Título, botões do menu, textos das Opções | `dados/textos.py` |
| Os cartões da introdução (e o cenário de cada um) | `dados/textos.py`, parte `INTRODUCAO` |
| O que acontece em cada dia: falas do pajé, visitante, perguntas, escolhas, sinal | `dados/dias.py` (as instruções estão no topo do arquivo) |
| Qual arquivo de imagem é cada cenário | `dados/arte.py` |
| Cores, tamanhos de letra, velocidade do texto | `config.py` |

Regras para não quebrar nada:
- Cada texto fica entre aspas: `"assim"`. Se o texto tiver aspas dentro, use `“aspas curvas”`.
- Não apague as vírgulas no fim das linhas nem as chaves `{ }` e colchetes `[ ]` da estrutura.
- **Palavra marcada (em âmbar):** escreva entre colchetes **dentro do texto**:
  `"Passei no meio de tudo e não peguei [nada]."` Pode marcar várias palavras juntas:
  `"[de dentro para fora]"`. Na tela, a palavra fica âmbar **e sublinhada**.
- Cada cartão da introdução deve caber em **3 linhas**. Se passar, o terminal mostra um
  "Aviso: texto com N linhas". Nas falas do jogo (próximas etapas) o máximo será 2 linhas.
  Exceções: um cartão pode ter `"titulo"` (fica no meio da tela, como o aviso de conteúdo e
  as regras) e `"max_linhas"` maior. Cartão sem `"fundo"` aparece numa tela preta, sem filtros.
  Para quebrar a linha à força, use `\n` dentro do texto.
- Depois de editar, rode o teste (seção 5) para ver se está tudo certo.

## 4. Colocar arte nova

As artes originais ficam em `Caraiba/Arte/` e **nunca são alteradas**. O jogo usa cópias
menores em `Jogo/assets/`, com nomes sem acento e sem espaço (acento quebra no navegador).

1. Coloque a arte nova em `Caraiba/Arte/`.
2. Abra `ferramentas/converter_arte.py` e acrescente uma linha na lista `CENARIOS`, por exemplo:
   `("Oca.png", "cenarios/cenario-oca.jpg"),`
   Para uma pessoa, use a lista `PERSONAGENS`, com o giro no fim:
   `("PP/Mbaé.png", "personagens/mbae.png", 90),`
   As artes de `Arte/PP/` vieram deitadas (cabeça para a direita): `90` deixa a pessoa de pé.
   O fundo branco que encosta na borda vira transparente sozinho.
3. Instale a ferramenta de imagens (só na primeira vez): `pip install -r requirements-ferramentas.txt`
4. Rode: `python ferramentas/converter_arte.py`
5. Em `dados/arte.py`, dê um apelido para o arquivo: `"oca": "cenarios/cenario-oca.jpg",`

Se um arquivo de arte não existir, o jogo **não trava**: desenha um retângulo provisório
com o nome e continua.

Tamanhos: cenários 1600 × 900 (JPG), pessoas com 860 de altura (PNG com fundo **transparente**).

## 5. Rodar os testes

Com o ambiente ativado, dentro da pasta `Jogo`:
```
python -m testes.teste_fluxo
```
O teste joga sozinho, sem abrir janela: menu → opções → introdução inteira → Dia 1 (duas
vezes: deixando Yara entrar e não deixando) → tela provisória da Noite 1 → menu. Se terminar com **TUDO CERTO**, está funcionando. Se der erro, a última linha diz o problema.

Para salvar imagens das telas durante o teste:
```
CARAIBA_CAPTURAS=capturas python -m testes.teste_fluxo        (Linux/Mac)
set CARAIBA_CAPTURAS=capturas && python -m testes.teste_fluxo  (Windows)
```

## 6. Como o código está organizado

```
Jogo/
├── main.py            Começa o jogo (laço principal)
├── config.py          Paleta, tamanhos, pastas
├── estado.py          As variáveis da partida (vivos, mortos, sanidade...)
├── dados/             CONTEÚDO: textos e lista de imagens (edite aqui)
├── cenas/             Cada tela do jogo: menu, opções, introdução, dia, em_construcao
├── motor/             Peças reutilizáveis:
│   ├── jogo.py          janela, escala para qualquer monitor, troca de cenas
│   ├── cena.py          o modelo de toda cena + fade entre cenas
│   ├── ui.py            Botao e CaixaTexto (palavras marcadas, texto letra a letra)
│   ├── efeitos.py       filtro da noite/dia, linhas, grão, vinheta, luz do fogo
│   ├── imagens.py       carrega cada imagem uma vez só (e faz provisórios)
│   ├── fontes.py        carrega as fontes
│   ├── preferencias.py  tamanho do texto e tela cheia
│   └── salvamento.py    salva no computador (pasta saves/) ou no navegador
├── assets/            Imagens convertidas e fontes (DejaVu, licença livre)
├── ferramentas/       converter_arte.py
└── testes/            teste_fluxo.py
```

Uma regra visual importante: o **tratamento** (linhas, grão, vinheta) vai só sobre a
**cena**; a **interface** (texto e botões) é desenhada depois, limpa. Cada cena separa
isso em `desenhar_cena()` e `desenhar_interface()`.

## 7. Jogar no navegador (pygbag)

O código já está pronto para o navegador. Quando for a hora do playtest:
```
pip install pygbag
pygbag Jogo          (rodado da pasta Caraiba)
```
e abra <http://localhost:8000>. No navegador o botão **Sair** some e a tela cheia é
controlada pela página.
