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
| `ficha_npc` | Ficha de NPC | ⏱️ Turnos, 📋 Ficha |
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
    mapaAtual: null,           // Caminho do cenário atual (relativo a Imagens/)
    combateAtivo: false,
    widgets: [],
    logCombate: [],
    ordemTurnos: [],          // Lista de participantes: [{tipo, id, nome, iniciativa, modDestreza}]
    turnoAtual: 0,            // Índice do turno atual (0 a length-1)
    contadorMonstros: {},     // Contador por tipo: { 'Goblin': 2 }
    turnoContador: 0          // Contador de turnos (0 = fora de combate, 1+ = em combate)
};
```

**⚠️ IMPORTANTE - Cenários**:
- `mapaAtual` armazena caminho relativo à pasta `Imagens/` (ex: `Cenários/mapa.png`)
- APIs `/sessao/api/cenarios` retornam caminhos já relativos a `Imagens/`
- URL final: `/sessao/imagens/{mapaAtual}` (ex: `/sessao/imagens/Cenários/mapa.png`)
- Função `restaurarEstado()` usa `aplicarCenario()` para carregar imagem

**⚠️ IMPORTANTE - Turnos**:
- `proximoTurno()` funciona com 0, 1 ou múltiplos participantes
- Com 0 participantes: apenas incrementa `turnoContador`
- Com 1 participante: sempre no índice 0, incrementa `turnoContador` a cada clique
- Com 2+ participantes: usa módulo `%` para circular, incrementa ao voltar ao início

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

## 5. Sistema de Testes e Perícias

### Atributos Clicáveis

Os atributos nos widgets de personagem e monstro são **clicáveis** e abrem automaticamente o submenu de perícias:

```html
<span class="attr-clicavel" 
      title="Clique para rolar FOR" 
      onclick="abrirSubmenuPericias(event, id, tipo, 'forca', valor, proficientes, expertise, bonusProf)">
    FOR +3
</span>
```

**Comportamento:**
- Clique direto no atributo (FOR, DES, CON, INT, SAB, CAR)
- Abre submenu ao lado direito com perícias daquele atributo
- Primeiro item: Teste puro do atributo (ex: "Força (puro)")
- Demais itens: Perícias relacionadas

### Mapeamento de Perícias (PERICIAS_POR_ATRIBUTO)

```javascript
const PERICIAS_POR_ATRIBUTO = {
    forca: [
        { id: 'forca', nome: 'Força (puro)', isPuro: true },
        { id: 'atletismo', nome: 'Atletismo' }
    ],
    destreza: [
        { id: 'destreza', nome: 'Destreza (puro)', isPuro: true },
        { id: 'acrobacia', nome: 'Acrobacia' },
        { id: 'furtividade', nome: 'Furtividade' },
        { id: 'prestidigitacao', nome: 'Prestidigitação' }
    ],
    constituicao: [
        { id: 'constituicao', nome: 'Constituição (puro)', isPuro: true }
    ],
    inteligencia: [
        { id: 'inteligencia', nome: 'Inteligência (puro)', isPuro: true },
        { id: 'arcanismo', nome: 'Arcanismo' },
        { id: 'historia', nome: 'História' },
        { id: 'investigacao', nome: 'Investigação' },
        { id: 'natureza', nome: 'Natureza' },
        { id: 'religiao', nome: 'Religião' }
    ],
    sabedoria: [
        { id: 'sabedoria', nome: 'Sabedoria (puro)', isPuro: true },
        { id: 'adestrar_animais', nome: 'Adestrar Animais' },
        { id: 'intuicao', nome: 'Intuição' },
        { id: 'medicina', nome: 'Medicina' },
        { id: 'percepcao', nome: 'Percepção' },
        { id: 'sobrevivencia', nome: 'Sobrevivência' }
    ],
    carisma: [
        { id: 'carisma', nome: 'Carisma (puro)', isPuro: true },
        { id: 'atuacao', nome: 'Atuação' },
        { id: 'enganacao', nome: 'Enganação' },
        { id: 'intimidacao', nome: 'Intimidação' },
        { id: 'persuasao', nome: 'Persuasão' }
    ]
};
```

### Funções de Teste

```javascript
// Abre submenu de perícias ao clicar no atributo
abrirSubmenuPericias(event, id, tipo, atributo, valorAtributo, proficientes, expertise, bonusProf)

