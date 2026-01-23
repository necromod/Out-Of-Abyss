/**
 * Out of the Abyss - JavaScript Base
 * Funções utilitárias globais
 */

// =========================================
// API Helper
// =========================================

const API = {
    async get(endpoint) {
        const response = await fetch(endpoint);
        return response.json();
    },
    
    async post(endpoint, data) {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async patch(endpoint, data) {
        const response = await fetch(endpoint, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async delete(endpoint) {
        const response = await fetch(endpoint, { method: 'DELETE' });
        return response.json();
    }
};

// =========================================
// Utilitários de DOM
// =========================================

function $(selector) {
    return document.querySelector(selector);
}

function $$(selector) {
    return document.querySelectorAll(selector);
}

function createElement(tag, classes = [], attributes = {}) {
    const el = document.createElement(tag);
    if (classes.length) el.classList.add(...classes);
    Object.entries(attributes).forEach(([key, value]) => {
        el.setAttribute(key, value);
    });
    return el;
}

// =========================================
// Modais
// =========================================

function abrirModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('modal-transparente');
        modal.classList.add('active');
        modal.style.display = 'flex';
    }
}

function abrirModalTransparente(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.add('modal-transparente');
        modal.classList.add('active');
        modal.style.display = 'flex';
    }
}

function fecharModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.classList.remove('active');
        modal.classList.remove('modal-transparente');
        modal.style.display = 'none';
    }
}

// Fechar modal ao clicar fora
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        fecharModal(e.target.id);
    }
});

// =========================================
// Dados (Rolagem)
// =========================================

async function rolarDados(expressao) {
    const resultado = await API.post('/api/dados/rolar', { expressao });
    return resultado;
}

// =========================================
// Edição em tempo real
// =========================================

function setupEditaveisEmTempoReal(container, callback) {
    const editaveis = container.querySelectorAll('[contenteditable="true"]');
    
    editaveis.forEach(el => {
        el.addEventListener('blur', async () => {
            const campo = el.dataset.campo;
            const id = el.dataset.id || container.dataset.id;
            let valor = el.textContent.trim();
            
            // Tenta converter para número se parecer número
            if (/^-?\d+$/.test(valor)) {
                valor = parseInt(valor);
            }
            
            if (callback) {
                await callback(id, campo, valor);
            }
        });
        
        // Enter confirma edição
        el.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                el.blur();
            }
        });
    });
}

// =========================================
// Formatação
// =========================================

function formatarModificador(valor) {
    const mod = Math.floor((valor - 10) / 2);
    return mod >= 0 ? `+${mod}` : `${mod}`;
}

function formatarHP(atual, maximo) {
    const porcentagem = Math.round((atual / maximo) * 100);
    return { atual, maximo, porcentagem };
}

// =========================================
// Notificações
// =========================================

function notificar(mensagem, tipo = 'info') {
    // TODO: Implementar sistema de notificações toast
    console.log(`[${tipo.toUpperCase()}] ${mensagem}`);
}

// =========================================
// Teclas de atalho
// =========================================

document.addEventListener('keydown', (e) => {
    // Escape fecha modais
    if (e.key === 'Escape') {
        $$('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// =========================================
// Menu Mobile
// =========================================

function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        menu.classList.toggle('active');
    }
}

console.log('🎲 Out of the Abyss - Sistema carregado');
