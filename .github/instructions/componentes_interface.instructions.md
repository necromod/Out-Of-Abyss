---
applyTo: "**/*.html,**/*.css,**/*.js"
---

# Componentes de Interface

Documentação dos componentes visuais reutilizáveis.

---

## 1. Layout de Fichas

### Ficha de Personagem

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER: Nome do Personagem          [Classe Nv X]          │
├─────────────────────────────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐           │
│ │ FOR │ │ DES │ │ CON │ │ INT │ │ SAB │ │ CAR │ ATRIBUTOS │
│ │ +2  │ │ +3  │ │ +1  │ │ +0  │ │ +1  │ │ -1  │           │
│ │ 14  │ │ 16  │ │ 12  │ │ 10  │ │ 12  │ │  8  │           │
│ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘           │
├─────────────────────────────────────────────────────────────┤
│ HP: [████████░░] 25/30  CA: 16  Iniciativa: +3  Veloc: 9m  │
├───────────────────────┬─────────────────────────────────────┤
│ PERÍCIAS              │ ARMAS                               │
│ ☑ Acrobacia +5       │ Espada Longa    +5  1d8+2 cort.    │
│ ☐ Arcanismo +0       │ Arco Curto      +5  1d6+3 perf.    │
│ ☑ Atletismo +4       │ [+ Adicionar Arma]                  │
├───────────────────────┴─────────────────────────────────────┤
│ EQUIPAMENTOS          MOEDAS                                │
│ • Mochila            PC: 50  PP: 10  PO: 25                │
│ • Corda 15m          PE: 0   PL: 0                         │
└─────────────────────────────────────────────────────────────┘
```

### Ficha de Monstro (Compacta)

```
┌─────────────────────────────────────────────────────────────┐
│ [Nome do Monstro        ] PV:[27] CA:[14] ND:[2] Vel:[9m]  │
├─────────────────────────────────────────────────────────────┤
│ [Médio    ] [aberração    ] [neutro maligno] [(5d8+5)    ] │
├─────────────────────────────────────────────────────────────┤
│  FOR   DES   CON   INT   SAB   CAR                         │
│  +2    +1    +1    -4    +1    -3                          │
│ [14]  [12]  [13]  [ 3]  [12]  [ 5]                         │
├─────────────────────────────────────────────────────────────┤
│ [Características: Percepção às cegas 9m, Senso Sísmico...] │
├─────────────────────────────────────────────────────────────┤
│ AÇÕES                                                       │
│ [Mordida    ] [+4 ] [1d8+2 perf.  ] [×]                    │
│ [Garras     ] [+4 ] [2d4+2 cort.  ] [×]                    │
│ [+ Ação]                                                    │
├─────────────────────────────────────────────────────────────┤
│ [Habilidades especiais...]                                  │
├─────────────────────────────────────────────────────────────┤
│ [← Voltar]                              [💾 Salvar/✅ Criar]│
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes CSS

### Caixa de Atributo (Personagem)

```css
.atributo-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: var(--cor-superficie);
    border: 1px solid var(--cor-borda);
    border-radius: var(--border-radius);
    padding: var(--spacing-sm);
    min-width: 60px;
}

.atributo-box .sigla {
    font-size: 0.7rem;
    color: var(--cor-texto-secundario);
    text-transform: uppercase;
}

.atributo-box .modificador {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--cor-texto);
}

.atributo-box .valor {
    font-size: 0.9rem;
    color: var(--cor-texto-secundario);
}
```

### Caixa de Atributo (Monstro - Compacto)

```css
.attr-monstro-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(0,0,0,0.2);
    border-radius: 6px;
    padding: 0.4rem;
    min-width: 48px;
}

.attr-monstro-box .attr-sigla {
    font-size: 0.65rem;
    color: #888;
    margin-bottom: 2px;
}

.attr-monstro-box .attr-mod-grande {
    font-size: 1.1rem;
    font-weight: bold;
    color: #f0f0f0;
}

.attr-monstro-box .attr-valor-input {
    width: 32px;
    text-align: center;
    font-size: 0.75rem;
    background: rgba(255,255,255,0.1);
    border: 1px solid #444;
    color: #aaa;
    padding: 2px;
    border-radius: 3px;
}

/* Remove spinners */
.attr-valor-input::-webkit-outer-spin-button,
.attr-valor-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
```

### Barra de HP

