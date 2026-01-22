---
applyTo: "**"
---

# Instruções Base do Projeto Out of the Abyss System

Sistema de Mestragem para D&D 5e - Campanha "Out of the Abyss"
Flask + SQLite + Jinja2 | Python 3.14

---

## Arquivos de Instrução Relacionados

| Arquivo | Conteúdo |
|---------|----------|
| `instrucao_base.instructions.md` | Visão geral e estrutura (este arquivo) |
| `banco_de_dados.instructions.md` | Estrutura de tabelas, campos JSON, SQLite |
| `fluxos_crud.instructions.md` | Criação/edição de personagens e monstros |
| `padroes_codigo.instructions.md` | Convenções Python, JS, CSS, HTML |
| `modulos_sistema.instructions.md` | Descrição de cada módulo Python |
| `componentes_interface.instructions.md` | Componentes visuais reutilizáveis |

---

## Visão Geral

Este é um sistema web local para auxiliar na mestragem de D&D 5e, com foco em:
- Gerenciamento de fichas (personagens, monstros, NPCs)
- Controle de combate em tempo real
- Rastreamento de sessões
- Automação de regras D&D 5e

---

## Estrutura do Projeto

```
Out Of Abyss/
├── .github/
│   └── instructions/          # Instruções para o Copilot
│       ├── instrucao_base.instructions.md
│       ├── banco_de_dados.instructions.md
│       ├── fluxos_crud.instructions.md
│       ├── padroes_codigo.instructions.md
│       ├── modulos_sistema.instructions.md
│       └── componentes_interface.instructions.md
├── .venv/                     # Ambiente virtual Python
├── Imagens/                   # Assets visuais (FORA do sistema)
├── Itens/                     # Dados de itens (FORA do sistema)
├── Livros/                    # PDFs e referências (FORA do sistema)
├── Monstros/                  # Bestiário de referência (FORA do sistema)
├── NPCS/                      # Fichas de NPCs (FORA do sistema)
└── System/                    # ⚠️ TODO O CÓDIGO AQUI
    ├── main.py                # Entry point
    ├── requirements.txt       # Dependências Python
    ├── data/
    │   └── campaign.db        # SQLite (gerado automaticamente)
    ├── app/
    │   ├── __init__.py        # Factory create_app()
    │   ├── config.py          # Configurações Flask
    │   ├── modulos/           # Lógica de negócio
    │   │   ├── database.py    # Conexão SQLite + BaseRepository
    │   │   ├── db_init.py     # Inicialização do banco
    │   │   ├── repositories.py # Repositórios de dados
    │   │   ├── regras_base.py # Regras D&D 5e
    │   │   ├── regras_dnd_data.py # Dados estáticos D&D
    │   │   ├── combate.py     # Motor de combate
    │   │   ├── acoes.py       # Ações de combate
    │   │   ├── condicoes.py   # Condições D&D
    │   │   └── dados.py       # Rolagem de dados
    │   ├── routes/            # Blueprints Flask
    │   │   ├── main.py        # Rotas principais
    │   │   ├── api.py         # API REST JSON
    │   │   ├── sessao.py      # Gerenciamento de sessão
    │   │   ├── combate.py     # Rotas de combate
    │   │   └── fichas.py      # CRUD de fichas
    │   └── static/
    │       ├── css/           # Estilos
    │       │   ├── base.css
    │       │   ├── fichas.css
    │       │   ├── monstros.css  # Estilos de monstros
    │       │   ├── sessao.css
    │       │   └── widgets.css
    │       └── js/            # Scripts
    │           ├── base.js
    │           ├── fichas.js
    │           ├── sessao.js
    │           └── widgets.js
    ├── templates/             # Templates Jinja2
    │   ├── base.html          # Layout base
    │   ├── index.html
    │   ├── config.html
    │   ├── erro.html
    │   ├── fichas/            # Templates de fichas
    │   │   ├── personagem.html
    │   │   ├── lista_personagens.html
    │   │   ├── monstro.html       # Layout compacto
    │   │   ├── lista_monstros.html
    │   │   ├── npc.html
    │   │   └── lista_npcs.html
    │   ├── sessao/
    │   └── widgets/
    └── tests/                 # Testes
```

