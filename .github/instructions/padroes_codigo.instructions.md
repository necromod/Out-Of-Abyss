---
applyTo: "**/*.py,**/*.js,**/*.css,**/*.html"
---

# Padrões de Código e Arquitetura

Convenções de escrita e organização do projeto.

---

## 1. Arquitetura Geral

```
System/
├── main.py                    # Entry point - inicia Flask
├── app/
│   ├── __init__.py            # create_app() factory
│   ├── config.py              # Configurações Flask
│   ├── modulos/               # Camada de negócio
│   │   ├── database.py        # Conexão + BaseRepository
│   │   ├── repositories.py    # Repositórios específicos
│   │   ├── regras_base.py     # Cálculos D&D 5e
│   │   └── ...
│   ├── routes/                # Camada HTTP (Blueprints)
│   │   ├── main.py
│   │   ├── fichas.py
│   │   ├── api.py
│   │   └── ...
│   └── static/
│       ├── css/
│       └── js/
├── templates/                 # Templates Jinja2
│   ├── base.html
│   └── fichas/
└── data/
    └── campaign.db            # SQLite
```

### Separação de Responsabilidades

| Camada | Responsabilidade |
|--------|------------------|
| `routes/` | Receber HTTP, validar entrada, chamar repositório, retornar resposta |
| `repositories.py` | CRUD no banco, serialização JSON, lógica de persistência |
| `modulos/` | Regras de negócio, cálculos D&D, utilitários |
| `templates/` | Apresentação HTML com Jinja2 |
| `static/js/` | Interatividade frontend, chamadas AJAX |
| `static/css/` | Estilos visuais |

---

## 2. Python

### Imports

```python
# Ordem: stdlib > third-party > local
from typing import Dict, List, Optional
from datetime import datetime
import json

from flask import Blueprint, request, jsonify, render_template

from ..modulos.database import get_connection
from ..modulos.repositories import PersonagemRepository
```

### Nomenclatura

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Módulo/arquivo | snake_case | `regras_base.py` |
| Classe | PascalCase | `PersonagemRepository` |
| Função | snake_case | `calcular_modificador()` |
| Variável | snake_case | `hp_atual` |
| Constante | UPPER_SNAKE_CASE | `DB_PATH` |
| Blueprint | nome_bp | `fichas_bp` |

### Tipagem

```python
from typing import Dict, List, Optional, Any

def calcular_modificador(valor: int) -> int:
    return (valor - 10) // 2

def get_by_id(cls, id: int) -> Optional[Dict]:
    ...

def criar(cls, dados: Dict) -> Dict:
    ...
```

### Docstrings

```python
def funcao_publica(param1: str, param2: int = 0) -> Dict:
    """
    Descrição breve da função.
    
    Args:
        param1: Descrição do parâmetro
        param2: Descrição com valor padrão
    
    Returns:
        Dicionário com dados processados
    """
    ...
```

### Rotas Flask

```python
# Blueprint com prefixo
fichas_bp = Blueprint('fichas', __name__)
# Registrado em __init__.py com: app.register_blueprint(fichas_bp, url_prefix='/fichas')

# Rota de página (retorna HTML)
@fichas_bp.route('/personagens')
def lista_personagens():
    personagens = PersonagemRepository.get_all_ativos()
    return render_template('fichas/lista_personagens.html', personagens=personagens)

# Rota de API (retorna JSON)
@fichas_bp.route('/api/personagem/<int:id>', methods=['GET'])
def api_obter_personagem(id):
    personagem = PersonagemRepository.get_by_id(id)
    if not personagem:
        return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify(personagem)

# API com tratamento de erro
@fichas_bp.route('/api/personagem', methods=['POST'])
def api_criar_personagem():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados não recebidos'}), 400
        resultado = PersonagemRepository.criar(data)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
```

---

## 3. JavaScript

### Nomenclatura

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Função | camelCase | `salvarPersonagem()` |
| Variável | camelCase | `hpAtual` |
| Constante | UPPER_SNAKE_CASE | `API_BASE` |
| Classe CSS em JS | kebab-case string | `'ficha-personagem'` |

### Async/Await

