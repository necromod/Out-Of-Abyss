/**
 * FICHAS.JS - Interatividade para fichas de personagens, monstros e NPCs
 */

// ==========================================================================
// DADOS DE RAÇAS E CLASSES D&D 5e (Livro do Jogador)
// ==========================================================================

/**
 * Mapeamento completo de RAÇAS do Livro do Jogador
 */
const RACAS_DND = {
    // ===== ANÕES =====
    'Anão': {
        bonus_atributos: { constituicao: 2 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Anão'],
        proficiencias: ['Machados de batalha', 'Machadinhas', 'Martelos leves', 'Martelos de guerra'],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Resiliência Anã (vantagem em testes de resistência contra veneno)',
            'Treinamento Anão em Combate',
            'Especialização em Rochas'
        ],
        resistencias: ['Veneno']
    },
    'Anão da Colina': {
        bonus_atributos: { constituicao: 2, sabedoria: 1 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Anão'],
        proficiencias: ['Machados de batalha', 'Machadinhas', 'Martelos leves', 'Martelos de guerra'],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Resiliência Anã (vantagem em testes de resistência contra veneno)',
            'Treinamento Anão em Combate',
            'Especialização em Rochas',
            'Tenacidade Anã (+1 HP por nível)'
        ],
        resistencias: ['Veneno'],
        hp_bonus_nivel: 1
    },
    'Anão da Montanha': {
        bonus_atributos: { constituicao: 2, forca: 2 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Anão'],
        proficiencias: ['Machados de batalha', 'Machadinhas', 'Martelos leves', 'Martelos de guerra', 'Armaduras leves', 'Armaduras médias'],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Resiliência Anã (vantagem em testes de resistência contra veneno)',
            'Treinamento Anão em Combate',
            'Especialização em Rochas',
            'Treinamento Anão com Armaduras'
        ],
        resistencias: ['Veneno']
    },

    // ===== ELFOS =====
    'Elfo': {
        bonus_atributos: { destreza: 2 },
        velocidade: '9m',
        idiomas: ['Comum', 'Élfico'],
        proficiencias: [],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Sentidos Aguçados (proficiência em Percepção)',
            'Ancestral Feérico (vantagem contra ser enfeitiçado, imune a sono mágico)',
            'Transe (4h de meditação = 8h de sono)'
        ],
        pericias_bonus: ['percepcao'],
        imunidades: ['Sono mágico']
    },
    'Alto Elfo': {
        bonus_atributos: { destreza: 2, inteligencia: 1 },
        velocidade: '9m',
        idiomas: ['Comum', 'Élfico', '(escolha um idioma adicional)'],
        proficiencias: ['Espadas longas', 'Espadas curtas', 'Arcos longos', 'Arcos curtos'],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Sentidos Aguçados (proficiência em Percepção)',
            'Ancestral Feérico (vantagem contra ser enfeitiçado, imune a sono mágico)',
            'Transe (4h de meditação = 8h de sono)',
            'Treinamento Élfico com Armas',
            'Truque (1 truque de mago à sua escolha, INT)'
        ],
        pericias_bonus: ['percepcao'],
        imunidades: ['Sono mágico'],
        idioma_extra: true
    },
    'Elfo da Floresta': {
        bonus_atributos: { destreza: 2, sabedoria: 1 },
        velocidade: '10,5m',
        idiomas: ['Comum', 'Élfico'],
        proficiencias: ['Espadas longas', 'Espadas curtas', 'Arcos longos', 'Arcos curtos'],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Sentidos Aguçados (proficiência em Percepção)',
            'Ancestral Feérico (vantagem contra ser enfeitiçado, imune a sono mágico)',
            'Transe (4h de meditação = 8h de sono)',
            'Treinamento Élfico com Armas',
            'Pés Ligeiros (velocidade 10,5m)',
            'Máscara da Natureza (pode se esconder com folhagem, chuva, neve, névoa)'
        ],
        pericias_bonus: ['percepcao'],
        imunidades: ['Sono mágico']
    },
    'Drow': {
        bonus_atributos: { destreza: 2, carisma: 1 },
        velocidade: '9m',
        idiomas: ['Comum', 'Élfico'],
        proficiencias: ['Rapieiras', 'Espadas curtas', 'Bestas de mão'],
        caracteristicas: [
            'Visão no Escuro Superior (36m)',
            'Sentidos Aguçados (proficiência em Percepção)',
            'Ancestral Feérico (vantagem contra ser enfeitiçado, imune a sono mágico)',
            'Transe (4h de meditação = 8h de sono)',
            'Sensibilidade à Luz do Sol (desvantagem em ataques e Percepção sob luz solar)',
            'Magia Drow (Globos de Luz, Fogo Feérico nv3, Escuridão nv5)'
        ],
        pericias_bonus: ['percepcao'],
        imunidades: ['Sono mágico']
    },

    // ===== HALFLINGS =====
    'Halfling': {
        bonus_atributos: { destreza: 2 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Halfling'],
        proficiencias: [],
        caracteristicas: [
            'Sortudo (re-rola 1 natural em d20)',
            'Corajoso (vantagem contra ser amedrontado)',
            'Agilidade Halfling (pode mover através de criaturas maiores)'
        ]
    },
    'Halfling Pés-Leves': {
        bonus_atributos: { destreza: 2, carisma: 1 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Halfling'],
        proficiencias: [],
        caracteristicas: [
            'Sortudo (re-rola 1 natural em d20)',
            'Corajoso (vantagem contra ser amedrontado)',
            'Agilidade Halfling (pode mover através de criaturas maiores)',
            'Furtividade Natural (pode se esconder atrás de criaturas maiores)'
        ]
    },
    'Halfling Robusto': {
        bonus_atributos: { destreza: 2, constituicao: 1 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Halfling'],
        proficiencias: [],
        caracteristicas: [
            'Sortudo (re-rola 1 natural em d20)',
            'Corajoso (vantagem contra ser amedrontado)',
            'Agilidade Halfling (pode mover através de criaturas maiores)',
            'Resiliência dos Robustos (vantagem contra veneno, resistência a dano de veneno)'
        ],
        resistencias: ['Veneno']
    },

    // ===== HUMANO =====
    'Humano': {
        bonus_atributos: { forca: 1, destreza: 1, constituicao: 1, inteligencia: 1, sabedoria: 1, carisma: 1 },
        velocidade: '9m',
        idiomas: ['Comum', '(escolha um idioma adicional)'],
        proficiencias: [],
        caracteristicas: [],
        idioma_extra: true
    },
    'Humano Variante': {
        bonus_atributos: { escolha_2: 1 }, // Jogador escolhe 2 atributos para +1
        velocidade: '9m',
        idiomas: ['Comum', '(escolha um idioma adicional)'],
        proficiencias: [],
        caracteristicas: [
            'Talento (escolha um talento)'
        ],
        pericias_bonus: ['escolha_1'], // Jogador escolhe 1 perícia
        idioma_extra: true,
        talento: true
    },

    // ===== DRACONATO =====
    'Draconato': {
        bonus_atributos: { forca: 2, carisma: 1 },
        velocidade: '9m',
        idiomas: ['Comum', 'Dracônico'],
        proficiencias: [],
        caracteristicas: [
            'Ancestral Dracônico (escolha tipo de dragão)',
            'Arma de Sopro (dano baseado no ancestral)',
            'Resistência a Dano (tipo baseado no ancestral)'
        ],
        escolha_ancestral: true
    },

    // ===== GNOMOS =====
    'Gnomo': {
        bonus_atributos: { inteligencia: 2 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Gnômico'],
        proficiencias: [],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Esperteza Gnômica (vantagem em INT, SAB, CAR contra magia)'
        ]
    },
    'Gnomo da Floresta': {
        bonus_atributos: { inteligencia: 2, destreza: 1 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Gnômico'],
        proficiencias: [],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Esperteza Gnômica (vantagem em INT, SAB, CAR contra magia)',
            'Ilusionista Natural (truque Ilusão Menor, INT)',
            'Falar com Bestas Pequenas'
        ]
    },
    'Gnomo das Rochas': {
        bonus_atributos: { inteligencia: 2, constituicao: 1 },
        velocidade: '7,5m',
        idiomas: ['Comum', 'Gnômico'],
        proficiencias: ['Ferramentas de Artesão'],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Esperteza Gnômica (vantagem em INT, SAB, CAR contra magia)',
            'Conhecimento de Artífice (dobro do bônus em História sobre itens mágicos/alquímicos/tecnológicos)',
            'Engenhoqueiro (pode criar pequenos dispositivos)'
        ]
    },

    // ===== MEIO-ELFO =====
    'Meio-Elfo': {
        bonus_atributos: { carisma: 2, escolha_2: 1 }, // +2 CAR, +1 em dois outros à escolha
        velocidade: '9m',
        idiomas: ['Comum', 'Élfico', '(escolha um idioma adicional)'],
        proficiencias: [],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Ancestral Feérico (vantagem contra ser enfeitiçado, imune a sono mágico)',
            'Versatilidade em Perícias (proficiência em 2 perícias à escolha)'
        ],
        pericias_bonus: ['escolha_2'], // Jogador escolhe 2 perícias
        imunidades: ['Sono mágico'],
        idioma_extra: true
    },

    // ===== MEIO-ORC =====
    'Meio-Orc': {
        bonus_atributos: { forca: 2, constituicao: 1 },
        velocidade: '9m',
        idiomas: ['Comum', 'Orc'],
        proficiencias: [],
        pericias_bonus: ['intimidacao'],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Ameaçador (proficiência em Intimidação)',
            'Resistência Implacável (ao cair para 0 HP, pode cair para 1 HP, 1x/descanso longo)',
            'Ataques Selvagens (+1 dado de dano em crítico corpo-a-corpo)'
        ]
    },

    // ===== TIEFLING =====
    'Tiefling': {
        bonus_atributos: { carisma: 2, inteligencia: 1 },
        velocidade: '9m',
        idiomas: ['Comum', 'Infernal'],
        proficiencias: [],
        caracteristicas: [
            'Visão no Escuro (18m)',
            'Resistência Infernal (resistência a dano de fogo)',
            'Legado Infernal (Taumaturgia, Repreensão Infernal nv3, Escuridão nv5)'
        ],
        resistencias: ['Fogo']
    }
};

