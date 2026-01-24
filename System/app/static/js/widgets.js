/**
 * Out of the Abyss - Sistema de Widgets
 * Blocos flutuantes arrastáveis e redimensionáveis
 */

class Widget {
    constructor(options = {}) {
        this.id = options.id || `widget-${Date.now()}`;
        this.tipo = options.tipo || 'generico';
        this.titulo = options.titulo || 'Widget';
        this.x = options.x || 100;
        this.y = options.y || 100;
        this.width = options.width || 300;
        this.height = options.height || 200;
        this.minimizado = false;
        
        this.element = null;
        this.conteudo = options.conteudo || '';
        
        this.criar();
    }
    
    criar() {
        // Container principal
        this.element = document.createElement('div');
        this.element.id = this.id;
        this.element.className = `widget widget-${this.tipo}`;
        this.element.style.left = `${this.x}px`;
        this.element.style.top = `${this.y}px`;
        this.element.style.width = `${this.width}px`;
        this.element.style.height = `${this.height}px`;
        
        // Determina se é widget de ficha (personagem, monstro ou NPC)
        const isFicha = this.tipo === 'ficha_personagem' || this.tipo === 'ficha_monstro';
        const isNPC = this.tipo === 'ficha_npc';
        
        // Header
        const header = document.createElement('div');
        header.className = 'widget-header';
        header.innerHTML = `
            <span class="widget-title">${this.titulo}</span>
            <div class="widget-controls">
                ${isFicha ? `
                    <button class="widget-control turnos" title="Adicionar aos Turnos" data-widget-id="${this.id}">⏱️</button>
                    <button class="widget-control ficha" title="Abrir Ficha Completa" data-widget-id="${this.id}">📋</button>
                ` : ''}
                ${isNPC ? `
                    <button class="widget-control ficha" title="Abrir Ficha Completa" data-widget-id="${this.id}">📋</button>
                ` : ''}
                <button class="widget-control minimize" title="Minimizar">−</button>
                <button class="widget-control close" title="Fechar">×</button>
            </div>
        `;
        
        // Body
        const body = document.createElement('div');
        body.className = 'widget-body';
        body.innerHTML = this.conteudo;
        
        this.element.appendChild(header);
        this.element.appendChild(body);
        
        // Event listeners
        this.setupDrag(header);
        this.setupControles(header);
        
        // Adiciona ao container
        const container = document.getElementById('widgets-container');
        if (container) {
            container.appendChild(this.element);
        }
        
        // Traz para frente ao clicar
        this.element.addEventListener('mousedown', () => this.trazerParaFrente());
    }
    
    setupDrag(header) {
        let isDragging = false;
        let startX, startY, initialX, initialY;
        
        // Middle-click para fechar widget
        header.addEventListener('mousedown', (e) => {
            if (e.button === 1) {
                e.preventDefault();
                this.fechar();
                return;
            }
            
            if (e.target.classList.contains('widget-control')) return;
            
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            initialX = this.element.offsetLeft;
            initialY = this.element.offsetTop;
            
            this.element.style.transition = 'none';
        });
        
        // Prevenir comportamento padrão do middle-click
        header.addEventListener('auxclick', (e) => {
            if (e.button === 1) e.preventDefault();
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            
            this.element.style.left = `${initialX + dx}px`;
            this.element.style.top = `${initialY + dy}px`;
        });
        
        document.addEventListener('mouseup', () => {
            isDragging = false;
            this.element.style.transition = '';
        });
    }
    
    setupControles(header) {
        const btnMinimizar = header.querySelector('.minimize');
        const btnFechar = header.querySelector('.close');
        const btnTurnos = header.querySelector('.turnos');
        const btnFicha = header.querySelector('.ficha');
        
        btnMinimizar.addEventListener('click', () => this.toggleMinimizar());
        btnFechar.addEventListener('click', () => this.fechar());
        
        // Botão de adicionar aos turnos
        if (btnTurnos) {
            btnTurnos.addEventListener('click', () => this.adicionarAosTurnos());
        }
        
        // Botão de abrir ficha completa
        if (btnFicha) {
            btnFicha.addEventListener('click', () => this.abrirFichaCompleta());
        }
    }
    
