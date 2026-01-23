/**
 * FICHAS.JS - Sistema de Fichas D&D 5e
 * Lógica de criação e gerenciamento de personagens
 */

// ==========================================================================
// CACHE DE REGRAS D&D (carregado do servidor)
// ==========================================================================

let REGRAS_DND = null;
let regrasCarregando = false;

/**
 * Carrega todas as regras D&D do servidor
 */
async function carregarRegrasDND() {
    if (REGRAS_DND) return REGRAS_DND;
    if (regrasCarregando) {
        // Aguarda carregamento em andamento
        while (regrasCarregando) {
            await new Promise(r => setTimeout(r, 50));
        }
        return REGRAS_DND;
    }
    
    regrasCarregando = true;
    try {
        const response = await fetch('/api/dnd/regras-completas');
        REGRAS_DND = await response.json();
        console.log('✅ Regras D&D carregadas:', Object.keys(REGRAS_DND.racas).length, 'raças,', Object.keys(REGRAS_DND.classes).length, 'classes');
        return REGRAS_DND;
    } catch (error) {
        console.error('❌ Erro ao carregar regras:', error);
        return null;
    } finally {
        regrasCarregando = false;
    }
}

// ==========================================================================
// CONSTANTES DE CRIAÇÃO DE PERSONAGEM
// ==========================================================================

// Point Buy (PHB)
const POINT_BUY_CUSTOS = { 8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9 };
const POINT_BUY_TOTAL = 27;

// Array Padrão
const ARRAY_PADRAO = [15, 14, 13, 12, 10, 8];

// Atributos
const ATRIBUTOS = ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma'];
const ATRIBUTOS_DISPLAY = {
    'forca': 'Força', 'destreza': 'Destreza', 'constituicao': 'Constituição',
    'inteligencia': 'Inteligência', 'sabedoria': 'Sabedoria', 'carisma': 'Carisma'
};
const ATRIBUTOS_SIGLAS = {
    'forca': 'FOR', 'destreza': 'DES', 'constituicao': 'CON',
    'inteligencia': 'INT', 'sabedoria': 'SAB', 'carisma': 'CAR'
};

// ==========================================================================
// ESTADO DA CRIAÇÃO DE PERSONAGEM
// ==========================================================================

const EstadoCriacao = {
    // Método de geração de atributos
    metodoAtributos: null, // 'rolar', 'array', 'pointbuy'
    
    // Point Buy
    pontosDisponiveis: POINT_BUY_TOTAL,
    atributosBase: { forca: 8, destreza: 8, constituicao: 8, inteligencia: 8, sabedoria: 8, carisma: 8 },
    
    // Array Padrão
    arrayDisponivel: [...ARRAY_PADRAO],
    arrayAtribuido: {},
    
    // Rolar Dados
    rolagemResultados: [],
    rolagemAtribuida: {},
    
    // Bônus de Raça
    bonusRaca: {},
    
    // Escolhas pendentes
    escolhasPendentes: {
        atributos: 0,        // +1 em X atributos (meio-elfo, humano variante)
        pericias: 0,         // Escolher X perícias
        idiomas: 0,          // Escolher X idiomas
        atributosEscolhidos: [],
        periciasEscolhidas: [],
        idiomasEscolhidos: []
    },
    
    // Opções disponíveis para escolha
    opcoesDisponiveis: {
        pericias: [],
        idiomas: []
    }
};

// ==========================================================================
// JANELA FLUTUANTE DE CRIAÇÃO (COMPACTA)
// ==========================================================================

/**
 * Cria a janela flutuante de criação de personagem - versão compacta
 */
function criarJanelaCriacao() {
    const existente = document.getElementById('janela-criacao');
    if (existente) existente.remove();
    
    const janela = document.createElement('div');
    janela.id = 'janela-criacao';
    janela.className = 'janela-criacao';
    janela.innerHTML = `
        <div class="janela-header">
            <span class="janela-titulo">🎲 Atributos</span>
            <div class="janela-controles">
                <button class="btn-janela" onclick="toggleJanelaCriacao()" title="Minimizar">−</button>
                <button class="btn-janela btn-fechar" onclick="fecharJanelaCriacao()" title="Fechar">×</button>
            </div>
        </div>
        <div class="janela-corpo">
            <div class="metodo-btns">
                <button class="btn-m" onclick="selecionarMetodo('rolar')" data-metodo="rolar" title="4d6 drop lowest">🎲</button>
                <button class="btn-m" onclick="selecionarMetodo('array')" data-metodo="array" title="15,14,13,12,10,8">📋</button>
                <button class="btn-m" onclick="selecionarMetodo('pointbuy')" data-metodo="pointbuy" title="27 pontos">💰</button>
            </div>
            <div id="conteudo-metodo"></div>
            <div id="escolhas-pendentes"></div>
        </div>
    `;
    
    document.body.appendChild(janela);
    tornarArrastavel(janela);
    return janela;
}

/**
 * Torna um elemento arrastável
 */
function tornarArrastavel(elemento) {
    const header = elemento.querySelector('.janela-header');
    let isDragging = false;
    let offsetX, offsetY;
    
    header.addEventListener('mousedown', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        isDragging = true;
        offsetX = e.clientX - elemento.offsetLeft;
        offsetY = e.clientY - elemento.offsetTop;
        elemento.style.cursor = 'grabbing';
    });
    
    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        elemento.style.left = (e.clientX - offsetX) + 'px';
        elemento.style.top = (e.clientY - offsetY) + 'px';
        elemento.style.right = 'auto';
    });
    
    document.addEventListener('mouseup', () => {
        isDragging = false;
        elemento.style.cursor = '';
    });
}

/**
 * Toggle minimizar/expandir janela
 */
function toggleJanelaCriacao() {
    const janela = document.getElementById('janela-criacao');
    const corpo = janela.querySelector('.janela-corpo');
    const btn = janela.querySelector('.btn-janela');
    
    if (corpo.style.display === 'none') {
        corpo.style.display = 'block';
        btn.textContent = '−';
        janela.classList.remove('minimizada');
    } else {
        corpo.style.display = 'none';
        btn.textContent = '+';
        janela.classList.add('minimizada');
    }
}

/**
 * Fecha a janela
 */
function fecharJanelaCriacao() {
    const janela = document.getElementById('janela-criacao');
    if (janela) janela.remove();
}

// ==========================================================================
// MÉTODOS DE GERAÇÃO DE ATRIBUTOS
// ==========================================================================

/**
 * Seleciona o método de geração de atributos
 */
function selecionarMetodo(metodo) {
    EstadoCriacao.metodoAtributos = metodo;
    
    document.querySelectorAll('.btn-m').forEach(btn => {
        btn.classList.toggle('ativo', btn.dataset.metodo === metodo);
    });
    
    const container = document.getElementById('conteudo-metodo');
    
    switch(metodo) {
        case 'rolar':
            renderizarRolarDados(container);
            break;
        case 'array':
            renderizarArrayPadrao(container);
            break;
        case 'pointbuy':
            renderizarPointBuy(container);
            break;
    }
}

/**
 * Renderiza interface de rolar dados (4d6 drop lowest) - COMPACTA
 */
function renderizarRolarDados(container) {
    container.innerHTML = `
        <button class="btn-rolar" onclick="rolarAtributos()">🎲 Rolar 4d6</button>
        <div id="grid-rolagem"></div>
    `;
}

/**
 * Rola 4d6 drop lowest, 6 vezes - ordena do maior ao menor
 */
async function rolarAtributos() {
    const resultados = [];
    
    for (let i = 0; i < 6; i++) {
        const dados = [1,2,3,4].map(() => Math.floor(Math.random() * 6) + 1);
        dados.sort((a, b) => a - b);
        const descartado = dados.shift();
        const total = dados.reduce((a, b) => a + b, 0);
        resultados.push({ total, dados, descartado });
    }
    
    // Ordena do maior ao menor
    resultados.sort((a, b) => b.total - a.total);
    EstadoCriacao.rolagemResultados = resultados;
    
    // Já atribui automaticamente na ordem dos atributos
    ATRIBUTOS.forEach((attr, i) => {
        EstadoCriacao.rolagemAtribuida[attr] = i;
    });
    
    renderizarGridRolagem();
}

/**
 * Renderiza o grid de rolagem com valores já posicionados
 */