/**
 * Mapeamento completo de CLASSES do Livro do Jogador
 */
const CLASSES_DND = {
    'Bárbaro': {
        dado_vida: 12,
        hp_primeiro_nivel: 12,
        salvaguardas_proficientes: ['forca', 'constituicao'],
        armaduras: ['Armaduras leves', 'Armaduras médias', 'Escudos'],
        armas: ['Armas simples', 'Armas marciais'],
        ferramentas: [],
        pericias_disponiveis: ['adestrar_animais', 'atletismo', 'intimidacao', 'natureza', 'percepcao', 'sobrevivencia'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Fúria (2/descanso longo)',
            'Defesa sem Armadura (CA = 10 + DES + CON)'
        ]
    },
    'Bardo': {
        dado_vida: 8,
        hp_primeiro_nivel: 8,
        salvaguardas_proficientes: ['destreza', 'carisma'],
        armaduras: ['Armaduras leves'],
        armas: ['Armas simples', 'Bestas de mão', 'Espadas longas', 'Rapieiras', 'Espadas curtas'],
        ferramentas: ['Três instrumentos musicais à sua escolha'],
        pericias_disponiveis: ['todas'], // Bardo pode escolher qualquer
        qtd_pericias: 3,
        caracteristicas_nivel_1: [
            'Conjuração (CAR)',
            'Inspiração de Bardo (d6, CAR vezes/descanso longo)'
        ],
        conjurador: true,
        atributo_conjuracao: 'carisma'
    },
    'Bruxo': {
        dado_vida: 8,
        hp_primeiro_nivel: 8,
        salvaguardas_proficientes: ['sabedoria', 'carisma'],
        armaduras: ['Armaduras leves'],
        armas: ['Armas simples'],
        ferramentas: [],
        pericias_disponiveis: ['arcanismo', 'enganacao', 'historia', 'intimidacao', 'investigacao', 'natureza', 'religiao'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Patrono Transcendental',
            'Magia de Pacto (CAR)'
        ],
        conjurador: true,
        atributo_conjuracao: 'carisma'
    },
    'Clérigo': {
        dado_vida: 8,
        hp_primeiro_nivel: 8,
        salvaguardas_proficientes: ['sabedoria', 'carisma'],
        armaduras: ['Armaduras leves', 'Armaduras médias', 'Escudos'],
        armas: ['Armas simples'],
        ferramentas: [],
        pericias_disponiveis: ['historia', 'intuicao', 'medicina', 'persuasao', 'religiao'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Conjuração (SAB)',
            'Domínio Divino'
        ],
        conjurador: true,
        atributo_conjuracao: 'sabedoria'
    },
    'Druida': {
        dado_vida: 8,
        hp_primeiro_nivel: 8,
        salvaguardas_proficientes: ['inteligencia', 'sabedoria'],
        armaduras: ['Armaduras leves', 'Armaduras médias', 'Escudos (não metálicos)'],
        armas: ['Clavas', 'Adagas', 'Dardos', 'Azagaias', 'Maças', 'Bordões', 'Cimitarras', 'Foices', 'Fundas', 'Lanças'],
        ferramentas: ['Kit de herbalismo'],
        pericias_disponiveis: ['adestrar_animais', 'arcanismo', 'intuicao', 'medicina', 'natureza', 'percepcao', 'religiao', 'sobrevivencia'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Druídico (idioma secreto)',
            'Conjuração (SAB)'
        ],
        conjurador: true,
        atributo_conjuracao: 'sabedoria',
        idiomas_bonus: ['Druídico']
    },
    'Feiticeiro': {
        dado_vida: 6,
        hp_primeiro_nivel: 6,
        salvaguardas_proficientes: ['constituicao', 'carisma'],
        armaduras: [],
        armas: ['Adagas', 'Dardos', 'Fundas', 'Bordões', 'Bestas leves'],
        ferramentas: [],
        pericias_disponiveis: ['arcanismo', 'enganacao', 'intuicao', 'intimidacao', 'persuasao', 'religiao'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Conjuração (CAR)',
            'Origem de Feitiçaria'
        ],
        conjurador: true,
        atributo_conjuracao: 'carisma'
    },
    'Guerreiro': {
        dado_vida: 10,
        hp_primeiro_nivel: 10,
        salvaguardas_proficientes: ['forca', 'constituicao'],
        armaduras: ['Armaduras leves', 'Armaduras médias', 'Armaduras pesadas', 'Escudos'],
        armas: ['Armas simples', 'Armas marciais'],
        ferramentas: [],
        pericias_disponiveis: ['acrobacia', 'adestrar_animais', 'atletismo', 'historia', 'intimidacao', 'intuicao', 'percepcao', 'sobrevivencia'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Estilo de Luta',
            'Retomar o Fôlego (1d10+nível HP, 1x/descanso curto)'
        ]
    },
    'Ladino': {
        dado_vida: 8,
        hp_primeiro_nivel: 8,
        salvaguardas_proficientes: ['destreza', 'inteligencia'],
        armaduras: ['Armaduras leves'],
        armas: ['Armas simples', 'Bestas de mão', 'Espadas longas', 'Rapieiras', 'Espadas curtas'],
        ferramentas: ['Ferramentas de ladrão'],
        pericias_disponiveis: ['acrobacia', 'atletismo', 'atuacao', 'enganacao', 'furtividade', 'intimidacao', 'intuicao', 'investigacao', 'percepcao', 'persuasao', 'prestidigitacao'],
        qtd_pericias: 4,
        caracteristicas_nivel_1: [
            'Especialização (dobro em 2 perícias)',
            'Ataque Furtivo (1d6)',
            'Gíria de Ladrão'
        ],
        idiomas_bonus: ['Gíria de Ladrão']
    },
    'Mago': {
        dado_vida: 6,
        hp_primeiro_nivel: 6,
        salvaguardas_proficientes: ['inteligencia', 'sabedoria'],
        armaduras: [],
        armas: ['Adagas', 'Dardos', 'Fundas', 'Bordões', 'Bestas leves'],
        ferramentas: [],
        pericias_disponiveis: ['arcanismo', 'historia', 'intuicao', 'investigacao', 'medicina', 'religiao'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Conjuração (INT)',
            'Recuperação Arcana (recupera slots = metade nível mago, 1x/dia)',
            'Grimório'
        ],
        conjurador: true,
        atributo_conjuracao: 'inteligencia'
    },
    'Monge': {
        dado_vida: 8,
        hp_primeiro_nivel: 8,
        salvaguardas_proficientes: ['forca', 'destreza'],
        armaduras: [],
        armas: ['Armas simples', 'Espadas curtas'],
        ferramentas: ['Um tipo de ferramenta de artesão OU um instrumento musical'],
        pericias_disponiveis: ['acrobacia', 'atletismo', 'furtividade', 'historia', 'intuicao', 'religiao'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Defesa sem Armadura (CA = 10 + DES + SAB)',
            'Artes Marciais (d4, pode usar DES para ataques desarmados)'
        ]
    },
    'Paladino': {
        dado_vida: 10,
        hp_primeiro_nivel: 10,
        salvaguardas_proficientes: ['sabedoria', 'carisma'],
        armaduras: ['Armaduras leves', 'Armaduras médias', 'Armaduras pesadas', 'Escudos'],
        armas: ['Armas simples', 'Armas marciais'],
        ferramentas: [],
        pericias_disponiveis: ['atletismo', 'intimidacao', 'intuicao', 'medicina', 'persuasao', 'religiao'],
        qtd_pericias: 2,
        caracteristicas_nivel_1: [
            'Sentido Divino (detectar celestiais, infernais, mortos-vivos)',
            'Cura pelas Mãos (cura = 5 × nível paladino)'
        ],
        conjurador: true, // A partir do nível 2
        atributo_conjuracao: 'carisma'
    },
    'Patrulheiro': {
        dado_vida: 10,
        hp_primeiro_nivel: 10,
        salvaguardas_proficientes: ['forca', 'destreza'],
        armaduras: ['Armaduras leves', 'Armaduras médias', 'Escudos'],
        armas: ['Armas simples', 'Armas marciais'],
        ferramentas: [],
        pericias_disponiveis: ['adestrar_animais', 'atletismo', 'furtividade', 'intuicao', 'investigacao', 'natureza', 'percepcao', 'sobrevivencia'],
        qtd_pericias: 3,
        caracteristicas_nivel_1: [
            'Inimigo Favorito',
            'Explorador Natural'
        ],
        conjurador: true, // A partir do nível 2
        atributo_conjuracao: 'sabedoria'
    }
};