    adicionarAosTurnos() {
        // Extrai dados do widget para adicionar aos turnos
        if (this.dadosCriatura) {
            // Widget já tem dados salvos (monstro instanciado ou personagem)
            if (typeof adicionarAosTurnos === 'function') {
                const modDes = this.dadosCriatura.modDestreza || 0;
                adicionarAosTurnos(this.dadosCriatura.tipo, this.dadosCriatura.id, this.dadosCriatura.nome, null, modDes);
            }
        } else {
            // Tenta extrair do conteúdo
            const conteudo = this.element.querySelector('.widget-personagem-conteudo, .widget-monstro-conteudo');
            if (conteudo) {
                const btnDano = conteudo.querySelector('.btn-danger');
                if (btnDano) {
                    const onclick = btnDano.getAttribute('onclick') || '';
                    // Extrai id e nome do onclick
                    const match = onclick.match(/abrirDanoRapido\(event,\s*(\d+),\s*'([^']+)',\s*'([^']+)'\)/);
                    if (match) {
                        const [, id, nome, tipo] = match;
                        // Tenta extrair modificador de destreza do widget
                        const desSpan = conteudo.querySelector('[title="Destreza"]');
                        let modDes = 0;
                        if (desSpan) {
                            const desText = desSpan.textContent.match(/[+-]?\d+$/);
                            if (desText) modDes = parseInt(desText[0]) || 0;
                        }
                        if (typeof adicionarAosTurnos === 'function') {
                            adicionarAosTurnos(tipo, parseInt(id), nome, null, modDes);
                        }
                    }
                }
            }
        }
    }
    
    abrirFichaCompleta() {
        // Tenta abrir a ficha completa baseado no tipo do widget
        if (this.dadosCriatura) {
            let url;
            if (this.dadosCriatura.tipo === 'personagem') {
                url = `/fichas/personagem/${this.dadosCriatura.id}`;
            } else if (this.dadosCriatura.tipo === 'npc') {
                url = `/fichas/npc/${this.dadosCriatura.id}`;
            } else {
                // Monstro ou instância
                url = `/fichas/monstro/${this.dadosCriatura.monstroId || this.dadosCriatura.id}`;
            }
            window.open(url, '_blank');
        } else {
            // Tenta extrair do conteúdo
            const conteudo = this.element.querySelector('.widget-personagem-conteudo, .widget-monstro-conteudo, .widget-npc-conteudo');
            if (conteudo) {
                // Verifica se é NPC
                const npcId = conteudo.dataset.npcId;
                if (npcId) {
                    window.open(`/fichas/npc/${npcId}`, '_blank');
                    return;
                }
                
                const btnDano = conteudo.querySelector('.btn-danger');
                if (btnDano) {
                    const onclick = btnDano.getAttribute('onclick') || '';
                    const match = onclick.match(/abrirDanoRapido\(event,\s*(\d+),\s*'([^']+)',\s*'([^']+)'\)/);
                    if (match) {
                        const [, id, , tipo] = match;
                        const url = tipo === 'personagem' 
                            ? `/fichas/personagem/${id}`
                            : `/fichas/monstro/${id}`;
                        window.open(url, '_blank');
                    }
                }
            }
        }
    }
    
    toggleMinimizar() {
        this.minimizado = !this.minimizado;
        this.element.classList.toggle('minimized', this.minimizado);
        
        const btn = this.element.querySelector('.minimize');
        btn.textContent = this.minimizado ? '+' : '−';
    }
    
    fechar() {
        this.element.remove();
        
        // Remove do gerenciador
        if (window.widgetManager) {
            window.widgetManager.remover(this.id);
        }
    }
    
    trazerParaFrente() {
        const widgets = document.querySelectorAll('.widget');
        widgets.forEach(w => w.style.zIndex = '100');
        this.element.style.zIndex = '101';
    }
    
    setConteudo(html) {
        const body = this.element.querySelector('.widget-body');
        if (body) {
            body.innerHTML = html;
        }
    }
    
    async carregarConteudo(url) {
        try {
            const response = await fetch(url);
            const html = await response.text();
            this.setConteudo(html);
        } catch (error) {
            console.error('Erro ao carregar conteúdo:', error);
        }
    }
}

// =========================================
// Gerenciador de Widgets
// =========================================

class WidgetManager {
    constructor() {
        this.widgets = new Map();
        this.contadorTipo = {};
    }
    
