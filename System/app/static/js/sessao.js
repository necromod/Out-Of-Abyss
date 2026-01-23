/**
 * Out of the Abyss - Tela de Sessão
 * Lógica da tela principal de mestragem
 */

// =========================================
// Estado da Sessão
// =========================================

const SessaoState = {
    mapaAtual: null,
    combateAtivo: false,
    widgets: [],
    logCombate: [],
    ordemTurnos: [],  // Lista de participantes no combate
    turnoAtual: 0,    // Índice do turno atual
    contadorMonstros: {},  // Contador de monstros por tipo: { 'Goblin': 2, 'Orc': 1 }
    roundAtual: 0     // Contador de rounds da batalha
};

// Condições do D&D 5e com descrições
const CONDICOES_DND = {
    'agarrado': {
        nome: 'Agarrado',
        descricao: 'Deslocamento 0, não se beneficia de bônus de deslocamento. Encerra se quem agarrou ficar incapacitado ou se um efeito remover do alcance.'
    },
    'amedrontado': {
        nome: 'Amedrontado',
        descricao: 'Desvantagem em testes de habilidade e ataques enquanto a fonte do medo estiver visível. Não pode se mover voluntariamente para mais perto da fonte.'
    },
    'atordoado': {
        nome: 'Atordoado',
        descricao: 'Incapacitado, não pode se mover, fala hesitante. Falha automática em resistências de FOR/DES. Ataques contra têm vantagem.'
    },
    'caido': {
        nome: 'Caído',
        descricao: 'Só pode rastejar. Desvantagem em ataques. Ataques até 1,5m têm vantagem, outros têm desvantagem.'
    },
    'cego': {
        nome: 'Cego',
        descricao: 'Falha automática em testes que precisem de visão. Ataques contra têm vantagem, seus ataques têm desvantagem.'
    },
    'enfeiticado': {
        nome: 'Enfeitiçado',
        descricao: 'Não pode atacar quem o enfeitiçou ou usar habilidades nocivas contra ele. Quem enfeitiçou tem vantagem em testes sociais.'
    },
    'envenenado': {
        nome: 'Envenenado',
        descricao: 'Desvantagem em jogadas de ataque e testes de habilidade.'
    },
    'impedido': {
        nome: 'Impedido',
        descricao: 'Deslocamento 0. Ataques contra têm vantagem, seus ataques têm desvantagem. Desvantagem em resistências de DES.'
    },
    'incapacitado': {
        nome: 'Incapacitado',
        descricao: 'Não pode realizar ações ou reações.'
    },
    'inconsciente': {
        nome: 'Inconsciente',
        descricao: 'Incapacitado, não pode se mover/falar, sem ciência dos arredores. Larga objetos, fica caído. Falha em FOR/DES. Ataques têm vantagem, crítico até 1,5m.'
    },
    'invisivel': {
        nome: 'Invisível',
        descricao: 'Impossível de ver sem magia. Considerado em escuridão densa. Ataques contra têm desvantagem, seus ataques têm vantagem.'
    },
    'paralisado': {
        nome: 'Paralisado',
        descricao: 'Incapacitado, não pode se mover ou falar. Falha em FOR/DES. Ataques têm vantagem, crítico até 1,5m.'
    },
    'petrificado': {
        nome: 'Petrificado',
        descricao: 'Transformado em pedra, peso x10, para de envelhecer. Incapacitado. Resistência a todos os danos. Imune a veneno/doença.'
    },
    'surdo': {
        nome: 'Surdo',
        descricao: 'Falha automática em testes que precisem de audição.'
    },
    'exaustao': {
        nome: 'Exaustão',
        descricao: '1: Desv. em testes. 2: Veloc./2. 3: Desv. ataques/resistências. 4: HP máx./2. 5: Veloc.=0. 6: Morte.'
    }
};

// =========================================
// Sistema de Input Flutuante
// =========================================

let inputFlutuanteAtivo = null;

function criarInputFlutuante(botao, tipo, callback) {
    // Fecha input anterior se existir
    fecharInputFlutuante();
    
    const rect = botao.getBoundingClientRect();
    const container = document.createElement('div');
    container.className = `input-flutuante input-flutuante-${tipo}`;
    container.innerHTML = `
        <input type="number" class="input-flutuante-valor" placeholder="0" min="0" autofocus>
        <button class="input-flutuante-confirmar">✓</button>
        <button class="input-flutuante-cancelar">✕</button>
    `;
    
    // Posiciona abaixo do botão
    container.style.position = 'fixed';
    container.style.left = `${rect.left}px`;
    container.style.top = `${rect.bottom + 5}px`;
    container.style.zIndex = '9999';
    
    document.body.appendChild(container);
    inputFlutuanteAtivo = container;
    
    const input = container.querySelector('.input-flutuante-valor');
    const btnConfirmar = container.querySelector('.input-flutuante-confirmar');
    const btnCancelar = container.querySelector('.input-flutuante-cancelar');
    
    // Foca no input
    setTimeout(() => input.focus(), 10);
    
    // Enter para confirmar
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const valor = parseInt(input.value) || 0;
            if (valor > 0) {
                callback(valor);
                fecharInputFlutuante();
            }
        } else if (e.key === 'Escape') {
            fecharInputFlutuante();
        }
    });
    
    btnConfirmar.addEventListener('click', () => {
        const valor = parseInt(input.value) || 0;
        if (valor > 0) {
            callback(valor);
            fecharInputFlutuante();
        }
    });
    
    btnCancelar.addEventListener('click', fecharInputFlutuante);
    
    // Fecha ao clicar fora
    setTimeout(() => {
        document.addEventListener('click', fecharInputFlutuanteClickFora);
    }, 100);
}

function fecharInputFlutuante() {
    if (inputFlutuanteAtivo) {
        inputFlutuanteAtivo.remove();
        inputFlutuanteAtivo = null;
    }
    document.removeEventListener('click', fecharInputFlutuanteClickFora);
}

function fecharInputFlutuanteClickFora(e) {
    if (inputFlutuanteAtivo && !inputFlutuanteAtivo.contains(e.target)) {
        fecharInputFlutuante();
    }
}

// =========================================
// Sistema de Log de Combate
// =========================================

function adicionarLogCombate(mensagem, tipo = 'info') {
    const timestamp = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    
    SessaoState.logCombate.push({
        timestamp,
        mensagem,
        tipo
    });
    
    atualizarWidgetLog();
    
    // Persiste no servidor
    API.post('/sessao/api/log', {
        tipo,
        mensagem,
        dados: {}
    }).catch(() => {});
}

function atualizarWidgetLog() {
    const logContainer = document.getElementById('log-combate');
    if (!logContainer) return;
    
    if (SessaoState.logCombate.length === 0) {
        logContainer.innerHTML = '<p class="text-muted">Nenhuma ação registrada</p>';
        return;
    }
    
    // Mostra os últimos 20 registros, mais recentes primeiro
    const logs = SessaoState.logCombate.slice(-20).reverse();
    logContainer.innerHTML = logs.map(log => `
        <div class="log-item log-${log.tipo}">
            <span class="log-time">${log.timestamp}</span>
            <span class="log-msg">${log.mensagem}</span>
        </div>
    `).join('');
    
    // Scroll para o topo (mais recente)
    logContainer.scrollTop = 0;
}