/**
 * Lista de idiomas disponíveis no D&D 5e
 */
const IDIOMAS_DND = [
    'Comum', 'Anão', 'Élfico', 'Gigante', 'Gnômico', 'Goblin', 'Halfling', 'Orc',
    'Abissal', 'Celestial', 'Dracônico', 'Dialeto Subterrâneo', 'Infernal', 'Primordial', 'Silvestre', 'Subcomum'
];

/**
 * Ancestrais Dracônicos para Draconatos
 */
const ANCESTRAIS_DRACONATOS = {
    'Negro': { dano: 'Ácido', arma: 'Linha 1,5m x 9m (DES)', resistencia: 'Ácido' },
    'Azul': { dano: 'Elétrico', arma: 'Linha 1,5m x 9m (DES)', resistencia: 'Elétrico' },
    'Latão': { dano: 'Fogo', arma: 'Linha 1,5m x 9m (DES)', resistencia: 'Fogo' },
    'Bronze': { dano: 'Elétrico', arma: 'Linha 1,5m x 9m (DES)', resistencia: 'Elétrico' },
    'Cobre': { dano: 'Ácido', arma: 'Linha 1,5m x 9m (DES)', resistencia: 'Ácido' },
    'Dourado': { dano: 'Fogo', arma: 'Cone 4,5m (DES)', resistencia: 'Fogo' },
    'Verde': { dano: 'Veneno', arma: 'Cone 4,5m (CON)', resistencia: 'Veneno' },
    'Vermelho': { dano: 'Fogo', arma: 'Cone 4,5m (DES)', resistencia: 'Fogo' },
    'Prata': { dano: 'Frio', arma: 'Cone 4,5m (CON)', resistencia: 'Frio' },
    'Branco': { dano: 'Frio', arma: 'Cone 4,5m (CON)', resistencia: 'Frio' }
};

// ==========================================================================
// UTILIDADES
// ==========================================================================

/**
 * Faz requisições à API
 */
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    return response.json();
}

/**
 * Calcula modificador de atributo D&D 5e
 */
function calcularModificador(valor) {
    return Math.floor((valor - 10) / 2);
}

/**
 * Formata modificador com sinal
 */
function formatarModificador(mod) {
    return mod >= 0 ? `+${mod}` : `${mod}`;
}

/**
 * Calcula porcentagem de HP
 */
function calcularPorcentagemHP(atual, max) {
    if (max <= 0) return 0;
    return Math.max(0, Math.min(100, (atual / max) * 100));
}

/**
 * Retorna a classe CSS para a cor do HP
 */
function getHPColorClass(porcentagem) {
    if (porcentagem > 75) return 'hp-100';
    if (porcentagem > 50) return 'hp-75';
    if (porcentagem > 25) return 'hp-50';
    if (porcentagem > 10) return 'hp-25';
    return 'hp-10';
}

/**
 * Rola dados (ex: "2d6+3")
 */
function rolarDados(expressao) {
    const regex = /(\d+)d(\d+)([+-]\d+)?/i;
    const match = expressao.match(regex);
    
    if (!match) return { total: 0, detalhes: 'Inválido' };
    
    const qtd = parseInt(match[1]);
    const lados = parseInt(match[2]);
    const mod = match[3] ? parseInt(match[3]) : 0;
    
    const resultados = [];
    let soma = 0;
    
    for (let i = 0; i < qtd; i++) {
        const resultado = Math.floor(Math.random() * lados) + 1;
        resultados.push(resultado);
        soma += resultado;
    }
    
    const total = soma + mod;
    const detalhes = `[${resultados.join(', ')}]${mod !== 0 ? (mod > 0 ? '+' : '') + mod : ''} = ${total}`;
    
    return { total, detalhes, resultados };
}

/**
 * Rola d20
 */
function rolarD20(modificador = 0) {
    const d20 = Math.floor(Math.random() * 20) + 1;
    const total = d20 + modificador;
    const critico = d20 === 20;
    const falha = d20 === 1;
    
    return { d20, modificador, total, critico, falha };
}

// ==========================================================================
// AUTO-SAVE
// ==========================================================================

let autoSaveTimeout = null;

/**
 * Inicializa auto-save nos campos editáveis
 */
function inicializarAutoSave() {
    document.querySelectorAll('[data-campo]').forEach(campo => {
        const evento = campo.tagName === 'SELECT' ? 'change' : 'input';
        
        campo.addEventListener(evento, function() {
            clearTimeout(autoSaveTimeout);
            
            autoSaveTimeout = setTimeout(() => {
                salvarCampo(this);
            }, 500);
        });
    });
}

/**
 * Salva um campo específico
 */
async function salvarCampo(elemento) {
    const campo = elemento.dataset.campo;
    const tipo = elemento.dataset.tipo || 'personagem';
    const id = elemento.dataset.id || document.querySelector('[data-ficha-id]')?.dataset.fichaId;
    
    if (!id || !campo) return;
    
    let valor = elemento.type === 'checkbox' ? elemento.checked : elemento.value;
    
    // Tenta converter para número se apropriado
    if (elemento.type === 'number') {
        valor = parseFloat(valor) || 0;
    }
    
    try {
        const response = await apiRequest(`/fichas/api/${tipo}/${id}/campo`, 'PATCH', {
            campo,
            valor
        });
        
        if (response.sucesso) {
            mostrarNotificacao('Salvo', 'success');
            
            // Atualiza modificadores se for atributo
            if (['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma'].includes(campo)) {
                atualizarModificadores();
            }
            
            // Atualiza barra de HP se necessário
            if (['hp_atual', 'hp_max'].includes(campo)) {
                atualizarBarraHP();
            }
        }
    } catch (error) {
        console.error('Erro ao salvar:', error);
        mostrarNotificacao('Erro ao salvar', 'error');
    }
}

