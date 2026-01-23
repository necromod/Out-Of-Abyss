---
applyTo: "**/widgets.js,**/sessao.js,**/sessao.css,**/widgets.css,**/sessao/**"
---

# Sistema de Widgets e Sessão

Documentação do sistema de widgets flutuantes e tela de sessão para mestragem em tempo real.

---

## 1. Visão Geral

O sistema de sessão é a interface principal de mestragem, com:
- **Widgets flutuantes**: Blocos arrastáveis, redimensionáveis e minimizáveis
- **Iniciativa e combate**: Ordem de turnos, contador de rounds, controle de turno
- **Fichas rápidas**: Widgets de personagens e monstros com dano/cura rápida
- **Log de combate**: Registro de ações durante o combate
- **Efeitos/Condições**: Sistema completo de condições D&D 5e com contador de turnos

---

## 2. Arquivos do Sistema

| Arquivo | Descrição |
|---------|-----------|
| `app/static/js/widgets.js` | Classe Widget e WidgetManager |
| `app/static/js/sessao.js` | Lógica de sessão, combate, efeitos |
| `app/static/css/widgets.css` | Estilos dos widgets |
| `app/static/css/sessao.css` | Estilos da tela de sessão |
| `templates/sessao/index.html` | Template da tela de sessão |

---

## 3. Classe Widget (widgets.js)

### Estrutura

```javascript
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
        this.conteudo = options.conteudo || '';
    }
}
```

### Tipos de Widget

| Tipo | Descrição | Controles Extras |
|------|-----------|------------------|
| `generico` | Widget básico | - |
| `ficha_personagem` | Ficha de PC | ⏱️ Turnos, 📋 Ficha |
| `ficha_monstro` | Ficha de monstro | ⏱️ Turnos, 📋 Ficha |
| `iniciativa` | Ordem de combate | - |
| `log` | Log de combate | - |

### Funcionalidades

- **Arrastar**: Clicar e segurar no header
- **Redimensionar**: Canto inferior direito (resize handle)
- **Minimizar**: Botão − no header
- **Fechar**: Botão × no header OU **middle-click no header**
- **Trazer para frente**: Clicar no widget

### Dados Armazenados no Widget

```javascript
// Para widgets de ficha, dados são salvos em:
widget.element.dataset.criaturaId   // ID da criatura
widget.element.dataset.criaturaTipo // 'personagem' ou 'instancia'
widget.element.dataset.modDestreza  // Modificador de DES para iniciativa
```

---

## 4. Estado da Sessão (sessao.js)

### SessaoState

```javascript
const SessaoState = {
    mapaAtual: null,
    combateAtivo: false,
    widgets: [],
    logCombate: [],
    ordemTurnos: [],   // Lista de participantes: [{tipo, id, nome, iniciativa, modDestreza}]
    turnoAtual: 0,     // Índice do turno atual
    contadorMonstros: {}, // Contador por tipo: { 'Goblin': 2 }
    roundAtual: 0      // Contador de rounds (1+ durante combate, 0 fora)
};
```

### Estrutura de Participante nos Turnos

```javascript
{
    tipo: 'personagem' | 'instancia',
    id: number,
    nome: string,
    iniciativa: number,   // Valor final (1d20 + mod)
    modDestreza: number,  // Modificador de DES
    efeitos: [            // Efeitos ativos
        { nome: 'envenenado', turnos: 3 }
    ]
}
```

---

## 5. Sistema de Condições D&D 5e

### Constante CONDICOES_DND