// Rola 1d20 + modificador da perícia
rolarTeste(event, id, tipo, testeId, testeNome, bonus)
```

### Cálculo de Bônus

```javascript
// Teste puro: apenas modificador do atributo
bonus = modAtributo

// Perícia proficiente: mod + bonus proficiência
if (proficientes.includes(pericia.id)) {
    bonus = modAtributo + bonusProf;
    marcador = '✓ ';
}

// Perícia com expertise: mod + (bonus proficiência × 2)
if (expertise.includes(pericia.id)) {
    bonus = modAtributo + (bonusProf * 2);
    marcador = '⭐ ';
}
```

### Resultado da Rolagem

```javascript
// d20 === 20: Crítico (🎯)
// d20 === 1: Falha Crítica (💀)
// Outros: Rolagem normal (🎲)

// Adiciona ao log de combate formatado:
"🎲 Percepção: 1d20(15) + 5 = 20"
```

---

## 6. Sistema de Condições D&D 5e

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
    'dano_acido': { nome: '🧪 Ácido', descricao: '...' },
    'dano_contundente': { nome: '🔨 Contundente', descricao: '...' },
    'dano_cortante': { nome: '⚔️ Cortante', descricao: '...' },
    'dano_eletrico': { nome: '⚡ Elétrico', descricao: '...' },
    'dano_energetico': { nome: '✨ Energético', descricao: '...' },
    'dano_gelido': { nome: '❄️ Gélido', descricao: '...' },
    'dano_igneo': { nome: '🔥 Ígneo', descricao: '...' },
    'dano_necrotico': { nome: '💀 Necrótico', descricao: '...' },
    'dano_perfurante': { nome: '🗡️ Perfurante', descricao: '...' },
    'dano_psiquico': { nome: '🧠 Psíquico', descricao: '...' },
    'dano_radiante': { nome: '✨ Radiante', descricao: '...' },
    'dano_trovejante': { nome: '🌩️ Trovejante', descricao: '...' },
    'dano_venenoso': { nome: '☠️ Venenoso', descricao: '...' }
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

## 7. Sistema de Combate

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

## 10. Persistência de Widgets

### Sistema de Salvamento

O estado da sessão (incluindo widgets) é salvo **automaticamente** de duas formas:

1. **Auto-save periódico**: A cada 10 segundos
2. **Save imediato**: Após carregar dados de personagem/monstro no widget

```javascript
// Auto-save configurado em DOMContentLoaded
setInterval(() => {
    salvarEstadoSessao();
}, 10000); // 10 segundos

// Save imediato após carregar dados
widget.dadosCriatura = { tipo, id, nome, modDestreza };
salvarEstadoSessao(); // ⚠️ CRÍTICO: Chama imediatamente
```

### Estrutura de Widget Salvo

```javascript
{
    id: 'widget-123',
    tipo: 'personagem' | 'instancia' | 'iniciativa' | 'log_combate' | 'dados' | 'notas',
    titulo: 'Azazel Ireth',
    x: 100,
    y: 200,
    width: 300,
    height: 400,
    minimizado: false,
    dadosCriatura: {  // ⚠️ Essencial para restaurar dados
        tipo: 'personagem' | 'instancia',
        id: 1,
        nome: 'Azazel Ireth',
        nomeBase: 'Goblin',  // Só para instancias
        modDestreza: 3
    }
}
```

### Restauração de Estado

```javascript
// Chamado no carregamento da página
restaurarEstado(estado)