// ==========================================================================
// HP MANAGEMENT
// ==========================================================================

/**
 * Atualiza a barra de HP visual
 */
function atualizarBarraHP() {
    const hpAtual = parseInt(document.querySelector('[data-campo="hp_atual"]')?.value) || 0;
    const hpMax = parseInt(document.querySelector('[data-campo="hp_maximo"]')?.value) || 
                  parseInt(document.querySelector('[data-campo="hp_max"]')?.value) || 1;
    
    const porcentagem = calcularPorcentagemHP(hpAtual, hpMax);
    const hpFill = document.querySelector('.hp-fill') || document.querySelector('.hp-atual');
    const hpValorAtual = document.querySelector('.hp-atual-texto');
    
    if (hpFill) {
        hpFill.style.width = `${porcentagem}%`;
        hpFill.className = hpFill.className.replace(/hp-(100|75|50|25|fill)/g, '').trim() + ` hp-fill ${getHPColorClass(porcentagem)}`;
    }
    
    if (hpValorAtual) {
        hpValorAtual.textContent = hpAtual;
    }
}

/**
 * Aplica dano ao personagem
 */
function aplicarDano(quantidade) {
    // Se não recebeu quantidade, pega do input do modal
    if (quantidade === undefined) {
        const input = document.getElementById('input-dano');
        quantidade = parseInt(input?.value) || 0;
        fecharModal('modal-dano');
    }
    
    const campoHP = document.querySelector('[data-campo="hp_atual"]');
    if (!campoHP) return;
    
    const hpAtual = parseInt(campoHP.value) || 0;
    const novoHP = Math.max(0, hpAtual - quantidade);
    
    campoHP.value = novoHP;
    campoHP.dispatchEvent(new Event('input'));
    
    atualizarBarraHP();
    mostrarNotificacao(`-${quantidade} HP`, 'danger');
}

/**
 * Cura o personagem
 */
function aplicarCura(quantidade) {
    // Se não recebeu quantidade, pega do input do modal
    if (quantidade === undefined) {
        const input = document.getElementById('input-cura');
        quantidade = parseInt(input?.value) || 0;
        fecharModal('modal-cura');
    }
    
    const campoHP = document.querySelector('[data-campo="hp_atual"]');
    const campoHPMax = document.querySelector('[data-campo="hp_maximo"]') || document.querySelector('[data-campo="hp_max"]');
    if (!campoHP) return;
    
    const hpAtual = parseInt(campoHP.value) || 0;
    const hpMax = parseInt(campoHPMax?.value) || 999;
    const novoHP = Math.min(hpMax, hpAtual + quantidade);
    
    campoHP.value = novoHP;
    campoHP.dispatchEvent(new Event('input'));
    
    atualizarBarraHP();
    mostrarNotificacao(`+${quantidade} HP`, 'success');
}

/**
 * Abre modal de dano
 */
function abrirModalDano() {
    const modal = document.getElementById('modal-dano');
    if (modal) {
        modal.classList.add('active');
        const input = modal.querySelector('input');
        if (input) {
            input.value = '';
            input.focus();
        }
    }
}

/**
 * Abre modal de cura
 */
function abrirModalCura() {
    const modal = document.getElementById('modal-cura');
    if (modal) {
        modal.classList.add('active');
        const input = modal.querySelector('input');
        if (input) {
            input.value = '';
            input.focus();
        }
    }
}

// ==========================================================================
// MODIFICADORES E PERÍCIAS - AUTOMAÇÃO D&D 5e
// ==========================================================================

/**
 * Mapeamento de perícias para seus atributos base
 */
const PERICIAS_ATRIBUTO = {
    'acrobacia': 'destreza',
    'adestrar_animais': 'sabedoria',
    'arcanismo': 'inteligencia',
    'atletismo': 'forca',
    'atuacao': 'carisma',
    'enganacao': 'carisma',
    'furtividade': 'destreza',
    'historia': 'inteligencia',
    'intimidacao': 'carisma',
    'intuicao': 'sabedoria',
    'investigacao': 'inteligencia',
    'medicina': 'sabedoria',
    'natureza': 'inteligencia',
    'percepcao': 'sabedoria',
    'persuasao': 'carisma',
    'prestidigitacao': 'destreza',
    'religiao': 'inteligencia',
    'sobrevivencia': 'sabedoria'
};

/**
 * Mapeamento de salvaguardas para seus atributos (são os mesmos)
 */
const SALVAGUARDAS_ATRIBUTO = {
    'forca': 'forca',
    'destreza': 'destreza',
    'constituicao': 'constituicao',
    'inteligencia': 'inteligencia',
    'sabedoria': 'sabedoria',
    'carisma': 'carisma'
};

/**
 * Calcula o bônus de proficiência baseado no nível
 * Níveis 1-4: +2, 5-8: +3, 9-12: +4, 13-16: +5, 17-20: +6
 */
function calcularBonusProficiencia(nivel) {
    return 2 + Math.floor((nivel - 1) / 4);
}

/**
 * Obtém o valor atual de um atributo
 */
function getValorAtributo(atributo) {
    const campo = document.querySelector(`[data-campo="atributos.${atributo}"]`);
    return parseInt(campo?.value) || 10;
}

/**
 * Obtém o bônus de proficiência atual
 */
function getBonusProficiencia() {
    const campo = document.querySelector('[data-campo="bonus_proficiencia"]');
    return parseInt(campo?.value) || 2;
}

/**
 * Obtém o nível atual do personagem
 */
function getNivelAtual() {
    const campo = document.querySelector('[data-campo="nivel"]');
    return parseInt(campo?.value) || 1;
}

/**
 * Atualiza o modificador visual de um atributo no card
 */
function atualizarModificadorAtributo(atributo) {
    const campoValor = document.querySelector(`[data-campo="atributos.${atributo}"]`);
    if (!campoValor) return;
    
    const card = campoValor.closest('.atributo-card');
    if (!card) return;
    
    const valor = parseInt(campoValor.value) || 10;
    const mod = calcularModificador(valor);
    
    const modDisplay = card.querySelector('.attr-mod');
    if (modDisplay) {
        modDisplay.textContent = formatarModificador(mod);
    }
}

/**
 * Atualiza todos os modificadores de atributos
 */
function atualizarModificadores() {
    const atributos = ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma'];
    atributos.forEach(attr => atualizarModificadorAtributo(attr));
    
    // Também atualiza perícias e salvaguardas
    atualizarTodasPericias();
    atualizarTodasSalvaguardas();
    atualizarIniciativa();
}

/**
 * Atualiza o modificador de uma perícia específica
 */
function atualizarPericia(periciaKey) {
    const atributo = PERICIAS_ATRIBUTO[periciaKey];
    if (!atributo) return;
    
    const checkbox = document.querySelector(`[data-campo="pericias_proficientes"][data-valor="${periciaKey}"]`);
    if (!checkbox) return;
    
    const linha = checkbox.closest('.pericia-linha');
    if (!linha) return;
    
    const modDisplay = linha.querySelector('.pericia-mod');
    if (!modDisplay) return;
    
    const valorAtributo = getValorAtributo(atributo);
    const modAtributo = calcularModificador(valorAtributo);
    const proficiente = checkbox.checked;
    const bonusProf = getBonusProficiencia();
    
    const modTotal = proficiente ? modAtributo + bonusProf : modAtributo;
    modDisplay.textContent = formatarModificador(modTotal);
}

/**
 * Atualiza todas as perícias
 */
function atualizarTodasPericias() {
    Object.keys(PERICIAS_ATRIBUTO).forEach(pericia => atualizarPericia(pericia));
}