```css
.hp-bar-container {
    width: 100%;
    height: 20px;
    background: #333;
    border-radius: 4px;
    overflow: hidden;
    position: relative;
}

.hp-bar {
    height: 100%;
    transition: width 0.3s ease, background-color 0.3s ease;
}

.hp-bar.hp-100 { background: var(--hp-100); }
.hp-bar.hp-75 { background: var(--hp-75); }
.hp-bar.hp-50 { background: var(--hp-50); }
.hp-bar.hp-25 { background: var(--hp-25); }

.hp-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.8rem;
    font-weight: bold;
    color: white;
    text-shadow: 1px 1px 2px black;
}
```

### Botões

```css
.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.2s, transform 0.1s;
}

.btn:hover {
    transform: translateY(-1px);
}

.btn:active {
    transform: translateY(0);
}

.btn-primario {
    background: var(--cor-primaria);
    color: white;
}

.btn-sucesso {
    background: var(--cor-sucesso);
    color: white;
}

.btn-perigo {
    background: var(--cor-perigo);
    color: white;
}

.btn-secundario {
    background: transparent;
    border: 1px solid var(--cor-borda);
    color: var(--cor-texto);
}
```

---

## 4. Cards Compactos de Listas

### Card de Personagem (Estilo Compacto)

**Arquivo**: `lista_personagens.html`  
**Classes**: `.card-personagem-compacto`, `.card-personagem-header`, `.card-stats-grid`, `.card-atributos`

```html
<div class="card-personagem-compacto hp-baixo">
    <div class="card-personagem-header">
        <h3 class="card-nome">Guerreiro</h3>
        <span class="card-nivel">Nv <span class="nivel-valor">5</span></span>
    </div>
    <p class="card-tipo-info">Humano Guerreiro</p>
    <p class="card-jogador-info">🎮 Jogador 1</p>
    
    <div class="card-stats-grid">
        <div class="stat-box"><span>HP</span><span>25/30</span></div>
        <div class="stat-box"><span>CA</span><span>16</span></div>
        <div class="stat-box"><span>PP</span><span>13</span></div>
    </div>
    
    <div class="card-atributos">
        <div class="attr-mini"><span>FOR</span><span>+3</span></div>
        <div class="attr-mini"><span>DES</span><span>+2</span></div>
        <div class="attr-mini"><span>CON</span><span>+1</span></div>
        <div class="attr-mini"><span>INT</span><span>+0</span></div>
        <div class="attr-mini"><span>SAB</span><span>+1</span></div>
        <div class="attr-mini"><span>CAR</span><span>-1</span></div>
    </div>
    
    <div class="card-acoes-lista">
        <div class="acoes-titulo">Ataques:</div>
        <div class="acao-mini"><strong>Espada Longa</strong>: +5 1d8+3</div>
    </div>
    
    <div class="card-botoes">
        <button class="btn-card-compacto btn-ver">👁️</button>
        <button class="btn-card-compacto btn-combate">⚔️</button>
        <button class="btn-card-compacto btn-widget">📌</button>
    </div>
</div>
```

**Características**:
- Header com nome + badge de nível
- Stats em grid 3 colunas (HP, CA, Percepção Passiva)
- Atributos em grid 6 colunas com modificadores calculados
- Lista de ataques (até 3)
- Alertas visuais: `.hp-critico` (<=25%), `.hp-baixo` (<=50%)

### Card de NPC (Estilo Compacto)

**Arquivo**: `lista_npcs.html`  
**Classes**: `.card-npc-compacto`, `.status-aliado`, `.status-hostil`, `.status-neutro`

```html
<div class="card-npc-compacto status-aliado">
    <div class="card-npc-header">
        <h3 class="card-nome">Mercador</h3>
        <span class="card-status-badge">💚</span>
    </div>
    <p class="card-tipo-info">Humano Comerciante</p>
    <p class="card-local-info">📍 Neverwinter</p>
    
    <div class="card-descricao-box">
        <p class="card-descricao-texto">Um mercador amigável...</p>
    </div>
    
    <div class="card-relacionamento">
        <div class="rel-mini">👥 Conhecido dos jogadores</div>
    </div>
    
    <div class="card-tags-inline">
        <span class="tag tag-morto" style="display: none;">💀 Morto</span>
        <span class="tag tag-desconhecido" style="display: none;">❓ Desconhecido</span>
    </div>
    
    <div class="card-botoes">
        <button class="btn-card-compacto btn-ver">👁️</button>
        <button class="btn-card-compacto btn-notas">📝</button>
        <button class="btn-card-compacto btn-widget">📌</button>
    </div>
</div>
```

