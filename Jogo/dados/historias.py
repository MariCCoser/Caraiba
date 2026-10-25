# As conversas da noite: cada pessoa tem 10 falas na oca e 10 na fogueira, e cada noite em que
# o jogador conversa com ela aparece a próxima (a 1ª conversa mostra a fala 1, a 2ª a fala 2...).
# Edite à vontade: aqui não há lógica.
#
# Fonte: Textos/Caraíba — Conversas na Fogueira.pdf.
#   "Conversar" (OCA): o agora (como a pessoa se sente, a oca, os moradores). Vem antes do exame.
#   "Sentar perto" (FOGUEIRA): o passado (de onde veio, quem perdeu). Vem depois da decisão.
# Não gasta energia, não muda variável e não entrega sinal: nenhuma fala diz o que o exame
# ainda não mostra. Alguns amaldiçoados se contradizem (a maldição embaralha a memória);
# Yara, que está sã, se contradiz uma vez: é a falsa pista. As palavras que se contradizem
# ficam entre [colchetes] (em âmbar). Ninguém mente.
# Krenan nunca entra: só tem falas de fogueira (as noites em que ele está no fogo).

FOGUEIRA = {
    "Potira": [
        "As roças do outro lado do rio estão cheias. A mandioca está apodrecendo no chão. "
        "Não tive coragem de arrancar a roça de quem morreu.",
        "Minha mãe conversava com a mandioca. Dizia que ela precisa de gente perto para crescer. "
        "Eu ria dela. Agora sou eu que converso.",
        "Antes de ir para a mata, meu pai me ensinou a amarrar palha de três em três. "
        "Disse que casa pequena é a que fica de pé.",
        "Lembra da festa do cauim, quando a gente era pequena? Tinha tanta gente que não dava "
        "para ver o fogo. Hoje dá para ver o fogo de qualquer lugar.",
        "Iandé e eu aprendemos a ralar mandioca juntas. Ela ralava mais depressa e ria de mim. "
        "Ela sempre foi a que ia mais longe. Eu, a que esperava.",
        "Minha avó fazia panela de barro. Eu queria aprender. Ela morreu antes de me mostrar "
        "como não deixar rachar no fogo. Todas as minhas racham.",
        "Na aldeia vazia rio abaixo tinha uma rede pequena ainda amarrada. Quase desamarrei "
        "para trazer. Deixei. Alguém pode voltar para ela.",
        "Não durmo na rede da minha mãe. Ainda tem o cheiro dela. Prefiro o chão. "
        "No chão eu sei onde estou.",
        "Antes de dormir eu conto as redes. Quando eu era menina, não conseguia contar até o fim. "
        "Agora consigo.",
        "Se nascer criança aqui de novo, alguém precisa lembrar de dar nome. Eu lembro.",
    ],
    "Tamandaré-mirim": [
        "Os inimigos da minha aldeia me pegaram na guerra e me trocaram com os homens dos barcos. "
        "Eu valia três machados. Penso nisso toda vez que vejo um.",
        "Nos últimos três dias, [uma moça andou atrás de mim] ouvindo a pregação. "
        "Tossia muito, coitada. Eu pregava mais alto para ela ouvir.",
        "No engenho, quem parava era amarrado no tronco. Eu parei. Esta marca é de lá. "
        "Foi a minha primeira pregação: parar.",
        "[Me trocaram por um machado só]. Eu lembro do brilho dele na mão do homem. "
        "Um homem por um machado.",
        "Minha aldeia ficava onde hoje é canavial. Sei onde era a casa da minha avó pelo pé de "
        "jenipapo. Cortaram tudo, menos ele.",
        "No engenho aprendi todas as rezas dos padres. Eles rezam para um homem que morreu "
        "amarrado num pau. Eu entendi esse homem melhor do que eles.",
        "Fiz esta cruz de goiabeira. Se o deus deles mora numa cruz, agora mora comigo. "
        "E sou eu que digo para onde ele vai.",
        "Na terra sem mal ninguém planta, ninguém morre, ninguém é dono de ninguém. Os velhos já "
        "procuravam antes dos barcos. Os barcos só deram pressa.",
        "Os pajés não gostam de mim. Dizem que caraíba que grita não fala com espírito. Talvez. "
        "Mas o espírito também nunca falou baixo comigo.",
        "Meu irmão ficou no engenho. Tem medo do tronco. Logo eu desço o rio e prego tão alto "
        "que chega lá. Minha voz volta. Ela sempre volta.",
    ],
    "Iandé": [
        "Troquei toda a mandioca por anzóis de ferro. Amanhã mostro aos pescadores. "
        "Ninguém aqui vai acreditar no tamanho da vila.",
        "Um padre magro escreveu meu nome num caderno. Disse que era para eu não ser esquecida. "
        "Ninguém nunca tinha escrito meu nome.",
        "As costas doem de dormir torta, mas já passou. E na vila [eu não cheguei perto de "
        "ninguém]. Troquei a mandioca na beira do caminho e voltei.",
        "Eu dancei na festa de santo. [Segurei a mão de todo mundo na roda]. Eu não sabia. "
        "Eu juro que não sabia.",
        "Na vila tem um sino. Quando ele bate, todo mundo para o que está fazendo. "
        "Parece pajé chamando, só que de ferro.",
        "Potira sempre teve medo do rio. Eu atravessava para mostrar que dava. "
        "Ela ficava gritando da margem, e eu ria lá do outro lado.",
        "Meu irmão pequeno morreu no começo da maldição. Fui à vila também por ele. "
        "Queria ver de onde as coisas vêm.",
        "Eu sempre tive sorte, desde menina. O rio nunca me levou. Talvez a sorte seja só um "
        "jeito de dizer que ainda não foi a sua vez.",
        "Quero ensinar todo mundo a pescar com anzol. Com ferro, uma pessoa pesca por três. "
        "Vai sobrar gente para a roça.",
        "Quando tudo isso passar, levo você até a vila. É logo ali. Você vai ver.",
    ],
    "Yara": [
        "Este machado custou uma estação de farinha. Minha mãe acha que foi caro. "
        "Ela nunca derrubou uma árvore antes de o sol ficar alto.",
        "[Saí da costa faz duas noites]. Meu pai fazia esse caminho carregando tronco de árvore "
        "de tinta até a praia. Em troca, ganhou o primeiro anzol de ferro da aldeia.",
        "Sei umas palavras da língua deles. Farinha, ferro, amanhã. Eles dizem muito amanhã.",
        "Hoje a gente planta mais mandioca do que come. O resto vira farinha para os barcos. "
        "Minha avó dizia que isso era plantar para a fome dos outros.",
        "Eu ia me casar com um homem que foi trabalhar num barco. Disse que voltava na outra "
        "estação. Já passaram quatro.",
        "Minha mãe está perdendo os olhos. Ela me reconhece pelas mãos. "
        "Diz que as minhas ficaram duras desde o machado.",
        "Escolhi as contas azuis porque ela ainda vê o azul. Quando segurar, vai saber que fui "
        "eu que trouxe.",
        "Eu disse duas noites? [Foram três]. Numa eu não dormi. Fiquei olhando a vila de longe. "
        "Tinha uma casa com cruz na porta.",
        "Vou pelo caminho da vila. É mais curto. Se a maldição estiver lá, passo depressa.",
        "Se alguém perguntar por mim, diz que eu segui viva. Foi assim que você me viu.",
    ],
    "Mbaé": [
        "Nas aldeias do caminho jogaram cinza atrás de mim. Disseram que a minha gente é "
        "amaldiçoada. A gente é calada. Para quem tem medo, dá no mesmo.",
        "Troquei peixe numa aldeia rio abaixo. Tinha gente tossindo lá. A maldição começou ali. "
        "[Faz quatro dias, cinco].",
        "A gente pesca de mão, no raso, quando a água baixa. Tem que ficar parado muito tempo. "
        "Quem tem pressa não come.",
        "Este arco era do meu pai. É mais alto que eu. Ele dizia que arco grande é para atirar "
        "longe e não precisar chegar perto de ninguém.",
        "Tenho uma filha de sete invernos que nada melhor que eu. Prometi trazer sal. "
        "O sal ficou na vontade.",
        "Os homens dos barcos subiram o nosso rio uma vez. Queriam gente para trabalhar. "
        "A gente entrou no alagado. Quem fica conta a história, e a história sempre diz que "
        "quem fugiu era o perigoso.",
        "Minha mulher pinta minhas costas antes de cada viagem. Esta pintura é dela. "
        "Está saindo com o suor.",
        "[Não troquei peixe nenhum]. O peixe todo ficou na trilha quando a maldição pesou. "
        "Algum bicho comeu melhor que eu esta semana.",
        "Se eu não voltar, fala meu nome perto de água corrente. O rio leva até lá.",
        "Vocês me deixaram deitar. Lá em casa vão dizer que não acreditam. Eu mesmo não acreditei.",
    ],
    "Araci": [
        "[Piatã ficou na praia consertando a canoa. Disse que vem depois]. Quando ele chegar, "
        "você pensa num nome com ele? Eu não tenho mais força para pensar.",
        "Ele morreu sem saber da criança. Eu ia contar na lua cheia.",
        "Minha mãe ajudava as mulheres a parir. Eu segurava a cuia de água. "
        "Agora não tem ninguém para segurar a minha.",
        "Na minha aldeia os meninos aprendiam a nadar antes de andar. O mar era a nossa roça.",
        "Quando a maldição chegou, os velhos foram primeiro. Depois as crianças. "
        "Eu fiquei, e não sei por quê.",
        "No fim eu não tinha mais força para enterrar ninguém. Só fechei os olhos deles, um por um.",
        "Numa aldeia do caminho jogaram pedra em mim. Disseram que eu era amaldiçoada. "
        "Talvez seja. Fui a última.",
        "Ela mexe quando eu canto. Só sei uma canção, a que minha mãe cantava para o mar "
        "ficar manso.",
        "Se for menina, queria que tivesse nome de árvore. Árvore fica no lugar.",
        "Não precisa me prometer nada. Só fica perto até de manhã.",
    ],
    "Krenan": [
        "Não vim pedir teto. Vim avisar. A mata é grande.",
        "Quando eu era moço, descia o rio para trocar arco por rede aqui. O pai do cacique de "
        "vocês me ensinou esta língua. Eu errava tudo. Ele ria.",
        "O botoque se põe na criança e cresce com ela. Os de fora acham feio. "
        "Para nós, quem não tem ainda não terminou de crescer.",
        "Enterramos a metade antes de subir. Eu cavei. Um velho não devia cavar tanto.",
        "Lá em cima a água é fria e a comida é pouca. Mas ninguém chega sem a gente ouvir.",
        "Os de fora contam coisas terríveis da minha gente. Não é verdade. Mas, se o medo deles "
        "nos deixa em paz, deixo que contem.",
        "Meu filho pediu para descer no meu lugar. Eu disse que velho é quem desce. "
        "Velho já viu o que tem aqui embaixo.",
        "Eu conto quem passa na trilha. É costume. Ultimamente só conto para um lado.",
        "Não entro na oca. Vi o que acontece com quem dorme debaixo do mesmo teto da maldição. "
        "Aqui fora, o vento leva.",
        "Quem subir comigo não olha para trás. Quem sobe tem que olhar para cima.",
    ],
}