/**
 * Atualiza o modificador de uma salvaguarda específica
 */
function atualizarSalvaguarda(salvKey) {
    const atributo = SALVAGUARDAS_ATRIBUTO[salvKey];
    if (!atributo) return;
    
    const checkbox = document.querySelector(`[data-campo="salvaguardas_proficientes"][data-valor="${salvKey}"]`);
    if (!checkbox) return;
    
    const item = checkbox.closest('.save-item');
    if (!item) return;
    
    const modDisplay = item.querySelector('.save-mod');
    if (!modDisplay) return;
    
    const valorAtributo = getValorAtributo(atributo);
    const modAtributo = calcularModificador(valorAtributo);
    const proficiente = checkbox.checked;
    const bonusProf = getBonusProficiencia();
    
    const modTotal = proficiente ? modAtributo + bonusProf : modAtributo;
    modDisplay.textContent = formatarModificador(modTotal);
}

/**
 * Atualiza todas as salvaguardas
 */
function atualizarTodasSalvaguardas() {
    Object.keys(SALVAGUARDAS_ATRIBUTO).forEach(salv => atualizarSalvaguarda(salv));
}

/**
 * Atualiza a iniciativa (baseada em Destreza)
 */
function atualizarIniciativa() {
    const iniciativaDisplay = document.getElementById('inicativa_padd');
    if (!iniciativaDisplay) return;
    
    const valorDestreza = getValorAtributo('destreza');
    const modDestreza = calcularModificador(valorDestreza);
    iniciativaDisplay.textContent = formatarModificador(modDestreza);
}

/**
 * Atualiza o bônus de proficiência baseado no nível
 */
function atualizarBonusProficienciaPorNivel() {
    const nivel = getNivelAtual();
    const bonusCalculado = calcularBonusProficiencia(nivel);
    
    const campoBonus = document.querySelector('[data-campo="bonus_proficiencia"]');
    if (campoBonus) {
        campoBonus.value = bonusCalculado;
    }
    
    // Recalcula tudo que depende do bônus de proficiência
    atualizarTodasPericias();
    atualizarTodasSalvaguardas();
}

/**
 * Inicializa os event listeners para automação
 */
function inicializarAutomacao() {
    // Listeners para mudança de atributos
    const atributos = ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma'];
    atributos.forEach(attr => {
        const campo = document.querySelector(`[data-campo="atributos.${attr}"]`);
        if (campo) {
            campo.addEventListener('input', function() {
                atualizarModificadorAtributo(attr);
                
                // Atualiza perícias que dependem deste atributo
                Object.entries(PERICIAS_ATRIBUTO).forEach(([pericia, attrPericia]) => {
                    if (attrPericia === attr) {
                        atualizarPericia(pericia);
                    }
                });
                
                // Atualiza salvaguarda deste atributo
                atualizarSalvaguarda(attr);
                
                // Atualiza iniciativa se for destreza
                if (attr === 'destreza') {
                    atualizarIniciativa();
                }
            });
        }
    });
    
    // Listeners para checkboxes de proficiência em perícias
    document.querySelectorAll('[data-campo="pericias_proficientes"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const periciaKey = this.dataset.valor;
            atualizarPericia(periciaKey);
        });
    });
    
    // Listeners para checkboxes de proficiência em salvaguardas
    document.querySelectorAll('[data-campo="salvaguardas_proficientes"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const salvKey = this.dataset.valor;
            atualizarSalvaguarda(salvKey);
        });
    });
    
    // Listener para mudança de nível
    const campoNivel = document.querySelector('[data-campo="nivel"]');
    if (campoNivel) {
        campoNivel.addEventListener('change', function() {
            atualizarBonusProficienciaPorNivel();
        });
    }
    
    // Listener para mudança manual do bônus de proficiência
    const campoBonus = document.querySelector('[data-campo="bonus_proficiencia"]');
    if (campoBonus) {
        campoBonus.addEventListener('input', function() {
            atualizarTodasPericias();
            atualizarTodasSalvaguardas();
        });
    }
    
    console.log('✅ Automação D&D 5e inicializada');
}

// ==========================================================================
// APLICAÇÃO AUTOMÁTICA DE RAÇA E CLASSE
// ==========================================================================

/**
 * Aplica os bônus e características de uma raça selecionada
 */
function aplicarRaca(racaNome) {
    const raca = RACAS_DND[racaNome];
    if (!raca) {
        console.log(`Raça "${racaNome}" não encontrada no mapeamento`);
        return;
    }
    
    console.log(`🧝 Aplicando raça: ${racaNome}`);
    
    // 1. Aplicar bônus de atributos
    if (raca.bonus_atributos) {
        Object.entries(raca.bonus_atributos).forEach(([attr, bonus]) => {
            if (attr === 'escolha_2') return; // Ignorar escolhas manuais
            
            const campo = document.querySelector(`[data-campo="atributos.${attr}"]`);
            if (campo) {
                const valorAtual = parseInt(campo.value) || 10;
                // Só aplica se o valor for o padrão (10) - evita sobrescrever valores já editados
                if (valorAtual === 10) {
                    campo.value = 10 + bonus;
                    atualizarModificadorAtributo(attr);
                }
            }
        });
    }
    
    // 2. Aplicar velocidade
    if (raca.velocidade) {
        const campoVelocidade = document.querySelector('[data-campo="velocidade"]');
        if (campoVelocidade) {
            campoVelocidade.value = raca.velocidade;
        }
    }
    
    // 3. Sugerir idiomas
    if (raca.idiomas) {
        const campoLinguas = document.querySelector('[data-campo="linguas"]');
        if (campoLinguas && !campoLinguas.value.trim()) {
            campoLinguas.value = raca.idiomas.join(', ');
        }
    }
    
    // 4. Aplicar proficiências de raça
    if (raca.proficiencias && raca.proficiencias.length > 0) {
        const campoProficiencias = document.querySelector('[data-campo="proficiencias"]');
        if (campoProficiencias) {
            const profAtual = campoProficiencias.value.trim();
            const novasProf = raca.proficiencias.join(', ');
            if (!profAtual) {
                campoProficiencias.value = novasProf;
            } else if (!profAtual.includes(novasProf)) {
                campoProficiencias.value = profAtual + '\n' + novasProf;
            }
        }
    }
    
    // 5. Aplicar características de raça
    if (raca.caracteristicas && raca.caracteristicas.length > 0) {
        const campoCaracteristicas = document.querySelector('[data-campo="caracteristicas"]');
        if (campoCaracteristicas) {
            const caracAtual = campoCaracteristicas.value.trim();
            const novasCarac = `[${racaNome}]\n` + raca.caracteristicas.join('\n');
            if (!caracAtual) {
                campoCaracteristicas.value = novasCarac;
            } else if (!caracAtual.includes(`[${racaNome}]`)) {
                campoCaracteristicas.value = caracAtual + '\n\n' + novasCarac;
            }
        }
    }
    
    // 6. Marcar perícias bonus de raça
    if (raca.pericias_bonus) {
        raca.pericias_bonus.forEach(pericia => {
            if (pericia.startsWith('escolha')) return; // Ignorar escolhas manuais
            
            const checkbox = document.querySelector(`[data-campo="pericias_proficientes"][data-valor="${pericia}"]`);
            if (checkbox && !checkbox.checked) {
                checkbox.checked = true;
                atualizarPericia(pericia);
            }
        });
    }
    
    // 7. Atualizar todos os modificadores
    atualizarModificadores();
    
    mostrarNotificacao(`Raça "${racaNome}" aplicada!`, 'success');
}

/**
 * Aplica os bônus e características de uma classe selecionada
 */