function renderizarGridRolagem() {
    const container = document.getElementById('grid-rolagem');
    if (!container) return;
    
    let html = '<div class="grid-attrs">';
    ATRIBUTOS.forEach((attr, i) => {
        const idx = EstadoCriacao.rolagemAtribuida[attr];
        const res = EstadoCriacao.rolagemResultados[idx];
        html += `
            <div class="attr-cell" data-attr="${attr}" onclick="iniciarTrocaAtributo('${attr}')">
                <span class="attr-sigla">${ATRIBUTOS_SIGLAS[attr]}</span>
                <span class="attr-valor" data-idx="${idx}">${res.total}</span>
            </div>
        `;
    });
    html += '</div>';
    html += '<button class="btn-aplicar" onclick="aplicarRolagem()">✓ Aplicar</button>';
    html += '<p class="hint">Clique em dois valores para trocar</p>';
    container.innerHTML = html;
}

// Variável para troca de atributos
let atributoSelecionado = null;

/**
 * Inicia ou completa troca de atributo
 */
function iniciarTrocaAtributo(attr) {
    const cell = document.querySelector(`.attr-cell[data-attr="${attr}"]`);
    
    if (!atributoSelecionado) {
        // Primeiro clique - seleciona
        atributoSelecionado = attr;
        cell.classList.add('selecionado');
    } else if (atributoSelecionado === attr) {
        // Clicou no mesmo - cancela
        cell.classList.remove('selecionado');
        atributoSelecionado = null;
    } else {
        // Segundo clique - troca
        const idx1 = EstadoCriacao.rolagemAtribuida[atributoSelecionado];
        const idx2 = EstadoCriacao.rolagemAtribuida[attr];
        
        EstadoCriacao.rolagemAtribuida[atributoSelecionado] = idx2;
        EstadoCriacao.rolagemAtribuida[attr] = idx1;
        
        atributoSelecionado = null;
        renderizarGridRolagem();
    }
}

/**
 * Aplica os valores da rolagem na ficha
 */
function aplicarRolagem() {
    for (const [atributo, index] of Object.entries(EstadoCriacao.rolagemAtribuida)) {
        const valor = EstadoCriacao.rolagemResultados[index].total;
        EstadoCriacao.atributosBase[atributo] = valor;
        
        const campo = document.querySelector(`[data-campo="atributos.${atributo}"]`);
        if (campo) {
            const valorTotal = valor + (EstadoCriacao.bonusRaca[atributo] || 0);
            campo.value = valorTotal;
            atualizarModificadorAtributo(atributo);
        }
    }
    
    mostrarNotificacao('Atributos aplicados!', 'success');
}

/**
 * Renderiza interface de Array Padrão - COMPACTA
 */
function renderizarArrayPadrao(container) {
    // Já atribui na ordem
    ATRIBUTOS.forEach((attr, i) => {
        EstadoCriacao.arrayAtribuido[attr] = ARRAY_PADRAO[i];
    });
    
    renderizarGridArray(container);
}

function renderizarGridArray(container) {
    let html = '<div class="grid-attrs">';
    ATRIBUTOS.forEach(attr => {
        const val = EstadoCriacao.arrayAtribuido[attr];
        html += `
            <div class="attr-cell" data-attr="${attr}" onclick="iniciarTrocaArray('${attr}')">
                <span class="attr-sigla">${ATRIBUTOS_SIGLAS[attr]}</span>
                <span class="attr-valor">${val}</span>
            </div>
        `;
    });
    html += '</div>';
    html += '<button class="btn-aplicar" onclick="aplicarArray()">✓ Aplicar</button>';
    html += '<p class="hint">Clique em dois valores para trocar</p>';
    container.innerHTML = html;
}

let arrayAtributoSelecionado = null;

function iniciarTrocaArray(attr) {
    const cell = document.querySelector(`.attr-cell[data-attr="${attr}"]`);
    
    if (!arrayAtributoSelecionado) {
        arrayAtributoSelecionado = attr;
        cell.classList.add('selecionado');
    } else if (arrayAtributoSelecionado === attr) {
        cell.classList.remove('selecionado');
        arrayAtributoSelecionado = null;
    } else {
        // Troca valores
        const val1 = EstadoCriacao.arrayAtribuido[arrayAtributoSelecionado];
        const val2 = EstadoCriacao.arrayAtribuido[attr];
        EstadoCriacao.arrayAtribuido[arrayAtributoSelecionado] = val2;
        EstadoCriacao.arrayAtribuido[attr] = val1;
        
        arrayAtributoSelecionado = null;
        renderizarGridArray(document.getElementById('conteudo-metodo'));
    }
}

/**
 * Aplica o array padrão na ficha
 */
function aplicarArray() {
    for (const [atributo, valor] of Object.entries(EstadoCriacao.arrayAtribuido)) {
        EstadoCriacao.atributosBase[atributo] = valor;
        
        const campo = document.querySelector(`[data-campo="atributos.${atributo}"]`);
        if (campo) {
            const valorTotal = valor + (EstadoCriacao.bonusRaca[atributo] || 0);
            campo.value = valorTotal;
            atualizarModificadorAtributo(atributo);
        }
    }
    
    mostrarNotificacao('Atributos aplicados!', 'success');
}

/**
 * Renderiza interface de Point Buy - COMPACTA
 */
function renderizarPointBuy(container) {
    EstadoCriacao.pontosDisponiveis = POINT_BUY_TOTAL;
    EstadoCriacao.atributosBase = { forca: 8, destreza: 8, constituicao: 8, inteligencia: 8, sabedoria: 8, carisma: 8 };
    
    let html = '<div class="pb-header">Pontos: <span id="pontos-restantes">' + POINT_BUY_TOTAL + '</span></div>';
    html += '<div class="pb-grid">';
    ATRIBUTOS.forEach(attr => {
        html += `
            <div class="pb-row">
                <span class="pb-sigla">${ATRIBUTOS_SIGLAS[attr]}</span>
                <button class="pb-btn" onclick="ajustarPointBuy('${attr}', -1)">−</button>
                <span class="pb-val" id="pb-${attr}">8</span>
                <button class="pb-btn" onclick="ajustarPointBuy('${attr}', 1)">+</button>
            </div>
        `;
    });
    html += '</div>';
    html += '<button class="btn-aplicar" onclick="aplicarPointBuy()">✓ Aplicar</button>';
    container.innerHTML = html;
}

/**
 * Ajusta valor no Point Buy
 */
function ajustarPointBuy(atributo, delta) {
    const valorAtual = EstadoCriacao.atributosBase[atributo];
    const novoValor = valorAtual + delta;
    
    if (novoValor < 8 || novoValor > 15) return;
    
    const custoAtual = POINT_BUY_CUSTOS[valorAtual];
    const custoNovo = POINT_BUY_CUSTOS[novoValor];
    const diferenca = custoNovo - custoAtual;
    
    if (EstadoCriacao.pontosDisponiveis - diferenca < 0) return;
    
    EstadoCriacao.atributosBase[atributo] = novoValor;
    EstadoCriacao.pontosDisponiveis -= diferenca;
    
    document.getElementById(`pb-${atributo}`).textContent = novoValor;
    const pontosEl = document.getElementById('pontos-restantes');
    pontosEl.textContent = EstadoCriacao.pontosDisponiveis;
    pontosEl.classList.toggle('zerado', EstadoCriacao.pontosDisponiveis === 0);
}

/**
 * Aplica Point Buy na ficha
 */
function aplicarPointBuy() {
    for (const [atributo, valor] of Object.entries(EstadoCriacao.atributosBase)) {
        const campo = document.querySelector(`[data-campo="atributos.${atributo}"]`);
        if (campo) {
            const valorTotal = valor + (EstadoCriacao.bonusRaca[atributo] || 0);
            campo.value = valorTotal;
            atualizarModificadorAtributo(atributo);
        }
    }
    
    mostrarNotificacao('Atributos aplicados!', 'success');
}

// ==========================================================================
// APLICAÇÃO AUTOMÁTICA DE RAÇA
// ==========================================================================

/**
 * Aplica automaticamente os bônus de uma raça
 */