OCA = {
    "Potira": [
        "Esta rede era da filha do pescador. Deito do lado, não dentro.",
        "Durmo perto da porta. Se alguém chegar de noite, eu escuto primeiro.",
        "A oca está grande demais. A gente fala baixo e a palha responde.",
        "Varri o chão hoje. Minha mãe dizia que oca suja chama tristeza.",
        "Os moradores perguntam de você. Digo que você está fazendo o que pode.",
        "Fiz caldo de peixe com o que tinha. Ficou ralo. Ninguém reclamou.",
        "Às vezes acordo achando que ouvi minha mãe ralando mandioca. É só o vento na palha.",
        "Se precisar de lugar, eu durmo lá fora. Eu sei erguer abrigo.",
        "Contei as redes de novo. Não vou dizer o número.",
        "Fica mais um pouco. Quando você está aqui, a oca parece cheia.",
    ],
    "Tamandaré-mirim": [
        "Estou bem. Só a garganta. Pregar gasta a voz.",
        "[Não estou quente]. É o calor de tanta gente dormindo junto.",
        "A luz do fogo machuca o olho. É fumaça. Esta oca tem fumaça demais.",
        "[Estou queimando por dentro]. É o espírito chegando. Os caraíbas sentem isso antes de falar.",
        "Rezei pelos moradores antes de dormir. Eles não pediram. Rezei mesmo assim.",
        "Deixa a cruz encostada perto de mim. Se eu dormir, ela fica acordada.",
        "Os moradores me olham de lado. Acham que eu trouxe alguma coisa. Eu só trouxe palavra.",
        "Sonhei de novo com a avó. Desta vez ela não disse nada.",
        "Minhas mãos tremem. É frio. Nunca senti frio assim perto do mar.",
        "Abre a porta da oca. Quero ver se o rio ainda está lá.",
    ],
    "Iandé": [
        "A oca está tão quieta. Na vila ninguém dorme quieto.",
        "Trouxe um anzol para cada pescador. Guarda o seu, depois eu te dou.",
        "Estou bem. [Não dói nada]. Não precisa olhar minhas costas.",
        "Não chega perto. Fala daí. Não sei o que é isso no meu rosto.",
        "Me ajuda a pendurar a rede mais alto. Quero ver o telhado como na vila.",
        "Potira ralou mandioca para mim. Ela sempre ralou para mim.",
        "Conta aos pescadores que o anzol não enferruja se secar no sol.",
        "Ainda ouço o sino. Aqui não tem sino. Ouço mesmo assim.",
        "Se eu dormir muito, me acorda. Não quero perder a manhã.",
        "Abre a palha. Quero ver se ainda é noite.",
    ],
    "Yara": [
        "Meus olhos ardem de tanta fumaça de fogueira na trilha. Amanhã já melhora.",
        "Durmo com o machado do lado. Não é por vocês. É costume da costa.",
        "Na costa a oca é comprida assim também. Só que tem mais criança gritando.",
        "As redes de vocês são bem tecidas. Minha mãe ia gostar de pegar numa.",
        "Ouvi alguém chorando do outro lado da oca. Não fui ver. Às vezes a pessoa quer chorar sozinha.",
        "Deixei um pouco de farinha perto da rede do canto. A mulher não quis aceitar. "
        "Deixei mesmo assim.",
        "Se meu noivo voltar, ele vai procurar ferro. É só disso que ele lembra.",
        "Guarda um pouco de fogo para mim de manhã.",
        "Amanhã cedo eu vou. Não precisa acordar ninguém.",
        "Obrigada pelo teto. Na costa a gente não esquece quem abre a porta.",
    ],
    "Mbaé": [
        "Deita longe de mim. Me chamaram de amaldiçoado no caminho. Melhor não arriscar.",
        "[Não é nada, é cansaço da trilha]. Amanhã já ando.",
        "O frio vem e vai. Pouco.",
        "A oca de vocês é seca. A nossa, no alagado, está sempre úmida.",
        "Me dá água. Só um gole. Depois eu mesmo busco.",
        "Minha filha dorme encostada em mim. Esta noite estou sem ela.",
        "Não quero morrer deitado. Se for o caso, me põe sentado.",
        "O arco fica do lado da porta. Se eu não acordar, ele é seu.",
        "Ouço alguém tossindo na oca. Não. Sou eu.",
        "Amanhã já ando. Já disse isso ontem?",
    ],
    "Araci": [
        "[Piatã morreu. Enterrei ele perto da canoa]. Me deixa no canto, longe das outras.",
        "A criança mexe mais de noite. Parece que ela sabe que é de noite.",
        "Tem cuia? Eu mesma seguro.",
        "Não precisa me cobrir. Estou com calor e com frio ao mesmo tempo.",
        "Ouvi o mar? Aqui não tem mar.",
        "Canta você. Eu esqueci o começo.",
        "Se eu dormir, conta para ela que eu andei dois dias.",
        "As manchas não doem. O que dói é ninguém olhar.",
        "Qual é o nome desta aldeia? Quero lembrar.",
        "Abre a porta quando o sol vier. Ela tem que ver o sol.",
    ],
}

# Os botões (cenas/dia.py).
CONVERSAR = "Conversar"          # a fala da oca, antes do exame
SENTAR_PERTO = "Sentar perto"    # a fala da fogueira, depois da decisão
VOLTAR = "Voltar para a fogueira"
# Uma fala longa aparece em partes de até este tamanho (letras), quebrando no fim de uma frase.
TAMANHO_DA_PARTE = 120