function aplicarClasse(classeNome) {
    const classe = CLASSES_DND[classeNome];
    if (!classe) {
        console.log(`Classe "${classeNome}" não encontrada no mapeamento`);
        return;
    }
    
    console.log(`⚔️ Aplicando classe: ${classeNome}`);
    
    // 1. Aplicar dados de vida
    const listaDados = document.getElementById('lista-dados-vida');
    if (listaDados) {
        const primeiraLinha = listaDados.querySelector('.dado-vida-linha');
        if (primeiraLinha) {
            const selectFaces = primeiraLinha.querySelector('.dado-faces');
            const inputQtd = primeiraLinha.querySelector('.dado-qtd');
            
            if (selectFaces) {
                selectFaces.value = classe.dado_vida;
            }
            if (inputQtd) {
                inputQtd.value = getNivelAtual();
            }
        }
    }
    
    // 2. Marcar salvaguardas proficientes
    if (classe.salvaguardas_proficientes) {
        // Primeiro, desmarcar todas
        document.querySelectorAll('[data-campo="salvaguardas_proficientes"]').forEach(cb => {
            cb.checked = false;
        });
        
        // Depois, marcar as da classe
        classe.salvaguardas_proficientes.forEach(salv => {
            const checkbox = document.querySelector(`[data-campo="salvaguardas_proficientes"][data-valor="${salv}"]`);
            if (checkbox) {
                checkbox.checked = true;
                atualizarSalvaguarda(salv);
            }
        });
    }
    
    // 3. Aplicar proficiências de armaduras e armas
    const campoProficiencias = document.querySelector('[data-campo="proficiencias"]');
    if (campoProficiencias) {
        let profTexto = [];
        
        if (classe.armaduras && classe.armaduras.length > 0) {
            profTexto.push('Armaduras: ' + classe.armaduras.join(', '));
        }
        if (classe.armas && classe.armas.length > 0) {
            profTexto.push('Armas: ' + classe.armas.join(', '));
        }
        if (classe.ferramentas && classe.ferramentas.length > 0) {
            profTexto.push('Ferramentas: ' + classe.ferramentas.join(', '));
        }
        
        const profAtual = campoProficiencias.value.trim();
        const novasProf = profTexto.join('\n');
        
        if (!profAtual) {
            campoProficiencias.value = novasProf;
        } else if (!profAtual.includes(classe.armas?.[0] || '')) {
            campoProficiencias.value = profAtual + '\n\n' + novasProf;
        }
    }
    
    // 4. Aplicar características de nível 1
    if (classe.caracteristicas_nivel_1 && classe.caracteristicas_nivel_1.length > 0) {
        const campoCaracteristicas = document.querySelector('[data-campo="caracteristicas"]');
        if (campoCaracteristicas) {
            const caracAtual = campoCaracteristicas.value.trim();
            const novasCarac = `[${classeNome} Nv1]\n` + classe.caracteristicas_nivel_1.join('\n');
            
            if (!caracAtual) {
                campoCaracteristicas.value = novasCarac;
            } else if (!caracAtual.includes(`[${classeNome}`)) {
                campoCaracteristicas.value = caracAtual + '\n\n' + novasCarac;
            }
        }
    }
    
    // 5. Adicionar idiomas bonus da classe (se houver)
    if (classe.idiomas_bonus) {
        const campoLinguas = document.querySelector('[data-campo="linguas"]');
        if (campoLinguas) {
            const linguasAtual = campoLinguas.value.trim();
            const novasLinguas = classe.idiomas_bonus.join(', ');
            
            if (!linguasAtual.includes(novasLinguas)) {
                campoLinguas.value = linguasAtual ? linguasAtual + ', ' + novasLinguas : novasLinguas;
            }
        }
    }
    
    // 6. Exibir informação sobre perícias disponíveis
    if (classe.pericias_disponiveis && classe.qtd_pericias) {
        const periciasDisponiveis = classe.pericias_disponiveis[0] === 'todas' 
            ? 'qualquer perícia' 
            : classe.pericias_disponiveis.map(p => {
                const nomes = {
                    'acrobacia': 'Acrobacia', 'adestrar_animais': 'Adestrar Animais',
                    'arcanismo': 'Arcanismo', 'atletismo': 'Atletismo', 'atuacao': 'Atuação',
                    'enganacao': 'Enganação', 'furtividade': 'Furtividade', 'historia': 'História',
                    'intimidacao': 'Intimidação', 'intuicao': 'Intuição', 'investigacao': 'Investigação',
                    'medicina': 'Medicina', 'natureza': 'Natureza', 'percepcao': 'Percepção',
                    'persuasao': 'Persuasão', 'prestidigitacao': 'Prestidigitação',
                    'religiao': 'Religião', 'sobrevivencia': 'Sobrevivência'
                };
                return nomes[p] || p;
            }).join(', ');
        
        console.log(`📜 ${classeNome}: Escolha ${classe.qtd_pericias} perícias de: ${periciasDisponiveis}`);
    }
    
    // 7. Atualizar salvaguardas
    atualizarTodasSalvaguardas();
    
    mostrarNotificacao(`Classe "${classeNome}" aplicada!`, 'success');
}

/**
 * Calcula e define o HP inicial baseado na classe e constituição
 */
function calcularHPInicial() {
    const campoClasse = document.querySelector('[data-campo="classe"]');
    const classeNome = campoClasse?.value;
    const classe = CLASSES_DND[classeNome];
    
    if (!classe) return;
    
    const valorCon = getValorAtributo('constituicao');
    const modCon = calcularModificador(valorCon);
    const nivel = getNivelAtual();
    
    // HP do primeiro nível = dado máximo + mod CON
    let hpTotal = classe.dado_vida + modCon;
    
    // Para níveis adicionais: média do dado + mod CON por nível
    // Média: d6=4, d8=5, d10=6, d12=7
    const mediasDado = { 6: 4, 8: 5, 10: 6, 12: 7 };
    const mediaDado = mediasDado[classe.dado_vida] || 5;
    
    for (let i = 2; i <= nivel; i++) {
        hpTotal += mediaDado + modCon;
    }
    
    // Garantir mínimo de 1 HP por nível
    hpTotal = Math.max(hpTotal, nivel);
    
    // Aplicar HP
    const campoHpMax = document.querySelector('[data-campo="hp_maximo"]');
    const campoHpAtual = document.querySelector('[data-campo="hp_atual"]');
    
    if (campoHpMax) campoHpMax.value = hpTotal;
    if (campoHpAtual) campoHpAtual.value = hpTotal;
    
    atualizarBarraHP();
    
    return hpTotal;
}

/**
 * Inicializa listeners para seleção de raça e classe
 */
function inicializarSelecaoRacaClasse() {
    // Listener para mudança de raça
    const campoRaca = document.querySelector('[data-campo="raca"]');
    if (campoRaca) {
        campoRaca.addEventListener('change', function() {
            const racaSelecionada = this.value;
            if (racaSelecionada) {
                // Perguntar se quer aplicar automaticamente
                if (confirm(`Deseja aplicar automaticamente os bônus da raça "${racaSelecionada}"?\n\nIsso irá:\n- Adicionar bônus aos atributos\n- Definir velocidade\n- Sugerir idiomas\n- Adicionar características`)) {
                    aplicarRaca(racaSelecionada);
                }
            }
        });
    }
    
    // Listener para mudança de classe
    const campoClasse = document.querySelector('[data-campo="classe"]');
    if (campoClasse) {
        campoClasse.addEventListener('change', function() {
            const classeSelecionada = this.value;
            if (classeSelecionada) {
                // Perguntar se quer aplicar automaticamente
                if (confirm(`Deseja aplicar automaticamente os bônus da classe "${classeSelecionada}"?\n\nIsso irá:\n- Definir dado de vida\n- Marcar salvaguardas proficientes\n- Adicionar proficiências\n- Adicionar características de nível 1`)) {
                    aplicarClasse(classeSelecionada);
                    
                    // Perguntar se quer calcular HP
                    if (confirm('Deseja calcular o HP inicial automaticamente?')) {
                        calcularHPInicial();
                    }
                }
            }
        });
    }
    
    console.log('✅ Seleção de Raça/Classe inicializada');
}

// ==========================================================================
// ROLAGEM DE DADOS
// ==========================================================================

/**
 * Rola um teste de atributo/perícia
 */
