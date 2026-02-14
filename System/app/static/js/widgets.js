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
        this.dados = options.dados || null;  // Adicionado suporte para dados
        
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
                <button class="widget-control popout" title="Abrir em Janela Externa">↗️</button>
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
        const btnPopout = header.querySelector('.popout');
        
        btnMinimizar.addEventListener('click', () => this.toggleMinimizar());
        btnFechar.addEventListener('click', () => this.fechar());
        
        // Botão de abrir em janela externa (pop-out)
        if (btnPopout) {
            btnPopout.addEventListener('click', () => this.abrirPopout());
        }
        
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
    
    /**
     * Abre o widget em uma janela externa (pop-out)
     * Permite visualizar o widget fora do navegador principal
     */
    abrirPopout() {
        // Pega o conteúdo atual do widget
        const body = this.element.querySelector('.widget-body');
        const titulo = this.element.querySelector('.widget-title')?.textContent || this.titulo;
        
        if (!body) {
            console.error('Widget sem body para pop-out');
            return;
        }
        
        // Dimensões da janela popup baseadas no widget atual
        const width = Math.max(this.element.offsetWidth + 40, 380);
        const height = Math.max(this.element.offsetHeight + 80, 450);
        
        // Posição central na tela
        const left = (screen.width - width) / 2;
        const top = (screen.height - height) / 2;
        
        // Abre a nova janela
        const popup = window.open(
            '', 
            `widget_popup_${this.id}_${Date.now()}`, 
            `width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes`
        );
        
        if (!popup) {
            alert('Popup bloqueado! Por favor, permita popups para este site.');
            return;
        }
        
        // Salva referências importantes antes de gerar o HTML
        const widgetId = this.id;
        const widgetTipo = this.tipo;
        const dadosCriatura = this.dadosCriatura;
        const parentWindow = window;
        
        // Gera o HTML da janela popup
        const htmlContent = this.gerarHTMLPopout(titulo, body.innerHTML, widgetId);
        
        popup.document.write(htmlContent);
        popup.document.close();
        
        // Mantém referência à janela pai para comunicação
        popup.widgetParent = parentWindow;
        popup.widgetId = widgetId;
        popup.widgetTipo = widgetTipo;
        popup.dadosCriatura = dadosCriatura;
        
        // Configura funções wrapper no popup após carregar
        popup.onload = () => {
            this.configurarFuncoesPopup(popup);
        };
        
        // Fallback se onload não disparar
        setTimeout(() => {
            if (popup && !popup.closed) {
                this.configurarFuncoesPopup(popup);
            }
        }, 500);
    }
    
    /**
     * Configura funções wrapper no popup para comunicar com a janela pai
     */
    configurarFuncoesPopup(popup) {
        if (!popup || popup.closed) return;
        
        const parent = popup.widgetParent;
        if (!parent) return;
        
        // Define funções wrapper que chamam a janela pai
        popup.rolarAtaque = function(...args) {
            if (parent && !parent.closed && parent.rolarAtaque) {
                parent.rolarAtaque(...args);
            }
        };
        
        // NOTA: abrirDanoRapido e abrirCuraRapida são tratadas localmente no popup
        // para que o input apareça na janela popup, não na janela pai
        
        popup.toggleMenuResistencia = function(...args) {
            if (parent && !parent.closed && parent.toggleMenuResistencia) {
                parent.toggleMenuResistencia(...args);
            }
        };
        
        popup.abrirModalEfeito = function(...args) {
            if (parent && !parent.closed && parent.abrirModalEfeito) {
                parent.abrirModalEfeito(...args);
            }
        };
        
        popup.abrirSubmenuPericias = function(...args) {
            if (parent && !parent.closed && parent.abrirSubmenuPericias) {
                parent.abrirSubmenuPericias(...args);
            }
        };
        
        popup.rolarMagiaNPC = function(...args) {
            if (parent && !parent.closed && parent.rolarMagiaNPC) {
                parent.rolarMagiaNPC(...args);
            }
        };
        
        popup.usarHabilidadeNPC = function(...args) {
            if (parent && !parent.closed && parent.usarHabilidadeNPC) {
                parent.usarHabilidadeNPC(...args);
            }
        };
        
        popup.marcarTesteMorte = function(...args) {
            if (parent && !parent.closed && parent.marcarTesteMorte) {
                parent.marcarTesteMorte(...args);
            }
        };
        
        popup.adicionarLogCombate = function(...args) {
            if (parent && !parent.closed && parent.adicionarLogCombate) {
                parent.adicionarLogCombate(...args);
            }
        };
        
        popup.mostrarNotificacao = function(...args) {
            if (parent && !parent.closed && parent.mostrarNotificacao) {
                parent.mostrarNotificacao(...args);
            }
        };
        
        console.log('[Popup] Funções wrapper configuradas');
    }
    
    /**
     * Gera o HTML completo para a janela popup
     */
    gerarHTMLPopout(titulo, conteudo, widgetId) {
        // Pega a URL base para os recursos
        const baseUrl = window.location.origin;
        
        return `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${titulo} - Out of the Abyss</title>
    
    <!-- CSS do Sistema -->
    <link rel="stylesheet" href="${baseUrl}/static/css/base.css">
    <link rel="stylesheet" href="${baseUrl}/static/css/widgets.css">
    <link rel="stylesheet" href="${baseUrl}/static/css/fichas.css">
    <link rel="stylesheet" href="${baseUrl}/static/css/sessao.css">
    
    <style>
        /* Estilos específicos do popup */
        body {
            background: var(--bg-primary);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        
        .popup-container {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        .popup-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: var(--spacing-sm) var(--spacing-md);
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .popup-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        .popup-badge {
            font-size: 0.65rem;
            padding: 2px 6px;
            background: var(--accent-info);
            color: white;
            border-radius: var(--radius-sm);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .popup-body {
            flex: 1;
            overflow-y: auto;
            background: var(--bg-secondary);
        }
        
        /* Ajustes para o conteúdo do widget no popup */
        .popup-body > * {
            border-radius: 0;
        }
        
        .popup-body .widget-personagem-conteudo,
        .popup-body .widget-monstro-conteudo,
        .popup-body .widget-npc-conteudo {
            padding: var(--spacing-md);
        }
        
        /* Indicador de conexão */
        .conexao-status {
            position: fixed;
            bottom: var(--spacing-sm);
            right: var(--spacing-sm);
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            z-index: 101;
        }
        
        .conexao-status.conectado {
            background: var(--accent-success);
            color: white;
        }
        
        .conexao-status.desconectado {
            background: var(--accent-danger);
            color: white;
        }
    </style>
</head>
<body class="tema-abyss">
    <div class="popup-container">
        <div class="popup-header">
            <span class="popup-title">${titulo}</span>
            <span class="popup-badge">Externo</span>
        </div>
        <div class="popup-body">
            ${conteudo}
        </div>
    </div>
    
    <div class="conexao-status conectado" id="conexao-status">● Conectado</div>
    
    <script>
        // Verifica conexão com a janela pai periodicamente
        let conexaoCheck = setInterval(function() {
            const status = document.getElementById('conexao-status');
            if (!window.widgetParent || window.widgetParent.closed) {
                status.textContent = '● Desconectado';
                status.className = 'conexao-status desconectado';
            } else {
                status.textContent = '● Conectado';
                status.className = 'conexao-status conectado';
            }
        }, 2000);
        
        // Limpa interval ao fechar
        window.addEventListener('beforeunload', function() {
            clearInterval(conexaoCheck);
        });
        
        // Notifica a janela pai sobre ações
        document.addEventListener('click', function(e) {
            // Verifica se clicou em um elemento com onclick
            const target = e.target.closest('[onclick]');
            if (!target) return;
            
            const onclickStr = target.getAttribute('onclick');
            if (!onclickStr) return;
            
            // Lista de funções que devem ser executadas na janela pai
            // NOTA: abrirDanoRapido e abrirCuraRapida são tratadas localmente no popup
            const funcoesParent = [
                'rolarAtaque',
                'toggleMenuResistencia',
                'abrirModalEfeito',
                'abrirSubmenuPericias',
                'rolarMagiaNPC',
                'usarHabilidadeNPC',
                'marcarTesteMorte',
                'adicionarLogCombate'
            ];
            
            // Verifica se a função deve ser redirecionada
            const deveRedirecionar = funcoesParent.some(fn => onclickStr.includes(fn));
            
            if (deveRedirecionar && window.widgetParent && !window.widgetParent.closed) {
                e.preventDefault();
                e.stopPropagation();
                
                try {
                    // Executa na janela pai
                    window.widgetParent.eval(onclickStr);
                } catch (err) {
                    console.error('[Popup] Erro ao executar na janela pai:', err);
                    // Tenta executar localmente como fallback
                    try {
                        eval(onclickStr);
                    } catch (err2) {
                        console.error('[Popup] Fallback também falhou:', err2);
                    }
                }
            }
        });
        
        console.log('[Popup] Widget ${widgetId} carregado');
        
        // =========================================
        // Sistema local de Dano/Cura para Popup
        // =========================================
        
        let inputFlutuantePopup = null;
        
        function fecharInputFlutuantePopup() {
            if (inputFlutuantePopup) {
                inputFlutuantePopup.remove();
                inputFlutuantePopup = null;
            }
        }
        
        function criarInputFlutuantePopup(botao, tipo, callback) {
            fecharInputFlutuantePopup();
            
            const rect = botao.getBoundingClientRect();
            const container = document.createElement('div');
            container.className = 'input-flutuante input-flutuante-' + tipo;
            container.innerHTML = [
                '<input type="number" class="input-flutuante-valor" placeholder="0" min="0" autofocus>',
                '<button class="input-flutuante-confirmar">✓</button>',
                '<button class="input-flutuante-cancelar">✕</button>'
            ].join('');
            
            container.style.cssText = 'position: fixed; left: ' + rect.left + 'px; top: ' + (rect.bottom + 5) + 'px; z-index: 9999;';
            
            document.body.appendChild(container);
            inputFlutuantePopup = container;
            
            const input = container.querySelector('.input-flutuante-valor');
            const btnConfirmar = container.querySelector('.input-flutuante-confirmar');
            const btnCancelar = container.querySelector('.input-flutuante-cancelar');
            
            setTimeout(function() { input.focus(); }, 10);
            
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    const valor = parseInt(input.value) || 0;
                    if (valor > 0) { callback(valor); fecharInputFlutuantePopup(); }
                } else if (e.key === 'Escape') {
                    fecharInputFlutuantePopup();
                }
            });
            
            btnConfirmar.addEventListener('click', function() {
                const valor = parseInt(input.value) || 0;
                if (valor > 0) { callback(valor); fecharInputFlutuantePopup(); }
            });
            
            btnCancelar.addEventListener('click', fecharInputFlutuantePopup);
            
            setTimeout(function() {
                document.addEventListener('click', function clickFora(e) {
                    if (inputFlutuantePopup && !inputFlutuantePopup.contains(e.target)) {
                        fecharInputFlutuantePopup();
                        document.removeEventListener('click', clickFora);
                    }
                });
            }, 100);
        }
        
        // Função local de Dano
        function abrirDanoRapido(event, id, nome, tipo) {
            event.stopPropagation();
            const botao = event.currentTarget;
            
            criarInputFlutuantePopup(botao, 'dano', async function(valor) {
                try {
                    let endpoint;
                    if (tipo === 'personagem') {
                        endpoint = '/api/personagens/' + id + '/dano';
                    } else if (tipo === 'npc') {
                        endpoint = '/api/npcs/' + id + '/dano';
                    } else {
                        endpoint = '/api/monstros/instancias/' + id + '/dano';
                    }
                    
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ dano: valor })
                    });
                    const resultado = await response.json();
                    
                    if (resultado && !resultado.erro) {
                        // Notifica a janela pai para atualizar
                        if (window.widgetParent && !window.widgetParent.closed) {
                            window.widgetParent.adicionarLogCombate('<strong>' + nome + '</strong> -' + valor + ' HP', 'dano');
                            window.widgetParent.atualizarWidgetCriatura(tipo, id, resultado);
                        }
                        // Atualiza HP local no popup
                        atualizarHPLocal(resultado);
                    }
                } catch (error) {
                    console.error('Erro ao aplicar dano:', error);
                }
            });
        }
        
        // Função local de Cura
        function abrirCuraRapida(event, id, nome, tipo) {
            event.stopPropagation();
            const botao = event.currentTarget;
            
            criarInputFlutuantePopup(botao, 'cura', async function(valor) {
                try {
                    let endpoint;
                    if (tipo === 'personagem') {
                        endpoint = '/api/personagens/' + id + '/curar';
                    } else if (tipo === 'npc') {
                        endpoint = '/api/npcs/' + id + '/curar';
                    } else {
                        endpoint = '/api/monstros/instancias/' + id + '/curar';
                    }
                    
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ quantidade: valor })
                    });
                    const resultado = await response.json();
                    
                    if (resultado && !resultado.erro) {
                        // Notifica a janela pai para atualizar
                        if (window.widgetParent && !window.widgetParent.closed) {
                            window.widgetParent.adicionarLogCombate('<strong>' + nome + '</strong> +' + valor + ' HP', 'cura');
                            window.widgetParent.atualizarWidgetCriatura(tipo, id, resultado);
                        }
                        // Atualiza HP local no popup
                        atualizarHPLocal(resultado);
                    }
                } catch (error) {
                    console.error('Erro ao aplicar cura:', error);
                }
            });
        }
        
        // Atualiza a barra de HP no popup
        function atualizarHPLocal(dados) {
            const hpAtual = dados.hp_atual;
            const hpMax = dados.hp_maximo;
            const percent = Math.max(0, Math.min(100, (hpAtual / hpMax) * 100));
            
            // Atualiza texto de HP
            const hpTexto = document.querySelector('.hp-atual');
            if (hpTexto) hpTexto.textContent = hpAtual;
            
            // Atualiza barra visual
            const hpFill = document.querySelector('.hp-fill');
            if (hpFill) {
                hpFill.style.width = percent + '%';
                // Atualiza cor
                let corClasse = 'hp-100';
                if (percent <= 0) corClasse = 'hp-0';
                else if (percent <= 25) corClasse = 'hp-25';
                else if (percent <= 50) corClasse = 'hp-50';
                else if (percent <= 75) corClasse = 'hp-75';
                hpFill.className = 'hp-fill ' + corClasse;
            }
        }
    </script>
</body>
</html>`;
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
            'nota': '📝 Nota',
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
        const widget = this.widgets.get(id);
        
        // Se for widget de nota, notifica para atualizar a lista
        if (widget && widget.tipo === 'nota') {
            // Remove do estado da sessão também
            if (window.SessaoState && window.SessaoState.widgets) {
                const index = window.SessaoState.widgets.findIndex(w => w.id === id);
                if (index !== -1) {
                    window.SessaoState.widgets.splice(index, 1);
                }
                
                // Atualiza lista de notas se a função existir
                if (typeof window.carregarListaNotas === 'function') {
                    window.carregarListaNotas();
                }
                
                // Salva estado se a função existir
                if (typeof window.salvarEstadoSessao === 'function') {
                    window.salvarEstadoSessao();
                }
            }
        }
        
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
            
            const widgetState = {
                id: widget.id,
                tipo: widget.tipo,
                titulo: tituloAtual,
                x: widget.element.offsetLeft,
                y: widget.element.offsetTop,
                width: widget.element.offsetWidth,
                height: widget.element.offsetHeight,
                minimizado: widget.minimizado,
                dadosCriatura: widget.dadosCriatura || null
            };
            
            // Para widgets de nota, salva os dados da nota
            if (widget.tipo === 'nota' && widget.dados) {
                widgetState.dados = widget.dados;
            }
            
            estado.push(widgetState);
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
            case 'nota':
                // Widget de nota individual - restaura diretamente de config.dados
                if (config.dados && typeof criarWidgetNota === 'function') {
                    // Remove widget temporário e cria um novo com dados corretos
                    widget.fechar();
                    criarWidgetNota(config.dados);
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