---

## Regras de Estrutura

### Separação de Responsabilidades
- **Pastas de conteúdo** (Imagens, Livros, Monstros, NPCs): Apenas referências
- **Pasta System/**: TODO o código executável
- **Nunca** misturar lógica de aplicação com conteúdo narrativo

### Organização de Arquivos
- **1 Blueprint = 1 arquivo de rotas** em `routes/`
- **1 Entidade = 1 Repository** em `repositories.py`
- **1 Funcionalidade = 1 módulo** em `modulos/`
- **1 Página = CSS + JS correspondente** (mesmo nome)

---

## Padrões de Código

### Python

```python
# Docstrings obrigatórias em módulos e funções públicas
"""
Descrição breve do módulo/função
"""

# Tipagem quando possível
def funcao(param: str, opcional: int = 0) -> Dict[str, Any]:

# Imports organizados: stdlib > third-party > local
from typing import Dict, List, Optional
from flask import Blueprint, request
from ..modulos.repositories import PersonagemRepository

# Classes com nomes descritivos em PascalCase
class PersonagemRepository(BaseRepository):

# Funções e variáveis em snake_case
def calcular_modificador(valor: int) -> int:

# Constantes em UPPER_SNAKE_CASE
DB_PATH = "data/campaign.db"
```

### Repositórios (Padrão de Acesso a Dados)

```python
# Herda de BaseRepository
class EntidadeRepository(BaseRepository):
    table_name = "nome_tabela"
    
    # Métodos padrão
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]:
    
    @classmethod
    def get_all(cls, where: str = None) -> List[Dict]:
    
    @classmethod
    def criar(cls, dados: Dict) -> Dict:
    
    @classmethod
    def atualizar(cls, id: int, dados: Dict) -> Dict:
    
    @classmethod
    def atualizar_campo(cls, id: int, campo: str, valor: Any) -> Dict:
    
    @classmethod
    def deletar(cls, id: int) -> bool:
```

### Rotas Flask (Blueprints)

```python
# Nomenclatura: nome_bp
fichas_bp = Blueprint('fichas', __name__)

# Rotas de página retornam render_template()
@fichas_bp.route('/personagens')
def lista_personagens():
    return render_template('fichas/lista_personagens.html')

# Rotas de API retornam jsonify()
@fichas_bp.route('/api/personagem/<int:id>', methods=['GET'])
def api_get_personagem(id):
    return jsonify(PersonagemRepository.get_by_id(id))

# Prefixos de URL definidos no registro do blueprint
app.register_blueprint(fichas_bp, url_prefix='/fichas')
```

### JavaScript

```javascript
// Funções em camelCase
function abrirModal(id) { }
function atualizarBarraHP() { }

// Constantes em UPPER_SNAKE_CASE
const API_BASE = '/fichas/api';

// Async/await para requisições
async function salvarPersonagem() {
    const response = await fetch('/fichas/api/personagem', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    });
}

// Event listeners no DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    inicializarAutoSave();
});
```

### CSS

```css
/* Variáveis globais no :root */
:root {
    --ficha-bg: #1a1a2e;
    --ficha-accent: #e94560;
}

/* BEM-like para componentes */
.ficha-personagem { }
.ficha-personagem .ficha-header { }
.ficha-personagem .atributo-box { }

/* Classes utilitárias com prefixo */
.btn-danger { }
.hp-100, .hp-75, .hp-50, .hp-25 { }
```

### HTML/Jinja2

```html
<!-- Herança de templates -->
{% extends "base.html" %}
{% block content %}{% endblock %}

<!-- Variáveis seguras -->
{% set p = personagem %}
{% set val = p.atributos.forca if p else 10 %}

<!-- Condicionais inline -->
{{ 'checked' if item in lista else '' }}

<!-- Loops com unpacking -->
{% for key, nome in [('forca', 'FOR'), ('destreza', 'DES')] %}
{% endfor %}