async function aplicarRaca(racaNome) {
    const regras = await carregarRegrasDND();
    if (!regras) return;
    
    const raca = regras.racas[racaNome];
    if (!raca) {
        console.log(`Raça "${racaNome}" não encontrada`);
        return;
    }
    
    console.log(`🧝 Aplicando raça: ${racaNome}`);
    
    // Limpa bônus anteriores
    EstadoCriacao.bonusRaca = {};
    EstadoCriacao.escolhasPendentes = {
        atributos: 0,
        pericias: 0,
        idiomas: 0,
        atributosEscolhidos: [],
        periciasEscolhidas: [],
        idiomasEscolhidos: []
    };
    
    // 1. Aplicar bônus fixos de atributos
    if (raca.bonus_atributos) {
        for (const [attr, bonus] of Object.entries(raca.bonus_atributos)) {
            EstadoCriacao.bonusRaca[attr] = bonus;
            
            const campo = document.querySelector(`[data-campo="atributos.${attr}"]`);
            if (campo) {
                const valorBase = EstadoCriacao.atributosBase[attr] || 8;
                campo.value = valorBase + bonus;
                atualizarModificadorAtributo(attr);
            }
        }
    }
    
    // 2. Aplicar velocidade
    if (raca.velocidade) {
        const campoVelocidade = document.querySelector('[data-campo="velocidade"]');
        if (campoVelocidade) {
            campoVelocidade.value = raca.velocidade + 'm';
        }
    }
    
    // 3. Aplicar idiomas fixos
    if (raca.idiomas && raca.idiomas.length > 0) {
        const campoLinguas = document.querySelector('[data-campo="linguas"]');
        if (campoLinguas) {
            campoLinguas.value = raca.idiomas.join(', ');
        }
    }
    
    // 4. Aplicar proficiências de raça
    const proficiencias = [];
    if (raca.proficiencias_armas?.length) proficiencias.push('Armas: ' + raca.proficiencias_armas.join(', '));
    if (raca.proficiencias_armaduras?.length) proficiencias.push('Armaduras: ' + raca.proficiencias_armaduras.join(', '));
    if (raca.proficiencias_ferramentas?.length) proficiencias.push('Ferramentas: ' + raca.proficiencias_ferramentas.join(', '));
    
    if (proficiencias.length > 0) {
        const campoProficiencias = document.querySelector('[data-campo="proficiencias"]');
        if (campoProficiencias) {
            const atual = campoProficiencias.value.trim();
            const novaProf = `[${racaNome}]\n${proficiencias.join('\n')}`;
            campoProficiencias.value = atual ? atual + '\n\n' + novaProf : novaProf;
        }
    }
    
    // 5. Aplicar características
    if (raca.caracteristicas?.length > 0) {
        const campoCaracteristicas = document.querySelector('[data-campo="caracteristicas"]');
        if (campoCaracteristicas) {
            const atual = campoCaracteristicas.value.trim();
            const novasCarac = `[${racaNome}]\n${raca.caracteristicas.join('\n')}`;
            campoCaracteristicas.value = atual ? atual + '\n\n' + novasCarac : novasCarac;
        }
    }
    
    // 6. Marcar perícias bonus
    if (raca.pericias_bonus?.length > 0) {
        raca.pericias_bonus.forEach(pericia => {
            const checkbox = document.querySelector(`[data-campo="pericias_proficientes"][data-valor="${pericia}"]`);
            if (checkbox && !checkbox.checked) {
                checkbox.checked = true;
                atualizarPericia(pericia);
            }
        });
    }
    
    // 7. Verificar escolhas pendentes
    if (raca.atributos_escolha > 0) {
        EstadoCriacao.escolhasPendentes.atributos = raca.atributos_escolha;
    }
    if (raca.pericias_escolha > 0) {
        EstadoCriacao.escolhasPendentes.pericias = raca.pericias_escolha;
    }
    if (raca.idiomas_escolha > 0) {
        EstadoCriacao.escolhasPendentes.idiomas = raca.idiomas_escolha;
    }
    
    // 8. Atualizar seção de raça na janela
    atualizarSecaoRaca(raca);
    
    // 9. Atualizar resumo
    atualizarResumo();
    
    // Recalcular tudo
    atualizarModificadores();
}

/**
 * Atualiza a seção de raça na janela de criação
 */
function atualizarSecaoRaca(raca) {
    const secao = document.getElementById('secao-raca');
    const conteudo = document.getElementById('conteudo-raca');
    
    if (!raca) {
        secao.style.display = 'none';
        return;
    }
    
    secao.style.display = 'block';
    
    let html = '';
    
    // Mostrar bônus fixos aplicados
    if (raca.bonus_atributos && Object.keys(raca.bonus_atributos).length > 0) {
        html += '<div class="bonus-aplicados">';
        html += '<strong>Bônus aplicados:</strong> ';
        html += Object.entries(raca.bonus_atributos)
            .map(([attr, val]) => `${ATRIBUTOS_SIGLAS[attr]} +${val}`)
            .join(', ');
        html += '</div>';
    }
    
    // Escolhas de atributos pendentes
    if (EstadoCriacao.escolhasPendentes.atributos > 0) {
        html += `
            <div class="escolha-pendente">
                <strong>Escolha +1 em ${EstadoCriacao.escolhasPendentes.atributos} atributo(s):</strong>
                <div class="opcoes-atributos">
                    ${ATRIBUTOS.map(attr => `
                        <label class="opcao-checkbox">
                            <input type="checkbox" 
                                   data-escolha="atributo" 
                                   data-valor="${attr}"
                                   ${raca.bonus_atributos?.[attr] ? 'disabled' : ''}
                                   onchange="escolherAtributoBonus('${attr}', this.checked)">
                            ${ATRIBUTOS_SIGLAS[attr]}
                        </label>
                    `).join('')}
                </div>
                <small class="contador-escolhas">
                    Escolhidos: <span id="contador-atributos">0</span>/${EstadoCriacao.escolhasPendentes.atributos}
                </small>
            </div>
        `;
    }
    
    // Escolhas de idiomas pendentes
    if (EstadoCriacao.escolhasPendentes.idiomas > 0) {
        html += `
            <div class="escolha-pendente">
                <strong>Escolha ${EstadoCriacao.escolhasPendentes.idiomas} idioma(s):</strong>
                <select id="select-idioma-bonus" onchange="escolherIdiomaBonus(this.value)">
                    <option value="">-- Selecione --</option>
                </select>
                <div id="idiomas-escolhidos"></div>
            </div>
        `;
    }
    
    conteudo.innerHTML = html;
    
    // Popula select de idiomas se necessário
    if (EstadoCriacao.escolhasPendentes.idiomas > 0) {
        popularSelectIdiomas();
    }
}

/**
 * Popula o select de idiomas disponíveis
 */
async function popularSelectIdiomas() {
    const regras = await carregarRegrasDND();
    if (!regras) return;
    
    const select = document.getElementById('select-idioma-bonus');
    if (!select) return;
    
    // Agrupa por tipo
    const comuns = regras.idiomas.filter(i => i.tipo === 'comum');
    const exoticos = regras.idiomas.filter(i => i.tipo === 'exotico');
    
    let options = '<option value="">-- Selecione --</option>';
    
    options += '<optgroup label="Comuns">';
    comuns.forEach(i => {
        options += `<option value="${i.nome}">${i.nome}</option>`;
    });
    options += '</optgroup>';
    
    options += '<optgroup label="Exóticos">';
    exoticos.forEach(i => {
        options += `<option value="${i.nome}">${i.nome}</option>`;
    });
    options += '</optgroup>';
    
    select.innerHTML = options;
}

/**
 * Escolhe um atributo para receber +1 de bônus
 */
function escolherAtributoBonus(atributo, checked) {
    const escolhidos = EstadoCriacao.escolhasPendentes.atributosEscolhidos;
    const max = EstadoCriacao.escolhasPendentes.atributos;
    
    if (checked) {
        if (escolhidos.length >= max) {
            // Já escolheu o máximo
            event.target.checked = false;
            return;
        }
        escolhidos.push(atributo);
        
        // Aplica +1 no atributo
        const campo = document.querySelector(`[data-campo="atributos.${atributo}"]`);
        if (campo) {
            campo.value = parseInt(campo.value) + 1;
            atualizarModificadorAtributo(atributo);
        }
    } else {
        const index = escolhidos.indexOf(atributo);
        if (index > -1) {
            escolhidos.splice(index, 1);
            
            // Remove +1 do atributo
            const campo = document.querySelector(`[data-campo="atributos.${atributo}"]`);
            if (campo) {
                campo.value = parseInt(campo.value) - 1;
                atualizarModificadorAtributo(atributo);
            }
        }
    }
    
    // Atualiza contador
    const contador = document.getElementById('contador-atributos');
    if (contador) contador.textContent = escolhidos.length;
    
    atualizarResumo();
}