```javascript
const CONDICOES_DND = {
    // Condições D&D 5e
    'agarrado': { nome: 'Agarrado', descricao: '...' },
    'amedrontado': { nome: 'Amedrontado', descricao: '...' },
    'atordoado': { nome: 'Atordoado', descricao: '...' },
    'caido': { nome: 'Caído', descricao: '...' },
    'cego': { nome: 'Cego', descricao: '...' },
    'enfeiticado': { nome: 'Enfeitiçado', descricao: '...' },
    'envenenado': { nome: 'Envenenado', descricao: '...' },
    'impedido': { nome: 'Impedido', descricao: '...' },
    'incapacitado': { nome: 'Incapacitado', descricao: '...' },
    'inconsciente': { nome: 'Inconsciente', descricao: '...' },
    'invisivel': { nome: 'Invisível', descricao: '...' },
    'paralisado': { nome: 'Paralisado', descricao: '...' },
    'petrificado': { nome: 'Petrificado', descricao: '...' },
    'surdo': { nome: 'Surdo', descricao: '...' },
    'exaustao': { nome: 'Exaustão', descricao: '...' },
    
    // Tipos de Dano (para resistências/vulnerabilidades)
    'dano_acido': { nome: 'Dano Ácido', descricao: '...' },
    'dano_contundente': { nome: 'Dano Contundente', descricao: '...' },
    'dano_cortante': { nome: 'Dano Cortante', descricao: '...' },
    'dano_eletrico': { nome: 'Dano Elétrico', descricao: '...' },
    'dano_energetico': { nome: 'Dano Energético', descricao: '...' },
    'dano_gelido': { nome: 'Dano Gélido', descricao: '...' },
    'dano_igneo': { nome: 'Dano Ígneo', descricao: '...' },
    'dano_necrotico': { nome: 'Dano Necrótico', descricao: '...' },
    'dano_perfurante': { nome: 'Dano Perfurante', descricao: '...' },
    'dano_psiquico': { nome: 'Dano Psíquico', descricao: '...' },
    'dano_radiante': { nome: 'Dano Radiante', descricao: '...' },
    'dano_trovejante': { nome: 'Dano Trovejante', descricao: '...' },
    'dano_venenoso': { nome: 'Dano Venenoso', descricao: '...' }
};
```

### Funções de Efeitos

```javascript
// Abrir modal para adicionar efeito
// O modal é criado dinamicamente com style="display: flex;"
abrirModalEfeito(event, tipo, id)

// Adicionar efeito a uma criatura
// Cria elemento visual em .efeitos-lista
adicionarEfeito(tipo, id)

// Remover efeito de uma criatura
removerEfeito(btn)  // Recebe o botão clicado

// Atualizar contadores de turno (chamado automaticamente em proximoTurno)
// Decrementa turnos de todos os efeitos, remove os que expiraram
atualizarContadoresEfeitos()
```

### Estrutura HTML do Efeito

```html
<div class="efeito-item" data-condicao="envenenado" data-turnos="3">
    <span class="efeito-nome" title="Descrição da condição">Envenenado</span>
    <span class="efeito-turnos">3</span>
    <button class="btn-mini btn-remover" onclick="removerEfeito(this)">✕</button>
</div>
```

---

## 6. Sistema de Combate

### Fluxo de Combate

```
1. iniciarCombate()
   └── SessaoState.combateAtivo = true
   └── SessaoState.roundAtual = 1
   └── ordena ordemTurnos por iniciativa

2. proximoTurno()
   └── turnoAtual++
   └── Se completou ciclo:
       └── roundAtual++
       └── atualizarContadoresEfeitos()
   └── atualizarWidgetIniciativa()

3. finalizarCombate()
   └── combateAtivo = false
   └── roundAtual = 0
   └── limpa ordemTurnos
```

### Iniciativa

```javascript
// Adicionar criatura aos turnos (rola 1d20 + modDestreza)
adicionarAosTurnos(tipo, id, nome, iniciativa, modDestreza)

// Editar iniciativa manualmente (clicando no valor)
editarIniciativa(event, index)

// O valor de iniciativa é contenteditable no widget
```

---

## 7. Sistema de Ataques

### Estrutura de Armas no Widget

Os botões de ataque são gerados automaticamente a partir do array `armas`:

```javascript
// Formato novo de armas (recomendado)
{
    nome: "Espada Longa",
    bonus: "+5",
    dados: ["1d8+3"],      // Array de dados de dano
    tipo: "Cortante"       // Tipo de dano
}

// Formato legado (ainda suportado)
{
    nome: "Espada Longa",
    ataque: "+5",
    dano: "1d8+3 cort."    // String com tipo embutido
}
```

### Função rolarAtaque()

```javascript
/**
 * Rola um ataque com d20 + bônus e mostra resultado no log
 * @param {Event} event - Evento do clique
 * @param {string} nomeAtacante - Nome de quem ataca
 * @param {string} nomeAtaque - Nome da arma/ataque
 * @param {string} bonusAtaque - Bônus de acerto (ex: "+5")
 * @param {string[]|string} dados - Array de dados de dano ou string única
 * @param {string} tipoDano - Tipo de dano (ex: "Cortante", "Ígneo")
 */
async function rolarAtaque(event, nomeAtacante, nomeAtaque, bonusAtaque, dados, tipoDano = '')

// Fluxo:
// 1. Rola 1d20 + bonus
// 2. Verifica crítico (20) ou falha crítica (1)
// 3. Se não for falha crítica, rola dano (dobrado em crítico)
// 4. Adiciona ao log de combate
```

### Detecção de Formato de Armas