// Para cada widget salvo:
1. Cria widget com WidgetManager
2. Se é 'personagem': carrega dados de /fichas/api/personagem/{id}
3. Se é 'instancia': carrega dados de /fichas/api/monstro/instancia/{id}
4. Se é 'iniciativa': renderiza lista de turnos
5. Se é 'log_combate': renderiza log de combate
```

### ⚠️ Erros Comuns de Persistência

**Problema**: Widgets salvos antes de `dadosCriatura` ser populado
```javascript
// ❌ ERRADO
widget.setConteudo(html);
// Auto-save pode acontecer aqui sem dadosCriatura!

// ✅ CORRETO
widget.setConteudo(html);
widget.dadosCriatura = { tipo, id, nome, modDestreza };
salvarEstadoSessao(); // Save imediato garante dados completos
```

**Problema**: Widget não reconhece tipo ao restaurar
```javascript
// Verificar se widget.tipo está correto:
// 'personagem' - carrega de /fichas/api/personagem/{id}
// 'instancia' - carrega de /fichas/api/monstro/instancia/{id}
// Outros tipos não têm dadosCriatura
```

### API de Persistência

```javascript
// Salvar estado
POST /sessao/api/estado
Body: {
    combateAtivo: false,
    ordemTurnos: [],
    turnoAtual: 0,
    roundAtual: 0,
    widgets: [...],  // Array de widgets serializados
    logCombate: [...],
    mapaAtual: 'Cenários/mapa.png'
}

// Carregar estado (automático ao abrir /sessao/)
GET /sessao/api/atual
Response: { estado: {...}, log: [...], ... }
```

### Fallback de Salvamento (Google Drive)

Se ocorrer `PermissionError` no Google Drive:

```python
# Sistema com retry em sessao.py
max_tentativas = 3
for tentativa in range(max_tentativas):
    try:
        os.replace(temp_path, caminho)
        break
    except PermissionError:
        if tentativa < max_tentativas - 1:
            time.sleep(0.1)  # Aguarda 100ms
        else:
            # Força sobrescrita direta
            with open(caminho, 'w') as f:
                json.dump(sessao, f)
```

---

## 11. CSS - Classes Importantes

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

### Atributos Clicáveis e Submenus

```css
/* Atributos clicáveis nos widgets */
.attr-clicavel {
    cursor: pointer;
    transition: all 0.15s ease;
}

.attr-clicavel:hover {
    background-color: var(--accent-success) !important;
    color: var(--bg-primary) !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(46, 204, 113, 0.3);
}

/* Submenu de perícias */
.submenu-pericias {
    position: fixed;
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding: 6px;
    background-color: var(--bg-elevated);
    border: 2px solid var(--accent-success);
    border-radius: var(--radius-sm);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    z-index: 10001;
    animation: slideLeft 0.15s ease-out;
    min-width: 150px;
    max-height: 400px;
    overflow-y: auto;
}

@keyframes slideLeft {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
}

.btn-pericia {
    padding: 6px 10px;
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: left;
    white-space: nowrap;
}

.btn-pericia:hover {
    background-color: var(--accent-success);
    border-color: var(--accent-success);
    color: var(--bg-primary);
    transform: translateX(2px);
}

/* Menu de resistências */
.menu-resistencia {
    position: fixed;
    display: flex;
    gap: 4px;
    padding: 6px;
    background-color: var(--bg-elevated);
    border: 2px solid var(--accent-primary);
    border-radius: var(--radius-sm);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    z-index: 10000;
    animation: slideDown 0.15s ease-out;
}

.btn-resist {
    min-width: 55px;
    padding: 6px 8px;
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    text-align: center;
}