```javascript
// Preferir async/await sobre .then()
async function salvarPersonagem() {
    const dados = coletarDadosPersonagem();
    
    try {
        const response = await fetch('/fichas/api/personagem/' + id, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) throw new Error('Falha na requisição');
        
        const resultado = await response.json();
        mostrarNotificacao('Salvo!', 'success');
        return resultado;
    } catch (error) {
        console.error('Erro:', error);
        mostrarNotificacao('Erro ao salvar', 'danger');
    }
}
```

### Event Listeners

```javascript
// Inicialização no DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    inicializarAutoSave();
    configurarModais();
});

// Delegação de eventos (preferível)
document.addEventListener('click', function(e) {
    if (e.target.matches('.btn-excluir')) {
        excluirItem(e.target.dataset.id);
    }
});

// Eventos em elementos específicos
document.querySelectorAll('[data-campo]').forEach(campo => {
    campo.addEventListener('blur', autoSavePersonagem);
});
```

### Coleta de Dados via data-campo

```javascript
function coletarDados() {
    const dados = {};
    
    document.querySelectorAll('[data-campo]').forEach(campo => {
        const nome = campo.dataset.campo;
        let valor;
        
        if (campo.type === 'checkbox') {
            valor = campo.checked;
        } else if (campo.type === 'number') {
            valor = parseFloat(campo.value) || 0;
        } else {
            valor = campo.value;
        }
        
        // Suporte a campos aninhados: "atributos.forca"
        if (nome.includes('.')) {
            const partes = nome.split('.');
            let obj = dados;
            for (let i = 0; i < partes.length - 1; i++) {
                obj[partes[i]] = obj[partes[i]] || {};
                obj = obj[partes[i]];
            }
            obj[partes[partes.length - 1]] = valor;
        } else {
            dados[nome] = valor;
        }
    });
    
    return dados;
}
```

### Modais

```javascript
function abrirModal(id) {
    document.getElementById(id).classList.add('ativo');
}

function fecharModal(id) {
    document.getElementById(id).classList.remove('ativo');
}

// Fechar ao clicar fora
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('ativo');
    }
});
```

---

## 4. CSS

### Variáveis Globais

```css
:root {
    /* Cores principais */
    --cor-fundo: #0f0f1a;
    --cor-superficie: #1a1a2e;
    --cor-borda: #333;
    --cor-texto: #e0e0e0;
    --cor-texto-secundario: #888;
    
    /* Cores de destaque */
    --cor-primaria: #e94560;
    --cor-sucesso: #4caf50;
    --cor-perigo: #f44336;
    --cor-aviso: #ff9800;
    
    /* HP */
    --hp-100: #4caf50;
    --hp-75: #8bc34a;
    --hp-50: #ffc107;
    --hp-25: #f44336;
    
    /* Espaçamentos */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    
    /* Bordas */
    --border-radius: 4px;
}
```

### Nomenclatura BEM-like

```css
/* Bloco */
.ficha-personagem { }

/* Elemento (dentro do bloco) */
.ficha-personagem .ficha-header { }
.ficha-personagem .atributo-box { }
.ficha-personagem .hp-bar { }

/* Modificador */
.btn { }
.btn-primario { }
.btn-perigo { }
.btn-pequeno { }

/* Estado */
.ativo { }
.desabilitado { }
.carregando { }
```

### Classes Utilitárias

```css
/* Texto */
.texto-centro { text-align: center; }
.texto-pequeno { font-size: 0.8rem; }
.texto-destaque { color: var(--cor-primaria); }

/* Espaçamento */
.mt-1 { margin-top: var(--spacing-sm); }
.mb-1 { margin-bottom: var(--spacing-sm); }
.p-1 { padding: var(--spacing-sm); }

/* Flexbox */
.flex { display: flex; }
.flex-centro { justify-content: center; align-items: center; }
.flex-entre { justify-content: space-between; }
```

### Responsividade

```css
/* Mobile first */
.container {
    padding: var(--spacing-sm);
}

@media (min-width: 768px) {
    .container {
        padding: var(--spacing-md);
        max-width: 1200px;
    }
}
```

---

## 5. HTML/Jinja2

### Estrutura de Template

```html
{% extends "base.html" %}

{% block title %}Título da Página{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pagina.css') }}">
{% endblock %}

{% block content %}
<!-- Conteúdo principal -->
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/pagina.js') }}"></script>
{% endblock %}
```