    /**
     * Encontra uma posição livre para um novo widget
     */
    encontrarPosicaoLivre(largura, altura, xBase = 100, yBase = 80) {
        const GAP = 20; // Espaço entre widgets
        const container = document.getElementById('widgets-container');
        const maxX = container ? container.offsetWidth - largura - 20 : window.innerWidth - largura - 20;
        const maxY = container ? container.offsetHeight - altura - 20 : window.innerHeight - altura - 100;
        
        // Coleta todas as posições ocupadas
        const ocupados = [];
        this.widgets.forEach(w => {
            ocupados.push({
                x: w.element.offsetLeft,
                y: w.element.offsetTop,
                w: w.element.offsetWidth,
                h: w.element.offsetHeight
            });
        });
        
        // Função para verificar colisão
        const colide = (x, y) => {
            return ocupados.some(o => 
                x < o.x + o.w + GAP && x + largura + GAP > o.x &&
                y < o.y + o.h + GAP && y + altura + GAP > o.y
            );
        };
        
        // Tenta posição base primeiro
        if (!colide(xBase, yBase)) {
            return { x: xBase, y: yBase };
        }
        
        // Tenta abaixo dos widgets existentes
        for (const o of ocupados) {
            const novoY = o.y + o.h + GAP;
            if (novoY + altura <= maxY && !colide(xBase, novoY)) {
                return { x: xBase, y: novoY };
            }
        }
        
        // Tenta à direita dos widgets existentes
        for (const o of ocupados) {
            const novoX = o.x + o.w + GAP;
            if (novoX + largura <= maxX && !colide(novoX, yBase)) {
                return { x: novoX, y: yBase };
            }
        }
        
        // Fallback: posição escalonada
        const offset = this.widgets.size * 30;
        return { x: xBase + offset, y: yBase + offset };
    }
    
    criar(tipo, options = {}) {
        // Incrementa contador por tipo
        if (!this.contadorTipo[tipo]) {
            this.contadorTipo[tipo] = 0;
        }
        this.contadorTipo[tipo]++;
        
        const largura = options.width || this.getLarguraPadrao(tipo);
        const altura = options.height || this.getAlturaPadrao(tipo);
        
        // Calcula posição: usa a fornecida ou encontra uma livre
        let posX = options.x;
        let posY = options.y;
        
        if (posX === undefined || posY === undefined) {
            const posLivre = this.encontrarPosicaoLivre(largura, altura);
            posX = posX !== undefined ? posX : posLivre.x;
            posY = posY !== undefined ? posY : posLivre.y;
        }
        
        const widget = new Widget({
            tipo,
            titulo: options.titulo || this.getTituloPadrao(tipo),
            x: posX,
            y: posY,
            width: largura,
            height: altura,
            conteudo: options.conteudo || ''
        });
        
        this.widgets.set(widget.id, widget);
        return widget;
    }
    
    getTituloPadrao(tipo) {
        const titulos = {
            'ficha_personagem': '👤 Personagem',
            'ficha_monstro': '👹 Monstro',
            'ficha_npc': '🎭 NPC',
            'iniciativa': '⏱️ Iniciativa',
            'log_combate': '📜 Log de Combate',
            'notas': '📝 Notas',
            'dados': '🎲 Dados',
            'condicoes': '⚠️ Condições',
            'magias': '✨ Magias'
        };
        return titulos[tipo] || 'Widget';
    }
    
    getLarguraPadrao(tipo) {
        const larguras = {
            'ficha_personagem': 320,
            'ficha_monstro': 350,
            'ficha_npc': 320,
            'iniciativa': 280,
            'log_combate': 350,
            'notas': 300,
            'dados': 250
        };
        return larguras[tipo] || 300;
    }
    
    getAlturaPadrao(tipo) {
        const alturas = {
            'ficha_personagem': 400,
            'ficha_monstro': 450,
            'ficha_npc': 400,
            'iniciativa': 300,
            'log_combate': 350,
            'notas': 250,
            'dados': 200
        };
        return alturas[tipo] || 200;
    }
    
    obter(id) {
        return this.widgets.get(id);
    }
    
    remover(id) {
        this.widgets.delete(id);
    }
    
    listar() {
        return Array.from(this.widgets.values());
    }
    
    salvarEstado() {
        const estado = [];
        this.widgets.forEach(widget => {
            // Pega o título atual do DOM (pode ter sido alterado)
            const tituloAtual = widget.element.querySelector('.widget-title')?.textContent || widget.titulo;
            
            estado.push({
                id: widget.id,
                tipo: widget.tipo,
                titulo: tituloAtual,
                x: widget.element.offsetLeft,
                y: widget.element.offsetTop,
                width: widget.element.offsetWidth,
                height: widget.element.offsetHeight,
                minimizado: widget.minimizado,
                dadosCriatura: widget.dadosCriatura || null
            });
        });
        return estado;
    }
    