/**
 * Escolhe um idioma bonus
 */
function escolherIdiomaBonus(idioma) {
    if (!idioma) return;
    
    const escolhidos = EstadoCriacao.escolhasPendentes.idiomasEscolhidos;
    const max = EstadoCriacao.escolhasPendentes.idiomas;
    
    if (escolhidos.length >= max) {
        mostrarNotificacao(`Já escolheu ${max} idioma(s)`, 'warning');
        return;
    }
    
    if (escolhidos.includes(idioma)) {
        mostrarNotificacao('Idioma já escolhido', 'warning');
        return;
    }
    
    escolhidos.push(idioma);
    
    // Atualiza campo de línguas
    const campoLinguas = document.querySelector('[data-campo="linguas"]');
    if (campoLinguas) {
        const atual = campoLinguas.value.trim();
        campoLinguas.value = atual ? atual + ', ' + idioma : idioma;
    }
    
    // Mostra idiomas escolhidos
    const container = document.getElementById('idiomas-escolhidos');
    if (container) {
        container.innerHTML = escolhidos.map(i => `<span class="tag-idioma">${i}</span>`).join(' ');
    }
    
    // Reset select
    document.getElementById('select-idioma-bonus').value = '';
    
    atualizarResumo();
}

// ==========================================================================
// APLICAÇÃO AUTOMÁTICA DE CLASSE
// ==========================================================================

/**
 * Aplica automaticamente os bônus de uma classe
 */