function rolarTeste(modificador, nome) {
    const resultado = rolarD20(modificador);
    
    let mensagem = `<strong>${nome}</strong><br>`;
    mensagem += `🎲 d20: ${resultado.d20}`;
    
    if (resultado.critico) {
        mensagem += ' <span class="text-success">(CRÍTICO!)</span>';
    } else if (resultado.falha) {
        mensagem += ' <span class="text-danger">(FALHA CRÍTICA!)</span>';
    }
    
    mensagem += `<br>Modificador: ${formatarModificador(resultado.modificador)}`;
    mensagem += `<br><strong>Total: ${resultado.total}</strong>`;
    
    mostrarResultadoDado(mensagem);
}

/**
 * Rola ataque
 */
function rolarAtaque(acerto, dano, nome) {
    const ataqueRoll = rolarD20(acerto);
    
    let mensagem = `<strong>Ataque: ${nome}</strong><br>`;
    mensagem += `🎲 Acerto: d20(${ataqueRoll.d20}) ${formatarModificador(acerto)} = ${ataqueRoll.total}`;
    
    if (ataqueRoll.critico) {
        mensagem += ' <span class="text-success">CRÍTICO!</span>';
        // Dobra os dados de dano
        const danoRoll = rolarDados(dano);
        const danoRoll2 = rolarDados(dano);
        const danoTotal = danoRoll.total + danoRoll2.total;
        mensagem += `<br>⚔️ Dano Crítico: ${danoRoll.detalhes} + ${danoRoll2.detalhes} = <strong>${danoTotal}</strong>`;
    } else if (ataqueRoll.falha) {
        mensagem += ' <span class="text-danger">FALHA!</span>';
    } else {
        const danoRoll = rolarDados(dano);
        mensagem += `<br>⚔️ Dano: ${danoRoll.detalhes}`;
    }
    
    mostrarResultadoDado(mensagem);
}

/**
 * Mostra resultado da rolagem em um popup
 */
function mostrarResultadoDado(mensagem) {
    let container = document.getElementById('resultado-dado');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'resultado-dado';
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--ficha-card-bg, #16213e);
            border: 2px solid var(--ficha-accent, #e94560);
            border-radius: 10px;
            padding: 1rem;
            z-index: 9999;
            max-width: 300px;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(container);
    }
    
    container.innerHTML = mensagem;
    container.style.display = 'block';
    
    // Auto-hide após 5 segundos
    setTimeout(() => {
        container.style.display = 'none';
    }, 5000);
}

// ==========================================================================
// MODAIS
// ==========================================================================

/**
 * Abre um modal
 */
function abrirModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add('active');
    }
}

/**
 * Fecha um modal
 */
function fecharModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('active');
    }
}

/**
 * Fecha modal ao clicar fora
 */
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay') || e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// ==========================================================================
// NOTIFICAÇÕES
// ==========================================================================

/**
 * Mostra notificação temporária
 */
function mostrarNotificacao(texto, tipo = 'info') {
    let container = document.getElementById('notificacoes');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'notificacoes';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        `;
        document.body.appendChild(container);
    }
    
    const cores = {
        success: '#4ade80',
        error: '#ef4444',
        warning: '#fbbf24',
        info: '#60a5fa',
        danger: '#ef4444'
    };
    
    const notif = document.createElement('div');
    notif.style.cssText = `
        background: ${cores[tipo] || cores.info};
        color: ${tipo === 'warning' ? '#000' : '#fff'};
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    `;
    notif.textContent = texto;
    
    container.appendChild(notif);
    
    setTimeout(() => {
        notif.remove();
    }, 2000);
}

// ==========================================================================
// LISTAS E FILTROS
// ==========================================================================

/**
 * Filtra cards na lista
 */
function filtrarCards() {
    const busca = document.getElementById('busca')?.value.toLowerCase() || '';
    const filtros = {};
    
    document.querySelectorAll('.lista-filtros select').forEach(select => {
        if (select.value) {
            filtros[select.dataset.filtro] = select.value;
        }
    });
    
    document.querySelectorAll('.card-item').forEach(card => {
        let visivel = true;
        
        // Filtro de busca por nome
        if (busca) {
            const nome = card.querySelector('.card-nome')?.textContent.toLowerCase() || '';
            if (!nome.includes(busca)) {
                visivel = false;
            }
        }
        
        // Filtros de select
        Object.entries(filtros).forEach(([key, value]) => {
            const cardValue = card.dataset[key];
            if (cardValue && cardValue !== value) {
                visivel = false;
            }
        });
        
        card.style.display = visivel ? '' : 'none';
    });
}

/**
 * Inicializa filtros nas listas
 */
function inicializarFiltros() {
    document.getElementById('busca')?.addEventListener('input', filtrarCards);
    
    document.querySelectorAll('.lista-filtros select').forEach(select => {
        select.addEventListener('change', filtrarCards);
    });
}

// ==========================================================================
// CRIAÇÃO E EDIÇÃO
// ==========================================================================

/**
 * Salva o formulário atual
 */
async function salvarFicha(tipo) {
    const form = document.querySelector('.ficha-form');
    if (!form) return;
    
    const formData = new FormData(form);
    const dados = Object.fromEntries(formData.entries());
    
    // Converte checkboxes para booleanos
    form.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        dados[cb.name] = cb.checked;
    });
    
    const id = document.querySelector('[data-ficha-id]')?.dataset.fichaId;
    const url = id ? `/fichas/api/${tipo}/${id}` : `/fichas/api/${tipo}`;
    const method = id ? 'PUT' : 'POST';
    
    try {
        const response = await apiRequest(url, method, dados);
        
        if (response.sucesso || response.id) {
            mostrarNotificacao('Salvo com sucesso!', 'success');
            
            // Se criou novo, redireciona para a página de visualização
            if (!id && response.id) {
                window.location.href = `/fichas/${tipo}/${response.id}`;
            }
        } else {
            mostrarNotificacao(response.erro || 'Erro ao salvar', 'error');
        }
    } catch (error) {
        console.error('Erro ao salvar:', error);
        mostrarNotificacao('Erro ao salvar', 'error');
    }
}

/**
 * Exclui uma ficha
 */
async function excluirFicha(tipo, id) {
    if (!confirm('Tem certeza que deseja excluir?')) return;
    
    try {
        const response = await apiRequest(`/fichas/api/${tipo}/${id}`, 'DELETE');
        
        if (response.sucesso) {
            mostrarNotificacao('Excluído com sucesso!', 'success');
            window.location.href = `/fichas/${tipo}s`;
        } else {
            mostrarNotificacao(response.erro || 'Erro ao excluir', 'error');
        }
    } catch (error) {
        console.error('Erro ao excluir:', error);
        mostrarNotificacao('Erro ao excluir', 'error');
    }
}

// ==========================================================================
// INSTÂNCIAS DE MONSTRO
// ==========================================================================

/**
 * Cria instância de monstro para combate
 */
async function criarInstanciaMonstro(monstroId, nome) {
    try {
        const response = await apiRequest('/fichas/api/monstro/instancia', 'POST', {
            monstro_id: monstroId,
            nome: nome
        });
        
        if (response.id) {
            mostrarNotificacao(`${nome} adicionado ao combate!`, 'success');
            return response;
        }
    } catch (error) {
        console.error('Erro ao criar instância:', error);
        mostrarNotificacao('Erro ao criar instância', 'error');
    }
    return null;
}

// ==========================================================================
// DESCANSO
// ==========================================================================

/**
 * Descanso curto - recupera dados de vida
 */
function descansoCurto() {
    mostrarNotificacao('Descanso curto realizado. Role seus dados de vida para recuperar HP.', 'info');
}

/**
 * Descanso longo - recupera HP total e metade dos dados de vida
 */
function descansoLongo() {
    const hpMax = document.querySelector('[data-campo="hp_maximo"]') || document.querySelector('[data-campo="hp_max"]');
    const hpAtual = document.querySelector('[data-campo="hp_atual"]');
    
    if (hpMax && hpAtual) {
        hpAtual.value = hpMax.value;
        hpAtual.dispatchEvent(new Event('input'));
        atualizarBarraHP();
    }
    
    mostrarNotificacao('Descanso longo realizado. HP restaurado ao máximo!', 'success');
}

// ==========================================================================
// PERSONAGEM - CRIAR/SALVAR
// ==========================================================================

/**
 * Salva personagem existente
 */
function salvarPersonagem() {
    const id = document.getElementById('personagem-id')?.value;
    if (!id) {
        mostrarNotificacao('Personagem não tem ID', 'error');
        return;
    }
    
    const dados = coletarDadosPersonagem();
    
    fetch(`/fichas/api/personagem/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            mostrarNotificacao('Personagem salvo!', 'success');
        } else {
            mostrarNotificacao(data.erro || 'Erro ao salvar', 'error');
        }
    })
    .catch(err => {
        console.error(err);
        mostrarNotificacao('Erro de conexão', 'error');
    });
}