**Características**:
- Header com nome + badge de status (emoji)
- Borda colorida à esquerda indica status (verde/vermelho/amarelo)
- Box de descrição com excerpt (120 chars)
- Relacionamento com jogadores
- Tags: Morto, Desconhecido (quando aplicável)
- NPCs mortos: opacity reduzida + grayscale

### Card de Monstro (Estilo Compacto)

**Arquivo**: `lista_monstros.html`  
**Classes**: `.card-monstro-compacto`, `.nd-lendario`, `.nd-muito-alto`, `.nd-alto`, `.nd-medio`

```html
<div class="card-monstro-compacto nd-medio">
    <div class="card-monstro-header">
        <h3 class="card-nome">Goblin</h3>
        <span class="card-nd">ND 1/4</span>
    </div>
    <p class="card-tipo-info">Pequeno humanoide (goblinoide)</p>
    
    <div class="card-stats-grid">
        <div class="stat-box"><span>CA</span><span>15</span></div>
        <div class="stat-box"><span>HP</span><span>7</span></div>
        <div class="stat-box"><span>XP</span><span>50</span></div>
    </div>
    
    <div class="card-atributos">
        <div class="attr-mini"><span>FOR</span><span>-1</span></div>
        <div class="attr-mini"><span>DES</span><span>+2</span></div>
        <div class="attr-mini"><span>CON</span><span>+0</span></div>
        <div class="attr-mini"><span>INT</span><span>+0</span></div>
        <div class="attr-mini"><span>SAB</span><span>-1</span></div>
        <div class="attr-mini"><span>CAR</span><span>-1</span></div>
    </div>
    
    <div class="card-acoes-lista">
        <div class="acoes-titulo">Ações:</div>
        <div class="acao-mini"><strong>Cimitarra</strong>: +4 1d6+2 cortante</div>
    </div>
    
    <div class="card-botoes">
        <button class="btn-card-compacto btn-ver">👁️</button>
        <button class="btn-card-compacto btn-instanciar">🎭</button>
        <button class="btn-card-compacto btn-widget">📌</button>
    </div>
</div>
```

**Características**:
- Cores de borda por ND: Lendário (roxo), Muito Alto (vermelho), Alto (laranja), Médio (amarelo)
- Grid de atributos 6 colunas
- Grid de stats 3 colunas (CA, HP, XP)
- Lista de ações

---

## 5. Modal

```css
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    z-index: 1000;
    justify-content: center;
    align-items: center;
}

.modal.ativo {
    display: flex;
}

.modal-content {
    background: var(--cor-superficie);
    border: 1px solid var(--cor-borda);
    border-radius: var(--border-radius);
    padding: var(--spacing-lg);
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-md);
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--cor-texto-secundario);
}

.modal-buttons {
    display: flex;
    gap: var(--spacing-sm);
    justify-content: flex-end;
    margin-top: var(--spacing-md);
}
```

### Notificação

```css
.notificacoes {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 2000;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.notificacao {
    padding: 12px 20px;
    border-radius: var(--border-radius);
    color: white;
    font-weight: 500;
    animation: slideIn 0.3s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.notificacao-success { background: var(--cor-sucesso); }
.notificacao-danger { background: var(--cor-perigo); }
.notificacao-warning { background: var(--cor-aviso); }
.notificacao-info { background: #2196f3; }

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
```

### Textarea Auto-Expand

```css
.auto-expand {
    width: 100%;
    min-height: 40px;
    resize: none;
    overflow: hidden;
    background: rgba(255,255,255,0.05);
    border: 1px solid #444;
    color: #ddd;
    padding: 0.5rem;
    border-radius: 4px;
    font-family: inherit;
    font-size: 0.85rem;
    line-height: 1.4;
}

.auto-expand:focus {
    outline: none;
    border-color: var(--cor-primaria);
}
```

---

## 3. Componentes JavaScript

### Auto-Expand Textarea

```javascript
document.querySelectorAll('.auto-expand').forEach(textarea => {
    const autoExpand = () => {
        textarea.style.height = 'auto';
        textarea.style.height = Math.max(40, textarea.scrollHeight) + 'px';
    };
    autoExpand();
    textarea.addEventListener('input', autoExpand);
});
```

