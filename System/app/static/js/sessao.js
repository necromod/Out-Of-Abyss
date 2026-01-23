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
    turnoAtual: 0,    // Índice do turno atual na ordem
    contadorMonstros: {},  // Contador de monstros por tipo: { 'Goblin': 2, 'Orc': 1 }
    turnoContador: 0  // Contador de turnos da batalha (era roundAtual)
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
    },
    // Tipos de Dano como condições (para efeitos persistentes)
    'dano_acido': {
        nome: '🧪 Ácido',
        descricao: 'Recebendo dano ácido contínuo. Substância corrosiva causa queimaduras.'
    },
    'dano_contundente': {
        nome: '🔨 Contundente',
        descricao: 'Recebendo dano contundente. Impacto físico causando hematomas.'
    },
    'dano_cortante': {
        nome: '⚔️ Cortante',
        descricao: 'Recebendo dano cortante. Ferimentos abertos sangrando.'
    },
    'dano_eletrico': {
        nome: '⚡ Elétrico',
        descricao: 'Recebendo dano elétrico. Choque percorrendo o corpo.'
    },
    'dano_energetico': {
        nome: '💫 Energético',
        descricao: 'Recebendo dano energético (força). Energia mágica pura.'
    },
    'dano_gelido': {
        nome: '❄️ Gélido',
        descricao: 'Recebendo dano gélido. Congelamento e hipotermia.'
    },
    'dano_igneo': {
        nome: '🔥 Ígneo',
        descricao: 'Recebendo dano ígneo. Queimando, em chamas.'
    },
    'dano_necrotico': {
        nome: '💀 Necrótico',
        descricao: 'Recebendo dano necrótico. Energia vital sendo drenada.'
    },
    'dano_perfurante': {
        nome: '🗡️ Perfurante',
        descricao: 'Recebendo dano perfurante. Feridas profundas penetrantes.'
    },
    'dano_psiquico': {
        nome: '🧠 Psíquico',
        descricao: 'Recebendo dano psíquico. Mente sendo atacada.'
    },
    'dano_radiante': {
        nome: '✨ Radiante',
        descricao: 'Recebendo dano radiante. Luz divina queimando.'
    },
    'dano_trovejante': {
        nome: '🌩️ Trovejante',
        descricao: 'Recebendo dano trovejante. Ondas sonoras devastadoras.'
    },
    'dano_venenoso': {
        nome: '☠️ Venenoso',
        descricao: 'Recebendo dano venenoso. Toxina no sistema.'
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
        <div class="log-item log-${log.tipo}" data-time="${log.timestamp}">
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
        <div class="iniciativa-turno" id="contador-turno">
            <span class="turno-label">Turno</span>
            <span class="turno-valor">${SessaoState.turnoContador}</span>
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
    
    // Opção de criar ficha rápida sempre visível
    const fichaRapidaHTML = `
        <div class="item-selecao item-criar-novo" onclick="criarFichaRapidaPersonagem('${widget.id}')">
            <div class="item-info">
                <strong>➕ Criar Ficha Rápida</strong>
                <span class="item-detalhes">Novo personagem temporário</span>
            </div>
        </div>
    `;
    
    if (!personagens || personagens.length === 0) {
        conteudo.innerHTML = `
            <div class="lista-selecao">
                ${fichaRapidaHTML}
            </div>
            <p class="text-muted mt-2">Nenhum personagem cadastrado</p>
        `;
    } else {
        conteudo.innerHTML = `
            <div class="lista-selecao">
                ${fichaRapidaHTML}
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
    
    abrirModalTransparente('modal-widget');
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
    const modDes = calcMod(attrs.destreza);
    const modFor = calcMod(attrs.forca);
    const modSab = calcMod(attrs.sabedoria);
    
    // Percepção Passiva: usa valor do banco ou calcula
    const percepcaoPassiva = p.percepcao_passiva || (10 + modSab);
    
    const hpPct = p.hp_maximo ? Math.round((p.hp_atual / p.hp_maximo) * 100) : 100;
    const hpClass = hpPct <= 25 ? 'hp-critico' : hpPct <= 50 ? 'hp-baixo' : '';
    
    // Gera botões de ações/ataques (nova estrutura: nome, bonus, dados[], tipo)
    const armas = p.armas || [];
    const acoesHTML = armas.length > 0 
        ? armas.map(a => {
            // Suporta estrutura antiga (dano) e nova (dados + tipo)
            const dadosStr = a.dados && a.dados.length > 0 
                ? JSON.stringify(a.dados).replace(/"/g, "'") 
                : `['${a.dano || '1d4'}']`;
            const tipo = a.tipo || '';
            const titulo = a.dados ? a.dados.join(' + ') + (tipo ? ` ${tipo}` : '') : (a.dano || '1d4');
            return `<button class="btn btn-xs btn-acao" onclick="rolarAtaque(event, '${p.nome}', '${a.nome}', '${a.bonus || '+0'}', ${dadosStr}, '${tipo}')" title="${titulo}">${a.nome} ${a.bonus || ''}</button>`;
        }).join('')
        : `<button class="btn btn-xs btn-acao" onclick="rolarAtaque(event, '${p.nome}', 'Ataque Básico', '${formatMod(attrs.forca)}', ['1d4${modFor >= 0 ? '+' + modFor : modFor}'], '')" title="1d4${modFor >= 0 ? '+' + modFor : modFor}">Ataque Básico ${formatMod(attrs.forca)}</button>`;
    
    return `
        <div class="widget-personagem-conteudo" data-personagem-id="${p.id}" data-personagem-nome="${p.nome}" data-mod-destreza="${modDes}">
            <div class="personagem-widget-header">
                <span class="personagem-info">${p.raca || ''} ${p.classe || ''} Nv.${p.nivel || 1}</span>
                <button class="btn-add-combate" onclick="adicionarPersonagemAoCombate(${p.id}, '${p.nome}', ${modDes})" title="Adicionar ao combate">⚔️</button>
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
                <div class="stat-box" title="Percepção Passiva"><span class="valor">👁${percepcaoPassiva}</span></div>
            </div>
            <div class="personagem-widget-attrs">
                <span title="Força">FOR ${formatMod(attrs.forca)}</span>
                <span title="Destreza">DES ${formatMod(attrs.destreza)}</span>
                <span title="Constituição">CON ${formatMod(attrs.constituicao)}</span>
                <span title="Inteligência">INT ${formatMod(attrs.inteligencia)}</span>
                <span title="Sabedoria">SAB ${formatMod(attrs.sabedoria)}</span>
                <span title="Carisma">CAR ${formatMod(attrs.carisma)}</span>
            </div>
            <div class="personagem-widget-acoes">
                <div class="acoes-titulo">⚔️ Ações</div>
                <div class="acoes-lista">${acoesHTML}</div>
            </div>
            <div class="personagem-widget-botoes">
                <button class="btn btn-sm btn-danger" onclick="abrirDanoRapido(event, ${p.id}, '${p.nome}', 'personagem')">💔 Dano</button>
                <button class="btn btn-sm btn-success" onclick="abrirCuraRapida(event, ${p.id}, '${p.nome}', 'personagem')">💚 Cura</button>
            </div>
            ${p.hp_atual !== undefined && p.hp_atual <= 0 ? `
            <div class="testes-morte ${(p.falha_morte || 0) >= 3 ? 'personagem-morto' : ''}" data-criatura-tipo="personagem" data-criatura-id="${p.id}">
                ${(p.falha_morte || 0) >= 3 ? '<div class="morte-label">💀 MORTO</div>' : ''}
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
                <button class="btn btn-xs btn-outline" onclick="resetarTestesMorte(event, ${p.id})">Resetar</button>
            </div>
            ` : ''}
            <div class="widget-efeitos" data-criatura-tipo="personagem" data-criatura-id="${p.id}">
                <div class="efeitos-lista"></div>
                <button class="btn btn-sm btn-outline" onclick="abrirModalEfeito(event, 'personagem', ${p.id})">+ Efeito</button>
            </div>
            <div class="widget-observacoes">
                <div class="observacoes-titulo">📝 Observações</div>
                <textarea class="observacoes-textarea" 
                    data-tipo="personagem" 
                    data-id="${p.id}" 
                    placeholder="Anotações rápidas..."
                    onblur="salvarObservacoes(this)">${p.observacoes || ''}</textarea>
            </div>
        </div>
    `;
}

async function salvarObservacoes(textarea) {
    const tipo = textarea.dataset.tipo;
    const id = textarea.dataset.id;
    const valor = textarea.value.trim();
    
    try {
        if (tipo === 'personagem') {
            await API.patch(`/fichas/api/personagem/${id}`, { observacoes: valor });
        } else if (tipo === 'instancia') {
            await API.patch(`/fichas/api/monstro/instancia/${id}`, { observacoes: valor });
        }
    } catch (error) {
        console.error('Erro ao salvar observações:', error);
    }
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

/**
 * Reseta os testes de morte de um personagem
 */
async function resetarTestesMorte(event, id) {
    event.stopPropagation();
    
    try {
        const resultado = await API.patch(`/fichas/api/personagem/${id}`, { 
            sucesso_morte: 0, 
            falha_morte: 0 
        });
        
        if (resultado && !resultado.erro) {
            // Atualiza widget
            atualizarWidgetCriatura('personagem', id, resultado);
            adicionarLogCombate(`<strong>${resultado.nome}</strong> testes de morte resetados`, 'info');
        }
    } catch (error) {
        console.error('Erro ao resetar testes de morte:', error);
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
        <div id="modal-efeito" class="modal" style="display: flex;">
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
                <div class="form-group">
                    <label>Descrição (opcional)</label>
                    <textarea id="efeito-descricao" rows="2" placeholder="Ex: Magia Sleep do mago inimigo"></textarea>
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
    const descricao = document.getElementById('efeito-descricao').value.trim();
    
    const condicao = CONDICOES_DND[condicaoKey];
    if (!condicao) return;
    
    // Encontra o container de efeitos do widget
    const widgetEfeitos = document.querySelector(`.widget-efeitos[data-criatura-tipo="${tipo}"][data-criatura-id="${id}"]`);
    if (!widgetEfeitos) {
        fecharModal('modal-efeito');
        return;
    }
    
    // Texto de turnos com singular/plural
    const textoTurnos = turnos > 0 
        ? `${turnos} ${turnos === 1 ? 'turno' : 'turnos'}` 
        : '∞';
    
    // Descrição entre parênteses se existir
    const textoDescricao = descricao ? ` <span class="efeito-desc">(${descricao})</span>` : '';
    
    const listaEfeitos = widgetEfeitos.querySelector('.efeitos-lista');
    const efeito = document.createElement('div');
    efeito.className = 'efeito-item';
    efeito.dataset.condicao = condicaoKey;
    efeito.dataset.turnos = turnos;
    efeito.dataset.descricao = descricao;
    efeito.innerHTML = `
        <span class="efeito-nome" title="${condicao.descricao}">${condicao.nome}</span>
        <span class="efeito-turnos">${textoTurnos}</span>${textoDescricao}
        <button class="btn-mini btn-remover" onclick="removerEfeito(this)">✕</button>
    `;
    
    listaEfeitos.appendChild(efeito);
    fecharModal('modal-efeito');
    
    // Log com descrição se houver
    const logDesc = descricao ? ` (${descricao})` : '';
    adicionarLogCombate(`Efeito <strong>${condicao.nome}</strong>${logDesc} aplicado`, 'info');
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
                const descricao = efeito.dataset.descricao;
                const logDesc = descricao ? ` (${descricao})` : '';
                adicionarLogCombate(`Efeito <strong>${nome}</strong>${logDesc} expirou`, 'cura');
                efeito.remove();
            } else {
                // Atualiza texto com singular/plural
                turnosSpan.textContent = `${turnos} ${turnos === 1 ? 'turno' : 'turnos'}`;
            }
        }
    });
}

// =========================================
// Sistema de Ataques/Ações
// =========================================

/**
 * Rola um ataque com d20 + bônus e mostra resultado
 * @param {Event} event - Evento do clique
 * @param {string} nomeAtacante - Nome de quem ataca
 * @param {string} nomeAtaque - Nome da arma/ataque
 * @param {string} bonusAtaque - Bônus de acerto (ex: "+5" ou "5")
 * @param {string[]|string} dados - Array de dados de dano ou string única (compatibilidade)
 * @param {string} tipoDano - Tipo de dano (ex: "Cortante", "Ígneo")
 */
async function rolarAtaque(event, nomeAtacante, nomeAtaque, bonusAtaque, dados, tipoDano = '') {
    event.stopPropagation();
    
    // Limpa o bônus para garantir formato correto
    const bonusNum = parseInt(String(bonusAtaque).replace('+', '').trim()) || 0;
    const bonusStr = bonusNum >= 0 ? `+${bonusNum}` : `${bonusNum}`;
    
    // Normaliza dados para array (compatibilidade com estrutura antiga)
    const dadosArray = Array.isArray(dados) ? dados : [dados];
    
    try {
        // Rola o d20 para acerto
        const resultadoAtaque = await API.post('/api/dados/rolar', { expressao: `1d20${bonusStr}` });
        
        if (resultadoAtaque && !resultadoAtaque.erro) {
            const d20 = resultadoAtaque.dados ? resultadoAtaque.dados[0] : resultadoAtaque.total - bonusNum;
            const totalAtaque = resultadoAtaque.total;
            const isCrit = d20 === 20;
            const isFumble = d20 === 1;
            
            // Ícone de status
            const statusIcon = isCrit ? '🎯' : (isFumble ? '💀' : '');
            const statusClass = isCrit ? 'crit' : (isFumble ? 'fumble' : '');
            
            // Linha 1: Nome usa Ataque TOTAL [ícone] (detalhes)
            let logMsg = `<strong>${nomeAtacante}</strong> usa <em>${nomeAtaque}</em> `;
            logMsg += `<span class="ataque-total ${statusClass}">${totalAtaque}</span>`;
            if (statusIcon) logMsg += ` ${statusIcon}`;
            logMsg += ` <span class="ataque-detalhes">(${d20}${bonusStr})</span>`;
            
            // Se acertou (não fumble), rola dano
            if (!isFumble) {
                let totalDano = 0;
                let expressoesDano = [];
                
                // Rola cada dado de dano separadamente
                for (const expr of dadosArray) {
                    // Prepara expressão de dano (dobra dados em crítico)
                    let expressaoDano = expr;
                    let expressaoOriginal = expr;
                    if (isCrit) {
                        // Dobra os dados (ex: 1d8+3 -> 2d8+3)
                        expressaoDano = expressaoDano.replace(/(\d+)d(\d+)/g, (match, qtd, faces) => {
                            return `${parseInt(qtd) * 2}d${faces}`;
                        });
                    }
                    
                    const resultadoDano = await API.post('/api/dados/rolar', { expressao: expressaoDano });
                    
                    if (resultadoDano && !resultadoDano.erro) {
                        totalDano += resultadoDano.total;
                        expressoesDano.push(expressaoDano);
                    }
                }
                
                // Linha 2: X dano tipo (expressão)
                const tipoLower = tipoDano ? tipoDano.toLowerCase() : '';
                const tipoStr = tipoLower ? ` <span class="tipo-dano" data-tipo="${tipoDano}">${tipoLower}</span>` : '';
                const expressaoStr = expressoesDano.join(' + ');
                logMsg += `<br><span class="dano-linha"><span class="dano">${totalDano}</span> dano${tipoStr} <span class="dano-expressao">(${expressaoStr})</span></span>`;
            }
            
            adicionarLogCombate(logMsg, isCrit ? 'crit' : (isFumble ? 'fumble' : 'ataque'));
        }
    } catch (error) {
        console.error('Erro ao rolar ataque:', error);
        adicionarLogCombate(`Erro ao rolar ataque de ${nomeAtacante}`, 'erro');
    }
}

/**
 * Rola dano direto (sem ataque)
 */
async function rolarDano(event, nomeAtacante, nomeAtaque, expressaoDano) {
    event.stopPropagation();
    
    try {
        const resultado = await API.post('/api/dados/rolar', { expressao: expressaoDano });
        
        if (resultado && !resultado.erro) {
            const logMsg = `<strong>${nomeAtacante}</strong> usa <em>${nomeAtaque}</em>: <span class="dano">${resultado.total} dano</span> (${expressaoDano})`;
            adicionarLogCombate(logMsg, 'ataque');
        }
    } catch (error) {
        console.error('Erro ao rolar dano:', error);
    }
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
                        const sucessoMorte = dadosAtualizados.sucesso_morte || 0;
                        const falhaMorte = dadosAtualizados.falha_morte || 0;
                        const estaMorto = falhaMorte >= 3;
                        
                        // Atualiza ou cria testes de morte
                        const testesMorteHTML = `
                            <div class="testes-morte ${estaMorto ? 'personagem-morto' : ''}" data-criatura-tipo="personagem" data-criatura-id="${id}">
                                ${estaMorto ? '<div class="morte-label">💀 MORTO</div>' : ''}
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
                                <button class="btn btn-xs btn-outline" onclick="resetarTestesMorte(event, ${id})">Resetar</button>
                            </div>
                        `;
                        
                        if (testesMorte) {
                            testesMorte.outerHTML = testesMorteHTML;
                        } else if (widgetEfeitos) {
                            widgetEfeitos.insertAdjacentHTML('beforebegin', testesMorteHTML);
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
    
    // Opção de criar ficha rápida sempre visível
    const fichaRapidaHTML = `
        <div class="item-selecao item-criar-novo" onclick="criarFichaRapidaMonstro('${widget.id}')">
            <div class="item-info">
                <strong>➕ Criar Monstro Rápido</strong>
                <span class="item-detalhes">Novo monstro temporário</span>
            </div>
        </div>
    `;
    
    if (!monstros || monstros.length === 0) {
        conteudo.innerHTML = `
            <div class="lista-selecao">
                ${fichaRapidaHTML}
            </div>
            <p class="text-muted mt-2">Nenhum monstro cadastrado</p>
        `;
    } else {
        conteudo.innerHTML = `
            <div class="lista-selecao">
                ${fichaRapidaHTML}
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
    
    abrirModalTransparente('modal-widget');
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
            
            // Adiciona automaticamente à lista de turnos
            adicionarAosTurnos('instancia', resultado.id, nome, null, modDes);
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
    const modDes = calcMod(attrs.destreza);
    const modFor = calcMod(attrs.forca);
    const modSab = calcMod(attrs.sabedoria);
    
    // Percepção Passiva: usa valor do monstro ou calcula
    const percepcaoPassiva = inst.percepcao_passiva || (10 + modSab);
    
    const hpPct = inst.hp_maximo ? Math.round((inst.hp_atual / inst.hp_maximo) * 100) : 100;
    const hpClass = hpPct <= 25 ? 'hp-critico' : hpPct <= 50 ? 'hp-baixo' : '';
    
    // Gera botões de ações (suporta estrutura nova e antiga)
    const acoes = inst.acoes || [];
    const ataqueBasico = { nome: 'Ataque Básico', ataque: formatMod(attrs.forca), dano: `1d4${modFor >= 0 ? '+' + modFor : modFor}` };
    const acoesHTML = acoes.length > 0 
        ? acoes.map(a => {
            const atk = a.ataque || formatMod(attrs.forca);
            // Suporta estrutura nova (dados[], tipo) ou antiga (dano)
            const dadosStr = a.dados && a.dados.length > 0 
                ? JSON.stringify(a.dados).replace(/"/g, "'") 
                : `['${a.dano || '1d4'}']`;
            const tipo = a.tipo || '';
            const titulo = a.dados ? a.dados.join(' + ') + (tipo ? ` ${tipo}` : '') : (a.dano || '1d4');
            return `<button class="btn btn-xs btn-acao" onclick="rolarAtaque(event, '${inst.nome}', '${a.nome}', '${atk}', ${dadosStr}, '${tipo}')" title="${titulo}">${a.nome} ${atk}</button>`;
        }).join('')
        : `<button class="btn btn-xs btn-acao" onclick="rolarAtaque(event, '${inst.nome}', 'Ataque Básico', '${formatMod(attrs.forca)}', ['1d4${modFor >= 0 ? '+' + modFor : modFor}'], '')" title="1d4${modFor >= 0 ? '+' + modFor : modFor}">Ataque Básico ${formatMod(attrs.forca)}</button>`;
    
    return `
        <div class="widget-monstro-conteudo widget-instancia" data-instancia-id="${inst.id}" data-nome-base="${nomeBase}" data-mod-destreza="${modDes}">
            <div class="monstro-widget-header">
                <span class="monstro-tipo">${inst.tamanho || 'Médio'} ${inst.tipo || 'Criatura'}</span>
                <button class="btn-add-combate" onclick="adicionarInstanciaAoCombate(${inst.id}, '${inst.nome}', ${modDes})" title="Adicionar ao combate">⚔️</button>
            </div>
            <div class="personagem-widget-hp ${hpClass}">
                <div class="hp-barra-mini">
                    <div class="hp-fill" style="width: ${hpPct}%"></div>
                    <span class="hp-texto">HP ${inst.hp_atual || 0}/${inst.hp_maximo || 0}</span>
                </div>
            </div>
            <div class="monstro-widget-stats">
                <div class="stat-box"><span class="valor">CA${inst.ca || 10}</span></div>
                <div class="stat-box"><span class="valor">ND ${formatarND(inst.nd)}</span></div>
                <div class="stat-box"><span class="valor">${inst.velocidade?.terrestre || inst.velocidade?.normal || 9}m</span></div>
                <div class="stat-box" title="Percepção Passiva"><span class="valor">👁${percepcaoPassiva}</span></div>
            </div>
            <div class="monstro-widget-attrs">
                <span title="Força">FOR ${formatMod(attrs.forca)}</span>
                <span title="Destreza">DES ${formatMod(attrs.destreza)}</span>
                <span title="Constituição">CON ${formatMod(attrs.constituicao)}</span>
                <span title="Inteligência">INT ${formatMod(attrs.inteligencia)}</span>
                <span title="Sabedoria">SAB ${formatMod(attrs.sabedoria)}</span>
                <span title="Carisma">CAR ${formatMod(attrs.carisma)}</span>
            </div>
            <div class="monstro-widget-acoes">
                <div class="acoes-titulo">⚔️ Ações</div>
                <div class="acoes-lista">${acoesHTML}</div>
            </div>
            <div class="monstro-widget-botoes">
                <button class="btn btn-sm btn-danger" onclick="abrirDanoRapido(event, ${inst.id}, '${inst.nome}', 'instancia')">💔 Dano</button>
                <button class="btn btn-sm btn-success" onclick="abrirCuraRapida(event, ${inst.id}, '${inst.nome}', 'instancia')">💚 Cura</button>
            </div>
            <div class="widget-efeitos" data-criatura-tipo="instancia" data-criatura-id="${inst.id}">
                <div class="efeitos-lista"></div>
                <button class="btn btn-sm btn-outline" onclick="abrirModalEfeito(event, 'instancia', ${inst.id})">+ Efeito</button>
            </div>
            <div class="widget-observacoes">
                <div class="observacoes-titulo">📝 Observações</div>
                <textarea class="observacoes-textarea" 
                    data-tipo="instancia" 
                    data-id="${inst.id}" 
                    placeholder="Anotações rápidas..."
                    onblur="salvarObservacoes(this)">${inst.observacoes || ''}</textarea>
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
// Fichas Rápidas (Criação inline)
// =========================================

/**
 * Exibe formulário de ficha rápida para personagem no widget
 */
function criarFichaRapidaPersonagem(widgetId) {
    fecharModal('modal-widget');
    
    const widget = window.widgetManager.obter(widgetId);
    if (!widget) return;
    
    widget.element.querySelector('.widget-title').textContent = '⚔️ Novo Personagem';
    
    widget.setConteudo(`
        <div class="ficha-rapida-form">
            <div class="form-grupo">
                <input type="text" id="fr-nome-${widgetId}" class="form-control" placeholder="Nome do Personagem" autofocus>
            </div>
            <div class="form-linha">
                <div class="form-grupo">
                    <label>HP Máximo</label>
                    <input type="number" id="fr-hp-${widgetId}" class="form-control" value="10" min="1">
                </div>
                <div class="form-grupo">
                    <label>CA</label>
                    <input type="number" id="fr-ca-${widgetId}" class="form-control" value="10" min="1">
                </div>
                <div class="form-grupo">
                    <label>Nível</label>
                    <input type="number" id="fr-nivel-${widgetId}" class="form-control" value="1" min="1" max="20">
                </div>
            </div>
            <div class="form-linha">
                <div class="form-grupo">
                    <label>Mod. Iniciativa</label>
                    <input type="number" id="fr-init-${widgetId}" class="form-control" value="0">
                </div>
                <div class="form-grupo">
                    <label>Mod. Destreza</label>
                    <input type="number" id="fr-dex-${widgetId}" class="form-control" value="0">
                </div>
            </div>
            <div class="form-acoes">
                <button class="btn btn-success" onclick="salvarFichaRapidaPersonagem('${widgetId}')">✓ Criar</button>
                <button class="btn btn-outline" onclick="widgetManager.remover('${widgetId}')">✕ Cancelar</button>
            </div>
        </div>
    `);
    
    // Foca no campo nome
    setTimeout(() => {
        const input = document.getElementById(`fr-nome-${widgetId}`);
        if (input) input.focus();
    }, 100);
}

/**
 * Salva a ficha rápida de personagem e exibe no widget
 */
function salvarFichaRapidaPersonagem(widgetId) {
    const widget = window.widgetManager.obter(widgetId);
    if (!widget) return;
    
    const nome = document.getElementById(`fr-nome-${widgetId}`)?.value || 'Personagem';
    const hpMax = parseInt(document.getElementById(`fr-hp-${widgetId}`)?.value) || 10;
    const ca = parseInt(document.getElementById(`fr-ca-${widgetId}`)?.value) || 10;
    const nivel = parseInt(document.getElementById(`fr-nivel-${widgetId}`)?.value) || 1;
    const modInit = parseInt(document.getElementById(`fr-init-${widgetId}`)?.value) || 0;
    const modDex = parseInt(document.getElementById(`fr-dex-${widgetId}`)?.value) || 0;
    
    // Cria objeto de personagem temporário (não salva no banco)
    const personagemTemp = {
        id: `temp_pc_${Date.now()}`,
        nome: nome,
        hp_atual: hpMax,
        hp_maximo: hpMax,
        ca: ca,
        nivel: nivel,
        bonus_iniciativa: modInit,
        mod_destreza: modDex,
        temporario: true
    };
    
    // Armazena no widget
    widget.dadosCriatura = personagemTemp;
    widget.element.querySelector('.widget-title').textContent = `⚔️ ${nome}`;
    
    // Gera HTML da ficha
    widget.setConteudo(gerarHTMLFichaRapidaPersonagem(personagemTemp, widgetId));
}

/**
 * Gera HTML de ficha rápida de personagem
 */
function gerarHTMLFichaRapidaPersonagem(p, widgetId) {
    const hpPct = p.hp_maximo ? Math.round((p.hp_atual / p.hp_maximo) * 100) : 100;
    const hpClass = hpPct <= 25 ? 'hp-critico' : hpPct <= 50 ? 'hp-baixo' : '';
    
    return `
        <div class="widget-personagem-conteudo ficha-temporaria" data-temp-id="${p.id}">
            <div class="personagem-widget-header">
                <span class="personagem-classe">Personagem Temporário</span>
                <span class="personagem-nivel">Nv.${p.nivel}</span>
            </div>
            <div class="personagem-widget-hp ${hpClass}">
                <div class="hp-barra-mini">
                    <div class="hp-fill" style="width: ${hpPct}%"></div>
                    <span class="hp-texto">HP ${p.hp_atual}/${p.hp_maximo}</span>
                </div>
            </div>
            <div class="personagem-widget-stats">
                <div class="stat-box"><span class="label">CA</span><span class="valor">${p.ca}</span></div>
                <div class="stat-box"><span class="label">Init</span><span class="valor">${p.bonus_iniciativa >= 0 ? '+' : ''}${p.bonus_iniciativa}</span></div>
            </div>
            <div class="personagem-widget-botoes">
                <button class="btn btn-sm btn-danger" onclick="aplicarDanoFichaRapida('${widgetId}')">⚔️ Dano</button>
                <button class="btn btn-sm btn-success" onclick="aplicarCuraFichaRapida('${widgetId}')">💚 Cura</button>
                <button class="btn btn-sm btn-primary" onclick="adicionarFichaRapidaCombate('${widgetId}', 'personagem')">⚔️ Combate</button>
            </div>
        </div>
    `;
}

/**
 * Exibe formulário de ficha rápida para monstro no widget
 */
function criarFichaRapidaMonstro(widgetId) {
    fecharModal('modal-widget');
    
    const widget = window.widgetManager.obter(widgetId);
    if (!widget) return;
    
    widget.element.querySelector('.widget-title').textContent = '👹 Novo Monstro';
    
    widget.setConteudo(`
        <div class="ficha-rapida-form">
            <div class="form-grupo">
                <input type="text" id="fr-nome-${widgetId}" class="form-control" placeholder="Nome do Monstro" autofocus>
            </div>
            <div class="form-linha">
                <div class="form-grupo">
                    <label>HP</label>
                    <input type="number" id="fr-hp-${widgetId}" class="form-control" value="10" min="1">
                </div>
                <div class="form-grupo">
                    <label>CA</label>
                    <input type="number" id="fr-ca-${widgetId}" class="form-control" value="10" min="1">
                </div>
                <div class="form-grupo">
                    <label>ND</label>
                    <input type="text" id="fr-nd-${widgetId}" class="form-control" value="1" placeholder="Ex: 1/4, 1, 5">
                </div>
            </div>
            <div class="form-linha">
                <div class="form-grupo">
                    <label>Mod. Destreza</label>
                    <input type="number" id="fr-dex-${widgetId}" class="form-control" value="0">
                </div>
                <div class="form-grupo">
                    <label>Ataque</label>
                    <input type="text" id="fr-ataque-${widgetId}" class="form-control" value="+3" placeholder="+3">
                </div>
                <div class="form-grupo">
                    <label>Dano</label>
                    <input type="text" id="fr-dano-${widgetId}" class="form-control" value="1d6+1" placeholder="1d6+1">
                </div>
            </div>
            <div class="form-acoes">
                <button class="btn btn-success" onclick="salvarFichaRapidaMonstro('${widgetId}')">✓ Criar</button>
                <button class="btn btn-outline" onclick="widgetManager.remover('${widgetId}')">✕ Cancelar</button>
            </div>
        </div>
    `);
    
    // Foca no campo nome
    setTimeout(() => {
        const input = document.getElementById(`fr-nome-${widgetId}`);
        if (input) input.focus();
    }, 100);
}

/**
 * Salva a ficha rápida de monstro e exibe no widget
 */
function salvarFichaRapidaMonstro(widgetId) {
    const widget = window.widgetManager.obter(widgetId);
    if (!widget) return;
    
    const nome = document.getElementById(`fr-nome-${widgetId}`)?.value || 'Monstro';
    const hp = parseInt(document.getElementById(`fr-hp-${widgetId}`)?.value) || 10;
    const ca = parseInt(document.getElementById(`fr-ca-${widgetId}`)?.value) || 10;
    const ndStr = document.getElementById(`fr-nd-${widgetId}`)?.value || '1';
    const modDex = parseInt(document.getElementById(`fr-dex-${widgetId}`)?.value) || 0;
    const ataque = document.getElementById(`fr-ataque-${widgetId}`)?.value || '+3';
    const dano = document.getElementById(`fr-dano-${widgetId}`)?.value || '1d6+1';
    
    // Converte ND para número
    let nd = 1;
    if (ndStr === '1/8') nd = 0.125;
    else if (ndStr === '1/4') nd = 0.25;
    else if (ndStr === '1/2') nd = 0.5;
    else nd = parseFloat(ndStr) || 1;
    
    // Cria objeto de monstro temporário (não salva no banco)
    const monstroTemp = {
        id: `temp_mon_${Date.now()}`,
        nome: nome,
        hp_atual: hp,
        hp_maximo: hp,
        ca: ca,
        nd: nd,
        mod_destreza: modDex,
        acoes: [{ nome: 'Ataque', ataque: ataque, dano: dano }],
        temporario: true
    };
    
    // Armazena no widget
    widget.dadosCriatura = monstroTemp;
    widget.element.querySelector('.widget-title').textContent = `👹 ${nome}`;
    
    // Gera HTML da ficha
    widget.setConteudo(gerarHTMLFichaRapidaMonstro(monstroTemp, widgetId));
}

/**
 * Gera HTML de ficha rápida de monstro
 */
function gerarHTMLFichaRapidaMonstro(m, widgetId) {
    const hpPct = m.hp_maximo ? Math.round((m.hp_atual / m.hp_maximo) * 100) : 100;
    const hpClass = hpPct <= 25 ? 'hp-critico' : hpPct <= 50 ? 'hp-baixo' : '';
    
    return `
        <div class="widget-monstro-conteudo ficha-temporaria" data-temp-id="${m.id}">
            <div class="monstro-widget-header">
                <span class="monstro-tipo">Monstro Temporário</span>
                <span class="monstro-nd">ND ${formatarND(m.nd)}</span>
            </div>
            <div class="personagem-widget-hp ${hpClass}">
                <div class="hp-barra-mini">
                    <div class="hp-fill" style="width: ${hpPct}%"></div>
                    <span class="hp-texto">HP ${m.hp_atual}/${m.hp_maximo}</span>
                </div>
            </div>
            <div class="monstro-widget-stats">
                <div class="stat-box"><span class="valor">CA ${m.ca}</span></div>
                <div class="stat-box"><span class="valor">DEX ${m.mod_destreza >= 0 ? '+' : ''}${m.mod_destreza}</span></div>
            </div>
            ${m.acoes && m.acoes.length > 0 ? `
                <div class="monstro-widget-acoes">
                    <strong>Ações:</strong>
                    ${m.acoes.map(a => `
                        <div class="acao-item-widget">
                            <span class="acao-nome">${a.nome}</span>
                            <span class="acao-ataque">${a.ataque}</span>
                            <span class="acao-dano">${a.dano}</span>
                        </div>
                    `).join('')}
                </div>
            ` : ''}
            <div class="monstro-widget-botoes">
                <button class="btn btn-sm btn-danger" onclick="aplicarDanoFichaRapida('${widgetId}')">⚔️ Dano</button>
                <button class="btn btn-sm btn-success" onclick="aplicarCuraFichaRapida('${widgetId}')">💚 Cura</button>
                <button class="btn btn-sm btn-primary" onclick="adicionarFichaRapidaCombate('${widgetId}', 'monstro')">⚔️ Combate</button>
            </div>
        </div>
    `;
}

/**
 * Aplica dano em ficha rápida
 */
function aplicarDanoFichaRapida(widgetId) {
    const widget = window.widgetManager.obter(widgetId);
    if (!widget || !widget.dadosCriatura) return;
    
    const dano = prompt('Quanto de dano?', '0');
    if (dano === null) return;
    
    const valor = parseInt(dano) || 0;
    widget.dadosCriatura.hp_atual = Math.max(0, widget.dadosCriatura.hp_atual - valor);
    
    // Atualiza widget
    const tipo = widget.dadosCriatura.id.startsWith('temp_pc_') ? 'personagem' : 'monstro';
    if (tipo === 'personagem') {
        widget.setConteudo(gerarHTMLFichaRapidaPersonagem(widget.dadosCriatura, widgetId));
    } else {
        widget.setConteudo(gerarHTMLFichaRapidaMonstro(widget.dadosCriatura, widgetId));
    }
}

/**
 * Aplica cura em ficha rápida
 */
function aplicarCuraFichaRapida(widgetId) {
    const widget = window.widgetManager.obter(widgetId);
    if (!widget || !widget.dadosCriatura) return;
    
    const cura = prompt('Quanto de cura?', '0');
    if (cura === null) return;
    
    const valor = parseInt(cura) || 0;
    widget.dadosCriatura.hp_atual = Math.min(widget.dadosCriatura.hp_maximo, widget.dadosCriatura.hp_atual + valor);
    
    // Atualiza widget
    const tipo = widget.dadosCriatura.id.startsWith('temp_pc_') ? 'personagem' : 'monstro';
    if (tipo === 'personagem') {
        widget.setConteudo(gerarHTMLFichaRapidaPersonagem(widget.dadosCriatura, widgetId));
    } else {
        widget.setConteudo(gerarHTMLFichaRapidaMonstro(widget.dadosCriatura, widgetId));
    }
}

/**
 * Adiciona ficha rápida ao combate
 */
function adicionarFichaRapidaCombate(widgetId, tipo) {
    const widget = window.widgetManager.obter(widgetId);
    if (!widget || !widget.dadosCriatura) return;
    
    const criatura = widget.dadosCriatura;
    const initRoll = Math.floor(Math.random() * 20) + 1;
    const modDex = tipo === 'personagem' ? (criatura.mod_destreza || 0) : (criatura.mod_destreza || 0);
    const bonus = tipo === 'personagem' ? (criatura.bonus_iniciativa || modDex) : modDex;
    const iniciativa = initRoll + bonus;
    
    adicionarAosTurnos('temp', criatura.id, criatura.nome, iniciativa, modDex, criatura);
    
    mostrarNotificacao(`${criatura.nome} adicionado ao combate (Iniciativa: ${iniciativa})`, 'success');
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
    
    // Reseta contador de turnos
    SessaoState.turnoContador = 1;
    SessaoState.combateAtivo = true;
    
    // Log de combate
    adicionarLogCombate('⚔️ <strong>Batalha iniciada!</strong>', 'info');
    adicionarLogCombate(`🔄 <strong>Turno 1</strong>`, 'info');
    
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
    
    // Limpa ordem de turnos e reseta contador
    SessaoState.ordemTurnos = [];
    SessaoState.turnoAtual = 0;
    SessaoState.turnoContador = 0;
    SessaoState.combateAtivo = false;
    atualizarWidgetIniciativa();
    
    // Atualiza indicador na navbar e salva estado
    atualizarIndicadorTurno();
    salvarEstadoSessao();
}

// =========================================
// Funções de Adicionar ao Combate
// =========================================

/**
 * Adiciona um personagem à lista de turnos
 */
function adicionarPersonagemAoCombate(id, nome, modDestreza = 0) {
    adicionarAosTurnos('personagem', id, nome, null, modDestreza);
    
    // Abre widget de iniciativa se não existir
    abrirWidgetIniciativa();
}

/**
 * Adiciona uma instância de monstro à lista de turnos
 */
function adicionarInstanciaAoCombate(id, nome, modDestreza = 0) {
    adicionarAosTurnos('instancia', id, nome, null, modDestreza);
    
    // Abre widget de iniciativa se não existir
    abrirWidgetIniciativa();
}

// =========================================
// Sistema de Turnos
// =========================================

function adicionarAosTurnos(tipo, id, nome, iniciativa = null, modDestreza = 0, dadosExtras = null) {
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
    
    const entrada = {
        tipo,
        id,
        nome,
        iniciativa,
        ativo: true
    };
    
    // Para fichas temporárias, armazena os dados
    if (dadosExtras && dadosExtras.temporario) {
        entrada.dadosTemp = dadosExtras;
    }
    
    SessaoState.ordemTurnos.push(entrada);
    
    // Reordena por iniciativa (maior primeiro)
    SessaoState.ordemTurnos.sort((a, b) => b.iniciativa - a.iniciativa);
    
    atualizarWidgetIniciativa();
    
    // Abre widget de iniciativa se não existir
    abrirWidgetIniciativa();
}

function removerDosTurnos(tipo, id) {
    console.log('[removerDosTurnos] Tentando remover:', { tipo, id, tipoOf: typeof id });
    console.log('[removerDosTurnos] ordemTurnos atual:', SessaoState.ordemTurnos);
    
    const index = SessaoState.ordemTurnos.findIndex(p => {
        // Converte ambos para string para comparação consistente
        const pIdStr = String(p.id);
        const idStr = String(id);
        const match = p.tipo === tipo && pIdStr === idStr;
        console.log(`  Comparando: p.tipo=${p.tipo} (${tipo}), p.id=${p.id} (${id}) -> ${match}`);
        return match;
    });
    
    console.log('[removerDosTurnos] Index encontrado:', index);
    
    if (index !== -1) {
        const removido = SessaoState.ordemTurnos.splice(index, 1)[0];
        adicionarLogCombate(`<strong>${removido.nome}</strong> removido dos turnos`, 'info');
        
        // Ajusta turno atual se necessário
        if (SessaoState.turnoAtual >= SessaoState.ordemTurnos.length) {
            SessaoState.turnoAtual = 0;
        }
        
        atualizarWidgetIniciativa();
        salvarEstadoSessao();
    } else {
        console.error('[removerDosTurnos] Participante não encontrado!');
    }
}

function proximoTurno() {
    // Se não há participantes, apenas incrementa o contador de turnos
    if (SessaoState.ordemTurnos.length === 0) {
        SessaoState.turnoContador++;
        adicionarLogCombate(`🔄 <strong>Turno ${SessaoState.turnoContador}</strong>`, 'info');
        atualizarContadoresEfeitos();
        atualizarIndicadorTurno();
        salvarEstadoSessao();
        return;
    }
    
    const turnoAnteriorIdx = SessaoState.turnoAtual;
    
    // Se só tem 1 participante, sempre fica no mesmo e incrementa turno
    if (SessaoState.ordemTurnos.length === 1) {
        SessaoState.turnoAtual = 0;
        SessaoState.turnoContador++;
        adicionarLogCombate(`🔄 <strong>Turno ${SessaoState.turnoContador}</strong>`, 'info');
        adicionarLogCombate(`➡️ Turno de <strong>${SessaoState.ordemTurnos[0].nome}</strong>`, 'info');
        atualizarContadoresEfeitos();
    } else {
        // Múltiplos participantes: avança normalmente
        SessaoState.turnoAtual = (SessaoState.turnoAtual + 1) % SessaoState.ordemTurnos.length;
        
        // Se voltou ao início, incrementa turno
        if (SessaoState.turnoAtual === 0 && turnoAnteriorIdx !== 0) {
            SessaoState.turnoContador++;
            adicionarLogCombate(`🔄 <strong>Turno ${SessaoState.turnoContador}</strong>`, 'info');
            atualizarContadoresEfeitos();
        }
        
        const atual = SessaoState.ordemTurnos[SessaoState.turnoAtual];
        adicionarLogCombate(`➡️ Turno de <strong>${atual.nome}</strong>`, 'info');
    }
    
    atualizarWidgetIniciativa();
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
    
    // Atualiza contador de turnos
    const contadorTurno = document.getElementById('contador-turno');
    if (contadorTurno) {
        contadorTurno.querySelector('.turno-valor').textContent = SessaoState.turnoContador;
    }
    
    if (SessaoState.ordemTurnos.length === 0) {
        lista.innerHTML = '<p class="text-muted">Adicione participantes usando ⏱️ nos widgets</p>';
        return;
    }
    
    lista.innerHTML = SessaoState.ordemTurnos.map((p, i) => {
        // Debug: log da estrutura do participante
        if (!p.id && p.id !== 0) {
            console.warn('[atualizarWidgetIniciativa] Participante sem ID:', p);
        }
        
        return `
        <div class="iniciativa-item ${i === SessaoState.turnoAtual ? 'turno-atual' : ''}" data-tipo="${p.tipo}" data-id="${p.id}" data-index="${i}">
            <span class="iniciativa-ordem" contenteditable="true" onblur="editarIniciativa(event, ${i})" onkeydown="if(event.key==='Enter'){event.preventDefault();this.blur();}">${p.iniciativa}</span>
            <span class="iniciativa-nome">${p.tipo === 'personagem' ? '👤' : '👹'} ${p.nome}</span>
            <button class="btn-mini btn-remover" onclick="removerDosTurnos('${p.tipo}', '${p.id}')" title="Remover">✕</button>
        </div>
        `;
    }).join('');
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
// Widgets de Log e Iniciativa
// =========================================

function abrirWidgetLogCombate() {
    // Verifica se já existe um widget de log aberto
    const existente = encontrarWidgetPorTipo('log_combate');
    
    if (!existente) {
        // Cria novo widget de log na posição padrão (canto direito)
        const widget = window.widgetManager.criar('log_combate', {
            titulo: '📜 Log de Combate',
            x: window.innerWidth - 380,
            y: 80
        });
        widget.setConteudo(getConteudoLog());
    } else {
        // Atualiza conteúdo do existente
        atualizarWidgetLog();
    }
}

function abrirWidgetIniciativa() {
    // Verifica se já existe um widget de iniciativa aberto
    const existente = encontrarWidgetPorTipo('iniciativa');
    
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
        
        // Restaura log ANTES de tudo (é persistente por sessão)
        if (sessao.log && sessao.log.length > 0) {
            SessaoState.logCombate = sessao.log.map(l => ({
                timestamp: new Date(l.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
                tipo: l.tipo,
                mensagem: l.mensagem
            }));
        }
        
        // Abre o widget de Log de Combate primeiro (sempre visível na sessão)
        abrirWidgetLogCombate();
        
        // Restaura estado (widgets, combate, etc)
        if (sessao.estado) {
            restaurarEstado(sessao.estado);
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
        SessaoState.turnoContador = 0;
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
    // Restaura mapa usando a função aplicarCenario
    if (estado.mapa_atual) {
        console.log('[restaurarEstado] Restaurando cenário:', estado.mapa_atual);
        aplicarCenario(estado.mapa_atual);
    }
    
    // Restaura estado do combate
    SessaoState.combateAtivo = estado.combate_ativo || false;
    SessaoState.turnoContador = estado.turno_contador || estado.round_atual || 0;
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
        turno_contador: SessaoState.turnoContador,
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
    
    if (SessaoState.combateAtivo && SessaoState.turnoContador > 0) {
        indicator.style.display = 'flex';
        numero.textContent = SessaoState.turnoContador;
    } else {
        indicator.style.display = 'none';
    }
}

// =========================================
// Sistema de Cenários (Drag-and-Drop + Menu)
// =========================================

// Configura drag-and-drop na área do mapa
function configurarDropZone() {
    const dropZone = document.getElementById('mapa-container');
    
    if (!dropZone) return;
    
    // Previne comportamento padrão do navegador
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Visual feedback
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('drag-over');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('drag-over');
        });
    });
    
    // Handle drop
    dropZone.addEventListener('drop', handleDrop);
}

async function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length === 0) return;
    
    const file = files[0];
    
    // Valida tipo de arquivo
    if (!file.type.startsWith('image/')) {
        mostrarNotificacao('❌ Apenas imagens são permitidas!', 'danger');
        return;
    }
    
    // Upload via FormData
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/sessao/api/cenarios/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok && result.sucesso) {
            mostrarNotificacao(result.mensagem, 'success');
            
            // Aplica o cenário automaticamente
            await aplicarCenario(result.caminho);
        } else {
            mostrarNotificacao('❌ ' + (result.erro || 'Erro ao fazer upload'), 'danger');
        }
    } catch (error) {
        console.error('Erro no upload:', error);
        mostrarNotificacao('❌ Erro de conexão ao fazer upload', 'danger');
    }
}

// Abre modal de seleção de cenários
async function abrirModalCenarios() {
    const modal = document.getElementById('modal-cenarios');
    const lista = document.getElementById('lista-cenarios');
    
    modal.style.display = 'flex';
    lista.innerHTML = '<div class="loading">Carregando cenários...</div>';
    
    try {
        const response = await fetch('/sessao/api/cenarios');
        const cenarios = await response.json();
        
        if (cenarios.length === 0) {
            lista.innerHTML = `
                <div class="lista-vazia">
                    <p>📂 Nenhum cenário encontrado</p>
                    <p class="hint">Arraste imagens para a tela ou coloque em <code>Imagens\\Cenários</code></p>
                </div>
            `;
            return;
        }
        
        // Monta grid de cenários
        lista.innerHTML = cenarios.map(c => `
            <div class="cenario-card" onclick="selecionarCenario('${c.caminho}')">
                <img src="/sessao/imagens/${c.caminho}" alt="${c.nome}" loading="lazy">
                <div class="cenario-nome">${c.nome}</div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Erro ao carregar cenários:', error);
        lista.innerHTML = '<div class="erro">❌ Erro ao carregar cenários</div>';
    }
}

// Seleciona cenário do modal
async function selecionarCenario(caminho) {
    fecharModal('modal-cenarios');
    await aplicarCenario(caminho);
}

// Aplica cenário na tela
async function aplicarCenario(caminho) {
    const container = document.getElementById('mapa-container');
    const placeholder = document.getElementById('mapa-placeholder');
    const imagem = document.getElementById('mapa-imagem');
    const btnRemover = document.getElementById('btn-remover-mapa');
    
    if (!imagem) return;
    
    console.log('Aplicando cenário:', caminho);
    
    // Carrega imagem - corrigido: rota é /sessao/imagens/ mas blueprint tem url_prefix=/sessao
    // então a URL final fica /sessao/imagens/
    imagem.src = `/sessao/imagens/${caminho}`;
    imagem.style.display = 'block';
    placeholder.style.display = 'none';
    btnRemover.style.display = 'block';
    
    // Verifica se carregou
    imagem.onload = () => {
        console.log('Imagem carregada com sucesso:', caminho);
    };
    imagem.onerror = () => {
        console.error('Erro ao carregar imagem:', caminho);
        mostrarNotificacao('Erro ao carregar cenário', 'danger');
    };
    
    // Atualiza estado
    SessaoState.mapaAtual = caminho;
    
    // Salva no backend
    try {
        await fetch('/sessao/api/cenarios/selecionar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ caminho })
        });
    } catch (error) {
        console.warn('Erro ao salvar cenário:', error);
    }
}

// Remove cenário
async function removerMapa() {
    const placeholder = document.getElementById('mapa-placeholder');
    const imagem = document.getElementById('mapa-imagem');
    const btnRemover = document.getElementById('btn-remover-mapa');
    
    if (!imagem) return;
    
    imagem.style.display = 'none';
    imagem.src = '';
    placeholder.style.display = 'flex';
    btnRemover.style.display = 'none';
    
    SessaoState.mapaAtual = null;
    
    // Salva no backend
    try {
        await fetch('/sessao/api/cenarios/selecionar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ caminho: null })
        });
    } catch (error) {
        console.warn('Erro ao remover cenário:', error);
    }
}

// Inicializa sistema de cenários
document.addEventListener('DOMContentLoaded', () => {
    configurarDropZone();
    // carregarCenarioSalvo() foi removida - agora usa restaurarEstado()
});