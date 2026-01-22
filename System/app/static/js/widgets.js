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
        
        // Header
        const header = document.createElement('div');
        header.className = 'widget-header';
        header.innerHTML = `
            <span class="widget-title">${this.titulo}</span>
            <div class="widget-controls">
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
        
        header.addEventListener('mousedown', (e) => {
            if (e.target.classList.contains('widget-control')) return;
            
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            initialX = this.element.offsetLeft;
            initialY = this.element.offsetTop;
            
            this.element.style.transition = 'none';
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
        
        btnMinimizar.addEventListener('click', () => this.toggleMinimizar());
        btnFechar.addEventListener('click', () => this.fechar());
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
            conteudo: options.conteudo || '',
            ...options
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
                x: widget.element.offsetLeft,
                y: widget.element.offsetTop,
                width: widget.element.offsetWidth,
                height: widget.element.offsetHeight,
                minimizado: widget.minimizado
            });
        });
        return estado;
    }
    
    restaurarEstado(estado) {
        // TODO: Implementar restauração de estado
    }
}

// Instância global
window.widgetManager = new WidgetManager();