### Atualizar Modificador de Atributo

```javascript
document.querySelectorAll('.attr-valor-input').forEach(input => {
    input.addEventListener('input', function() {
        const valor = parseInt(this.value) || 10;
        const mod = Math.floor((valor - 10) / 2);
        const attrName = this.dataset.campo.replace('atributos.', '');
        const modSpan = document.querySelector(`[data-mod="${attrName}"]`);
        if (modSpan) {
            modSpan.textContent = (mod >= 0 ? '+' : '') + mod;
        }
    });
});
```

### Atualizar Barra de HP

```javascript
function atualizarBarraHP(hpAtual, hpMax) {
    const bar = document.querySelector('.hp-bar');
    const text = document.querySelector('.hp-text');
    
    const porcentagem = Math.max(0, Math.min(100, (hpAtual / hpMax) * 100));
    bar.style.width = porcentagem + '%';
    
    // Remove classes antigas
    bar.classList.remove('hp-100', 'hp-75', 'hp-50', 'hp-25');
    
    // Adiciona classe apropriada
    if (porcentagem > 75) bar.classList.add('hp-100');
    else if (porcentagem > 50) bar.classList.add('hp-75');
    else if (porcentagem > 25) bar.classList.add('hp-50');
    else bar.classList.add('hp-25');
    
    if (text) text.textContent = `${hpAtual}/${hpMax}`;
}
```

### Adicionar/Remover Item Dinâmico

```javascript
// Adicionar arma (formato novo)
function adicionarAtaque() {
    const container = document.getElementById('lista-armas');
    const index = container.querySelectorAll('.arma-item').length;
    
    const novaArma = document.createElement('div');
    novaArma.className = 'arma-item';
    novaArma.innerHTML = `
        <input type="text" data-campo="armas.${index}.nome" placeholder="Nome">
        <input type="text" data-campo="armas.${index}.bonus" placeholder="+0">
        <div class="dados-dano-container">
            <input class="dado-dano-input" placeholder="1d6+2">
            <button type="button" class="btn-add-dado" onclick="adicionarDadoDano(this)">+</button>
        </div>
        <select data-campo="armas.${index}.tipo">
            <option value="">—</option>
            <option value="Ácido" title="Dissolve matéria orgânica">Ácido</option>
            <option value="Contundente" title="Impacto, esmagamento">Contundente</option>
            <option value="Cortante" title="Lâminas, corte">Cortante</option>
            <option value="Elétrico" title="Raios, eletricidade">Elétrico</option>
            <option value="Energético" title="Energia pura, força">Energético</option>
            <option value="Gélido" title="Frio intenso, congelamento">Gélido</option>
            <option value="Ígneo" title="Fogo, calor intenso">Ígneo</option>
            <option value="Necrótico" title="Energia negativa, morte">Necrótico</option>
            <option value="Perfurante" title="Pontas, flechas, espinhos">Perfurante</option>
            <option value="Psíquico" title="Dano mental, ilusões">Psíquico</option>
            <option value="Radiante" title="Luz divina, energia positiva">Radiante</option>
            <option value="Trovejante" title="Som, ondas de choque">Trovejante</option>
            <option value="Venenoso" title="Toxinas, venenos">Venenoso</option>
        </select>
        <button type="button" class="btn-remover" onclick="removerAtaque(this)">×</button>
    `;
    container.appendChild(novaArma);
}

// Adicionar dado de dano extra (para múltiplos tipos)
function adicionarDadoDano(btn) {
    const container = btn.closest('.dados-dano-container');
    const novoInput = document.createElement('input');
    novoInput.className = 'dado-dano-input';
    novoInput.placeholder = '1d6';
    container.insertBefore(novoInput, btn);
}

// Remover arma
function removerAtaque(btn) {
    btn.closest('.arma-item').remove();
}
```

### CSS de Armas (Formato Novo)

```css
.arma-item {
    display: grid;
    grid-template-columns: 2fr 60px 1fr 100px 30px;
    gap: var(--spacing-xs);
    align-items: center;
    padding: var(--spacing-xs);
    background: rgba(0,0,0,0.2);
    border-radius: var(--radius-sm);
    margin-bottom: var(--spacing-xs);
}

.dados-dano-container {
    display: flex;
    gap: 2px;
    flex-wrap: wrap;
}

.dado-dano-input {
    width: 60px;
    text-align: center;
}

.btn-add-dado {
    width: 20px;
    height: 20px;
    padding: 0;
    font-size: 0.8rem;
}
```

