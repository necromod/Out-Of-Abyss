"""
Script para adicionar NPCs prisioneiros dos drows
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.modulos.repositories import NPCRepository

npcs = [
    {
        'nome': 'Buppido',
        'raca': 'Derro',
        'classe': 'Assassino',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'neutro',
        'notas': '''**Derro macho, comunicativo e astuto** - Surpreendentemente sociável, esconde alma de assassino insano que acredita ser a encarnação viva do deus derro Diinkarazan. Planeja sacrifícios rituais para criar carnificina através do Subterrâneo. Mortes são ritualísticas (abre vítimas e rearranja órgãos). Completamente destemido por acreditar que não pode morrer. Sagaz e esconde verdadeira natureza.'''
    },
    {
        'nome': 'Príncipe Derendil',
        'raca': 'Quaggoth',
        'classe': 'Nobre (ilusório)',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'amigável',
        'notas': '''**Quaggoth que crê ser príncipe élfico** - Acredita ser Príncipe Derendil de Nelrindenvane, transformado por maldição. Fala élfico urbano, comporta-se como nobre mas responde ao estresse com violência quaggoth. NA VERDADE: Louco, tocado por Fraz-Urb'luu (Príncipe Demônio da Enganação). Reino não existe. Recusa verdade - evidência incontroversa causa fúria assassina. Está perdendo-se para selvageria.'''
    },
    {
        'nome': 'Eldeth Feldrun',
        'raca': 'Anã do Escudo',
        'classe': 'Batedora',
        'ocupacao': 'Batedora de Gauntlgrym',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'amigável',
        'notas': '''**Batedora de Gauntlgrym** - Animada e orgulhosa, sugere Gauntlgrym como caminho de escape. Teimosa, odeia drows e "corruptos seres da escuridão". Desafiadora, tende a sacrificar-se pelos outros. ⚠️ ALTA CHANCE DE PERECER. Se morrer, pede que informem família em Gauntlgrym e devolvam escudo/martelo - ganha aprovação dos parentes.'''
    },
    {
        'nome': 'Jimjar',
        'raca': 'Gnomo das Profundezas',
        'classe': 'Espião/Ladino',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'amigável',
        'notas': '''**Svirfneblin viciado em apostas** - Espião com atitude insubordinada, carinho por moedas, obsessão em apostar em TUDO. Oferece apostas constantes ("10 PO que você não consegue..."). Tem dificuldade em recusar apostas - pode ser usado contra ele. Comportamento incomum - outros gnomos o acham irritante/louco. Sempre fiel à palavra, mantém registro mental de débitos/créditos, paga imediatamente. Não se importa em embolsar moedas extras. Habilidade incrível de esconder riqueza. Sente algo estranho em Topsy e Turvy.'''
    },
    {
        'nome': 'Ront',
        'raca': 'Orc',
        'classe': 'Guerreiro',
        'ocupacao': 'Guerreiro da Tribo Escudo de Gelo',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'hostil',
        'notas': '''**Orc valentão da Tribo Escudo de Gelo** - Fugiu do massacre de seu bando por anões, caiu em fenda. Envergonhado da covardia, acredita que Gruumsh o pune. Não quer morrer como prisioneiro. Perverso, estúpido e odioso, mas submisso à autoridade e ameaças. Odeia especialmente Eldeth (tribos em guerra). Comportamento ameaçador com prisioneiros, a menos que alguém o enfrente.'''
    },
    {
        'nome': 'Sarith Kzekarit',
        'raca': 'Drow',
        'classe': 'Guerreiro',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'indiferente',
        'notas': '''**Drow acusado de assassinato** - Mal-humorado e reservado, rejeita diálogo. Envergonhado mas resignado. Acusado de assassinar companheiro em acesso de loucura, sem memória do evento. Será enviado a Menzoberranzan como sacrifício para Lolth. ⚠️ INFECTADO: Esporos contaminados de miconides corrompidos por Zuggtmoy (Rainha Demoníaca dos Fungos) causaram ataque. Saúde e sanidade DETERIORAM conforme esporos crescem no cérebro. 📌 INFORMAÇÃO: Sabe sobre limo cinzento no lago e patrulha atrasada de Menzoberranzan.'''
    },
    {
        'nome': 'Shuushar, o Desperto',
        'raca': 'Kuo-toa',
        'classe': 'Monge/Eremita',
        'ocupacao': 'Eremita iluminado',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'amigável',
        'notas': '''**Kuo-toa místico e eremita** - Presença calma e pacífica. Passou vida em meditação para superar loucura natural kuo-toa. Exala equilíbrio iluminado. Aceita aprisionamento: "isso é o que é". ⚠️ PACIFISTA TOTAL: NÃO LUTA, NÃO MACHUCA, NÃO DEFENDE-SE OU OUTROS. Inútil em combate mas sensato, estável, honesto. Familiarizado com Sloobludop (cidade kuo-toa no Lago Escuro), navegou rotas do lago por anos. Espera compartilhar iluminação com kuo-toa (não sabe eventos recentes em Sloobludop - cap. 3).'''
    },
    {
        'nome': 'Stool',
        'raca': 'Miconide Broto',
        'ocupacao': 'Broto miconide',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'amigável',
        'notas': '''**Miconide broto capturado** - Capturado por Sarith Kzekarit. Sozinho e assustado, quer apenas retornar ao Bosque Nunca Claro. Se fizer amizade, guia ao lar prometendo refúgio (não sabe dos perigos de Zuggtmoy - cap. 5). 🍄 ESPOROS HARMONIOSOS: Estabelece comunicação telepática. Ajuda personagens a comunicar-se com habitantes do Subterrâneo sem idioma comum. Comporta-se como irmão mais novo entusiasmado e curioso, faz muitas perguntas.'''
    },
    {
        'nome': 'Topsy',
        'raca': 'Gnomo das Profundezas',
        'classe': 'Civil',
        'ocupacao': 'Coletora de cogumelos',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'amigável',
        'notas': '''**Gnoma das profundezas gêmea** - Gêmea de Turvy, capturados coletando cogumelos perto de Pedra do Massacre do Refúgio. Cabelo fibroso emaranhado. Mais sociável dos dois, repete/traduz murmúrios de Turvy. 🐺 SEGREDO: HOMEM-RATO (licantropia). Não abraçou maldição completamente, luta para controlar instintos. TEMEROSA de reação dos aliados. Transformação controlada por ciclo da lua. ⚠️ Prisioneira há menos de 1 mês - LUA CHEIA SE APROXIMA! Cuida de si e do irmão acima de tudo.'''
    },
    {
        'nome': 'Turvy',
        'raca': 'Gnomo das Profundezas',
        'classe': 'Civil',
        'ocupacao': 'Coletor de cogumelos',
        'localizacao': 'Velkenvelve (Prisioneiro)',
        'alinhamento': 'indiferente',
        'notas': '''**Gnomo das profundezas gêmeo** - Gêmeo de Topsy, capturados coletando cogumelos perto de Pedra do Massacre do Refúgio. Tufos de cabelo no topo da cabeça, quase calvo. Constantemente resmunga e murmura sombriamente, Topsy traduz. 🐺 SEGREDO: HOMEM-RATO (licantropia). Não abraçou maldição completamente, luta para controlar instintos. TEMEROSO de reação dos aliados. Transformação controlada por ciclo da lua. ⚠️ Prisioneiro há menos de 1 mês - LUA CHEIA SE APROXIMA! Cuida de si e da irmã acima de tudo.'''
    }
]

print("Adicionando NPCs prisioneiros dos drows...")
for npc_data in npcs:
    npc_id = NPCRepository.insert(npc_data)
    npc = NPCRepository.get_by_id(npc_id)
    print(f"✅ {npc['nome']} ({npc['raca']}) - ID: {npc['id']}")

print(f"\n✨ {len(npcs)} NPCs adicionados com sucesso!")