```javascript
// Detecta se é formato novo ou legado
const isFormatoNovo = a.dados !== undefined;

if (isFormatoNovo) {
    // Usa a.bonus e a.dados[]
    const dadosStr = JSON.stringify(a.dados);
    const tipo = a.tipo || '';
} else {
    // Usa a.ataque e a.dano (extrai tipo do texto)
    const bonus = a.ataque || a.bonus;
    const danoMatch = a.dano.match(/^([^a-zA-Z]+)/);
}
```

---

## 8. Log de Combate

### Formato das Mensagens

```javascript
// Ataque normal
"Azazel Ireth usa Raio de fogo 15 (8+7)"
"8 dano ígneo (1d10)"

// Crítico (🎯)
"Azazel Ireth usa Raio de fogo 26 🎯 (20+6)"
"17 dano ígneo (2d10)"  // Dados dobrados

// Falha Crítica (💀)
"Azazel Ireth usa Raio de fogo 7 💀 (1+6)"
// Sem linha de dano
```

### Estrutura do Log Item

```html
<div class="log-item log-ataque" data-time="16:09">
    <span class="log-msg">
        <strong>Azazel Ireth</strong> usa <em>Raio de fogo</em> 
        <span class="ataque-total">15</span> 
        <span class="ataque-detalhes">(8+7)</span>
        <br>
        <span class="dano-linha">
            <span class="dano">8</span> dano
            <span class="tipo-dano" data-tipo="Ígneo">ígneo</span>
            <span class="dano-expressao">(1d10)</span>
        </span>
    </span>
</div>
```

### Tooltip de Horário

O horário aparece apenas no hover, usando CSS puro (sem delay):

```css
.log-item[data-time]::after {
    content: attr(data-time);
    position: absolute;
    right: var(--spacing-sm);
    opacity: 0;
}

.log-item[data-time]:hover::after {
    opacity: 1;
}
```

### Tipos de Log

| Tipo | Uso | Cor da Borda |
|------|-----|--------------|
| `info` | Mensagens gerais | Azul primário |
| `ataque` | Ataques normais | Amarelo/warning |
| `crit` | Críticos | Roxo |
| `fumble` | Falhas críticas | Cinza escuro |
| `dano` | Dano aplicado | Vermelho |
| `cura` | Cura/efeito expirado | Verde |
| `erro` | Erros | Vermelho escuro |

---

## 9. Widgets de Ficha

### Estrutura HTML do Widget de Personagem

```html
<div class="widget-personagem-conteudo">
    <div class="personagem-widget-header">...</div>
    <div class="personagem-widget-hp">...</div>
    
    <!-- Stats com Percepção Passiva -->
    <div class="personagem-widget-stats">
        CA: 15 | +3 | 9m | 👁10
    </div>
    
    <div class="personagem-widget-attrs">...</div>
    
    <!-- Ações/Ataques -->
    <div class="personagem-widget-acoes">
        <button onclick="rolarAtaque(...)">Espada +5</button>
    </div>
    
    <!-- Dano/Cura -->
    <div class="personagem-widget-botoes">
        <button onclick="abrirDanoRapido(...)">⚔️ Dano</button>
        <button onclick="abrirCuraRapida(...)">💚 Cura</button>
    </div>
    
    <!-- Notas -->
    <div class="personagem-widget-notas">
        <textarea class="notas-rapidas" data-personagem-id="..."></textarea>
    </div>
    
    <!-- Testes de Morte (só aparece se HP <= 0) -->
    <div class="testes-morte" data-criatura-tipo="personagem" data-criatura-id="...">
        ...
    </div>
    
    <!-- Efeitos/Condições -->
    <div class="widget-efeitos" data-criatura-tipo="personagem" data-criatura-id="...">
        <div class="efeitos-lista"></div>
        <button onclick="abrirModalEfeito(...)">+ Efeito</button>
    </div>
</div>
```

### Dano/Cura Rápido

```javascript
// Abre input flutuante para dano
abrirDanoRapido(event, id, nome, tipo)

// Abre input flutuante para cura
abrirCuraRapida(event, id, nome, tipo)

// APIs chamadas:
// POST /api/personagens/{id}/dano  { dano: number }
// POST /api/personagens/{id}/curar { quantidade: number }
// POST /api/monstros/instancias/{id}/dano  { dano: number }
// POST /api/monstros/instancias/{id}/curar { quantidade: number }
```

### Atualização de Widget Após Dano/Cura

```javascript
// Atualiza barra de HP e testes de morte dinamicamente
atualizarWidgetCriatura(tipo, id, dadosAtualizados)

// Se HP <= 0: adiciona seção testes-morte
// Se HP > 0: remove seção testes-morte
```