### Notificações

```javascript
function mostrarNotificacao(mensagem, tipo = 'info') {
    let container = document.getElementById('notificacoes');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notificacoes';
        container.className = 'notificacoes';
        document.body.appendChild(container);
    }
    
    const notif = document.createElement('div');
    notif.className = `notificacao notificacao-${tipo}`;
    notif.textContent = mensagem;
    container.appendChild(notif);
    
    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}
```

---

## 4. Templates Jinja2

### Base de Atributos (Personagem)

```html
{% set attrs = p.atributos if p and p.atributos else {} %}
<div class="atributos-row">
    {% for attr, sigla in [('forca', 'FOR'), ('destreza', 'DES'), ('constituicao', 'CON'), 
                           ('inteligencia', 'INT'), ('sabedoria', 'SAB'), ('carisma', 'CAR')] %}
    {% set valor = attrs.get(attr, 10) if attrs is mapping else 10 %}
    {% set mod = ((valor - 10) // 2) %}
    <div class="atributo-box">
        <span class="sigla">{{ sigla }}</span>
        <span class="modificador">{{ '+' if mod >= 0 else '' }}{{ mod }}</span>
        <input type="number" class="valor" data-campo="atributos.{{ attr }}" 
               value="{{ valor }}" min="1" max="30">
    </div>
    {% endfor %}
</div>
```

### Lista de Armas (Formato Novo)

```html
<div id="lista-armas">
    {% if p and p.armas %}
        {% for arma in p.armas %}
        <div class="arma-item">
            <input type="text" data-campo="armas.{{ loop.index0 }}.nome" 
                   value="{{ arma.nome }}" placeholder="Nome">
            <input type="text" data-campo="armas.{{ loop.index0 }}.bonus" 
                   value="{{ arma.bonus or arma.ataque }}" placeholder="+0">
            <div class="dados-dano-container">
                {% if arma.dados %}
                    {% for dado in arma.dados %}
                    <input class="dado-dano-input" value="{{ dado }}" placeholder="1d6">
                    {% endfor %}
                {% else %}
                    <input class="dado-dano-input" value="{{ arma.dano }}" placeholder="1d6">
                {% endif %}
                <button type="button" class="btn-add-dado" onclick="adicionarDadoDano(this)">+</button>
            </div>
            <select data-campo="armas.{{ loop.index0 }}.tipo">
                <option value="">—</option>
                {% for tipo in ['Ácido', 'Contundente', 'Cortante', 'Elétrico', 'Energético', 
                                'Gélido', 'Ígneo', 'Necrótico', 'Perfurante', 'Psíquico', 
                                'Radiante', 'Trovejante', 'Venenoso'] %}
                <option value="{{ tipo }}" {{ 'selected' if arma.tipo == tipo }}>{{ tipo }}</option>
                {% endfor %}
            </select>
            <button type="button" onclick="removerAtaque(this)">×</button>
        </div>
        {% endfor %}
    {% endif %}
</div>
<button type="button" onclick="adicionarAtaque()">+ Ataque</button>
```

### Checkboxes de Perícias

```html
{% set pericias_prof = p.pericias_proficientes if p else [] %}
{% for pericia, attr in [('acrobacia', 'DES'), ('arcanismo', 'INT'), ('atletismo', 'FOR')] %}
<label class="pericia-item">
    <input type="checkbox" 
           data-campo="pericias_proficientes" 
           data-valor="{{ pericia }}"
           {{ 'checked' if pericia in pericias_prof else '' }}>
    <span class="pericia-nome">{{ pericia|title }}</span>
    <span class="pericia-attr">({{ attr }})</span>
</label>
{% endfor %}
```

### Moedas

```html
{% set moedas = p.moedas if p and p.moedas else {} %}
<div class="moedas-row">
    {% for tipo, nome in [('pc', 'PC'), ('pp', 'PP'), ('pe', 'PE'), ('po', 'PO'), ('pl', 'PL')] %}
    <div class="moeda-item">
        <label>{{ nome }}</label>
        <input type="number" data-campo="moedas.{{ tipo }}" 
               value="{{ moedas.get(tipo, 0) if moedas is mapping else 0 }}" min="0">
    </div>
    {% endfor %}
</div>
```