async function aplicarClasse(classeNome) {
    const regras = await carregarRegrasDND();
    if (!regras) return;
    
    const classe = regras.classes[classeNome];
    if (!classe) {
        console.log(`Classe "${classeNome}" não encontrada`);
        return;
    }
    
    console.log(`⚔️ Aplicando classe: ${classeNome}`);
    
    // 1. Aplicar dados de vida
    const listaDados = document.getElementById('lista-dados-vida');
    if (listaDados) {
        const primeiraLinha = listaDados.querySelector('.dado-vida-linha');
        if (primeiraLinha) {
            const selectFaces = primeiraLinha.querySelector('.dado-faces');
            if (selectFaces) selectFaces.value = classe.dado_vida;
        }
    }
    
    // 2. Marcar salvaguardas proficientes
    if (classe.salvaguardas_proficientes) {
        // Desmarca todas primeiro
        document.querySelectorAll('[data-campo="salvaguardas_proficientes"]').forEach(cb => {
            cb.checked = false;
        });
        
        // Marca as da classe
        classe.salvaguardas_proficientes.forEach(salv => {
            const checkbox = document.querySelector(`[data-campo="salvaguardas_proficientes"][data-valor="${salv}"]`);
            if (checkbox) {
                checkbox.checked = true;
                atualizarSalvaguarda(salv);
            }
        });
    }
    
    // 3. Aplicar proficiências
    const proficiencias = [];
    if (classe.armaduras?.length) proficiencias.push('Armaduras: ' + classe.armaduras.join(', '));
    if (classe.armas?.length) proficiencias.push('Armas: ' + classe.armas.join(', '));
    if (classe.ferramentas?.length) proficiencias.push('Ferramentas: ' + classe.ferramentas.join(', '));
    
    if (proficiencias.length > 0) {
        const campoProficiencias = document.querySelector('[data-campo="proficiencias"]');
        if (campoProficiencias) {
            const atual = campoProficiencias.value.trim();
            const novaProf = `[${classeNome}]\n${proficiencias.join('\n')}`;
            
            // Remove proficiências de classe anterior se houver
            const limpo = atual.replace(/\[(?:Bárbaro|Bardo|Bruxo|Clérigo|Druida|Feiticeiro|Guerreiro|Ladino|Mago|Monge|Paladino|Patrulheiro)\][\s\S]*?(?=\[|$)/g, '').trim();
            campoProficiencias.value = limpo ? limpo + '\n\n' + novaProf : novaProf;
        }
    }
    
    // 4. Aplicar características nível 1
    if (classe.caracteristicas_nivel_1?.length > 0) {
        const campoCaracteristicas = document.querySelector('[data-campo="caracteristicas"]');
        if (campoCaracteristicas) {
            const atual = campoCaracteristicas.value.trim();
            const novasCarac = `[${classeNome} Nv1]\n${classe.caracteristicas_nivel_1.join('\n')}`;
            
            // Remove características de classe anterior
            const limpo = atual.replace(/\[(?:Bárbaro|Bardo|Bruxo|Clérigo|Druida|Feiticeiro|Guerreiro|Ladino|Mago|Monge|Paladino|Patrulheiro) Nv\d+\][\s\S]*?(?=\[|$)/g, '').trim();
            campoCaracteristicas.value = limpo ? limpo + '\n\n' + novasCarac : novasCarac;
        }
    }
    
    // 5. Configurar escolha de perícias
    EstadoCriacao.opcoesDisponiveis.pericias = classe.pericias_disponiveis || [];
    const qtdPericias = classe.qtd_pericias || 2;
    
    // 6. Atualizar seção de classe na janela
    atualizarSecaoClasse(classe, classeNome);
    
    // 7. Calcular HP inicial
    calcularHPInicial(classe);
    
    // 8. Atualizar resumo
    atualizarResumo();
    
    // Recalcular salvaguardas
    atualizarTodasSalvaguardas();
}

/**
 * Atualiza a seção de classe na janela de criação
 */
async function atualizarSecaoClasse(classe, classeNome) {
    const secao = document.getElementById('secao-classe');
    const conteudo = document.getElementById('conteudo-classe');
    
    if (!classe) {
        secao.style.display = 'none';
        return;
    }
    
    const regras = await carregarRegrasDND();
    secao.style.display = 'block';
    
    const periciasDisponiveis = classe.pericias_disponiveis || [];
    const qtdPericias = classe.qtd_pericias || 2;
    const todasPericias = periciasDisponiveis[0] === 'todas';
    
    let html = `
        <div class="info-classe">
            <p><strong>Dado de Vida:</strong> d${classe.dado_vida}</p>
            <p><strong>Salvaguardas:</strong> ${classe.salvaguardas_proficientes?.map(s => ATRIBUTOS_SIGLAS[s]).join(', ') || 'Nenhuma'}</p>
        </div>
        <div class="escolha-pericias">
            <strong>Escolha ${qtdPericias} perícia(s)${todasPericias ? ' (qualquer)' : ''}:</strong>
            <div class="opcoes-pericias">
    `;
    
    // Lista de perícias para escolher
    const periciasParaMostrar = todasPericias 
        ? Object.values(regras.pericias)
        : periciasDisponiveis.map(p => regras.pericias[p]).filter(Boolean);
    
    periciasParaMostrar.forEach(p => {
        if (!p) return;
        html += `
            <label class="opcao-checkbox">
                <input type="checkbox" 
                       data-escolha="pericia-classe" 
                       data-valor="${p.nome}"
                       onchange="escolherPericiaClasse('${p.nome}', this.checked)">
                ${p.nome_display}
            </label>
        `;
    });
    
    html += `
            </div>
            <small class="contador-escolhas">
                Escolhidas: <span id="contador-pericias-classe">0</span>/${qtdPericias}
            </small>
        </div>
    `;
    
    conteudo.innerHTML = html;
    
    // Guarda quantidade de perícias da classe
    EstadoCriacao.qtdPericiasClasse = qtdPericias;
    EstadoCriacao.periciasClasseEscolhidas = [];
}

/**
 * Escolhe uma perícia da classe
 */
function escolherPericiaClasse(pericia, checked) {
    const escolhidas = EstadoCriacao.periciasClasseEscolhidas || [];
    const max = EstadoCriacao.qtdPericiasClasse || 2;
    
    if (checked) {
        if (escolhidas.length >= max) {
            event.target.checked = false;
            return;
        }
        escolhidas.push(pericia);
        
        // Marca na ficha
        const checkbox = document.querySelector(`[data-campo="pericias_proficientes"][data-valor="${pericia}"]`);
        if (checkbox && !checkbox.checked) {
            checkbox.checked = true;
            atualizarPericia(pericia);
        }
    } else {
        const index = escolhidas.indexOf(pericia);
        if (index > -1) {
            escolhidas.splice(index, 1);
            
            // Desmarca na ficha
            const checkbox = document.querySelector(`[data-campo="pericias_proficientes"][data-valor="${pericia}"]`);
            if (checkbox && checkbox.checked) {
                checkbox.checked = false;
                atualizarPericia(pericia);
            }
        }
    }
    
    EstadoCriacao.periciasClasseEscolhidas = escolhidas;
    
    // Atualiza contador
    const contador = document.getElementById('contador-pericias-classe');
    if (contador) contador.textContent = escolhidas.length;
    
    atualizarResumo();
}

/**
 * Calcula HP inicial baseado na classe
 */
function calcularHPInicial(classe) {
    const valorCon = getValorAtributo('constituicao');
    const modCon = calcularModificador(valorCon);
    const nivel = getNivelAtual();
    
    // HP do primeiro nível = dado máximo + mod CON
    let hpTotal = classe.dado_vida + modCon;
    
    // Para níveis adicionais: média do dado + mod CON
    const mediasDado = { 6: 4, 8: 5, 10: 6, 12: 7 };
    const mediaDado = mediasDado[classe.dado_vida] || 5;
    
    for (let i = 2; i <= nivel; i++) {
        hpTotal += mediaDado + modCon;
    }
    
    // Mínimo 1 HP por nível
    hpTotal = Math.max(hpTotal, nivel);
    
    // Aplica
    const campoHpMax = document.querySelector('[data-campo="hp_maximo"]');
    const campoHpAtual = document.querySelector('[data-campo="hp_atual"]');
    
    if (campoHpMax) campoHpMax.value = hpTotal;
    if (campoHpAtual) campoHpAtual.value = hpTotal;
    
    atualizarBarraHP();
    
    return hpTotal;
}

// ==========================================================================
// RESUMO E ATUALIZAÇÃO
// ==========================================================================

/**
 * Atualiza o resumo na janela de criação
 */
function atualizarResumo() {
    const conteudo = document.getElementById('conteudo-resumo');
    if (!conteudo) return;
    
    const raca = document.querySelector('[data-campo="raca"]')?.value || '';
    const classe = document.querySelector('[data-campo="classe"]')?.value || '';
    const nivel = getNivelAtual();
    
    let html = '<div class="resumo-criacao">';
    
    // Info básica
    html += `<p><strong>Raça:</strong> ${raca || 'Não selecionada'}</p>`;
    html += `<p><strong>Classe:</strong> ${classe || 'Não selecionada'} Nv${nivel}</p>`;
    
    // Atributos finais
    html += '<div class="resumo-atributos"><strong>Atributos:</strong><br>';
    ATRIBUTOS.forEach(attr => {
        const base = EstadoCriacao.atributosBase[attr] || 8;
        const bonus = EstadoCriacao.bonusRaca[attr] || 0;
        const escolhaBonus = EstadoCriacao.escolhasPendentes.atributosEscolhidos?.includes(attr) ? 1 : 0;
        const total = base + bonus + escolhaBonus;
        const mod = calcularModificador(total);
        const modStr = mod >= 0 ? `+${mod}` : `${mod}`;
        
        html += `<span class="resumo-attr">${ATRIBUTOS_SIGLAS[attr]}: ${total} (${modStr})</span> `;
    });
    html += '</div>';
    
    // Escolhas pendentes
    const pendentes = [];
    if (EstadoCriacao.escolhasPendentes.atributos > 0) {
        const faltam = EstadoCriacao.escolhasPendentes.atributos - (EstadoCriacao.escolhasPendentes.atributosEscolhidos?.length || 0);
        if (faltam > 0) pendentes.push(`${faltam} atributo(s)`);
    }
    if (EstadoCriacao.escolhasPendentes.pericias > 0) {
        const faltam = EstadoCriacao.escolhasPendentes.pericias - (EstadoCriacao.escolhasPendentes.periciasEscolhidas?.length || 0);
        if (faltam > 0) pendentes.push(`${faltam} perícia(s) de raça`);
    }
    if (EstadoCriacao.escolhasPendentes.idiomas > 0) {
        const faltam = EstadoCriacao.escolhasPendentes.idiomas - (EstadoCriacao.escolhasPendentes.idiomasEscolhidos?.length || 0);
        if (faltam > 0) pendentes.push(`${faltam} idioma(s)`);
    }
    if (EstadoCriacao.qtdPericiasClasse > 0) {
        const faltam = EstadoCriacao.qtdPericiasClasse - (EstadoCriacao.periciasClasseEscolhidas?.length || 0);
        if (faltam > 0) pendentes.push(`${faltam} perícia(s) de classe`);
    }
    
    if (pendentes.length > 0) {
        html += `<p class="pendentes-aviso">⚠️ Falta escolher: ${pendentes.join(', ')}</p>`;
    } else if (raca && classe) {
        html += '<p class="completo-aviso">✅ Criação completa!</p>';
    }
    
    html += '</div>';
    conteudo.innerHTML = html;
}

// ==========================================================================
// FUNÇÕES DE CÁLCULO D&D 5e
// ==========================================================================

/**
 * Calcula modificador de atributo
 */
function calcularModificador(valor) {
    return Math.floor((valor - 10) / 2);
}

/**
 * Formata modificador (+X ou -X)
 */
function formatarModificador(mod) {
    return mod >= 0 ? `+${mod}` : `${mod}`;
}

/**
 * Obtém valor atual de um atributo
 */
function getValorAtributo(atributo) {
    const campo = document.querySelector(`[data-campo="atributos.${atributo}"]`);
    return campo ? parseInt(campo.value) || 10 : 10;
}

/**
 * Obtém nível atual
 */
function getNivelAtual() {
    const campo = document.querySelector('[data-campo="nivel"]');
    return campo ? parseInt(campo.value) || 1 : 1;
}

/**
 * Calcula bônus de proficiência por nível
 */
function calcularBonusProficiencia(nivel) {
    return 2 + Math.floor((nivel - 1) / 4);
}

/**
 * Atualiza o modificador de um atributo específico
 */
function atualizarModificadorAtributo(atributo) {
    const valor = getValorAtributo(atributo);
    const mod = calcularModificador(valor);
    
    const displayMod = document.querySelector(`[data-mod="${atributo}"]`);
    if (displayMod) {
        displayMod.textContent = formatarModificador(mod);
    }
    
    // Atualiza perícias relacionadas
    atualizarPericiasPorAtributo(atributo);
    
    // Atualiza salvaguarda relacionada
    atualizarSalvaguarda(atributo);
    
    // Se for destreza, atualiza iniciativa
    if (atributo === 'destreza') {
        atualizarIniciativa();
    }
}

/**
 * Atualiza todos os modificadores
 */
function atualizarModificadores() {
    ATRIBUTOS.forEach(attr => atualizarModificadorAtributo(attr));
}

/**
 * Mapeamento de perícias para atributos
 */
const PERICIAS_ATRIBUTOS = {
    'acrobacia': 'destreza', 'furtividade': 'destreza', 'prestidigitacao': 'destreza',
    'atletismo': 'forca',
    'arcanismo': 'inteligencia', 'historia': 'inteligencia', 'investigacao': 'inteligencia',
    'natureza': 'inteligencia', 'religiao': 'inteligencia',
    'lidar_animais': 'sabedoria', 'intuicao': 'sabedoria', 'medicina': 'sabedoria',
    'percepcao': 'sabedoria', 'sobrevivencia': 'sabedoria',
    'atuacao': 'carisma', 'blefar': 'carisma', 'intimidacao': 'carisma', 'persuasao': 'carisma'
};

/**
 * Atualiza perícias de um atributo específico
 */
function atualizarPericiasPorAtributo(atributo) {
    for (const [pericia, attr] of Object.entries(PERICIAS_ATRIBUTOS)) {
        if (attr === atributo) {
            atualizarPericia(pericia);
        }
    }
}

/**
 * Atualiza uma perícia específica
 */
function atualizarPericia(pericia) {
    const atributo = PERICIAS_ATRIBUTOS[pericia];
    if (!atributo) return;
    
    const valorAtributo = getValorAtributo(atributo);
    const modAtributo = calcularModificador(valorAtributo);
    
    const checkbox = document.querySelector(`[data-campo="pericias_proficientes"][data-valor="${pericia}"]`);
    const proficiente = checkbox?.checked || false;
    
    const nivel = getNivelAtual();
    const bonusProf = calcularBonusProficiencia(nivel);
    
    const total = modAtributo + (proficiente ? bonusProf : 0);
    
    const display = document.querySelector(`[data-pericia-valor="${pericia}"]`);
    if (display) {
        display.textContent = formatarModificador(total);
    }
}

/**
 * Atualiza uma salvaguarda
 */
function atualizarSalvaguarda(atributo) {
    const valorAtributo = getValorAtributo(atributo);
    const modAtributo = calcularModificador(valorAtributo);
    
    const checkbox = document.querySelector(`[data-campo="salvaguardas_proficientes"][data-valor="${atributo}"]`);
    const proficiente = checkbox?.checked || false;
    
    const nivel = getNivelAtual();
    const bonusProf = calcularBonusProficiencia(nivel);
    
    const total = modAtributo + (proficiente ? bonusProf : 0);
    
    const display = document.querySelector(`[data-salvaguarda-valor="${atributo}"]`);
    if (display) {
        display.textContent = formatarModificador(total);
    }
}

/**
 * Atualiza todas as salvaguardas
 */
function atualizarTodasSalvaguardas() {
    ATRIBUTOS.forEach(attr => atualizarSalvaguarda(attr));
}

/**
 * Atualiza iniciativa
 */
function atualizarIniciativa() {
    const valorDestreza = getValorAtributo('destreza');
    const modDestreza = calcularModificador(valorDestreza);
    
    const campoBonus = document.querySelector('[data-campo="iniciativa_bonus"]');
    const bonus = campoBonus ? parseInt(campoBonus.value) || 0 : 0;
    
    const total = modDestreza + bonus;
    
    const display = document.querySelector('[data-display="iniciativa"]');
    if (display) {
        display.textContent = formatarModificador(total);
    }
}

/**
 * Atualiza bônus de proficiência quando nível muda
 */
function atualizarBonusProficienciaPorNivel() {
    const nivel = getNivelAtual();
    const bonus = calcularBonusProficiencia(nivel);
    
    const display = document.querySelector('[data-campo="bonus_proficiencia"]');
    if (display) {
        display.value = bonus;
    }
    
    atualizarTudoComProficiencia();
}

/**
 * Recalcula tudo que usa bônus de proficiência
 */
function atualizarTudoComProficiencia() {
    // Recalcula todas as perícias
    for (const pericia of Object.keys(PERICIAS_ATRIBUTOS)) {
        atualizarPericia(pericia);
    }
    // Recalcula todas as salvaguardas
    atualizarTodasSalvaguardas();
}

// ==========================================================================
// BARRA DE HP
// ==========================================================================

function atualizarBarraHP() {
    const hpAtual = parseInt(document.querySelector('[data-campo="hp_atual"]')?.value) || 0;
    const hpMax = parseInt(document.querySelector('[data-campo="hp_maximo"]')?.value) || 1;
    
    const porcentagem = Math.max(0, Math.min(100, (hpAtual / hpMax) * 100));
    
    const barra = document.querySelector('.hp-bar-fill');
    if (barra) {
        barra.style.width = porcentagem + '%';
        
        // Cores baseadas em HP
        barra.classList.remove('hp-100', 'hp-75', 'hp-50', 'hp-25');
        if (porcentagem > 75) barra.classList.add('hp-100');
        else if (porcentagem > 50) barra.classList.add('hp-75');
        else if (porcentagem > 25) barra.classList.add('hp-50');
        else barra.classList.add('hp-25');
    }
}

// ==========================================================================
// NOTIFICAÇÕES
// ==========================================================================

function mostrarNotificacao(mensagem, tipo = 'info') {
    const container = document.getElementById('notificacoes') || criarContainerNotificacoes();
    
    const notif = document.createElement('div');
    notif.className = `notificacao notif-${tipo}`;
    notif.innerHTML = `
        <span>${mensagem}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(notif);
    
    setTimeout(() => notif.remove(), 4000);
}

function criarContainerNotificacoes() {
    const container = document.createElement('div');
    container.id = 'notificacoes';
    container.className = 'container-notificacoes';
    document.body.appendChild(container);
    return container;
}

// ==========================================================================
// FUNÇÕES DE AÇÃO (BOTÕES DA FICHA)
// ==========================================================================

/**
 * Abre modal para aplicar dano
 */
function abrirModalDano() {
    const modal = document.getElementById('modal-dano');
    if (modal) {
        modal.style.display = 'flex';
        const input = document.getElementById('input-dano');
        if (input) {
            input.value = '';
            input.focus();
        }
    }
}

/**
 * Abre modal para curar
 */
function abrirModalCura() {
    const modal = document.getElementById('modal-cura');
    if (modal) {
        modal.style.display = 'flex';
        const input = document.getElementById('input-cura');
        if (input) {
            input.value = '';
            input.focus();
        }
    }
}

/**
 * Fecha um modal pelo ID
 */
function fecharModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

/**
 * Aplica dano ao personagem
 */
function aplicarDano() {
    const input = document.getElementById('input-dano');
    const dano = parseInt(input?.value) || 0;
    if (dano <= 0) {
        mostrarNotificacao('Informe o valor do dano', 'warning');
        return;
    }
    
    const campoHP = document.querySelector('[data-campo="hp_atual"]');
    const campoTemp = document.querySelector('[data-campo="hp_temporario"]');
    
    let hpAtual = parseInt(campoHP?.value) || 0;
    let hpTemp = parseInt(campoTemp?.value) || 0;
    let danoRestante = dano;
    
    // Primeiro absorve com HP temporário
    if (hpTemp > 0) {
        if (hpTemp >= danoRestante) {
            hpTemp -= danoRestante;
            danoRestante = 0;
        } else {
            danoRestante -= hpTemp;
            hpTemp = 0;
        }
        if (campoTemp) campoTemp.value = hpTemp;
    }
    
    // Depois aplica no HP atual
    hpAtual = Math.max(0, hpAtual - danoRestante);
    if (campoHP) campoHP.value = hpAtual;
    
    atualizarBarraHP();
    fecharModal('modal-dano');
    mostrarNotificacao(`⚔️ -${dano} HP`, 'danger');
}

/**
 * Aplica cura ao personagem
 */
function aplicarCura() {
    const input = document.getElementById('input-cura');
    const cura = parseInt(input?.value) || 0;
    if (cura <= 0) {
        mostrarNotificacao('Informe o valor da cura', 'warning');
        return;
    }
    
    const campoHP = document.querySelector('[data-campo="hp_atual"]');
    const campoHPMax = document.querySelector('[data-campo="hp_maximo"]');
    
    const hpAtual = parseInt(campoHP?.value) || 0;
    const hpMax = parseInt(campoHPMax?.value) || 1;
    
    const novoHP = Math.min(hpMax, hpAtual + cura);
    if (campoHP) campoHP.value = novoHP;
    
    atualizarBarraHP();
    fecharModal('modal-cura');
    mostrarNotificacao(`💚 +${cura} HP`, 'success');
}

/**
 * Descanso Curto - Recupera HP usando dados de vida
 */
function descansoCurto() {
    mostrarNotificacao('🌙 Descanso Curto - Use seus Dados de Vida para recuperar HP', 'info');
    // TODO: Implementar modal para gastar dados de vida
}

/**
 * Descanso Longo - Recupera HP total e metade dos dados de vida
 */
function descansoLongo() {
    const campoHP = document.querySelector('[data-campo="hp_atual"]');
    const campoHPMax = document.querySelector('[data-campo="hp_maximo"]');
    const campoDVAtual = document.querySelector('[data-campo="dados_vida_atual"]');
    const campoDVMax = document.querySelector('[data-campo="dados_vida_max"]');
    
    // Recupera HP total
    const hpMax = parseInt(campoHPMax?.value) || 1;
    if (campoHP) campoHP.value = hpMax;
    
    // Recupera metade dos dados de vida
    if (campoDVAtual && campoDVMax) {
        const dvMax = parseInt(campoDVMax.value) || 1;
        const dvAtual = parseInt(campoDVAtual.value) || 0;
        const recupera = Math.max(1, Math.floor(dvMax / 2));
        campoDVAtual.value = Math.min(dvMax, dvAtual + recupera);
    }
    
    atualizarBarraHP();
    mostrarNotificacao('🛏️ Descanso Longo - HP restaurado, dados de vida recuperados', 'success');
}

/**
 * Rola um dado e mostra o resultado
 */
function rolarDado(notacao) {
    // Parseia notação tipo "1d20", "2d6+3", etc
    const match = notacao.match(/(\d+)?d(\d+)([+-]\d+)?/i);
    if (!match) {
        mostrarNotificacao('Notação de dado inválida', 'danger');
        return;
    }
    
    const quantidade = parseInt(match[1]) || 1;
    const faces = parseInt(match[2]);
    const modificador = parseInt(match[3]) || 0;
    
    let total = 0;
    const resultados = [];
    
    for (let i = 0; i < quantidade; i++) {
        const resultado = Math.floor(Math.random() * faces) + 1;
        resultados.push(resultado);
        total += resultado;
    }
    
    total += modificador;
    
    const detalhes = resultados.join(' + ') + (modificador ? ` ${modificador >= 0 ? '+' : ''}${modificador}` : '');
    mostrarNotificacao(`🎲 ${notacao}: ${total} (${detalhes})`, 'info');
    
    return total;
}

/**
 * Adiciona um novo ataque à lista
 */
function adicionarAtaque() {
    const container = document.getElementById('lista-ataques');
    if (!container) return;
    
    // Conta quantas armas já existem para o índice
    const linhas = container.querySelectorAll('tr');
    const index = linhas.length;
    
    const novaLinha = document.createElement('tr');
    novaLinha.innerHTML = `
        <td><input type="text" placeholder="Nome da Arma/Magia" data-campo="armas.${index}.nome"></td>
        <td><input type="text" placeholder="+0" data-campo="armas.${index}.bonus" class="input-bonus"></td>
        <td class="td-dados">
            <div class="dados-container" data-index="${index}">
                <div class="dado-linha">
                    <input type="text" class="input-dado" placeholder="1d8+3">
                    <button type="button" class="btn-remover-dado" onclick="removerDado(this)">×</button>
                </div>
            </div>
            <button type="button" class="btn-add-dado" onclick="adicionarDado(this)" title="Adicionar dado">+</button>
        </td>
        <td>
            <select data-campo="armas.${index}.tipo" class="select-tipo-dano" title="Selecione o tipo de dano">
                <option value="">-</option>
                <option value="Ácido" title="Substância corrosiva causa queimaduras">Ácido</option>
                <option value="Contundente" title="Impacto físico causando hematomas">Contundente</option>
                <option value="Cortante" title="Ferimentos abertos sangrando">Cortante</option>
                <option value="Elétrico" title="Choque percorrendo o corpo">Elétrico</option>
                <option value="Energético" title="Energia mágica pura (força)">Energético</option>
                <option value="Gélido" title="Congelamento e hipotermia">Gélido</option>
                <option value="Ígneo" title="Queimando, em chamas">Ígneo</option>
                <option value="Necrótico" title="Energia vital sendo drenada">Necrótico</option>
                <option value="Perfurante" title="Feridas profundas penetrantes">Perfurante</option>
                <option value="Psíquico" title="Mente sendo atacada">Psíquico</option>
                <option value="Radiante" title="Luz divina queimando">Radiante</option>
                <option value="Trovejante" title="Ondas sonoras devastadoras">Trovejante</option>
                <option value="Venenoso" title="Toxina no sistema">Venenoso</option>
            </select>
        </td>
        <td><button type="button" class="btn-remover-item" onclick="removerAtaque(this)">×</button></td>
    `;
    container.appendChild(novaLinha);
}

/**
 * Adiciona um dado extra ao ataque (para múltiplos dados de dano)
 */
function adicionarDado(btn) {
    const container = btn.previousElementSibling;
    if (!container || !container.classList.contains('dados-container')) return;
    
    const novoDiv = document.createElement('div');
    novoDiv.className = 'dado-linha';
    novoDiv.innerHTML = `
        <input type="text" class="input-dado" placeholder="1d6">
        <button type="button" class="btn-remover-dado" onclick="removerDado(this)">×</button>
    `;
    container.appendChild(novoDiv);
    agendarAutoSave();
}

/**
 * Remove um dado da lista de dados do ataque
 */
function removerDado(btn) {
    const linha = btn.closest('.dado-linha');
    const container = linha?.parentElement;
    
    // Não permite remover se for o único dado
    if (container && container.querySelectorAll('.dado-linha').length > 1) {
        linha.remove();
        agendarAutoSave();
    }
}

/**
 * Remove um ataque da lista
 */
function removerAtaque(btn) {
    const linha = btn.closest('tr');
    if (linha) linha.remove();
}

/**
 * Adiciona um novo item de equipamento
 */
function adicionarEquipamento() {
    const container = document.getElementById('lista-equipamentos');
    if (!container) return;
    
    // Conta quantos itens já existem para o índice
    const linhas = container.querySelectorAll('.equipamento-linha');
    const index = linhas.length;
    
    const novoItem = document.createElement('div');
    novoItem.className = 'equipamento-linha';
    novoItem.innerHTML = `
        <input type="text" class="equipamento-input" data-campo="equipamentos.${index}" placeholder="Item...">
        <button type="button" class="btn-remover-item" onclick="removerEquipamento(this)">×</button>
    `;
    container.appendChild(novoItem);
}

/**
 * Remove um equipamento da lista
 */
function removerEquipamento(btn) {
    const item = btn.closest('.equipamento-linha');
    if (item) item.remove();
}

/**
 * Adiciona um dado de vida (quando sobe de nível)
 */
function adicionarDadoVida() {
    const campoDVAtual = document.querySelector('[data-campo="dados_vida_atual"]');
    const campoDVMax = document.querySelector('[data-campo="dados_vida_max"]');
    
    if (campoDVAtual && campoDVMax) {
        const dvMax = parseInt(campoDVMax.value) || 0;
        campoDVMax.value = dvMax + 1;
        campoDVAtual.value = dvMax + 1;
    }
}

/**
 * Cria um novo personagem (para ficha nova)
 */
async function criarPersonagem() {
    const form = document.querySelector('.ficha-personagem');
    if (!form) return;
    
    const dados = coletarDadosPersonagem();
    
    // Validação básica
    if (!dados.nome || dados.nome.trim() === '') {
        mostrarNotificacao('Informe o nome do personagem', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/fichas/api/personagem', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (response.ok) {
            const resultado = await response.json();
            form.dataset.id = resultado.id;
            history.replaceState(null, '', `/fichas/personagem/${resultado.id}`);
            mostrarNotificacao('✅ Personagem criado com sucesso!', 'success');
            
            // Remove janela de criação
            fecharJanelaCriacao();
        } else {
            mostrarNotificacao('Erro ao criar personagem', 'danger');
        }
    } catch (error) {
        console.error('Erro:', error);
        mostrarNotificacao('Erro de conexão', 'danger');
    }
}

// ==========================================================================
// AUTO-SAVE
// ==========================================================================

let autoSaveTimeout = null;

function inicializarAutoSave() {
    document.querySelectorAll('[data-campo]').forEach(campo => {
        campo.addEventListener('change', () => agendarAutoSave());
        if (campo.tagName === 'INPUT' || campo.tagName === 'TEXTAREA') {
            campo.addEventListener('input', () => agendarAutoSave());
        }
    });
}

function agendarAutoSave() {
    if (autoSaveTimeout) clearTimeout(autoSaveTimeout);
    autoSaveTimeout = setTimeout(salvarPersonagem, 2000);
}

async function salvarPersonagem() {
    const form = document.querySelector('.ficha-personagem');
    if (!form) return;
    
    const dados = coletarDadosPersonagem();
    const id = form.dataset.id;
    
    // Debug: ver o que está sendo enviado
    console.log('📤 Dados a salvar:', JSON.stringify(dados, null, 2));
    console.log('📤 Armas:', dados.armas);
    console.log('📤 Equipamentos:', dados.equipamentos);
    
    try {
        const url = id ? `/fichas/api/personagem/${id}` : '/fichas/api/personagem';
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (response.ok) {
            const resultado = await response.json();
            if (!id && resultado.id) {
                form.dataset.id = resultado.id;
                history.replaceState(null, '', `/fichas/personagem/${resultado.id}`);
            }
            mostrarNotificacao('💾 Ficha salva com sucesso!', 'success');
            console.log('💾 Salvo');
        } else {
            mostrarNotificacao('❌ Erro ao salvar ficha', 'danger');
        }
    } catch (error) {
        console.error('Erro ao salvar:', error);
        mostrarNotificacao('❌ Erro de conexão ao salvar', 'danger');
    }
}

async function deletarPersonagem() {
    const form = document.querySelector('.ficha-personagem');
    if (!form) return;
    
    const id = form.dataset.id;
    if (!id) return;
    
    const nome = document.querySelector('.input-nome-personagem')?.value || 'este personagem';
    
    if (!confirm(`⚠️ Tem certeza que deseja DELETAR ${nome}?\n\nEsta ação não pode ser desfeita!`)) {
        return;
    }
    
    try {
        const response = await fetch(`/fichas/api/personagem/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            mostrarNotificacao('🗑️ Personagem deletado!', 'info');
            setTimeout(() => window.location.href = '/fichas/personagens', 1000);
        } else {
            mostrarNotificacao('❌ Erro ao deletar', 'danger');
        }
    } catch (error) {
        console.error('Erro ao deletar:', error);
        mostrarNotificacao('❌ Erro de conexão', 'danger');
    }
}

