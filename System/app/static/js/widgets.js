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
        
        // Determina se é widget de ficha (personagem ou monstro)
        const isFicha = this.tipo === 'ficha_personagem' || this.tipo === 'ficha_monstro';
        
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
            const url = this.dadosCriatura.tipo === 'personagem' 
                ? `/fichas/personagem/${this.dadosCriatura.id}`
                : `/fichas/monstro/${this.dadosCriatura.monstroId || this.dadosCriatura.id}`;
            window.open(url, '_blank');
        } else {
            // Tenta extrair do conteúdo
            const conteudo = this.element.querySelector('.widget-personagem-conteudo, .widget-monstro-conteudo');
            if (conteudo) {
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
    
    criar(tipo, options = {}) {
        // Incrementa contador por tipo
        if (!this.contadorTipo[tipo]) {
            this.contadorTipo[tipo] = 0;
        }
        this.contadorTipo[tipo]++;
        
        // Posição inicial escalonada
        const offset = this.widgets.size * 30;
        
        const widget = new Widget({
            tipo,
            titulo: options.titulo || this.getTituloPadrao(tipo),
            x: options.x || 100 + offset,
            y: options.y || 80 + offset,
            width: options.width || this.getLarguraPadrao(tipo),
            height: options.height || this.getAlturaPadrao(tipo),
            conteudo: options.conteudo || ''
        });
        
        this.widgets.set(widget.id, widget);
        return widget;
    }
    
    getTituloPadrao(tipo) {
        const titulos = {
            'ficha_personagem': '👤 Personagem',
            'ficha_monstro': '👹 Monstro',
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
            estado.push({
                id: widget.id,
                tipo: widget.tipo,
                titulo: widget.titulo,
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
        // Verifica se já existe (para singletons)
        const existente = Array.from(this.widgets.values()).find(w => w.tipo === config.tipo && 
            (config.tipo === 'iniciativa' || config.tipo === 'log_combate'));
        if (existente) {
            // Atualiza posição
            existente.element.style.left = `${config.x}px`;
            existente.element.style.top = `${config.y}px`;
            existente.element.style.width = `${config.width}px`;
            existente.element.style.height = `${config.height}px`;
            return existente;
        }
        
        const widget = this.criar(config.tipo, {
            titulo: config.titulo,
            x: config.x,
            y: config.y,
            width: config.width,
            height: config.height
        });
        
        if (config.minimizado) {
            widget.toggleMinimizar();
        }
        
        // Carrega conteúdo apropriado
        if (typeof adicionarWidget === 'function') {
            switch (config.tipo) {
                case 'iniciativa':
                    widget.setConteudo(getConteudoIniciativa());
                    atualizarWidgetIniciativa();
                    break;
                case 'log_combate':
                    widget.setConteudo(getConteudoLog());
                    break;
                case 'dados':
                    widget.setConteudo(getConteudoDados());
                    break;
                case 'notas':
                    widget.setConteudo(getConteudoNotas());
                    break;
                case 'ficha_personagem':
                    if (config.dadosCriatura) {
                        carregarPersonagemWidget(widget.id, config.dadosCriatura.id);
                    }
                    break;
                case 'ficha_monstro':
                    if (config.dadosCriatura) {
                        carregarMonstroWidget(widget.id, config.dadosCriatura.id);
                    }
                    break;
            }
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