    restaurarWidget(config) {
        console.log('[WidgetManager.restaurarWidget] Iniciando restauração:', config);
        
        // Normaliza tipo (pode vir como objeto de sessões antigas corrompidas)
        let tipo = config.tipo;
        if (typeof tipo === 'object' && tipo !== null) {
            tipo = tipo.tipo || 'desconhecido';
        }
        
        console.log('[WidgetManager.restaurarWidget] Tipo normalizado:', tipo);
        
        // Verifica se já existe (para singletons)
        const existente = Array.from(this.widgets.values()).find(w => w.tipo === tipo && 
            (tipo === 'iniciativa' || tipo === 'log_combate'));
        if (existente) {
            // Atualiza posição e título
            existente.element.style.left = `${config.x}px`;
            existente.element.style.top = `${config.y}px`;
            existente.element.style.width = `${config.width}px`;
            existente.element.style.height = `${config.height}px`;
            // Garante título correto
            const tituloCorreto = this.getTituloPadrao(tipo);
            existente.element.querySelector('.widget-title').textContent = tituloCorreto;
            return existente;
        }
        
        // Determina título: usa o salvo apenas se não for genérico "Widget"
        let titulo = config.titulo;
        if (!titulo || titulo === 'Widget') {
            titulo = this.getTituloPadrao(tipo);
        }
        
        const widget = this.criar(tipo, {
            titulo: titulo,
            x: config.x,
            y: config.y,
            width: config.width,
            height: config.height
        });
        
        // Salva dadosCriatura no widget para referência futura
        if (config.dadosCriatura) {
            widget.dadosCriatura = config.dadosCriatura;
        }
        
        if (config.minimizado) {
            widget.toggleMinimizar();
        }
        
        // Carrega conteúdo apropriado (funções definidas em sessao.js)
        switch (tipo) {
            case 'iniciativa':
                if (typeof getConteudoIniciativa === 'function') {
                    widget.setConteudo(getConteudoIniciativa());
                    if (typeof atualizarWidgetIniciativa === 'function') {
                        atualizarWidgetIniciativa();
                    }
                }
                break;
            case 'log_combate':
                if (typeof getConteudoLog === 'function') {
                    widget.setConteudo(getConteudoLog());
                }
                break;
            case 'dados':
                if (typeof getConteudoDados === 'function') {
                    widget.setConteudo(getConteudoDados());
                }
                break;
            case 'notas':
                if (typeof getConteudoNotas === 'function') {
                    widget.setConteudo(getConteudoNotas());
                }
                break;
            case 'ficha_personagem':
                console.log('[restaurarWidget] Restaurando personagem:', config.dadosCriatura);
                if (config.dadosCriatura && config.dadosCriatura.id && typeof carregarPersonagemWidget === 'function') {
                    carregarPersonagemWidget(widget.id, config.dadosCriatura.id);
                } else {
                    console.warn('Widget de personagem sem dados válidos:', config);
                    // Não fecha automaticamente - aguarda carregamento
                }
                break;
            case 'ficha_monstro':
                // Verifica se tem dados de criatura
                console.log('[restaurarWidget] Restaurando monstro:', config.dadosCriatura);
                if (config.dadosCriatura && config.dadosCriatura.id) {
                    // Verifica se é instância ou monstro base pelo tipo
                    if (config.dadosCriatura.tipo === 'instancia' && typeof carregarMonstroInstanciaWidget === 'function') {
                        console.log('[restaurarWidget] Carregando instância de monstro:', config.dadosCriatura.id);
                        carregarMonstroInstanciaWidget(widget.id, config.dadosCriatura.id);
                    } else if (typeof carregarMonstroWidget === 'function') {
                        console.log('[restaurarWidget] Carregando monstro base:', config.dadosCriatura.id);
                        carregarMonstroWidget(widget.id, config.dadosCriatura.id);
                    }
                } else {
                    console.warn('Widget de monstro sem dados válidos:', config);
                    // Não fecha automaticamente - aguarda carregamento
                }
                break;
            case 'ficha_npc':
                console.log('[restaurarWidget] Restaurando NPC:', config.dadosCriatura);
                if (config.dadosCriatura && config.dadosCriatura.id && typeof carregarNPCWidget === 'function') {
                    carregarNPCWidget(widget.id, config.dadosCriatura.id);
                } else {
                    console.warn('Widget de NPC sem dados válidos:', config);
                }
                break;
        }
        
        return widget;
    }
    
    restaurarEstado(estado) {
        if (!Array.isArray(estado)) return;
        estado.forEach(config => {
            try {
                this.restaurarWidget(config);
            } catch (e) {
                console.warn('Erro ao restaurar widget:', e);
            }
        });
    }
}

// Instância global
window.widgetManager = new WidgetManager();