---

## 8. Testes de Morte

### Exibição Automática

- Aparece automaticamente quando `hp_atual <= 0`
- Desaparece automaticamente quando `hp_atual > 0`
- Ao curar, os valores são resetados (sucesso_morte=0, falha_morte=0)

### Campos no Banco

```sql
-- Tabela personagens
sucesso_morte INTEGER DEFAULT 0,  -- 0-3 sucessos
falha_morte INTEGER DEFAULT 0     -- 0-3 falhas
```

### API

```javascript
// Marcar teste de morte
marcarTesteMorte(event, id, tipo, valor)
// PATCH /fichas/api/personagem/{id} { sucesso_morte: N } ou { falha_morte: N }
```

---

## 9. Widget de Iniciativa

### Estrutura

```html
<div class="iniciativa-header">
    <div class="iniciativa-round">
        <span class="round-label">Round</span>
        <span class="round-valor">1</span>
    </div>
</div>
<div class="iniciativa-lista">
    <!-- Participantes ordenados por iniciativa -->
    <div class="iniciativa-item ativo">
        <span class="iniciativa-ordem" contenteditable="true" 
              onblur="editarIniciativa(event, 0)">15</span>
        <span class="iniciativa-nome">Guerreiro</span>
        <button onclick="removerDosTurnos(0)">×</button>
    </div>
</div>
<div class="iniciativa-controles">
    <button onclick="iniciarCombate()">▶️ Iniciar</button>
    <button onclick="proximoTurno()">⏭️ Próximo</button>
    <button onclick="finalizarCombate()">⏹️ Finalizar</button>
</div>
```

---

## 10. CSS - Classes Importantes

### Widgets

```css
.widget { } /* Container principal */
.widget-header { } /* Barra de título */
.widget-body { } /* Conteúdo */
.widget-controls { } /* Botões do header */
.widget[data-tipo="iniciativa"] .widget-body { display: flex; flex-direction: column; }
.widget[data-tipo="log"] .widget-body { display: flex; flex-direction: column; }
```

### Iniciativa

```css
.iniciativa-round { }
.round-valor { }
.iniciativa-lista { flex: 1; overflow-y: auto; }
.iniciativa-item { }
.iniciativa-item.ativo { } /* Turno atual */
.iniciativa-ordem { cursor: text; } /* Editável */
.iniciativa-controles { flex-shrink: 0; }
```

### Efeitos

```css
.widget-efeitos { }
.efeitos-lista { }
.efeito-item { }
.efeito-nome { }
.efeito-turnos { }
.btn-outline { } /* Botão + Efeito */
```

### Testes de Morte

```css
.testes-morte { }
.teste-linha { }
.teste-label { }
.teste-check { }
.teste-check.marcado { }
```

---

## 11. Integrações Críticas

### Manter Sincronizados

1. **IDs de criatura**: `data-criatura-id` e `data-personagem-id` / `data-monstro-id`
2. **Tipos de criatura**: `'personagem'` vs `'instancia'` (não 'monstro')
3. **Seletores CSS**: Classes como `.widget-personagem-conteudo` devem existir no HTML
4. **APIs de dano/cura**: Retornam objeto completo com `hp_atual`, `hp_maximo`, `sucesso_morte`, `falha_morte`

### Ao Modificar Fichas

- Verificar se seletores CSS ainda funcionam no sessao.js
- Verificar se `data-campo` atributos existem para coleta de dados
- Verificar se APIs retornam todos os campos necessários
- Testar dano/cura e testes de morte na tela de sessão

---

## 12. Ordem de Seções no Widget de Ficha

Ordem fixa para manter consistência:

1. Header (nome, classe, nível)
2. HP (barra de vida)
3. Stats (CA, Iniciativa, Velocidade)
4. Atributos (FOR, DES, CON, INT, SAB, CAR)
5. **Botões de Dano/Cura**
6. **Notas Rápidas**
7. **Testes de Morte** (condicional: HP <= 0)
8. **Efeitos/Condições**

---

## 13. Checklist para Novas Funcionalidades

- [ ] Adicionar estilos em `sessao.css` ou `widgets.css`
- [ ] Implementar lógica em `sessao.js`
- [ ] Verificar compatibilidade com `atualizarWidgetCriatura()`
- [ ] Testar iniciativa (adicionar, editar, ordenar)
- [ ] Testar dano/cura (verificar testes de morte)
- [ ] Testar efeitos (adicionar, remover, countdown)
- [ ] Verificar middle-click fecha widget