function coletarDadosPersonagem() {
    const dados = {
        atributos: {},
        pericias_proficientes: [],
        salvaguardas_proficientes: [],
        armas: [],
        equipamentos: [],
        moedas: { pc: 0, pp: 0, pe: 0, po: 0, pl: 0 }
    };
    
    // Coleta armas com nova estrutura (nome, bonus, dados[], tipo)
    document.querySelectorAll('#lista-ataques tr').forEach((tr, index) => {
        const nome = tr.querySelector('[data-campo*=".nome"]')?.value || '';
        const bonus = tr.querySelector('[data-campo*=".bonus"]')?.value || '';
        const tipo = tr.querySelector('[data-campo*=".tipo"]')?.value || '';
        
        // Coleta todos os dados de dano
        const dadosDano = [];
        tr.querySelectorAll('.dados-container .input-dado').forEach(input => {
            const valor = input.value.trim();
            if (valor) dadosDano.push(valor);
        });
        
        if (nome || bonus || dadosDano.length > 0) {
            dados.armas.push({ nome, bonus, dados: dadosDano, tipo });
        }
    });
    
    // Coleta equipamentos
    document.querySelectorAll('#lista-equipamentos .equipamento-linha').forEach((linha, index) => {
        const input = linha.querySelector('.equipamento-input');
        if (input && input.value.trim()) {
            dados.equipamentos.push(input.value.trim());
        }
    });
    
    // Coleta moedas
    ['pc', 'pp', 'pe', 'po', 'pl'].forEach(moeda => {
        const campo = document.querySelector(`[data-campo="moedas.${moeda}"]`);
        if (campo) {
            dados.moedas[moeda] = parseInt(campo.value) || 0;
        }
    });
    
    document.querySelectorAll('[data-campo]').forEach(campo => {
        const nomeCampo = campo.dataset.campo;
        
        // Pula campos já coletados explicitamente
        if (nomeCampo.startsWith('armas.') || 
            nomeCampo.startsWith('equipamentos.') ||
            nomeCampo.startsWith('moedas.')) {
            return;
        }
        
        // Pula campos internos/computados (com . exceto atributos)
        if (nomeCampo.includes('.') && !nomeCampo.startsWith('atributos.')) {
            return;
        }
        
        if (nomeCampo.startsWith('atributos.')) {
            const attr = nomeCampo.replace('atributos.', '');
            dados.atributos[attr] = parseInt(campo.value) || 10;
        } else if (nomeCampo === 'pericias_proficientes') {
            if (campo.checked) {
                dados.pericias_proficientes.push(campo.dataset.valor);
            }
        } else if (nomeCampo === 'salvaguardas_proficientes') {
            if (campo.checked) {
                dados.salvaguardas_proficientes.push(campo.dataset.valor);
            }
        } else if (campo.type === 'checkbox') {
            dados[nomeCampo] = campo.checked ? 1 : 0;
        } else if (campo.type === 'number') {
            dados[nomeCampo] = parseInt(campo.value) || 0;
        } else {
            dados[nomeCampo] = campo.value;
        }
    });
    
    return dados;
}