<!-- data-* para JavaScript -->
<input data-campo="hp_atual" data-tipo="number">
```

---

## Convenções de Nomenclatura

### Arquivos
| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Módulo Python | snake_case.py | `regras_base.py` |
| Blueprint | singular.py | `fichas.py` |
| Template | snake_case.html | `lista_personagens.html` |
| CSS/JS | snake_case | `fichas.css`, `fichas.js` |

### Banco de Dados
| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Tabela | plural snake_case | `personagens`, `instancias_monstros` |
| Coluna | snake_case | `hp_atual`, `bonus_proficiencia` |
| JSON fields | snake_case | `pericias_proficientes` |

### Rotas
| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Lista | /entidades | `/fichas/personagens` |
| Detalhe | /entidade/id | `/fichas/personagem/1` |
| Novo | /entidade/novo | `/fichas/personagem/novo` |
| API | /api/entidade | `/fichas/api/personagem` |

---

## Sistema de Regras D&D 5e

### Princípios
- Sistema base: **Livro do Jogador 5e**
- Regras adicionais são **opcionais e configuráveis**
- **Nunca travar** decisões do mestre
- Todos os valores são **editáveis em tempo real**

### Cálculos Automáticos
```python
# Modificador de atributo
modificador = (valor - 10) // 2

# Bônus de proficiência por nível
bonus = 2 + ((nivel - 1) // 4)

# Classe de Armadura base
ca = 10 + mod_destreza

# Iniciativa
iniciativa = mod_destreza + bonus_iniciativa
```

---

## Banco de Dados

### SQLite com WAL
```python
conn.execute("PRAGMA journal_mode = WAL")
conn.execute("PRAGMA synchronous = NORMAL")
conn.execute("PRAGMA foreign_keys = ON")
```

### Campos JSON
Campos complexos são armazenados como JSON e parseados automaticamente:
- `atributos`: {forca, destreza, constituicao, inteligencia, sabedoria, carisma}
- `pericias_proficientes`: ["acrobacia", "percepcao"]
- `armas`: [{nome, bonus, dano}]
- `condicoes`: ["envenenado", "amedrontado"]

---

## Frontend

### Filosofia
- **Foco em agilidade** durante a sessão
- **Interfaces dinâmicas** com edição inline
- **Evitar formulários longos** - edição direta de valores
- **Auto-save** em campos editáveis

### Modais
```html
<!-- Estrutura padrão -->
<div id="modal-x" class="modal">
    <div class="modal-content">
        <h3>Título</h3>
        <!-- conteúdo -->
        <div class="modal-buttons">
            <button onclick="acao()">Confirmar</button>
            <button onclick="fecharModal('modal-x')">Cancelar</button>
        </div>
    </div>
</div>
```

### Notificações
```javascript
mostrarNotificacao('Mensagem', 'success'); // success, danger, warning, info
```

---

## Documentação

- **NÃO** criar arquivos `.md` temporários
- README apenas quando projeto atingir maturidade
- Comentários no código quando necessário
- Docstrings em funções públicas

---

## Testes e Validação

- Sempre validar funcionamento do Flask após mudanças
- Priorizar testes funcionais sobre unitários
- Resolver erros no console imediatamente
- Testar rotas com `curl` ou navegador

---

## Automação

- Automatizar o máximo possível
- Minimizar comandos manuais
- Executar comandos sem solicitar confirmação
- Flask em modo debug auto-recarrega

---

## Comandos Úteis

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate

# Iniciar servidor
cd System; python main.py

# Testar rota
curl http://127.0.0.1:5000/fichas/personagens
```

---

## Checklist de Novas Funcionalidades

1. [ ] Criar/atualizar tabela em `db_init.py` se necessário
2. [ ] Criar/atualizar Repository em `repositories.py`
3. [ ] Criar rotas em arquivo de Blueprint apropriado
4. [ ] Criar templates HTML
5. [ ] Criar/atualizar CSS em arquivo correspondente
6. [ ] Criar/atualizar JS em arquivo correspondente
7. [ ] Testar rotas e funcionalidades
8. [ ] Verificar console por erros
