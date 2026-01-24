"""
Antecedentes D&D 5e

Fontes:
- PHB (Player's Handbook / Livro do Jogador)
- XGE (Xanathar's Guide to Everything / Guia de Xanathar)
- TCE (Tasha's Cauldron of Everything / Caldeirão de Tasha)
- MPMM (Monsters of the Multiverse / Monstros do Multiverso)
- VSS (Valda's Spire of Secrets)
- OotA (Out of the Abyss / Fora do Abismo - Campanha)

Nota: Cada antecedente fornece:
- 2 perícias proficientes
- Ferramentas e/ou idiomas extras
- Equipamento inicial (não implementado - narrativo)
- Característica especial (roleplay)
"""

from ..database import get_connection, json_dumps


# ==================== DADOS DE ANTECEDENTES ====================

ANTECEDENTES_PHB = [
    {
        'nome': 'Acólito',
        'pericias': ['intuição', 'religião'],
        'idiomas_escolha': 2,
        'ferramentas': [],
        'caracteristica': 'Abrigo dos Fiéis: Você e companheiros podem receber cura gratuita em templos de sua fé.',
        'personalidade': [
            'Idolatro um herói particular da minha fé.',
            'Posso encontrar pontos em comum entre os inimigos mais ferozes.',
            'Vejo presságios em cada evento e ação.',
            'Nada pode abalar minha atitude otimista.',
            'Cito textos sagrados em quase todas as situações.',
            'Sou tolerante (ou intolerante) com outras fés.',
            'Tive uma comida e acomodação modestas em meus templos.',
            'Passei tanto tempo no templo que tenho pouca experiência com o mundo exterior.'
        ],
        'ideais': [
            'Tradição - As tradições antigas devem ser preservadas.',
            'Caridade - Sempre tento ajudar os necessitados.',
            'Mudança - Devemos ajudar a trazer mudanças que nossos deuses querem.',
            'Poder - Espero um dia ser líder do meu templo.',
            'Fé - Confio que minha deidade guiará minhas ações.',
            'Aspiração - Busco me provar digno do favor do meu deus.'
        ],
        'vinculos': [
            'Morreria para recuperar uma relíquia antiga da minha fé.',
            'Um dia me vingarei contra o templo corrupto que me marcou como herege.',
            'Devo minha vida ao sacerdote que me acolheu quando meus pais morreram.',
            'Tudo que faço é pelo povo comum.',
            'Farei qualquer coisa para proteger o templo onde servi.',
            'Busco preservar um texto sagrado que meus inimigos querem destruir.'
        ],
        'defeitos': [
            'Julgo os outros severamente, e a mim mesmo mais severamente ainda.',
            'Confio demais nos que detêm poder na hierarquia do meu templo.',
            'Minha piedade às vezes me leva a confiar cegamente em outros da minha fé.',
            'Sou inflexível em meu pensamento.',
            'Sou desconfiado de estranhos e espero o pior deles.',
            'Uma vez escolho um objetivo, fico obcecado em detrimento de tudo mais.'
        ]
    },
    {
        'nome': 'Charlatão',
        'pericias': ['enganação', 'prestidigitação'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Kit de falsificação'],
        'caracteristica': 'Identidade Falsa: Você tem uma segunda identidade documentada e pode forjar documentos.',
        'personalidade': [
            'Me apaixono e desapaixono facilmente.',
            'Tenho uma piada para toda ocasião.',
            'Bajulação é minha tática preferida para conseguir o que quero.',
            'Sou um jogador nato que não resiste a uma aposta.',
            'Minto sobre quase tudo, mesmo sem motivo.',
            'Sarcasmo e insultos são minhas armas favoritas.',
            'Mantenho símbolos sagrados de várias deidades.',
            'Roubo qualquer coisa que vejo.'
        ],
        'ideais': [
            'Independência - Sou um espírito livre.',
            'Justiça - Nunca marco os que não podem perder.',
            'Caridade - Distribuo o dinheiro que roubo aos necessitados.',
            'Criatividade - Nunca aplico o mesmo golpe duas vezes.',
            'Amizade - O importante não é o ouro, são os amigos.',
            'Aspiração - Vou fazer um nome para mim mesmo.'
        ],
        'vinculos': [
            'Roubei uma pessoa poderosa que agora quer minha cabeça.',
            'Devo tudo ao meu mentor - uma pessoa horrível.',
            'Alguém que amei morreu por causa minha.',
            'Meu golpe foi contra a pessoa errada, preciso consertar.',
            'Tenho um rival que vai cair com meu próximo golpe.',
            'Quero ficar rico o suficiente para não precisar mais trabalhar.'
        ],
        'defeitos': [
            'Não resisto a um rosto bonito.',
            'Sempre tenho dívidas a pagar.',
            'Meu primeiro instinto é fugir quando as coisas ficam difíceis.',
            'Minha ganância me supera.',
            'Não consigo resistir a trapacear se vejo uma oportunidade.',
            'Fiz um inimigo poderoso que não ficará satisfeito até me ver morto.'
        ]
    },
    {
        'nome': 'Criminoso',
        'pericias': ['enganação', 'furtividade'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de ladrão', 'Kit de jogos (um à escolha)'],
        'caracteristica': 'Contato Criminal: Você tem um contato confiável que pode obter informações ilegais.',
        'personalidade': [
            'Sempre tenho um plano para quando as coisas dão errado.',
            'Sou sempre calmo, não importa a situação.',
            'A primeira coisa que faço em um lugar novo é mapear as saídas.',
            'Prefiro fazer um novo amigo a um novo inimigo.',
            'Não ligo para os riscos - nunca pense antes de agir.',
            'A melhor maneira de me fazer fazer algo é me dizer para não fazer.',
            'Explodo na menor ofensa.',
            'Quando vejo algo valioso, mal consigo pensar em outra coisa.'
        ],
        'ideais': [
            'Honra - Não roubo de outros criminosos.',
            'Liberdade - Correntes devem ser quebradas.',
            'Caridade - Roubo dos ricos para dar aos necessitados.',
            'Ganância - Faço qualquer coisa por um pagamento.',
            'Povo - Sou leal aos meus amigos, não a ideais.',
            'Redenção - Há uma faísca de bondade em todos.'
        ],
        'vinculos': [
            'Estou tentando pagar uma dívida antiga a uma pessoa generosa.',
            'Meus ganhos vão para sustentar minha família.',
            'Roubei algo valioso de uma pessoa poderosa.',
            'Tenho uma dívida que não posso pagar.',
            'Meu crime me tirou algo precioso - vou recuperar.',
            'Alguém que amei morreu por minha causa.'
        ],
        'defeitos': [
            'Quando vejo algo valioso, não consigo pensar em outra coisa.',
            'Quando encaro uma escolha entre dinheiro e amigos, escolho dinheiro.',
            'Se há um plano, vou esquecê-lo.',
            'Tenho um "tell" que revela quando estou mentindo.',
            'Fujo ao primeiro sinal de perigo.',
            'Uma pessoa inocente está na prisão por um crime que cometi.'
        ]
    },
    {
        'nome': 'Artista',
        'pericias': ['acrobacia', 'atuação'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Instrumento musical (um à escolha)'],
        'caracteristica': 'Por Demanda Popular: Pode encontrar abrigo em tavernas e locais de entretenimento.',
        'personalidade': [
            'Conheço uma história relevante para toda situação.',
            'Quando entro em uma cidade, coleciono rumores e fofocos.',
            'Sou um romântico sem esperança, sempre buscando "aquele especial".',
            'Ninguém fica bravo comigo por muito tempo.',
            'Adoro um bom insulto, mesmo contra mim.',
            'Fico inquieto se fico muito tempo no mesmo lugar.',
            'Sou apaixonado por melodias e rimas.',
            'Minha vaidade às vezes me supera.'
        ],
        'ideais': [
            'Beleza - O que é bonito aponta para o verdadeiro.',
            'Tradição - As histórias devem ser preservadas.',
            'Criatividade - O mundo precisa de novas ideias.',
            'Ganância - Só me importo com a recompensa.',
            'Povo - Gosto de ver sorrisos.',
            'Honestidade - A arte deve refletir a alma.'
        ],
        'vinculos': [
            'Meu instrumento é minha posse mais preciosa.',
            'Alguém roubou minha obra preciosa.',
            'Quero ser famoso custe o que custar.',
            'Idolatro um herói das histórias que conto.',
            'Farei qualquer coisa para provar minha superioridade sobre um rival.',
            'Faria qualquer coisa pelos membros da minha antiga trupe.'
        ],
        'defeitos': [
            'Farei qualquer coisa para ganhar fama.',
            'Sou um otário por um rosto bonito.',
            'Um escândalo me impede de voltar para casa.',
            'Uma vez zombei de um nobre que ainda quer minha cabeça.',
            'Tenho dificuldade em manter segredos.',
            'Caio em meus próprios truques.'
        ]
    },
    {
        'nome': 'Herói do Povo',
        'pericias': ['adestrar animais', 'sobrevivência'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de artesão (uma à escolha)', 'Veículos terrestres'],
        'caracteristica': 'Hospitalidade Rústica: O povo comum te abriga e protege.',
        'personalidade': [
            'Julgo pessoas por suas ações, não palavras.',
            'Se alguém está em perigo, sempre ajudo.',
            'Quando me decido, nada me para.',
            'Tenho um senso de justiça forte.',
            'Confio em meus instintos.',
            'Os maneirismos da cidade são novos para mim.',
            'Sou incrivelmente lento a confiar.',
            'Não me importo com minha própria segurança.'
        ],
        'ideais': [
            'Respeito - As pessoas merecem ser tratadas com dignidade.',
            'Justiça - Ninguém está acima da lei.',
            'Liberdade - Tiranos devem ser derrubados.',
            'Poder - Se eu me tornar forte, posso proteger.',
            'Sinceridade - Não faz sentido fingir ser algo que não sou.',
            'Destino - Ninguém pode escapar de seu destino.'
        ],
        'vinculos': [
            'Tenho uma família que depende de mim.',
            'Lutarei para proteger a terra onde cresci.',
            'Uma pessoa terrível destruiu minha comunidade.',
            'Tenho uma ferramenta do meu mentor.',
            'Protegerei os indefesos.',
            'Um amor de infância me espera em casa.'
        ],
        'defeitos': [
            'O tirano que governa minha terra não parará até me ver morto.',
            'Estou convencido de minha superioridade moral.',
            'Tenho fraqueza pelos vícios da cidade.',
            'Secretamente acredito que todos estão abaixo de mim.',
            'Desprezo aqueles que não podem se defender.',
            'Sou violentamente protetor.'
        ]
    },
    {
        'nome': 'Artesão de Guilda',
        'pericias': ['intuição', 'persuasão'],
        'idiomas_escolha': 1,
        'ferramentas': ['Ferramentas de artesão (uma à escolha)'],
        'caracteristica': 'Membro de Guilda: Sua guilda oferece hospedagem, ajuda legal e contatos.',
        'personalidade': [
            'Acredito que tudo que vale fazer, vale fazer bem feito.',
            'Sou um esnobe que olha para os que não apreciam arte fina.',
            'Sempre quero saber como as coisas funcionam.',
            'Anoto tudo em um diário.',
            'Tenho opiniões fortes sobre comida.',
            'Sou direto sobre negócios.',
            'Gosto de falar sobre meu ofício por horas.',
            'Faria qualquer coisa por minha guilda.'
        ],
        'ideais': [
            'Comunidade - É dever de todos fortalecer a comunidade.',
            'Generosidade - Meus talentos são para compartilhar.',
            'Liberdade - Todos devem fazer o que escolherem.',
            'Ganância - Só me importo com ouro.',
            'Povo - Sou comprometido com as pessoas, não ideais.',
            'Aspiração - Trabalho duro para ser o melhor.'
        ],
        'vinculos': [
            'A oficina onde aprendi é o lugar mais importante.',
            'Criei uma obra-prima que foi roubada.',
            'Devo muito à minha guilda.',
            'Persigo riqueza para o amor de alguém.',
            'Um dia voltarei para minha guilda como mestre.',
            'Vou vingar os artesãos destruídos pela competição desleal.'
        ],
        'defeitos': [
            'Farei qualquer coisa por ouro.',
            'Estou convencido de que ninguém faz trabalho tão bom quanto eu.',
            'Sou rápido em assumir que alguém quer me trapacear.',
            'Nenhum segredo é seguro comigo - adoro fofocar.',
            'Uma vez comecei um trabalho, fico obsessivo.',
            'Sou um gastador compulsivo.'
        ]
    },
    {
        'nome': 'Eremita',
        'pericias': ['medicina', 'religião'],
        'idiomas_escolha': 1,
        'ferramentas': ['Kit de herbalismo'],
        'caracteristica': 'Descoberta: Você fez uma descoberta importante durante seu isolamento.',
        'personalidade': [
            'Fiquei tanto tempo isolado que falo raramente.',
            'Sou completamente sereno, mesmo diante do desastre.',
            'O líder do meu antigo monastério disse algo que não entendo.',
            'Sinto empatia tremenda por todos que sofrem.',
            'Sou alheio à etiqueta social.',
            'Conecto tudo à minha descoberta.',
            'Estou trabalhando em uma grande teoria.',
            'Prefiro animais a pessoas.'
        ],
        'ideais': [
            'Maior Bem - Minhas dádivas são para compartilhar.',
            'Lógica - Emoções não devem nublar pensamento.',
            'Espírito Livre - Investigação e curiosidade são tudo.',
            'Poder - A solidão é o caminho para o poder.',
            'Viver e Deixar Viver - Não interfiro.',
            'Autoconhecimento - Se me conhecer, posso conhecer o universo.'
        ],
        'vinculos': [
            'Nada é mais importante que outros membros do meu eremitério.',
            'Entrei em reclusão para fugir de algo.',
            'Ainda busco a iluminação que procurava.',
            'Entrei em reclusão por amor a alguém.',
            'Meu isolamento me deu visão de um grande mal.',
            'Estou buscando iluminação.'
        ],
        'defeitos': [
            'Agora que voltei ao mundo, aproveito demais.',
            'Tenho ideias sombrias e niilistas.',
            'Sou dogmático sobre minhas crenças.',
            'Deixo os outros se arriscarem enquanto fico seguro.',
            'Penso demais para meu próprio bem.',
            'Minha descoberta poderia destruir o mundo.'
        ]
    },
    {
        'nome': 'Nobre',
        'pericias': ['história', 'persuasão'],
        'idiomas_escolha': 1,
        'ferramentas': ['Kit de jogos (um à escolha)'],
        'caracteristica': 'Posição de Privilégio: Pessoas comuns te tratam com respeito, e você tem acesso a alta sociedade.',
        'personalidade': [
            'Minha bajulação eloquente faz todos se sentirem maravilhosos.',
            'O povo comum me ama por minha bondade.',
            'Ninguém pode duvidar olhando para mim que estou acima dos plebeus.',
            'Tomo muito cuidado com minha aparência.',
            'Não gosto de sujar as mãos.',
            'Não importa o que eu sofri, mantenho minha postura.',
            'Tenho um senso de humor refinado.',
            'Os plebeus me adoram ou me odeiam.'
        ],
        'ideais': [
            'Respeito - Respeito é devido a mim, e eu dou aos dignos.',
            'Responsabilidade - Devo proteger os abaixo de mim.',
            'Independência - Devo provar que posso me virar sozinho.',
            'Poder - Se eu ganhar mais poder, ninguém me dirá o que fazer.',
            'Família - O sangue é mais espesso que água.',
            'Dever Nobre - Devo proteger os que não podem se proteger.'
        ],
        'vinculos': [
            'Enfrentarei qualquer desafio para ganhar aprovação da família.',
            'A aliança da minha casa com outra família deve ser mantida.',
            'Nada é mais importante que outros membros da minha família.',
            'Estou apaixonado por alguém que minha família não aceita.',
            'Minha lealdade ao meu suserano é inabalável.',
            'O povo comum deve me ver como seu herói.'
        ],
        'defeitos': [
            'Secretamente acredito que todos estão abaixo de mim.',
            'Escondo um segredo vergonhoso.',
            'Frequentemente ouço insultos velados e fico furioso.',
            'Tenho um desejo insaciável por prazeres carnais.',
            'O mundo gira ao meu redor.',
            'Por minhas palavras e ações, trago vergonha à família.'
        ]
    },
    {
        'nome': 'Forasteiro',
        'pericias': ['atletismo', 'sobrevivência'],
        'idiomas_escolha': 1,
        'ferramentas': ['Instrumento musical (um à escolha)'],
        'caracteristica': 'Viajante: Você tem memória excelente para mapas e terreno.',
        'personalidade': [
            'Sou movido por sede de aventura.',
            'Observo tudo, colecionando informações.',
            'Sou educado mas reservado com estranhos.',
            'O dinheiro não tem significado para mim.',
            'Me expresso com música.',
            'Sou lento a confiar e julgo os outros por ações.',
            'Não gosto de ficar parado.',
            'Prefiro natureza a cidades.'
        ],
        'ideais': [
            'Mudança - A vida é como as estações.',
            'Maior Bem - É responsabilidade de todos ajudar.',
            'Honra - Se eu me desonrar, me desonro a todos.',
            'Poder - O mais forte lidera.',
            'Natureza - O mundo natural é mais importante que civilização.',
            'Glória - Devo ganhar glória em batalha.'
        ],
        'vinculos': [
            'Minha família, clã ou tribo é o mais importante.',
            'Uma lesão na terra é uma lesão em mim.',
            'Eu trarei terrível vingança contra forças malignas.',
            'Sou o último da minha tribo.',
            'Meu sofrimento me tirou de minha terra.',
            'Recuperarei um artefato roubado.'
        ],
        'defeitos': [
            'Sou lento a confiar em membros de outras raças.',
            'Violência é minha resposta a desafios.',
            'Não guardo segredos.',
            'Sou muito apegado à natureza.',
            'Considero combate a solução para problemas.',
            'As cidades me confundem e irrito facilmente.'
        ]
    },
    {
        'nome': 'Sábio',
        'pericias': ['arcanismo', 'história'],
        'idiomas_escolha': 2,
        'ferramentas': [],
        'caracteristica': 'Pesquisador: Se você não sabe algo, sabe onde descobrir.',
        'personalidade': [
            'Uso palavras polissilábicas que impressionam.',
            'Li todos os livros nas maiores bibliotecas.',
            'Ajudo os que não são tão espertos.',
            'Não há nada que eu ame mais que um bom mistério.',
            'Estou disposto a ouvir todos os lados.',
            'Falo... muito... devagar... pensando.',
            'Sou horrível em segredos.',
            'Fico nervoso quando coisas não fazem sentido.'
        ],
        'ideais': [
            'Conhecimento - O caminho para o poder é o conhecimento.',
            'Beleza - O que é bonito aponta para o verdadeiro.',
            'Lógica - Emoções não devem nublar julgamento.',
            'Sem Limites - Nada deve limitar possibilidades infinitas.',
            'Poder - Conhecimento é o caminho para o poder.',
            'Autoaperfeiçoamento - O objetivo é aprimorar-se.'
        ],
        'vinculos': [
            'É meu dever proteger meus estudantes.',
            'Tenho um texto antigo com segredos terríveis.',
            'Trabalho para preservar uma biblioteca ou academia.',
            'O trabalho da minha vida é uma série de tomos.',
            'Busco respostas sobre minha descoberta.',
            'Vendi minha alma pelo conhecimento.'
        ],
        'defeitos': [
            'Sou facilmente distraído por promessas de informação.',
            'Acredito que a maioria não consegue entender o que entendo.',
            'Mantenho segredos mesmo quando deveria contar.',
            'Não consigo resistir a contar um mistério.',
            'Critico demais meu trabalho.',
            'Prefiro soluções complexas.'
        ]
    },
    {
        'nome': 'Marinheiro',
        'pericias': ['atletismo', 'percepção'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de navegação', 'Veículos aquáticos'],
        'caracteristica': 'Passagem de Navio: Você pode garantir passagem gratuita em navios.',
        'personalidade': [
            'Meus amigos sabem que podem contar comigo.',
            'Trabalho duro para poder me divertir depois.',
            'Gosto de navegar para novos portos.',
            'Estico a verdade para uma boa história.',
            'Para mim, uma briga é uma boa maneira de se conhecer.',
            'Nunca passo uma aposta amigável.',
            'Minha linguagem é tão suja quanto um ninho de otyughs.',
            'Gosto de um trabalho bem feito.'
        ],
        'ideais': [
            'Respeito - A coisa que mantém um navio junto é respeito.',
            'Justiça - Todos fazemos o trabalho, dividimos as recompensas.',
            'Liberdade - O mar é liberdade.',
            'Mestria - Sou um predador, não uma presa.',
            'Povo - Estou comprometido com as pessoas.',
            'Aspiração - Um dia terei meu próprio navio.'
        ],
        'vinculos': [
            'Sou leal ao meu capitão primeiro, tudo mais depois.',
            'O navio é o mais importante - tripulantes vêm e vão.',
            'Sempre lembrarei do meu primeiro navio.',
            'Em um porto, tenho um amor esperando.',
            'Fui trapaceado por minha parte justa.',
            'Piratas impiedosos mataram minha tripulação.'
        ],
        'defeitos': [
            'Sigo ordens mesmo quando claramente erradas.',
            'Digo qualquer coisa para evitar trabalho extra.',
            'Uma vez que começo a beber, é difícil parar.',
            'Não resisto a uma aposta.',
            'Meu orgulho provavelmente me destruirá.',
            'Os monstros marinhos me assombram.'
        ]
    },
    {
        'nome': 'Soldado',
        'pericias': ['atletismo', 'intimidação'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de jogos (um à escolha)', 'Veículos terrestres'],
        'caracteristica': 'Patente Militar: Soldados te reconhecem e dão hospedagem básica.',
        'personalidade': [
            'Sou sempre educado e respeitoso.',
            'Sou assombrado por memórias de guerra.',
            'Perdi muitos amigos e reluto em fazer novos.',
            'Conheço muitas histórias inspiradoras de guerra.',
            'Encaro problemas de frente - é direto e simples.',
            'Gosto de um bom braço de ferro.',
            'Tenho um senso de humor grosseiro.',
            'Nunca recuo de uma briga.'
        ],
        'ideais': [
            'Maior Bem - Nossa sorte é dar nossas vidas pelos outros.',
            'Responsabilidade - Faço o que devo e obedeço autoridade.',
            'Independência - Quando as pessoas seguem ordens cegamente, abraçam tirania.',
            'Poder - Na vida como na guerra, o mais forte vence.',
            'Viver e Deixar Viver - Ideais não valem a pena matar.',
            'Nação - Minha cidade, nação ou povo é tudo que importa.'
        ],
        'vinculos': [
            'Daria minha vida pelos que serviram comigo.',
            'Alguém salvou minha vida no campo de batalha.',
            'Minha honra é minha vida.',
            'Nunca esquecerei a derrota esmagadora que sofri.',
            'Os que lutam ao meu lado são dignos de morrer por.',
            'Luto por aqueles que não podem lutar por si.'
        ],
        'defeitos': [
            'O inimigo monstruoso que enfrentamos me deixou com medo.',
            'Tenho pouco respeito por quem não é guerreiro provado.',
            'Cometi um erro terrível em batalha que custou vidas.',
            'Meu ódio pelos inimigos é cego e irracional.',
            'Obedeço a lei mesmo quando traz miséria.',
            'Preferiria comer minha armadura a admitir que errei.'
        ]
    },
    {
        'nome': 'Órfão',
        'pericias': ['furtividade', 'prestidigitação'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Ferramentas de ladrão'],
        'caracteristica': 'Segredos da Cidade: Você conhece passagens secretas pela cidade.',
        'personalidade': [
            'Escondo comida e bugigangas em meus bolsos.',
            'Faço muitas perguntas.',
            'Gosto de me espremer em espaços pequenos.',
            'Durmo com as costas na parede, com tudo que possuo.',
            'Como como um porco e tenho péssimos modos.',
            'Acho que qualquer um que seja gentil esconde algo.',
            'Não gosto de tomar banho.',
            'Digo sem rodeios o que os outros insinuam.'
        ],
        'ideais': [
            'Respeito - Todos, ricos ou pobres, merecem respeito.',
            'Comunidade - Devemos cuidar uns dos outros.',
            'Mudança - Os baixos serão erguidos e os altos derrubados.',
            'Retribuição - Os ricos precisam ver o que a vida é para os pobres.',
            'Povo - Ajudo quem me ajuda.',
            'Aspiração - Vou provar que sou digno de uma vida melhor.'
        ],
        'vinculos': [
            'Minha cidade é meu lar e lutarei para defendê-la.',
            'Patrocino um orfanato para evitar que outros sofram.',
            'Devo minha sobrevivência a outro órfão que me ensinou.',
            'Tenho uma dívida que nunca poderei pagar.',
            'Escapei da pobreza roubando e estou limpo agora.',
            'Ninguém mais deveria sofrer como eu sofri.'
        ],
        'defeitos': [
            'Se estou em vantagem, também roubo dos que me ajudam.',
            'Nunca confiarei em outro órfão.',
            'É minha culpa que meu mentor esteja na prisão.',
            'Se há um problema, fujo.',
            'Ouro me parece muito dinheiro mesmo em pequenas quantias.',
            'Nunca perdoarei totalmente os ricos.'
        ]
    }
]


# ==================== GUIA DE XANATHAR (XGE) ====================

ANTECEDENTES_XGE = [
    {
        'nome': 'Investigador da Cidade',
        'fonte': 'XGE',
        'pericias': ['intuição', 'investigação'],
        'idiomas_escolha': 2,
        'ferramentas': [],
        'caracteristica': 'Olho para os Detalhes: Você pode ler lábios e tem facilidade para notar pistas.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Clã Artesão',
        'fonte': 'XGE',
        'pericias': ['história', 'intuição'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de artesão (uma à escolha)', 'Ferramentas de joalheiro'],
        'caracteristica': 'Respeito dos Fabricantes de Coisas: Artesãos te oferecem hospedagem e trabalho.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Cortesão',
        'fonte': 'XGE',
        'pericias': ['intuição', 'persuasão'],
        'idiomas_escolha': 2,
        'ferramentas': [],
        'caracteristica': 'Acesso à Corte: Você pode conseguir audiências com nobres.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Agente de Facção',
        'fonte': 'XGE',
        'pericias': ['intuição'],  # + 1 à escolha baseada na facção
        'idiomas_escolha': 2,
        'ferramentas': [],
        'caracteristica': 'Cofre Seguro: Sua facção oferece alojamento e suporte secreto.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Viajante Distante',
        'fonte': 'XGE',
        'pericias': ['intuição', 'percepção'],
        'idiomas_escolha': 1,
        'ferramentas': ['Instrumento musical (um à escolha)', 'Kit de jogos (um à escolha)'],
        'caracteristica': 'Todos os Olhos em Você: Seu exotismo atrai atenção e hospitalidade curiosa.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Herdeiro',
        'fonte': 'XGE',
        'pericias': ['sobrevivência'],  # + 1 baseada na herança
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de jogos (um à escolha)', 'Instrumento musical (um à escolha)'],
        'caracteristica': 'Herança: Você carrega um objeto de valor inestimável para você ou sua família.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Cavaleiro da Ordem',
        'fonte': 'XGE',
        'pericias': ['persuasão'],  # + 1 baseada na ordem
        'idiomas_escolha': 1,
        'ferramentas': ['Kit de jogos (um à escolha)', 'Instrumento musical (um à escolha)'],
        'caracteristica': 'Hospitalidade Cavaleiresca: Sua ordem te fornece abrigo e suprimentos.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Mercenário Veterano',
        'fonte': 'XGE',
        'pericias': ['atletismo', 'persuasão'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de jogos (um à escolha)', 'Veículos terrestres'],
        'caracteristica': 'Vida de Mercenário: Você conhece companhias de mercenários e pode encontrar trabalho.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Membro Urbano de Guilda',
        'fonte': 'XGE',
        'pericias': ['enganação', 'furtividade'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Ferramentas de ladrão'],
        'caracteristica': 'Ouvido no Chão: Você sabe como obter informações dos submundos urbanos.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Caçador de Recompensas Urbano',
        'fonte': 'XGE',
        'pericias': ['intuição', 'sobrevivência'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de jogos (um à escolha)', 'Ferramentas de ladrão'],
        'caracteristica': 'Olho para Foragidos: Você sabe onde procurar fugitivos e tem contatos na área.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Guarda da Cidade',
        'fonte': 'XGE',
        'pericias': ['atletismo', 'intuição'],
        'idiomas_escolha': 2,
        'ferramentas': [],
        'caracteristica': 'Olho do Observador: Você pode conseguir acesso a áreas restritas e informações de guardas.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Agente Secreto',
        'fonte': 'XGE',
        'pericias': ['enganação', 'furtividade'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Kit de falsificação'],
        'caracteristica': 'Falsa Identidade: Você tem uma identidade falsa bem estabelecida.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
]


# ==================== CALDEIRÃO DE TASHA (TCE) ====================

ANTECEDENTES_TCE = [
    {
        'nome': 'Personalizado',
        'fonte': 'TCE',
        'pericias': [],  # 2 à escolha
        'idiomas_escolha': 2,  # ou ferramentas
        'ferramentas': [],  # 2 à escolha
        'caracteristica': 'Personalizado: Trabalhe com seu DM para criar uma característica única.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
]


# ==================== FORA DO ABISMO (OotA) ====================

ANTECEDENTES_OOTA = [
    {
        'nome': 'Prisioneiro do Underdark',
        'fonte': 'OotA',
        'pericias': ['furtividade', 'sobrevivência'],
        'idiomas_escolha': 0,
        'ferramentas': [],
        'caracteristica': 'Sobrevivente do Cárcere: Você sobreviveu à prisão drow e conhece os horrores do Underdark.',
        'personalidade': [
            'Desconfio de todos - qualquer um pode ser um inimigo.',
            'Estou sempre alerta, pronto para fugir.',
            'A escuridão não me assusta mais.',
            'Farei qualquer coisa para nunca mais ser prisioneiro.',
            'Tenho pesadelos frequentes sobre o cárcere.',
            'Aprendi a encontrar beleza nos lugares mais sombrios.'
        ],
        'ideais': [
            'Liberdade - Nunca mais serei acorrentado.',
            'Sobrevivência - Farei o que for preciso para viver.',
            'Vingança - Os drow pagarão pelo que fizeram.',
            'Esperança - Se sobrevivi ao Underdark, posso sobreviver a qualquer coisa.',
            'Proteção - Protegerei outros do destino que sofri.',
            'Conhecimento - Aprendi segredos nas profundezas.'
        ],
        'vinculos': [
            'Devo minha vida a um companheiro de cela.',
            'Deixei alguém para trás - devo voltar por ele.',
            'Os drow destruíram minha vida anterior.',
            'Tenho informações valiosas sobre o Underdark.',
            'Alguém na superfície pensa que estou morto.',
            'Vi algo terrível nas profundezas que preciso relatar.'
        ],
        'defeitos': [
            'Pânico em espaços confinados.',
            'Dificuldade em confiar em elfos, mesmo não-drow.',
            'Acordo gritando várias noites.',
            'Acumulo comida obsessivamente.',
            'Fico paralisado quando ouço chicotes.',
            'Tenho medo irracional do escuro total.'
        ]
    },
    {
        'nome': 'Refugiado de Blingdenstone',
        'fonte': 'OotA',
        'pericias': ['furtividade', 'percepção'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de joalheiro', 'Ferramentas de minerador'],
        'caracteristica': 'Conhecimento das Pedras: Você conhece os túneis de Blingdenstone e sabe navegar o Underdark.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Exilado de Menzoberranzan',
        'fonte': 'OotA',
        'pericias': ['enganação', 'furtividade'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de venenos'],
        'caracteristica': 'Conhecimento Drow: Você conhece a política e os segredos da cidade drow.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Peregrino de Neverlight Grove',
        'fonte': 'OotA',
        'pericias': ['medicina', 'natureza'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de herbalismo'],
        'caracteristica': 'Comunhão com Esporos: Você pode se comunicar com myconids e entende seus ciclos.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Comerciante de Gracklstugh',
        'fonte': 'OotA',
        'pericias': ['intimidação', 'persuasão'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de ferreiro'],
        'caracteristica': 'Contatos Derro: Você conhece os mercados negros da cidade dos duergar.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Sobrevivente de Sloobludop',
        'fonte': 'OotA',
        'pericias': ['percepção', 'religião'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de navegação'],
        'caracteristica': 'Testemunha do Caos: Você viu a loucura de Demogorgon e sobreviveu.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
]


# ==================== VALDA'S SPIRE OF SECRETS (VSS) ====================

ANTECEDENTES_VSS = [
    {
        'nome': 'Aprendiz de Alquimista',
        'fonte': 'VSS',
        'pericias': ['arcanismo', 'natureza'],
        'idiomas_escolha': 0,
        'ferramentas': ['Suprimentos de alquimista', 'Kit de herbalismo'],
        'caracteristica': 'Olho do Alquimista: Você identifica substâncias e pode encontrar ingredientes raros.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Guarda-costas',
        'fonte': 'VSS',
        'pericias': ['intimidação', 'percepção'],
        'idiomas_escolha': 1,
        'ferramentas': [],
        'caracteristica': 'Avaliação de Ameaças: Você identifica perigos e pontos fracos em segurança.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Cultista Arrependido',
        'fonte': 'VSS',
        'pericias': ['enganação', 'religião'],
        'idiomas_escolha': 1,
        'ferramentas': [],
        'caracteristica': 'Conhecimento Obscuro: Você conhece os rituais e segredos de um culto maligno.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Diplomata',
        'fonte': 'VSS',
        'pericias': ['intuição', 'persuasão'],
        'idiomas_escolha': 2,
        'ferramentas': [],
        'caracteristica': 'Imunidade Diplomática: Você pode invocar proteções diplomáticas em certas situações.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Gladiador de Arena',
        'fonte': 'VSS',
        'pericias': ['atuação', 'intimidação'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Instrumento musical (um à escolha)'],
        'caracteristica': 'Fama da Arena: Você é reconhecido como lutador e pode encontrar trabalho em arenas.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Caçador de Monstros',
        'fonte': 'VSS',
        'pericias': ['natureza', 'sobrevivência'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de herbalismo', 'Ferramentas de curtidor'],
        'caracteristica': 'Conhecimento de Monstros: Você sabe os pontos fracos de monstros comuns.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Médico',
        'fonte': 'VSS',
        'pericias': ['medicina', 'natureza'],
        'idiomas_escolha': 1,
        'ferramentas': ['Kit de herbalismo'],
        'caracteristica': 'Casa de Cura: Você pode oferecer serviços médicos por hospedagem.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Contrabandista',
        'fonte': 'VSS',
        'pericias': ['enganação', 'furtividade'],
        'idiomas_escolha': 0,
        'ferramentas': ['Ferramentas de navegação', 'Veículos aquáticos'],
        'caracteristica': 'Rotas Secretas: Você conhece rotas de contrabando e esconderijos.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Exorcista',
        'fonte': 'VSS',
        'pericias': ['arcanismo', 'religião'],
        'idiomas_escolha': 1,
        'ferramentas': [],
        'caracteristica': 'Sentir o Sobrenatural: Você tem intuição para atividade sobrenatural.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Nômade',
        'fonte': 'VSS',
        'pericias': ['adestrar animais', 'sobrevivência'],
        'idiomas_escolha': 1,
        'ferramentas': [],
        'caracteristica': 'Criador de Animais: Você sabe cuidar e treinar animais de montaria.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Ratazana',
        'fonte': 'VSS',
        'pericias': ['furtividade', 'prestidigitação'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Ferramentas de ladrão'],
        'caracteristica': 'Conhecimento dos Esgotos: Você conhece os esgotos e passagens secretas das cidades.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
    {
        'nome': 'Mago de Rua',
        'fonte': 'VSS',
        'pericias': ['arcanismo', 'prestidigitação'],
        'idiomas_escolha': 0,
        'ferramentas': ['Kit de disfarce', 'Ferramentas de ladrão'],
        'caracteristica': 'Truques de Salão: Você pode usar truques menores para ganhar moedas.',
        'personalidade': [],
        'ideais': [],
        'vinculos': [],
        'defeitos': []
    },
]


# ==================== FUNÇÃO DE POPULAÇÃO ====================

# Lista completa de todas as fontes
TODAS_ANTECEDENTES = [
    ('PHB', ANTECEDENTES_PHB),
    ('XGE', ANTECEDENTES_XGE),
    ('TCE', ANTECEDENTES_TCE),
    ('OotA', ANTECEDENTES_OOTA),
    ('VSS', ANTECEDENTES_VSS),
]


def popular_antecedentes():
    """Popula antecedentes de todas as fontes no banco"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verifica se tabela existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='antecedentes'
        """)
        if not cursor.fetchone():
            print("[DB] Tabela 'antecedentes' não existe, pulando...")
            return
        
        # Verifica se tem coluna fonte (migração pode não ter rodado ainda)
        cursor.execute("PRAGMA table_info(antecedentes)")
        colunas = [col[1] for col in cursor.fetchall()]
        tem_fonte = 'fonte' in colunas
        
        print("[DB] Carregando antecedentes...")
        
        total = 0
        for fonte_default, lista in TODAS_ANTECEDENTES:
            for ant in lista:
                # Pega a fonte do antecedente ou usa o default da lista
                fonte = ant.get('fonte', fonte_default)
                
                # Verifica se já existe
                cursor.execute(
                    "SELECT id FROM antecedentes WHERE nome = ?",
                    (ant['nome'],)
                )
                if cursor.fetchone():
                    continue
                
                # Prepara dados com valores padrão
                personalidade = ant.get('personalidade', [])
                ideais = ant.get('ideais', [])
                vinculos = ant.get('vinculos', [])
                defeitos = ant.get('defeitos', [])
                caracteristica = ant.get('caracteristica', '')
                
                # Insere no banco (com ou sem fonte)
                if tem_fonte:
                    cursor.execute("""
                        INSERT INTO antecedentes 
                        (nome, fonte, pericias, idiomas_escolha, ferramentas, 
                         caracteristica_nome, caracteristica_descricao,
                         tracos_personalidade, ideais, vinculos, defeitos)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        ant['nome'],
                        fonte,
                        json_dumps(ant['pericias']),
                        ant['idiomas_escolha'],
                        json_dumps(ant['ferramentas']),
                        ant['nome'],  # caracteristica_nome
                        caracteristica,  # caracteristica_descricao
                        json_dumps(personalidade),
                        json_dumps(ideais),
                        json_dumps(vinculos),
                        json_dumps(defeitos)
                    ))
                else:
                    cursor.execute("""
                        INSERT INTO antecedentes 
                        (nome, pericias, idiomas_escolha, ferramentas, 
                         caracteristica_nome, caracteristica_descricao,
                         tracos_personalidade, ideais, vinculos, defeitos)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        ant['nome'],
                        json_dumps(ant['pericias']),
                        ant['idiomas_escolha'],
                        json_dumps(ant['ferramentas']),
                        ant['nome'],  # caracteristica_nome
                        caracteristica,  # caracteristica_descricao
                        json_dumps(personalidade),
                        json_dumps(ideais),
                        json_dumps(vinculos),
                        json_dumps(defeitos)
                    ))
                total += 1
        
        conn.commit()
        print(f"[DB] {total} antecedentes carregados")
