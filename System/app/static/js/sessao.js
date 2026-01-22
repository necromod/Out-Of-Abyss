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
    widgets: []
};

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
        <div class="iniciativa-lista" id="lista-iniciativa">
            <p class="text-muted">Nenhum combate ativo</p>
        </div>
        <div class="mt-2">
            <button class="btn btn-sm" onclick="adicionarParticipante()">+ Adicionar</button>
            <button class="btn btn-sm" onclick="ordenarIniciativa()">Ordenar</button>
        </div>
    `;
}

function getConteudoLog() {
    return `
        <div class="log-lista" id="log-combate">
            <p class="text-muted">Nenhuma ação registrada</p>
        </div>
    `;
}

// =========================================
// Seletores de Conteúdo
// =========================================

async function abrirSeletorPersonagem(widget) {
    document.getElementById('modal-widget-titulo').textContent = 'Selecionar Personagem';
    
    const personagens = await API.get('/fichas/personagens');
    const conteudo = document.getElementById('modal-widget-conteudo');
    
    if (personagens.length === 0) {
        conteudo.innerHTML = `
            <p class="text-muted">Nenhum personagem cadastrado</p>
            <button class="btn btn-primary mt-2" onclick="criarPersonagemRapido('${widget.id}')">+ Criar Personagem</button>
        `;
    } else {
        conteudo.innerHTML = personagens.map(p => `
            <div class="acao-item" onclick="carregarPersonagemWidget('${widget.id}', '${p.id}')">
                <strong>${p.nome}</strong>
                <span>${p.classe} ${p.nivel}</span>
            </div>
        `).join('');
    }
    
    abrirModal('modal-widget');
}

async function carregarPersonagemWidget(widgetId, personagemId) {
    fecharModal('modal-widget');
    
    const widget = window.widgetManager.obter(widgetId);
    if (widget) {
        await widget.carregarConteudo(`/fichas/widget/personagem/${personagemId}`);
    }
}

async function abrirSeletorMonstro(widget) {
    document.getElementById('modal-widget-titulo').textContent = 'Selecionar Monstro';
    
    const monstros = await API.get('/fichas/monstros');
    const conteudo = document.getElementById('modal-widget-conteudo');
    
    conteudo.innerHTML = monstros.map(m => `
        <div class="acao-item" onclick="criarInstanciaMonstro('${widget.id}', '${m.id}')">
            <strong>${m.nome}</strong>
            <span>ND ${m.nd}</span>
        </div>
    `).join('');
    
    abrirModal('modal-widget');
}

async function criarInstanciaMonstro(widgetId, monstroId) {
    fecharModal('modal-widget');
    
    const resultado = await API.post('/fichas/monstro/instancia', {
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

function toggleCombate() {
    SessaoState.combateAtivo = !SessaoState.combateAtivo;
    
    const btn = document.querySelector('.btn-combat');
    btn.classList.toggle('active', SessaoState.combateAtivo);
    
    if (SessaoState.combateAtivo) {
        iniciarCombate();
    } else {
        finalizarCombate();
    }
}

async function iniciarCombate() {
    const resultado = await API.post('/combate/iniciar', {});
    notificar('Combate iniciado!', 'success');
    
    // Atualiza widget de iniciativa se existir
    atualizarWidgetIniciativa();
}

async function finalizarCombate() {
    const resultado = await API.post('/combate/finalizar', {});
    notificar('Combate finalizado', 'info');
}

function atualizarWidgetIniciativa() {
    const lista = document.getElementById('lista-iniciativa');
    if (!lista) return;
    
    // TODO: Carregar ordem de iniciativa real
    lista.innerHTML = '<p class="text-muted">Configure a iniciativa</p>';
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

// =========================================
// Inicialização
// =========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎲 Tela de Sessão carregada');
    
    // Verifica status da API
    API.get('/api/status').then(status => {
        console.log('API:', status);
    });
});

// Salvar estado periodicamente
setInterval(() => {
    const estado = window.widgetManager.salvarEstado();
    // TODO: Enviar para o servidor
}, 30000);