// =========================================
// Funções de Mapa
// =========================================

async function abrirSeletorMapa() {
    abrirModal('modal-mapa');
    await carregarListaMapas();
}

async function carregarListaMapas() {
    try {
        const mapas = await API.get('/api/imagens/cenarios');
        const container = document.getElementById('lista-mapas');
        
        if (mapas.length === 0) {
            container.innerHTML = '<p class="text-muted">Nenhum mapa encontrado em Imagens/Cenários</p>';
            return;
        }
        
        container.innerHTML = mapas.map(mapa => `
            <div class="mapa-item" onclick="selecionarMapa('${mapa.caminho.replace(/\\/g, '\\\\')}')">
                <span class="mapa-nome">${mapa.nome}</span>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar mapas:', error);
    }
}

function selecionarMapa(caminho) {
    const container = document.getElementById('mapa-container');
    container.innerHTML = '';
    container.style.backgroundImage = `url('file:///${caminho}')`;
    
    SessaoState.mapaAtual = caminho;
    fecharModal('modal-mapa');
    
    notificar('Mapa alterado', 'success');
}

// =========================================
// Funções de Widget
// =========================================

function adicionarWidget(tipo) {
    // Widgets singleton (apenas uma instância)
    const singletonTypes = ['iniciativa', 'log_combate'];
    
    if (singletonTypes.includes(tipo)) {
        // Verifica se já existe
        const existente = encontrarWidgetPorTipo(tipo);
        if (existente) {
            // Traz para frente e retorna
            existente.trazerParaFrente();
            return existente;
        }
    }
    
    const widget = window.widgetManager.criar(tipo);
    
    // Carrega conteúdo específico
    switch (tipo) {
        case 'dados':
            widget.setConteudo(getConteudoDados());
            break;
        case 'notas':
            widget.setConteudo(getConteudoNotas());
            break;
        case 'iniciativa':
            widget.setConteudo(getConteudoIniciativa());
            atualizarWidgetIniciativa();
            break;
        case 'log_combate':
            widget.setConteudo(getConteudoLog());
            break;
        case 'ficha_personagem':
            abrirSeletorPersonagem(widget);
            break;
        case 'ficha_monstro':
            abrirSeletorMonstro(widget);
            break;
        default:
            widget.setConteudo('<p class="text-muted">Conteúdo não disponível</p>');
    }
    
    return widget;
}

function encontrarWidgetPorTipo(tipo) {
    if (!window.widgetManager) return null;
    const widgets = window.widgetManager.widgets;
    return Array.from(widgets.values()).find(w => w.tipo === tipo);
}

// =========================================
// Conteúdos de Widgets
// =========================================

function getConteudoDados() {
    return `
        <div class="widget-dados">
            <div class="dados-input">
                <input type="text" id="dados-expressao" placeholder="Ex: 1d20+5, 2d6+3" value="1d20">
                <button class="btn btn-primary mt-1" onclick="executarRolagem()">🎲 Rolar</button>
            </div>
            <div class="dados-resultado" id="dados-resultado">-</div>
            <div class="dados-detalhes" id="dados-detalhes"></div>
        </div>
    `;
}

async function executarRolagem() {
    const expressao = document.getElementById('dados-expressao').value;
    const resultado = await rolarDados(expressao);
    
    document.getElementById('dados-resultado').textContent = resultado.total;
    
    let detalhes = `Dados: [${resultado.dados.join(', ')}]`;
    if (resultado.modificador !== 0) {
        detalhes += ` ${resultado.modificador >= 0 ? '+' : ''}${resultado.modificador}`;
    }
    if (resultado.critico) detalhes += ' 🎯 CRÍTICO!';
    if (resultado.falha_critica) detalhes += ' 💀 FALHA CRÍTICA!';
    
    document.getElementById('dados-detalhes').textContent = detalhes;
}

function getConteudoNotas() {
    return `
        <textarea class="notas-textarea" placeholder="Anotações da sessão..."></textarea>
    `;
}

function getConteudoIniciativa() {
    return `
        <div class="iniciativa-round" id="contador-round">
            <span class="round-label">Round</span>
            <span class="round-valor">${SessaoState.roundAtual}</span>
        </div>
        <div class="iniciativa-lista" id="lista-iniciativa">
            <p class="text-muted">Adicione participantes usando ⏱️ nos widgets</p>
        </div>
        <div class="iniciativa-controles">
            <button class="btn btn-sm" onclick="turnoAnterior()" title="Turno Anterior">◀</button>
            <button class="btn btn-sm btn-primary" onclick="proximoTurno()" title="Próximo Turno">▶ Próximo</button>
        </div>
    `;
}

function getConteudoLog() {
    return `
        <div class="log-lista" id="log-combate">
            ${SessaoState.logCombate.length === 0 
                ? '<p class="text-muted">Nenhuma ação registrada</p>'
                : SessaoState.logCombate.slice(-20).reverse().map(log => `
                    <div class="log-item log-${log.tipo}">
                        <span class="log-time">${log.timestamp}</span>
                        <span class="log-msg">${log.mensagem}</span>
                    </div>
                `).join('')
            }
        </div>
        <div class="log-acoes">
            <button class="btn btn-sm" onclick="limparLogCombate()">🗑️ Limpar</button>
        </div>
    `;
}

function limparLogCombate() {
    SessaoState.logCombate = [];
    atualizarWidgetLog();
}

// =========================================
// Seletores de Conteúdo
// =========================================

async function abrirSeletorPersonagem(widget) {
    document.getElementById('modal-widget-titulo').textContent = 'Selecionar Personagem';
    
    const personagens = await API.get('/api/personagens');
    const conteudo = document.getElementById('modal-widget-conteudo');
    
    if (!personagens || personagens.length === 0) {
        conteudo.innerHTML = `
            <p class="text-muted">Nenhum personagem cadastrado</p>
            <a href="/fichas/personagem/novo" class="btn btn-primary mt-2">+ Criar Personagem</a>
        `;
    } else {
        conteudo.innerHTML = `
            <div class="lista-selecao">
                ${personagens.map(p => `
                    <div class="item-selecao" onclick="carregarPersonagemWidget('${widget.id}', ${p.id})">
                        <div class="item-info">
                            <strong>${p.nome || 'Sem nome'}</strong>
                            <span class="item-detalhes">${p.raca || ''} ${p.classe || ''} Nv.${p.nivel || 1}</span>
                        </div>
                        <div class="item-stats">
                            <span class="stat-mini">HP ${p.hp_atual || 0}/${p.hp_maximo || 0}</span>
                            <span class="stat-mini">CA ${p.ca || 10}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    abrirModal('modal-widget');
}

async function carregarPersonagemWidget(widgetId, personagemId) {
    fecharModal('modal-widget');
    
    const widget = window.widgetManager.obter(widgetId);
    if (widget) {
        try {
            const p = await API.get(`/fichas/api/personagem/${personagemId}`);
            widget.setConteudo(gerarHTMLPersonagemWidget(p));
            widget.element.querySelector('.widget-title').textContent = `👤 ${p.nome}`;
            
            // Calcula modificador de destreza
            const attrs = p.atributos || {};
            const modDes = Math.floor(((attrs.destreza || 10) - 10) / 2);
            
            // Salva dados no widget para referência
            widget.dadosCriatura = {
                tipo: 'personagem',
                id: p.id,
                nome: p.nome,
                modDestreza: modDes
            };
        } catch (error) {
            console.error('Erro ao carregar personagem:', error);
            widget.setConteudo('<p class="text-muted">Erro ao carregar personagem</p>');
        }
    }
}

function gerarHTMLPersonagemWidget(p) {
    const attrs = p.atributos || {};
    const calcMod = (val) => Math.floor(((val || 10) - 10) / 2);
    const formatMod = (val) => { const mod = calcMod(val); return mod >= 0 ? `+${mod}` : mod; };
    
    const hpPct = p.hp_maximo ? Math.round((p.hp_atual / p.hp_maximo) * 100) : 100;
    const hpClass = hpPct <= 25 ? 'hp-critico' : hpPct <= 50 ? 'hp-baixo' : '';
    
    return `
        <div class="widget-personagem-conteudo">
            <div class="personagem-widget-header">
                <span class="personagem-info">${p.raca || ''} ${p.classe || ''} Nv.${p.nivel || 1}</span>
                <span class="personagem-jogador">${p.jogador || ''}</span>
            </div>
            <div class="personagem-widget-hp ${hpClass}">
                <div class="hp-barra-mini">
                    <div class="hp-fill" style="width: ${hpPct}%"></div>
                    <span class="hp-texto">HP ${p.hp_atual || 0}/${p.hp_maximo || 0}</span>
                </div>
            </div>
            <div class="personagem-widget-stats">
                <div class="stat-box"><span class="valor">CA${p.ca || 10}</span></div>
                <div class="stat-box"><span class="valor">Inic${formatMod(attrs.destreza)}</span></div>
                <div class="stat-box"><span class="valor">${p.velocidade || '9m'}</span></div>
            </div>
            <div class="personagem-widget-attrs">
                <span title="Força">FOR ${formatMod(attrs.forca)}</span>
                <span title="Destreza">DES ${formatMod(attrs.destreza)}</span>
                <span title="Constituição">CON ${formatMod(attrs.constituicao)}</span>
                <span title="Inteligência">INT ${formatMod(attrs.inteligencia)}</span>
                <span title="Sabedoria">SAB ${formatMod(attrs.sabedoria)}</span>
                <span title="Carisma">CAR ${formatMod(attrs.carisma)}</span>
            </div>
            <div class="personagem-widget-botoes">
                <button class="btn btn-sm btn-danger" onclick="abrirDanoRapido(event, ${p.id}, '${p.nome}', 'personagem')">⚔️ Dano</button>
                <button class="btn btn-sm btn-success" onclick="abrirCuraRapida(event, ${p.id}, '${p.nome}', 'personagem')">💚 Cura</button>
            </div>
            <div class="personagem-widget-notas">
                <textarea class="notas-rapidas" placeholder="Anotações rápidas..." data-personagem-id="${p.id}" onblur="salvarNotasRapidas(event)"></textarea>
            </div>
            ${p.hp_atual !== undefined && p.hp_atual <= 0 ? `
            <div class="testes-morte" data-criatura-tipo="personagem" data-criatura-id="${p.id}">
                <div class="teste-linha">
                    <span class="teste-label">Vida</span>
                    <span class="teste-checks" data-tipo="sucesso" data-id="${p.id}">
                        <span class="teste-check ${(p.sucesso_morte || 0) >= 1 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${p.id}, 'sucesso', 1)">☐</span>
                        <span class="teste-check ${(p.sucesso_morte || 0) >= 2 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${p.id}, 'sucesso', 2)">☐</span>
                        <span class="teste-check ${(p.sucesso_morte || 0) >= 3 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${p.id}, 'sucesso', 3)">☐</span>
                    </span>
                </div>
                <div class="teste-linha">
                    <span class="teste-label">Morte</span>
                    <span class="teste-checks" data-tipo="falha" data-id="${p.id}">
                        <span class="teste-check ${(p.falha_morte || 0) >= 1 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${p.id}, 'falha', 1)">☐</span>
                        <span class="teste-check ${(p.falha_morte || 0) >= 2 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${p.id}, 'falha', 2)">☐</span>
                        <span class="teste-check ${(p.falha_morte || 0) >= 3 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${p.id}, 'falha', 3)">☐</span>
                    </span>
                </div>
            </div>
            ` : ''}
            <div class="widget-efeitos" data-criatura-tipo="personagem" data-criatura-id="${p.id}">
                <div class="efeitos-lista"></div>
                <button class="btn btn-sm btn-outline" onclick="abrirModalEfeito(event, 'personagem', ${p.id})">+ Efeito</button>
            </div>
        </div>
    `;
}

async function salvarNotasRapidas(event) {
    const textarea = event.target;
    const id = textarea.dataset.personagemId || textarea.dataset.monstroId;
    const tipo = textarea.dataset.personagemId ? 'personagem' : 'monstro';
    // Opcional: salvar no servidor
    // Por enquanto apenas mantém na memória do widget
}

async function marcarTesteMorte(event, id, tipo, valor) {
    event.stopPropagation();
    
    try {
        const campo = tipo === 'sucesso' ? 'sucesso_morte' : 'falha_morte';
        const resultado = await API.patch(`/fichas/api/personagem/${id}`, { [campo]: valor });
        
        if (resultado && !resultado.erro) {
            // Atualiza visualmente os checkboxes
            const container = event.target.closest('.teste-checks');
            const checks = container.querySelectorAll('.teste-check');
            checks.forEach((check, i) => {
                check.classList.toggle('marcado', i < valor);
            });
            
            // Log
            const tipoTexto = tipo === 'sucesso' ? '✓ Sucesso' : '✗ Falha';
            adicionarLogCombate(`<strong>${resultado.nome}</strong> teste de morte: ${tipoTexto}`, tipo === 'sucesso' ? 'cura' : 'dano');
        }
    } catch (error) {
        console.error('Erro ao marcar teste de morte:', error);
    }
}

// =========================================
// Sistema de Efeitos/Condições
// =========================================

function abrirModalEfeito(event, tipo, id) {
    event.stopPropagation();
    
    // Cria lista de condições disponíveis
    const opcoesCondicoes = Object.entries(CONDICOES_DND).map(([key, cond]) => 
        `<option value="${key}">${cond.nome}</option>`
    ).join('');
    
    const modalHTML = `
        <div id="modal-efeito" class="modal ativo">
            <div class="modal-content modal-sm">
                <h3>Adicionar Efeito</h3>
                <div class="form-group">
                    <label>Condição</label>
                    <select id="efeito-condicao">${opcoesCondicoes}</select>
                </div>
                <div class="form-group">
                    <label>Turnos (0 = permanente)</label>
                    <input type="number" id="efeito-turnos" value="1" min="0">
                </div>
                <div class="modal-buttons">
                    <button class="btn btn-primary" onclick="adicionarEfeito('${tipo}', ${id})">Adicionar</button>
                    <button class="btn" onclick="fecharModal('modal-efeito')">Cancelar</button>
                </div>
            </div>
        </div>
    `;
    
    // Remove modal existente se houver
    const existente = document.getElementById('modal-efeito');
    if (existente) existente.remove();
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function adicionarEfeito(tipo, id) {
    const condicaoKey = document.getElementById('efeito-condicao').value;
    const turnos = parseInt(document.getElementById('efeito-turnos').value) || 0;
    
    const condicao = CONDICOES_DND[condicaoKey];
    if (!condicao) return;
    
    // Encontra o container de efeitos do widget
    const widgetEfeitos = document.querySelector(`.widget-efeitos[data-criatura-tipo="${tipo}"][data-criatura-id="${id}"]`);
    if (!widgetEfeitos) {
        fecharModal('modal-efeito');
        return;
    }
    
    const listaEfeitos = widgetEfeitos.querySelector('.efeitos-lista');
    const efeito = document.createElement('div');
    efeito.className = 'efeito-item';
    efeito.dataset.condicao = condicaoKey;
    efeito.dataset.turnos = turnos;
    efeito.innerHTML = `
        <span class="efeito-nome" title="${condicao.descricao}">${condicao.nome}</span>
        ${turnos > 0 ? `<span class="efeito-turnos">${turnos}</span>` : '<span class="efeito-turnos">∞</span>'}
        <button class="btn-mini btn-remover" onclick="removerEfeito(this)">✕</button>
    `;
    
    listaEfeitos.appendChild(efeito);
    fecharModal('modal-efeito');
    
    // Log
    adicionarLogCombate(`Efeito <strong>${condicao.nome}</strong> aplicado`, 'info');
}

function removerEfeito(btn) {
    const efeito = btn.closest('.efeito-item');
    const nome = efeito.querySelector('.efeito-nome').textContent;
    efeito.remove();
    adicionarLogCombate(`Efeito <strong>${nome}</strong> removido`, 'info');
}

function atualizarContadoresEfeitos() {
    // Atualiza todos os contadores de efeitos em todos os widgets
    document.querySelectorAll('.efeito-item').forEach(efeito => {
        const turnosSpan = efeito.querySelector('.efeito-turnos');
        let turnos = parseInt(efeito.dataset.turnos) || 0;
        
        if (turnos > 0) {
            turnos--;
            efeito.dataset.turnos = turnos;
            
            if (turnos <= 0) {
                // Efeito expirou
                const nome = efeito.querySelector('.efeito-nome').textContent;
                adicionarLogCombate(`Efeito <strong>${nome}</strong> expirou`, 'cura');
                efeito.remove();
            } else {
                turnosSpan.textContent = turnos;
            }
        }
    });
}

function abrirDanoRapido(event, id, nome, tipo) {
    event.stopPropagation();
    const botao = event.currentTarget;
    
    criarInputFlutuante(botao, 'dano', async (valor) => {
        try {
            const endpoint = tipo === 'personagem' 
                ? `/api/personagens/${id}/dano`
                : `/api/monstros/instancias/${id}/dano`;
            
            const resultado = await API.post(endpoint, { dano: valor });
            
            if (resultado && !resultado.erro) {
                // Log de combate
                adicionarLogCombate(`<strong>${nome}</strong> -${valor} HP`, 'dano');
                
                // Atualiza o widget
                atualizarWidgetCriatura(tipo, id, resultado);
            }
        } catch (error) {
            console.error('Erro ao aplicar dano:', error);
        }
    });
}

function abrirCuraRapida(event, id, nome, tipo) {
    event.stopPropagation();
    const botao = event.currentTarget;
    
    criarInputFlutuante(botao, 'cura', async (valor) => {
        try {
            const endpoint = tipo === 'personagem' 
                ? `/api/personagens/${id}/curar`
                : `/api/monstros/instancias/${id}/curar`;
            
            const resultado = await API.post(endpoint, { quantidade: valor });
            
            if (resultado && !resultado.erro) {
                // Log de combate
                adicionarLogCombate(`<strong>${nome}</strong> +${valor} HP`, 'cura');
                
                // Atualiza o widget
                atualizarWidgetCriatura(tipo, id, resultado);
            }
        } catch (error) {
            console.error('Erro ao aplicar cura:', error);
        }
    });
}

function atualizarWidgetCriatura(tipo, id, dadosAtualizados) {
    // Encontra todos os widgets que mostram essa criatura
    const widgets = document.querySelectorAll('.widget');
    
    widgets.forEach(widget => {
        const conteudo = widget.querySelector('.widget-personagem-conteudo, .widget-monstro-conteudo');
        if (!conteudo) return;
        
        // Verifica se o botão de dano tem o ID correto
        const btnDano = conteudo.querySelector('.btn-danger');
        if (!btnDano) return;
        
        const onclickAttr = btnDano.getAttribute('onclick') || '';
        if (onclickAttr.includes(`${id},`) || onclickAttr.includes(`${id})`)) {
            // Atualiza a barra de HP
            const hpBarra = conteudo.querySelector('.hp-barra-mini');
            const hpTexto = conteudo.querySelector('.hp-texto');
            const hpContainer = conteudo.querySelector('.personagem-widget-hp');
            
            if (hpBarra && hpTexto && dadosAtualizados.hp_atual !== undefined) {
                const hpAtual = dadosAtualizados.hp_atual;
                const hpMax = dadosAtualizados.hp_maximo;
                const hpPct = hpMax ? Math.round((hpAtual / hpMax) * 100) : 100;
                
                const hpFill = hpBarra.querySelector('.hp-fill');
                if (hpFill) {
                    hpFill.style.width = `${Math.max(0, Math.min(100, hpPct))}%`;
                }
                hpTexto.textContent = `HP ${hpAtual}/${hpMax}`;
                
                // Atualiza classes de estado
                if (hpContainer) {
                    hpContainer.classList.remove('hp-critico', 'hp-baixo');
                    if (hpPct <= 25) {
                        hpContainer.classList.add('hp-critico');
                    } else if (hpPct <= 50) {
                        hpContainer.classList.add('hp-baixo');
                    }
                }
                
                // Mostra/esconde testes de morte para personagens (HP = 0)
                if (tipo === 'personagem') {
                    let testesMorte = conteudo.querySelector('.testes-morte');
                    const widgetEfeitos = conteudo.querySelector('.widget-efeitos');
                    
                    if (hpAtual <= 0) {
                        // Adiciona testes de morte se não existir
                        if (!testesMorte) {
                            const sucessoMorte = dadosAtualizados.sucesso_morte || 0;
                            const falhaMorte = dadosAtualizados.falha_morte || 0;
                            
                            const testesMorteHTML = `
                                <div class="testes-morte" data-criatura-tipo="personagem" data-criatura-id="${id}">
                                    <div class="teste-linha">
                                        <span class="teste-label">Vida</span>
                                        <span class="teste-checks" data-tipo="sucesso" data-id="${id}">
                                            <span class="teste-check ${sucessoMorte >= 1 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${id}, 'sucesso', 1)">☐</span>
                                            <span class="teste-check ${sucessoMorte >= 2 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${id}, 'sucesso', 2)">☐</span>
                                            <span class="teste-check ${sucessoMorte >= 3 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${id}, 'sucesso', 3)">☐</span>
                                        </span>
                                    </div>
                                    <div class="teste-linha">
                                        <span class="teste-label">Morte</span>
                                        <span class="teste-checks" data-tipo="falha" data-id="${id}">
                                            <span class="teste-check ${falhaMorte >= 1 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${id}, 'falha', 1)">☐</span>
                                            <span class="teste-check ${falhaMorte >= 2 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${id}, 'falha', 2)">☐</span>
                                            <span class="teste-check ${falhaMorte >= 3 ? 'marcado' : ''}" onclick="marcarTesteMorte(event, ${id}, 'falha', 3)">☐</span>
                                        </span>
                                    </div>
                                </div>
                            `;
                            
                            // Insere antes do widget de efeitos
                            if (widgetEfeitos) {
                                widgetEfeitos.insertAdjacentHTML('beforebegin', testesMorteHTML);
                            }
                        }
                    } else {
                        // Remove testes de morte se HP > 0
                        if (testesMorte) {
                            testesMorte.remove();
                        }
                    }
                }
            }
        }
    });
}

async function criarInstanciaCombate(monstroId) {
    const nome = prompt('Nome da instância (ex: Goblin 1):');
    if (!nome) return;
    
    try {
        const resultado = await API.post('/fichas/api/monstro/instancia', {
            monstro_id: monstroId,
            nome: nome
        });
        
        if (resultado && resultado.id) {
            notificar(`${nome} adicionado ao combate!`, 'success');
        }
    } catch (error) {
        console.error('Erro ao criar instância:', error);
        notificar('Erro ao criar instância', 'danger');
    }
}

async function abrirSeletorMonstro(widget) {
    document.getElementById('modal-widget-titulo').textContent = 'Adicionar Monstro ao Combate';
    
    const monstros = await API.get('/api/monstros');
    const conteudo = document.getElementById('modal-widget-conteudo');
    
    if (!monstros || monstros.length === 0) {
        conteudo.innerHTML = `
            <p class="text-muted">Nenhum monstro cadastrado</p>
            <a href="/fichas/monstro/novo" class="btn btn-primary mt-2">+ Criar Monstro</a>
        `;
    } else {
        conteudo.innerHTML = `
            <div class="lista-selecao">
                ${monstros.map(m => `
                    <div class="item-selecao" onclick="adicionarMonstroAoCombate('${widget.id}', ${m.id}, '${m.nome}')">
                        <div class="item-info">
                            <strong>${m.nome}</strong>
                            <span class="item-detalhes">${m.tamanho || 'Médio'} ${m.tipo || 'Criatura'}</span>
                        </div>
                        <div class="item-stats">
                            <span class="stat-mini nd">ND ${formatarND(m.nd)}</span>
                            <span class="stat-mini">HP ${m.hp_medio || '?'}</span>
                            <span class="stat-mini">CA ${m.ca || 10}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    abrirModal('modal-widget');
}

async function adicionarMonstroAoCombate(widgetId, monstroId, nomeBase) {
    fecharModal('modal-widget');
    
    // Incrementa contador global de monstros por tipo
    if (!SessaoState.contadorMonstros[nomeBase]) {
        SessaoState.contadorMonstros[nomeBase] = 0;
    }
    SessaoState.contadorMonstros[nomeBase]++;
    const numero = SessaoState.contadorMonstros[nomeBase];
    const nome = `${nomeBase} ${numero}`;
    
    try {
        // Cria instância do monstro
        const resultado = await API.post('/api/monstros/instanciar', {
            monstro_id: monstroId,
            nome: nome
        });
        
        if (resultado && resultado.id) {
            // Calcula modificador de destreza
            const attrs = resultado.atributos || {};
            const modDes = Math.floor(((attrs.destreza || 10) - 10) / 2);
            
            // Carrega o widget com a instância
            const widget = window.widgetManager.obter(widgetId);
            if (widget) {
                widget.setConteudo(gerarHTMLInstanciaMonstroWidget(resultado, nomeBase));
                widget.element.querySelector('.widget-title').textContent = `👹 ${nome}`;
                
                // Salva dados extras no widget para referência
                widget.dadosCriatura = {
                    tipo: 'instancia',
                    id: resultado.id,
                    nome: nome,
                    nomeBase: nomeBase,
                    modDestreza: modDes
                };
            }
            
            // Log
            adicionarLogCombate(`<strong>${nome}</strong> entrou no combate`, 'info');
        }
    } catch (error) {
        console.error('Erro ao adicionar monstro:', error);
    }
}

function formatarND(nd) {
    if (nd === 0.125) return '1/8';
    if (nd === 0.25) return '1/4';
    if (nd === 0.5) return '1/2';
    return nd || 0;
}

async function carregarMonstroWidget(widgetId, monstroId) {
    fecharModal('modal-widget');
    
    // Carrega dados do monstro diretamente (não precisa criar instância para visualizar)
    const widget = window.widgetManager.obter(widgetId);
    if (widget) {
        try {
            const monstro = await API.get(`/fichas/api/monstro/${monstroId}`);
            widget.setConteudo(gerarHTMLMonstroWidget(monstro));
            widget.element.querySelector('.widget-title').textContent = `👹 ${monstro.nome}`;
        } catch (error) {
            console.error('Erro ao carregar monstro:', error);
            widget.setConteudo('<p class="text-muted">Erro ao carregar monstro</p>');
        }
    }
}

function gerarHTMLMonstroWidget(m) {
    const attrs = m.atributos || {};
    const calcMod = (val) => Math.floor(((val || 10) - 10) / 2);
    const formatMod = (val) => { const mod = calcMod(val); return mod >= 0 ? `+${mod}` : mod; };
    
    return `
        <div class="widget-monstro-conteudo" data-monstro-id="${m.id}">
            <div class="monstro-widget-header">
                <span class="monstro-tipo">${m.tamanho || 'Médio'} ${m.tipo || 'Criatura'}</span>
                <span class="monstro-nd">ND ${formatarND(m.nd)}</span>
            </div>
            <div class="monstro-widget-stats">
                <div class="stat-box"><span class="label">CA</span><span class="valor">${m.ca || 10}</span></div>
                <div class="stat-box"><span class="label">HP</span><span class="valor">${m.hp_medio || '?'}</span></div>
                <div class="stat-box"><span class="label">Vel</span><span class="valor">${m.velocidade?.terrestre || 9}m</span></div>
            </div>
            <div class="monstro-widget-attrs">
                <span title="Força">FOR ${formatMod(attrs.forca)}</span>
                <span title="Destreza">DES ${formatMod(attrs.destreza)}</span>
                <span title="Constituição">CON ${formatMod(attrs.constituicao)}</span>
                <span title="Inteligência">INT ${formatMod(attrs.inteligencia)}</span>
                <span title="Sabedoria">SAB ${formatMod(attrs.sabedoria)}</span>
                <span title="Carisma">CAR ${formatMod(attrs.carisma)}</span>
            </div>
            ${m.acoes && m.acoes.length > 0 ? `
                <div class="monstro-widget-acoes">
                    <strong>Ações:</strong>
                    ${m.acoes.map(a => `
                        <div class="acao-item-widget">
                            <span class="acao-nome">${a.nome}</span>
                            ${a.ataque ? `<span class="acao-ataque">${a.ataque}</span>` : ''}
                            ${a.dano ? `<span class="acao-dano">${a.dano}</span>` : ''}
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        </div>
    `;
}

function gerarHTMLInstanciaMonstroWidget(inst, nomeBase) {
    const attrs = inst.atributos || {};
    const calcMod = (val) => Math.floor(((val || 10) - 10) / 2);
    const formatMod = (val) => { const mod = calcMod(val); return mod >= 0 ? `+${mod}` : mod; };
    
    const hpPct = inst.hp_maximo ? Math.round((inst.hp_atual / inst.hp_maximo) * 100) : 100;
    const hpClass = hpPct <= 25 ? 'hp-critico' : hpPct <= 50 ? 'hp-baixo' : '';
    
    return `
        <div class="widget-monstro-conteudo widget-instancia" data-instancia-id="${inst.id}" data-nome-base="${nomeBase}">
            <div class="monstro-widget-header">
                <span class="monstro-tipo">${inst.tamanho || 'Médio'} ${inst.tipo || 'Criatura'}</span>
                <span class="monstro-nd">ND ${formatarND(inst.nd)}</span>
            </div>
            <div class="personagem-widget-hp ${hpClass}">
                <div class="hp-barra-mini">
                    <div class="hp-fill" style="width: ${hpPct}%"></div>
                    <span class="hp-texto">HP ${inst.hp_atual || 0}/${inst.hp_maximo || 0}</span>
                </div>
            </div>
            <div class="monstro-widget-stats">
                <div class="stat-box"><span class="valor">CA${inst.ca || 10}</span></div>
                <div class="stat-box"><span class="valor">${inst.velocidade?.terrestre || 9}m</span></div>
            </div>
            <div class="monstro-widget-attrs">
                <span title="Força">FOR ${formatMod(attrs.forca)}</span>
                <span title="Destreza">DES ${formatMod(attrs.destreza)}</span>
                <span title="Constituição">CON ${formatMod(attrs.constituicao)}</span>
                <span title="Inteligência">INT ${formatMod(attrs.inteligencia)}</span>
                <span title="Sabedoria">SAB ${formatMod(attrs.sabedoria)}</span>
                <span title="Carisma">CAR ${formatMod(attrs.carisma)}</span>
            </div>
            ${inst.acoes && inst.acoes.length > 0 ? `
                <div class="monstro-widget-acoes">
                    <strong>Ações:</strong>
                    ${inst.acoes.map(a => `
                        <div class="acao-item-widget">
                            <span class="acao-nome">${a.nome}</span>
                            ${a.ataque ? `<span class="acao-ataque">${a.ataque}</span>` : ''}
                            ${a.dano ? `<span class="acao-dano">${a.dano}</span>` : ''}
                        </div>
                    `).join('')}
                </div>
            ` : ''}
            <div class="monstro-widget-botoes">
                <button class="btn btn-sm btn-danger" onclick="abrirDanoRapido(event, ${inst.id}, '${inst.nome}', 'instancia')">⚔️ Dano</button>
                <button class="btn btn-sm btn-success" onclick="abrirCuraRapida(event, ${inst.id}, '${inst.nome}', 'instancia')">💚 Cura</button>
            </div>
            <div class="monstro-widget-notas">
                <textarea class="notas-rapidas" placeholder="Anotações rápidas..." data-monstro-id="${inst.id}" onblur="salvarNotasRapidas(event)"></textarea>
            </div>
            <div class="widget-efeitos" data-criatura-tipo="instancia" data-criatura-id="${inst.id}">
                <div class="efeitos-lista"></div>
                <button class="btn btn-sm btn-outline" onclick="abrirModalEfeito(event, 'instancia', ${inst.id})">+ Efeito</button>
            </div>
        </div>
    `;
}

async function criarInstanciaMonstro(widgetId, monstroId) {
    fecharModal('modal-widget');
    
    const resultado = await API.post('/fichas/api/monstro/instancia', {
        monstro_id: monstroId
    });
    
    if (resultado.sucesso) {
        const widget = window.widgetManager.obter(widgetId);
        if (widget) {
            await widget.carregarConteudo(`/fichas/widget/monstro/${resultado.instancia.instancia_id}`);
        }
    }
}

// =========================================
// Sistema de Combate
// =========================================

async function toggleCombate() {
    const btn = document.querySelector('.btn-combat');
    
    if (!SessaoState.combateAtivo) {
        await iniciarCombate();
    } else {
        await finalizarCombate();
    }
    
    // Atualiza o botão após as funções de combate atualizarem o estado
    btn.classList.toggle('active', SessaoState.combateAtivo);
    // Muda o ícone: 🛡️ fora de batalha, ⚔️ em batalha
    btn.textContent = SessaoState.combateAtivo ? '⚔️' : '🛡️';
}

async function iniciarCombate() {
    try {
        await API.post('/combate/iniciar', {});
    } catch (e) { /* ignora erro se rota não existir */ }
    
    // Reseta contador de rounds
    SessaoState.roundAtual = 1;
    SessaoState.combateAtivo = true;
    
    // Log de combate
    adicionarLogCombate('⚔️ <strong>Batalha iniciada!</strong>', 'info');
    adicionarLogCombate(`🔄 <strong>Round 1</strong>`, 'info');
    
    // Atualiza widget de iniciativa se existir
    atualizarWidgetIniciativa();
    
    // Atualiza indicador na navbar e salva estado
    atualizarIndicadorTurno();
    salvarEstadoSessao();
}

async function finalizarCombate() {
    try {
        await API.post('/combate/finalizar', {});
    } catch (e) { /* ignora erro se rota não existir */ }
    
    // Log de combate
    adicionarLogCombate('🛡️ <strong>Batalha encerrada!</strong>', 'info');
    
    // Limpa ordem de turnos e reseta rounds
    SessaoState.ordemTurnos = [];
    SessaoState.turnoAtual = 0;
    SessaoState.roundAtual = 0;
    SessaoState.combateAtivo = false;
    atualizarWidgetIniciativa();
    
    // Atualiza indicador na navbar e salva estado
    atualizarIndicadorTurno();
    salvarEstadoSessao();
}

// =========================================
// Sistema de Turnos
// =========================================

function adicionarAosTurnos(tipo, id, nome, iniciativa = null, modDestreza = 0) {
    // Verifica se já está na lista
    const jaExiste = SessaoState.ordemTurnos.find(p => p.tipo === tipo && p.id === id);
    if (jaExiste) {
        adicionarLogCombate(`<strong>${nome}</strong> já está nos turnos`, 'info');
        return;
    }
    
    // Se não passou iniciativa, rola 1d20 + mod destreza
    if (iniciativa === null) {
        const d20 = Math.floor(Math.random() * 20) + 1;
        iniciativa = d20 + modDestreza;
        const modTexto = modDestreza >= 0 ? `+${modDestreza}` : modDestreza;
        adicionarLogCombate(`<strong>${nome}</strong> rolou iniciativa: ${d20}${modTexto} = ${iniciativa}`, 'info');
    }
    
    SessaoState.ordemTurnos.push({
        tipo,
        id,
        nome,
        iniciativa,
        ativo: true
    });
    
    // Reordena por iniciativa (maior primeiro)
    SessaoState.ordemTurnos.sort((a, b) => b.iniciativa - a.iniciativa);
    
    atualizarWidgetIniciativa();
    
    // Abre widget de iniciativa se não existir
    abrirWidgetIniciativa();
}

function removerDosTurnos(tipo, id) {
    const index = SessaoState.ordemTurnos.findIndex(p => p.tipo === tipo && p.id === id);
    if (index !== -1) {
        const removido = SessaoState.ordemTurnos.splice(index, 1)[0];
        adicionarLogCombate(`<strong>${removido.nome}</strong> removido dos turnos`, 'info');
        
        // Ajusta turno atual se necessário
        if (SessaoState.turnoAtual >= SessaoState.ordemTurnos.length) {
            SessaoState.turnoAtual = 0;
        }
        
        atualizarWidgetIniciativa();
    }
}

function proximoTurno() {
    if (SessaoState.ordemTurnos.length === 0) return;
    
    const turnoAnteriorIdx = SessaoState.turnoAtual;
    SessaoState.turnoAtual = (SessaoState.turnoAtual + 1) % SessaoState.ordemTurnos.length;
    
    // Se voltou ao início, incrementa round
    if (SessaoState.turnoAtual === 0 && turnoAnteriorIdx !== 0) {
        SessaoState.roundAtual++;
        adicionarLogCombate(`🔄 <strong>Round ${SessaoState.roundAtual}</strong>`, 'info');
        // Atualiza contadores de efeitos de todos os widgets
        atualizarContadoresEfeitos();
    }
    
    const atual = SessaoState.ordemTurnos[SessaoState.turnoAtual];
    adicionarLogCombate(`➡️ Turno de <strong>${atual.nome}</strong>`, 'info');
    atualizarWidgetIniciativa();
    
    // Atualiza indicador na navbar e salva estado
    atualizarIndicadorTurno();
    salvarEstadoSessao();
}

function turnoAnterior() {
    if (SessaoState.ordemTurnos.length === 0) return;
    
    SessaoState.turnoAtual = SessaoState.turnoAtual === 0 
        ? SessaoState.ordemTurnos.length - 1 
        : SessaoState.turnoAtual - 1;
    
    atualizarWidgetIniciativa();
}

function atualizarWidgetIniciativa() {
    const lista = document.getElementById('lista-iniciativa');
    if (!lista) return;
    
    // Atualiza contador de rounds
    const contadorRound = document.getElementById('contador-round');
    if (contadorRound) {
        contadorRound.querySelector('.round-valor').textContent = SessaoState.roundAtual;
    }
    
    if (SessaoState.ordemTurnos.length === 0) {
        lista.innerHTML = '<p class="text-muted">Adicione participantes usando ⏱️ nos widgets</p>';
        return;
    }
    
    lista.innerHTML = SessaoState.ordemTurnos.map((p, i) => `
        <div class="iniciativa-item ${i === SessaoState.turnoAtual ? 'turno-atual' : ''}" data-tipo="${p.tipo}" data-id="${p.id}" data-index="${i}">
            <span class="iniciativa-ordem" contenteditable="true" onblur="editarIniciativa(event, ${i})" onkeydown="if(event.key==='Enter'){event.preventDefault();this.blur();}">${p.iniciativa}</span>
            <span class="iniciativa-nome">${p.tipo === 'personagem' ? '👤' : '👹'} ${p.nome}</span>
            <button class="btn-mini btn-remover" onclick="removerDosTurnos('${p.tipo}', ${p.id})" title="Remover">✕</button>
        </div>
    `).join('');
}

function editarIniciativa(event, index) {
    const novoValor = parseInt(event.target.textContent) || 0;
    if (SessaoState.ordemTurnos[index]) {
        SessaoState.ordemTurnos[index].iniciativa = novoValor;
        // Reordena por iniciativa
        SessaoState.ordemTurnos.sort((a, b) => b.iniciativa - a.iniciativa);
        atualizarWidgetIniciativa();
    }
}

// =========================================
// Ações de Combate
// =========================================

async function rolarAtaque(personagemId) {
    const expressao = prompt('Bônus de ataque (ex: 1d20+5):', '1d20+5');
    if (!expressao) return;
    
    const resultado = await rolarDados(expressao);
    alert(`Ataque: ${resultado.total}\nDados: [${resultado.dados.join(', ')}]${resultado.critico ? '\n🎯 CRÍTICO!' : ''}`);
}

async function aplicarDano(criatura, id) {
    const dano = prompt('Quantidade de dano:');
    if (!dano || isNaN(dano)) return;
    
    // TODO: Aplicar dano via API
    notificar(`${dano} de dano aplicado`, 'danger');
}

async function curar(criatura, id) {
    const cura = prompt('Quantidade de cura:');
    if (!cura || isNaN(cura)) return;
    
    // TODO: Aplicar cura via API
    notificar(`${cura} de cura aplicado`, 'success');
}

function abrirWidgetIniciativa() {
    // Verifica se já existe um widget de iniciativa aberto
    const widgets = window.widgetManager.widgets;
    const existente = Array.from(widgets.values()).find(w => 
        w.element.querySelector('.widget-title')?.textContent?.includes('Iniciativa')
    );
    
    if (!existente) {
        // Cria novo widget de iniciativa
        const widget = window.widgetManager.criar('iniciativa', {
            titulo: '⏱️ Iniciativa',
            x: window.innerWidth - 320,
            y: 130
        });
        widget.setConteudo(getConteudoIniciativa());
    }
    
    // Atualiza lista
    atualizarWidgetIniciativa();
}

// =========================================
// Inicialização
// =========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎲 Tela de Sessão carregada');
    
    // Carrega sessão atual
    carregarSessaoAtual();
    
    // Mostra dropdown de sessão na navbar
    const sessaoDropdown = document.getElementById('sessao-dropdown');
    if (sessaoDropdown) {
        sessaoDropdown.style.display = 'flex';
    }
    
    // Verifica status da API
    API.get('/api/status').then(status => {
        console.log('API:', status);
    }).catch(() => {});
});

// Salvar estado periodicamente
setInterval(() => {
    salvarEstadoSessao();
}, 10000); // A cada 10 segundos

// =========================================
// Sistema de Sessões Persistentes
// =========================================

let sessaoAtual = null;

async function carregarSessaoAtual() {
    try {
        const sessao = await API.get('/sessao/api/atual');
        sessaoAtual = sessao;
        
        // Atualiza label na navbar
        const label = document.getElementById('sessao-label');
        if (label) {
            label.textContent = `Sessão ${sessao.numero}`;
        }
        
        // Restaura estado
        if (sessao.estado) {
            restaurarEstado(sessao.estado);
        }
        
        // Restaura log
        if (sessao.log && sessao.log.length > 0) {
            SessaoState.logCombate = sessao.log.map(l => ({
                timestamp: new Date(l.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
                tipo: l.tipo,
                mensagem: l.mensagem
            }));
            atualizarWidgetLog();
        }
        
        // Carrega lista de sessões
        await carregarListaSessoes();
        
        console.log('📂 Sessão carregada:', sessao.numero);
    } catch (error) {
        console.error('Erro ao carregar sessão:', error);
    }
}

async function carregarListaSessoes() {
    try {
        const sessoes = await API.get('/sessao/api/lista');
        const container = document.getElementById('sessao-historico');
        if (!container) return;
        
        container.innerHTML = sessoes.reverse().map(s => `
            <button class="sessao-menu-item ${sessaoAtual && s.numero === sessaoAtual.numero ? 'sessao-ativa' : ''}" 
                    onclick="visualizarSessao('${s.data}')">
                ${s.titulo}
                <span class="sessao-item-data">${formatarData(s.data)}</span>
            </button>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar lista de sessões:', error);
    }
}

function formatarData(dataStr) {
    const [ano, mes, dia] = dataStr.split('-');
    return `${dia}/${mes}`;
}

async function criarNovaSessao() {
    if (!confirm('Criar nova sessão? O log de combate será limpo.')) return;
    
    try {
        const novaSessao = await API.post('/sessao/api/nova', {});
        sessaoAtual = novaSessao;
        
        // Limpa log local
        SessaoState.logCombate = [];
        SessaoState.ordemTurnos = [];
        SessaoState.turnoAtual = 0;
        SessaoState.roundAtual = 0;
        SessaoState.combateAtivo = false;
        
        // Atualiza UI
        const label = document.getElementById('sessao-label');
        if (label) {
            label.textContent = `Sessão ${novaSessao.numero}`;
        }
        
        atualizarWidgetIniciativa();
        atualizarWidgetLog();
        atualizarIndicadorTurno();
        
        await carregarListaSessoes();
        fecharSessaoMenu();
        
        notificar(`Nova sessão ${novaSessao.numero} criada!`, 'success');
    } catch (error) {
        console.error('Erro ao criar nova sessão:', error);
        notificar('Erro ao criar sessão', 'danger');
    }
}

async function visualizarSessao(dataSessao) {
    try {
        const sessao = await API.get(`/sessao/api/${dataSessao}`);
        
        // Se é a sessão atual, apenas fecha o menu
        if (sessaoAtual && sessao.numero === sessaoAtual.numero) {
            fecharSessaoMenu();
            return;
        }
        
        // Mostra log da sessão passada (somente leitura)
        alert(`Sessão ${sessao.numero} (${formatarData(sessao.data)})\n\nLog com ${sessao.log.length} entradas.\n\nEsta é uma visualização de consulta. Para editar, crie uma nova sessão.`);
        
        fecharSessaoMenu();
    } catch (error) {
        console.error('Erro ao visualizar sessão:', error);
    }
}

function toggleSessaoMenu() {
    const menu = document.getElementById('sessao-menu');
    if (menu) {
        menu.classList.toggle('ativo');
    }
}

function fecharSessaoMenu() {
    const menu = document.getElementById('sessao-menu');
    if (menu) {
        menu.classList.remove('ativo');
    }
}

// Fecha menu ao clicar fora
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('sessao-dropdown');
    if (dropdown && !dropdown.contains(e.target)) {
        fecharSessaoMenu();
    }
});

function restaurarEstado(estado) {
    // Restaura mapa
    if (estado.mapa_atual) {
        const container = document.getElementById('mapa-container');
        if (container) {
            container.innerHTML = '';
            container.style.backgroundImage = `url('file:///${estado.mapa_atual}')`;
        }
        SessaoState.mapaAtual = estado.mapa_atual;
    }
    
    // Restaura estado do combate
    SessaoState.combateAtivo = estado.combate_ativo || false;
    SessaoState.roundAtual = estado.round_atual || 0;
    SessaoState.turnoAtual = estado.turno_atual || 0;
    SessaoState.ordemTurnos = estado.ordem_turnos || [];
    
    // Atualiza botão de combate
    const btn = document.querySelector('.btn-combat');
    if (btn) {
        btn.classList.toggle('active', SessaoState.combateAtivo);
        btn.textContent = SessaoState.combateAtivo ? '⚔️' : '🛡️';
    }
    
    // Atualiza indicador de turno na navbar
    atualizarIndicadorTurno();
    
    // Atualiza widget de iniciativa se existir
    atualizarWidgetIniciativa();
    
    // Restaura widgets
    if (estado.widgets && estado.widgets.length > 0 && window.widgetManager) {
        estado.widgets.forEach(w => {
            try {
                window.widgetManager.restaurarWidget(w);
            } catch (e) {
                console.warn('Erro ao restaurar widget:', e);
            }
        });
    }
}

async function salvarEstadoSessao() {
    if (!sessaoAtual) return;
    
    const estado = {
        mapa_atual: SessaoState.mapaAtual,
        combate_ativo: SessaoState.combateAtivo,
        round_atual: SessaoState.roundAtual,
        turno_atual: SessaoState.turnoAtual,
        ordem_turnos: SessaoState.ordemTurnos,
        widgets: window.widgetManager ? window.widgetManager.salvarEstado() : []
    };
    
    try {
        await API.post('/sessao/api/estado', { estado });
    } catch (error) {
        console.warn('Erro ao salvar estado:', error);
    }
}

// =========================================
// Indicador de Turno na Navbar
// =========================================

function atualizarIndicadorTurno() {
    const indicator = document.getElementById('turno-indicator');
    const numero = document.getElementById('turno-numero');
    
    if (!indicator || !numero) return;
    
    if (SessaoState.combateAtivo && SessaoState.roundAtual > 0) {
        indicator.style.display = 'flex';
        numero.textContent = SessaoState.roundAtual;
    } else {
        indicator.style.display = 'none';
    }
}