// ==========================================================================
// INICIALIZAÇÃO
// ==========================================================================

function inicializarAutomacao() {
    // Listeners para mudança de atributos
    ATRIBUTOS.forEach(attr => {
        const campo = document.querySelector(`[data-campo="atributos.${attr}"]`);
        if (campo) {
            campo.addEventListener('change', () => atualizarModificadorAtributo(attr));
            campo.addEventListener('input', () => atualizarModificadorAtributo(attr));
        }
    });
    
    // Listeners para proficiência em perícias
    document.querySelectorAll('[data-campo="pericias_proficientes"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const pericia = checkbox.dataset.valor;
            atualizarPericia(pericia);
        });
    });
    
    // Listeners para proficiência em salvaguardas
    document.querySelectorAll('[data-campo="salvaguardas_proficientes"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const atributo = checkbox.dataset.valor;
            atualizarSalvaguarda(atributo);
        });
    });
    
    // Listener para mudança de nível
    const campoNivel = document.querySelector('[data-campo="nivel"]');
    if (campoNivel) {
        campoNivel.addEventListener('change', atualizarBonusProficienciaPorNivel);
        campoNivel.addEventListener('input', atualizarBonusProficienciaPorNivel);
    }
    
    // Listener para mudança manual do bônus de proficiência
    const campoBonus = document.querySelector('[data-campo="bonus_proficiencia"]');
    if (campoBonus) {
        campoBonus.addEventListener('change', atualizarTudoComProficiencia);
        campoBonus.addEventListener('input', atualizarTudoComProficiencia);
    }
    
    // Listeners para HP
    const campoHpAtual = document.querySelector('[data-campo="hp_atual"]');
    const campoHpMax = document.querySelector('[data-campo="hp_maximo"]');
    if (campoHpAtual) campoHpAtual.addEventListener('input', atualizarBarraHP);
    if (campoHpMax) campoHpMax.addEventListener('input', atualizarBarraHP);
    
    // Inicializa textareas auto-expand
    inicializarAutoExpand();
    
    console.log('✅ Automação D&D 5e inicializada');
}