.btn-resist:hover {
    background-color: var(--accent-primary);
    border-color: var(--accent-primary);
    color: var(--bg-primary);
    transform: translateY(-2px);
}
```

---

## 12. Widgets de NPC

Os NPCs possuem widgets completos com ataques, magias e habilidades funcionais para uso em combate.

### Estrutura HTML do Widget de NPC

```html
<div class="widget-npc-conteudo">
    <div class="npc-widget-header">
        <span class="npc-nome">Nome do NPC</span>
        <span class="npc-info">Título | Raça Classe</span>
    </div>
    
    <!-- HP -->
    <div class="npc-widget-hp">
        <div class="hp-barra-container">
            <div class="hp-barra" style="width: 80%"></div>
        </div>
        <div class="hp-valores">
            <span>24/30</span>
        </div>
    </div>
    
    <!-- Stats -->
    <div class="npc-widget-stats">
        CA: 15 | Vel: 9m
    </div>
    
    <!-- Atributos -->
    <div class="npc-widget-attrs">
        <span title="Clique para rolar">FOR +1</span>
        <span title="Clique para rolar">DES +2</span>
        ...
    </div>
    
    <!-- Ações de Combate -->
    <div class="npc-acoes-combate">
        <div class="acoes-grupo">
            <div class="grupo-titulo">⚔️ Ataques</div>
            <button class="btn-ataque" onclick="rolarAtaque(...)">
                Espada +4 (1d8+2)
            </button>
        </div>
        <div class="acoes-grupo">
            <div class="grupo-titulo">✨ Magias</div>
            <button class="btn-magia" onclick="rolarMagiaNPC(...)">
                Bola de Fogo (CD 15)
            </button>
        </div>
        <div class="acoes-grupo">
            <div class="grupo-titulo">🔮 Habilidades</div>
            <button class="btn-habilidade" onclick="usarHabilidadeNPC(...)">
                Cura Ferimentos
            </button>
        </div>
    </div>
    
    <!-- Dano/Cura -->
    <div class="npc-widget-botoes">
        <button class="btn-small btn-dano" onclick="abrirDanoRapido(...)">⚔️ Dano</button>
        <button class="btn-small btn-cura" onclick="abrirCuraRapida(...)">💚 Cura</button>
        <button class="btn-small btn-iniciativa" onclick="adicionarNPCAoCombate(...)">⏱️ Turnos</button>
    </div>
    
    <!-- Observações (visíveis ao grupo) -->
    <div class="npc-observacoes">
        <span>Observações públicas...</span>
    </div>
    
    <!-- Efeitos -->
    <div class="widget-efeitos" data-criatura-tipo="npc" data-criatura-id="...">
        <div class="efeitos-lista"></div>
        <button onclick="abrirModalEfeito(...)">+ Efeito</button>
    </div>
</div>
```

### Funções de NPC (sessao.js)

```javascript
/**
 * Gera HTML do widget de NPC com ações de combate
 * @param {Object} npc - Dados do NPC da API
 * @returns {string} HTML do widget
 */
function gerarHTMLNPCWidget(npc)

/**
 * Rola dados de uma magia de NPC (sem d20)
 * @param {Event} event - Evento do clique
 * @param {string} nomeNPC - Nome do NPC
 * @param {string} nomeMagia - Nome da magia
 * @param {string[]} dados - Array de dados ["8d6"]
 * @param {string} tipoDano - Tipo de dano
 * @param {number|null} cd - CD da salvaguarda
 */
function rolarMagiaNPC(event, nomeNPC, nomeMagia, dados, tipoDano, cd)

/**
 * Usa habilidade de NPC (log sem rolagem)
 * @param {Event} event - Evento do clique
 * @param {string} nomeNPC - Nome do NPC
 * @param {string} nomeHabilidade - Nome da habilidade
 * @param {string} descricao - Descrição da habilidade
 * @param {number|null} cd - CD se houver
 */
function usarHabilidadeNPC(event, nomeNPC, nomeHabilidade, descricao, cd)

/**
 * Adiciona NPC à ordem de iniciativa
 * @param {number} id - ID do NPC
 * @param {string} nome - Nome do NPC
 * @param {number} modDestreza - Modificador de DES
 */