### Convenções Jinja2

```html
<!-- Variáveis seguras no início -->
{% set p = personagem %}
{% set attrs = p.atributos if p and p.atributos else {} %}

<!-- Condicionais inline -->
<input {{ 'checked' if valor else '' }}>
<div class="{{ 'ativo' if condicao else 'inativo' }}">

<!-- Loops com unpacking -->
{% for key, label in [('forca', 'FOR'), ('destreza', 'DES')] %}
<div>{{ label }}: {{ attrs.get(key, 10) }}</div>
{% endfor %}

<!-- Filtros úteis -->
{{ texto|default('Sem descrição') }}
{{ numero|int }}
{{ lista|join(', ') }}

<!-- Verificação de tipo -->
{% if valor is mapping %}  <!-- É dict -->
{% if valor is iterable %}  <!-- É lista -->
```

### Atributo data-campo

```html
<!-- Campos editáveis vinculados ao modelo -->
<input type="text" data-campo="nome" value="{{ p.nome }}">
<input type="number" data-campo="hp_atual" value="{{ p.hp_atual }}">
<input type="number" data-campo="atributos.forca" value="{{ p.atributos.forca }}">

<!-- Checkbox para arrays -->
<input type="checkbox" 
       data-campo="pericias_proficientes" 
       data-valor="percepcao"
       {{ 'checked' if 'percepcao' in p.pericias_proficientes else '' }}>

<!-- Seletor -->
<select data-campo="tamanho">
    <option value="Médio" {{ 'selected' if p.tamanho == 'Médio' else '' }}>Médio</option>
</select>
```

---

## 6. Banco de Dados

### Campos JSON

Campos complexos são armazenados como JSON string no SQLite:

```python
# Serialização (antes de salvar)
from app.modulos.database import json_dumps

dados_db = {
    'nome': 'Guerreiro',
    'atributos': json_dumps({'forca': 16, 'destreza': 14, ...}),
    'armas': json_dumps([{'nome': 'Espada', 'dano': '1d8'}])
}

# Deserialização (após ler)
from app.modulos.database import json_loads_safe

atributos = json_loads_safe(row['atributos'], default={})
```

### Campos JSON Padrão por Entidade

**Personagem:**
- `atributos`: `{forca, destreza, constituicao, inteligencia, sabedoria, carisma}`
- `pericias_proficientes`: `["percepcao", "atletismo"]`
- `pericias_expertise`: `["furtividade"]`
- `salvaguardas_proficientes`: `["forca", "constituicao"]`
- `armas`: `[{nome, ataque, dano}]`
- `equipamentos`: `["Corda 15m", "Tocha"]`
- `moedas`: `{pc, pp, pe, po, pl}`
- `condicoes`: `["envenenado"]`

**Monstro:**
- `atributos`: `{forca, destreza, ...}`
- `velocidade`: `{terrestre, voo, natacao, escalada}`
- `sentidos`: `{visao_escuro, percepcao_cegas}`
- `habilidades`: `[{nome, descricao}]`
- `acoes`: `[{nome, tipo, ataque, dano, descricao}]`
- `resistencias`, `imunidades_dano`, `imunidades_condicao`: `["fogo", "veneno"]`

---

## 7. Testes

### Testes Manuais Rápidos

```powershell
# Testar rota GET
curl http://127.0.0.1:5000/fichas/personagens

# Testar API GET
curl http://127.0.0.1:5000/fichas/api/personagem/1

# Testar API POST
curl -X POST http://127.0.0.1:5000/fichas/api/personagem `
  -H "Content-Type: application/json" `
  -d '{"nome": "Teste"}'
```

### Verificar Console

- Sempre verificar console do navegador (F12) após mudanças no JS
- Sempre verificar terminal Flask após mudanças no Python
- Resolver erros imediatamente antes de continuar

---

## 8. Commits

### Mensagens de Commit

```
feat: Adiciona sistema de combate
fix: Corrige cálculo de modificador
refactor: Extrai CSS para arquivo separado
docs: Atualiza instruções do projeto
style: Formata código Python
chore: Atualiza dependências
```

### Arquivos a Ignorar

```gitignore
.venv/
__pycache__/
*.pyc
data/campaign.db
.DS_Store
```