/**
 * Inicializa textareas com auto-expand
 */
function inicializarAutoExpand() {
    document.querySelectorAll('.auto-expand').forEach(textarea => {
        // Ajusta altura inicial baseado no conteúdo
        autoExpandTextarea(textarea);
        
        // Listeners para ajustar conforme digita
        textarea.addEventListener('input', () => autoExpandTextarea(textarea));
        textarea.addEventListener('change', () => autoExpandTextarea(textarea));
    });
}

/**
 * Ajusta a altura do textarea baseado no conteúdo
 */
function autoExpandTextarea(textarea) {
    // Reseta a altura para calcular corretamente
    textarea.style.height = 'auto';
    
    // Define a nova altura baseada no scrollHeight
    const minHeight = textarea.classList.contains('textarea-bloco') ? 60 : 45;
    const newHeight = Math.max(minHeight, textarea.scrollHeight);
    textarea.style.height = newHeight + 'px';
}

/**
 * Inicializa listeners para seleção de raça e classe
 */
function inicializarSelecaoRacaClasse() {
    // Listener para mudança de raça - aplicação automática
    const campoRaca = document.querySelector('[data-campo="raca"]');
    if (campoRaca) {
        campoRaca.addEventListener('change', function() {
            if (this.value) {
                aplicarRaca(this.value);
            }
        });
    }
    
    // Listener para mudança de classe - aplicação automática
    const campoClasse = document.querySelector('[data-campo="classe"]');
    if (campoClasse) {
        campoClasse.addEventListener('change', function() {
            if (this.value) {
                aplicarClasse(this.value);
            }
        });
    }
    
    console.log('✅ Seleção automática de Raça/Classe inicializada');
}

/**
 * Inicializa filtros de listas
 */
function inicializarFiltros() {
    const filtro = document.getElementById('filtro-lista');
    if (filtro) {
        filtro.addEventListener('input', function() {
            const termo = this.value.toLowerCase();
            document.querySelectorAll('.lista-item').forEach(item => {
                const texto = item.textContent.toLowerCase();
                item.style.display = texto.includes(termo) ? '' : 'none';
            });
        });
    }
}

// ==========================================================================
// INICIALIZAÇÃO PRINCIPAL
// ==========================================================================

document.addEventListener('DOMContentLoaded', async function() {
    // Carrega regras D&D
    await carregarRegrasDND();
    
    // Inicializa sistemas
    inicializarAutoSave();
    inicializarFiltros();
    inicializarAutomacao();
    inicializarSelecaoRacaClasse();
    
    // Atualiza valores iniciais
    atualizarModificadores();
    atualizarBarraHP();
    
    // Cria janela de criação se for novo personagem
    const ficha = document.querySelector('.ficha-personagem');
    if (ficha && !ficha.dataset.id) {
        criarJanelaCriacao();
    }
});