function adicionarNPCAoCombate(id, nome, modDestreza)

/**
 * Rola expressão de dados localmente
 * @param {string} expressao - Ex: "2d6+3", "1d8", "3d10"
 * @returns {Object} { dados: [...], soma: n, expressao, texto }
 */
function rolarExpressao(expressao)
```

### Tipos de Ação de NPC

| Tipo | Rolagem | Uso |
|------|---------|-----|
| `ataque` | d20 + bônus, depois dano | Armas corpo-a-corpo/distância |
| `magia` | Apenas dados de dano | Magias de dano (alvo faz save) |
| `habilidade` | Nenhuma (descrição) | Curas, buffs, utilitários |

### Estrutura JSON de Ações

```json
[
  {
    "nome": "Espada Curta",
    "tipo": "ataque",
    "bonus": "+4",
    "dados": ["1d6+2"],
    "tipo_dano": "Perfurante"
  },
  {
    "nome": "Bola de Fogo",
    "tipo": "magia",
    "dados": ["8d6"],
    "tipo_dano": "Ígneo",
    "cd": 15,
    "descricao": "CD 15 DES, metade em sucesso"
  },
  {
    "nome": "Cura Ferimentos",
    "tipo": "habilidade",
    "cd": null,
    "descricao": "Cura 2d8+3 pontos de vida"
  }
]
```

### API de NPC

```javascript
// Obter NPC por ID
GET /api/npcs/{id}
Response: { id, nome, titulo, hp_atual, hp_maximo, ca, atributos, acoes, ... }

// Aplicar dano ao NPC
POST /api/npcs/{id}/dano
Body: { dano: number }
Response: { sucesso: true, hp_atual: n, hp_maximo: n }

// Curar NPC
POST /api/npcs/{id}/curar
Body: { quantidade: number }
Response: { sucesso: true, hp_atual: n, hp_maximo: n }
```

### CSS de Ações de NPC

```css
.npc-acoes-combate {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
}

.acoes-grupo {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.grupo-titulo {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.btn-ataque {
    background: linear-gradient(135deg, #c0392b, #e74c3c);
    border: none;
    color: white;
}

.btn-magia {
    background: linear-gradient(135deg, #2980b9, #3498db);
    border: none;
    color: white;
}

.btn-habilidade {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    border: none;
    color: white;
}

/* Log de magia */
.log-magia {
    border-left-color: var(--accent-primary);
}
```

---

## 13. Integrações Críticas

### Manter Sincronizados

1. **IDs de criatura**: `data-criatura-id` e `data-personagem-id` / `data-monstro-id` / `data-npc-id`
2. **Tipos de criatura**: `'personagem'` vs `'instancia'` vs `'npc'`
3. **Seletores CSS**: Classes como `.widget-personagem-conteudo`, `.widget-npc-conteudo` devem existir no HTML
4. **APIs de dano/cura**: Retornam objeto completo com `hp_atual`, `hp_maximo`, `sucesso_morte`, `falha_morte`

### Ao Modificar Fichas

- Verificar se seletores CSS ainda funcionam no sessao.js
- Verificar se `data-campo` atributos existem para coleta de dados
- Verificar se APIs retornam todos os campos necessários
- Testar dano/cura e testes de morte na tela de sessão

---

## 14. Ordem de Seções no Widget de Ficha

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

## 15. Checklist para Novas Funcionalidades

- [ ] Adicionar estilos em `sessao.css` ou `widgets.css`
- [ ] Implementar lógica em `sessao.js`
- [ ] Verificar compatibilidade com `atualizarWidgetCriatura()`
- [ ] Testar iniciativa (adicionar, editar, ordenar)
- [ ] Testar dano/cura (verificar testes de morte)
- [ ] Testar efeitos (adicionar, remover, countdown)
- [ ] Verificar middle-click fecha widget
- [ ] Testar ações de NPC (ataques, magias, habilidades)