/**
 * Cria novo personagem
 */
function criarPersonagem() {
    const dados = coletarDadosPersonagem();
    
    if (!dados.nome || dados.nome.trim() === '' || dados.nome === 'Nome do Personagem') {
        mostrarNotificacao('Informe o nome do personagem', 'warning');
        return;
    }
    
    fetch('/fichas/api/personagem', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(res => res.json())
    .then(data => {
        if (data.id) {
            mostrarNotificacao('Personagem criado!', 'success');
            window.location.href = `/fichas/personagem/${data.id}`;
        } else {
            mostrarNotificacao(data.erro || 'Erro ao criar', 'error');
        }
    })
    .catch(err => {
        console.error(err);
        mostrarNotificacao('Erro de conexão', 'error');
    });
}

/**
 * Coleta dados do formulário de personagem
 */
function coletarDadosPersonagem() {
    const dados = {};
    
    // Campos contenteditable
    document.querySelectorAll('[data-campo][contenteditable]').forEach(el => {
        dados[el.dataset.campo] = el.textContent.trim();
    });
    
    // Inputs e textareas
    document.querySelectorAll('input[data-campo], textarea[data-campo], select[data-campo]').forEach(el => {
        const campo = el.dataset.campo;
        let valor;
        
        if (el.type === 'checkbox') {
            return; // Checkboxes são tratados separadamente
        } else if (el.type === 'number') {
            valor = parseFloat(el.value) || 0;
        } else {
            valor = el.value;
        }
        
        // Campos aninhados (ex: atributos.forca, moedas.po)
        if (campo.includes('.')) {
            const partes = campo.split('.');
            if (!dados[partes[0]]) dados[partes[0]] = {};
            if (partes.length === 2) {
                dados[partes[0]][partes[1]] = valor;
            } else if (partes.length === 3) {
                if (!dados[partes[0]][partes[1]]) dados[partes[0]][partes[1]] = {};
                dados[partes[0]][partes[1]][partes[2]] = valor;
            }
        } else {
            dados[campo] = valor;
        }
    });
    
    // Proficiências em salvaguardas
    dados.salvaguardas_proficientes = [];
    document.querySelectorAll('[data-campo="salvaguardas_proficientes"]:checked').forEach(cb => {
        dados.salvaguardas_proficientes.push(cb.dataset.valor);
    });
    
    // Proficiências em perícias
    dados.pericias_proficientes = [];
    document.querySelectorAll('[data-campo="pericias_proficientes"]:checked').forEach(cb => {
        dados.pericias_proficientes.push(cb.dataset.valor);
    });
    
    return dados;
}

/**
 * Adiciona linha de ataque na tabela
 */
function adicionarAtaque() {
    const tbody = document.getElementById('lista-ataques');
    if (!tbody) return;
    
    const index = tbody.querySelectorAll('tr').length;
    const tr = document.createElement('tr');
    tr.className = 'ataque-item';
    tr.dataset.index = index;
    tr.innerHTML = `
        <td><input type="text" placeholder="Nome da arma" data-campo="armas.${index}.nome"></td>
        <td><input type="text" placeholder="+0" data-campo="armas.${index}.bonus"></td>
        <td><input type="text" placeholder="1d8+0 cort." data-campo="armas.${index}.dano"></td>
    `;
    tbody.appendChild(tr);
}

/**
 * Adiciona linha de equipamento
 */
function adicionarEquipamento() {
    const lista = document.getElementById('lista-equipamentos');
    if (!lista) return;
    
    const index = lista.querySelectorAll('.equipamento-linha').length;
    const div = document.createElement('div');
    div.className = 'equipamento-linha';
    div.innerHTML = `
        <input type="text" class="equipamento-input" data-campo="equipamentos.${index}" placeholder="Item...">
        <button type="button" class="btn-remover-item" onclick="removerEquipamento(this)">×</button>
    `;
    lista.appendChild(div);
    
    // Foca no novo input
    div.querySelector('input').focus();
}

/**
 * Remove linha de equipamento
 */
function removerEquipamento(btn) {
    const linha = btn.closest('.equipamento-linha');
    const lista = linha.parentElement;
    
    // Não remover se for a única linha
    if (lista.querySelectorAll('.equipamento-linha').length > 1) {
        linha.remove();
        // Reindexar os campos
        lista.querySelectorAll('.equipamento-linha').forEach((linha, index) => {
            linha.querySelector('input').dataset.campo = `equipamentos.${index}`;
        });
    } else {
        // Limpar o valor ao invés de remover
        linha.querySelector('input').value = '';
    }
}

/**
 * Adiciona nova linha de dado de vida
 */
function adicionarDadoVida() {
    const lista = document.getElementById('lista-dados-vida');
    if (!lista) return;
    
    const index = lista.querySelectorAll('.dado-vida-linha').length;
    const div = document.createElement('div');
    div.className = 'dado-vida-linha';
    div.innerHTML = `
        <input type="number" class="dado-qtd" value="1" min="0" data-campo="dados_vida.${index}.qtd">
        <span>d</span>
        <select class="dado-faces" data-campo="dados_vida.${index}.faces">
            <option value="6">d6</option>
            <option value="8" selected>d8</option>
            <option value="10">d10</option>
            <option value="12">d12</option>
        </select>
        <button type="button" class="btn-remove-dado" onclick="removerDadoVida(this)" title="Remover">×</button>
    `;
    lista.appendChild(div);
}

/**
 * Remove linha de dado de vida
 */
function removerDadoVida(btn) {
    const linha = btn.closest('.dado-vida-linha');
    const lista = linha.parentElement;
    
    // Não remover se for a única linha
    if (lista.querySelectorAll('.dado-vida-linha').length > 1) {
        linha.remove();
        // Reindexar os campos
        lista.querySelectorAll('.dado-vida-linha').forEach((linha, index) => {
            linha.querySelector('.dado-qtd').dataset.campo = `dados_vida.${index}.qtd`;
            linha.querySelector('.dado-faces').dataset.campo = `dados_vida.${index}.faces`;
        });
    } else {
        // Resetar valores ao invés de remover
        linha.querySelector('.dado-qtd').value = 1;
        linha.querySelector('.dado-faces').value = 8;
    }
}

/**
 * Rola dado
 */
function rolarDado(dado) {
    const match = dado.match(/(\d*)d(\d+)([+-]\d+)?/);
    if (!match) return;
    
    const qtd = parseInt(match[1]) || 1;
    const faces = parseInt(match[2]);
    const mod = parseInt(match[3]) || 0;
    
    let total = mod;
    let rolls = [];
    
    for (let i = 0; i < qtd; i++) {
        const roll = Math.floor(Math.random() * faces) + 1;
        rolls.push(roll);
        total += roll;
    }
    
    const texto = `🎲 ${dado}: [${rolls.join(', ')}]${mod ? ` ${mod >= 0 ? '+' : ''}${mod}` : ''} = ${total}`;
    mostrarNotificacao(texto, 'info');
}

// ==========================================================================
// INICIALIZAÇÃO
// ==========================================================================

document.addEventListener('DOMContentLoaded', function() {
    inicializarAutoSave();
    inicializarFiltros();
    inicializarAutomacao(); // Automação de modificadores D&D 5e
    inicializarSelecaoRacaClasse(); // Automação de raça e classe
    atualizarModificadores();
    atualizarBarraHP();
});

// CSS Animation para notificações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
