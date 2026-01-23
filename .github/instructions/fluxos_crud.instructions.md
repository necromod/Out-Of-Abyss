---
applyTo: "**/repositories.py,**/fichas.py,**/api.py,**/*.js"
---

# Fluxos de CRUD - Personagens e Monstros

Documentação dos fluxos de criação, leitura, atualização e exclusão.

---

## 1. Personagens (PCs)

### Arquivos Envolvidos
- **Backend:**
  - `app/routes/fichas.py` - Rotas HTTP
  - `app/modulos/repositories.py` - PersonagemRepository
  - `app/modulos/database.py` - BaseRepository
- **Frontend:**
  - `templates/fichas/personagem.html` - Template
  - `templates/fichas/lista_personagens.html` - Lista
  - `app/static/js/fichas.js` - JavaScript
  - `app/static/css/fichas.css` - Estilos

### Rotas

| Método | Rota | Função | Descrição |
|--------|------|--------|-----------|
| GET | `/fichas/personagens` | `lista_personagens()` | Lista todos |
| GET | `/fichas/personagem/<id>` | `ficha_personagem(id)` | Visualizar/editar |
| GET | `/fichas/personagem/novo` | `novo_personagem()` | Formulário novo |
| GET | `/fichas/api/personagem/<id>` | `api_obter_personagem(id)` | JSON da ficha |
| POST | `/fichas/api/personagem` | `api_criar_personagem()` | Criar novo |
| PUT | `/fichas/api/personagem/<id>` | `api_atualizar_personagem(id)` | Atualizar |
| PATCH | `/fichas/api/personagem/<id>` | `api_atualizar_personagem(id)` | Atualizar parcial |
| DELETE | `/fichas/api/personagem/<id>` | `api_deletar_personagem(id)` | Remover |

### Fluxo de Criação

```
[Usuário] → /fichas/personagem/novo
    ↓
[Template] personagem.html (sem dados, m = None)
    ↓
[Usuário preenche] → Clica "Criar"
    ↓
[JS] criarPersonagem() → coletarDadosPersonagem()
    ↓
[fetch] POST /fichas/api/personagem
    ↓
[Python] api_criar_personagem()
    ↓
[Repository] PersonagemRepository.criar(dados)
    ↓ dados_db = _prepare_for_db(dados)  # Serializa JSON
    ↓ id = insert(dados_db)
    ↓ return get_by_id(id)
    ↓
[Response] JSON { id, nome, ... }
    ↓
[JS] Redireciona para /fichas/personagem/{id}
```

### Fluxo de Atualização (Auto-save)

```
[Usuário] Edita campo com data-campo="hp_atual"
    ↓
[JS] blur ou change event
    ↓
[JS] autoSavePersonagem()
    ↓
[JS] coletarDadosPersonagem() → Coleta TODOS os campos
    ↓
[fetch] PUT /fichas/api/personagem/{id}
    ↓
[Python] api_atualizar_personagem(id)
    ↓
[Repository] PersonagemRepository.atualizar(id, dados)
    ↓
[Response] JSON atualizado
    ↓
[JS] mostrarNotificacao('Salvo!', 'success')
```

### Coleta de Dados (coletarDadosPersonagem)

```javascript
function coletarDadosPersonagem() {
    const dados = {
        atributos: {},
        pericias_proficientes: [],
        pericias_expertise: [],
        salvaguardas_proficientes: [],
        armas: [],
        equipamentos: [],
        moedas: { pc: 0, pp: 0, pe: 0, po: 0, pl: 0 }
    };
    
    // Coleta campos simples por data-campo
    document.querySelectorAll('[data-campo]').forEach(campo => {
        const nome = campo.dataset.campo;
        // ... processa cada tipo
    });
    
    // Coleta armas (formato novo)
    document.querySelectorAll('.arma-item').forEach((item, i) => {
        const dadosDano = [];
        item.querySelectorAll('.dado-dano-input').forEach(input => {
            if (input.value.trim()) {
                dadosDano.push(input.value.trim());
            }
        });
        
        const arma = {
            nome: item.querySelector('[data-campo*=".nome"]')?.value || '',
            bonus: item.querySelector('[data-campo*=".bonus"]')?.value || '',
            dados: dadosDano,
            tipo: item.querySelector('[data-campo*=".tipo"]')?.value || ''
        };
        
        if (arma.nome) {
            dados.armas.push(arma);
        }
    });
    
    // Coleta moedas
    ['pc', 'pp', 'pe', 'po', 'pl'].forEach(tipo => {
        const input = document.querySelector(`[data-campo="moedas.${tipo}"]`);
        if (input) dados.moedas[tipo] = parseInt(input.value) || 0;
    });
    
    return dados;
}
```

### Estrutura de Armas (Formato Novo)

```javascript
// Cada arma no formato novo:
{
    nome: "Espada Longa",       // Nome da arma
    bonus: "+5",                // Bônus de ataque
    dados: ["1d8+3"],           // Array de dados de dano
    tipo: "Cortante"            // Tipo de dano (dropdown)
}

// Múltiplos dados de dano:
{
    nome: "Espada Flamejante",
    bonus: "+5",
    dados: ["1d8+3", "1d6"],    // 1d8+3 cortante + 1d6 ígneo
    tipo: "Cortante"
}
```

### Tipos de Dano Disponíveis

```javascript
const TIPOS_DANO = [
    { valor: '',            nome: '—' },
    { valor: 'Ácido',       nome: 'Ácido' },
    { valor: 'Contundente', nome: 'Contundente' },
    { valor: 'Cortante',    nome: 'Cortante' },
    { valor: 'Elétrico',    nome: 'Elétrico' },
    { valor: 'Energético',  nome: 'Energético' },
    { valor: 'Gélido',      nome: 'Gélido' },
    { valor: 'Ígneo',       nome: 'Ígneo' },
    { valor: 'Necrótico',   nome: 'Necrótico' },
    { valor: 'Perfurante',  nome: 'Perfurante' },
    { valor: 'Psíquico',    nome: 'Psíquico' },
    { valor: 'Radiante',    nome: 'Radiante' },
    { valor: 'Trovejante',  nome: 'Trovejante' },
    { valor: 'Venenoso',    nome: 'Venenoso' }
];
```

### Campos com data-campo

O atributo `data-campo` vincula inputs ao modelo de dados:

```html
<!-- Campo simples -->
<input data-campo="nome" value="{{ p.nome }}">

<!-- Campo numérico -->
<input type="number" data-campo="hp_atual" value="{{ p.hp_atual }}">

<!-- Campo aninhado (objeto) -->
<input data-campo="atributos.forca" value="{{ p.atributos.forca }}">

<!-- Armas - Formato Novo -->
<input data-campo="armas.0.nome" value="{{ p.armas[0].nome }}">
<input data-campo="armas.0.bonus" value="{{ p.armas[0].bonus }}">
<input class="dado-dano-input" value="{{ p.armas[0].dados[0] }}">
<select data-campo="armas.0.tipo">
    <option value="Cortante">Cortante</option>
    <!-- ... -->
</select>

<!-- Checkbox para arrays -->
<input type="checkbox" data-campo="pericias_proficientes" data-valor="percepcao">

<!-- Moedas -->
<input data-campo="moedas.po" value="{{ p.moedas.po }}">
```

---

## 2. Monstros (Bestiário)

### Arquivos Envolvidos
- **Backend:**
  - `app/routes/fichas.py` - Rotas HTTP
  - `app/modulos/repositories.py` - MonstroRepository
- **Frontend:**
  - `templates/fichas/monstro.html` - Template compacto
  - `templates/fichas/lista_monstros.html` - Lista
  - `app/static/css/monstros.css` - Estilos específicos

### Rotas

| Método | Rota | Função | Descrição |
|--------|------|--------|-----------|
| GET | `/fichas/monstros` | `lista_monstros()` | Lista todos |
| GET | `/fichas/monstro/<id>` | `ficha_monstro(id)` | Visualizar/editar |
| GET | `/fichas/monstro/novo` | `novo_monstro()` | Formulário novo |
| GET | `/fichas/api/monstro/<id>` | `api_obter_monstro(id)` | JSON da ficha |
| POST | `/fichas/api/monstro` | `api_criar_monstro()` | Criar novo |
| PUT | `/fichas/api/monstro/<id>` | `api_atualizar_monstro(id)` | Atualizar |
| DELETE | `/fichas/api/monstro/<id>` | `api_deletar_monstro(id)` | Remover |

### Fluxo de Criação

```
[Usuário] → /fichas/monstro/novo
    ↓
[Template] monstro.html (m = None)
    ↓
[Usuário preenche] → Clica "✅ Criar"
    ↓
[JS] criarMonstro() → coletarDadosMonstro()
    ↓
[fetch] POST /fichas/api/monstro
    ↓
[Python] api_criar_monstro()
    ↓ Valida dados (nome obrigatório)
    ↓
[Repository] MonstroRepository.criar(dados)
    ↓ dados_db = _prepare_for_db(dados)
    ↓ id = insert(dados_db)
    ↓ return get_by_id(id)
    ↓
[Response] JSON { id, nome, ... }
    ↓
[JS] Redireciona para /fichas/monstro/{id}
```

### Coleta de Dados (coletarDadosMonstro)

```javascript
function coletarDadosMonstro() {
    const dados = {
        atributos: {},
        acoes: [],
        velocidade: {}
    };
    
    // Coleta ações (array de objetos)
    document.querySelectorAll('#lista-acoes-monstro .acao-linha').forEach(linha => {
        const nome = linha.querySelector('[data-campo*=".nome"]')?.value || '';
        const ataque = linha.querySelector('[data-campo*=".ataque"]')?.value || '';
        const dano = linha.querySelector('[data-campo*=".dano"]')?.value || '';
        
        if (nome) {
            dados.acoes.push({ nome, ataque, dano });
        }
    });
    
    // Coleta outros campos
    document.querySelectorAll('[data-campo]').forEach(campo => {
        const nomeCampo = campo.dataset.campo;
        
        if (nomeCampo.startsWith('acoes.')) return; // Já coletado
        
        if (nomeCampo.startsWith('atributos.')) {
            const attr = nomeCampo.replace('atributos.', '');
            dados.atributos[attr] = parseInt(campo.value) || 10;
        } else if (nomeCampo === 'velocidade_str') {
            // Converte "9m" para {terrestre: 9}
            const match = campo.value.match(/(\d+)/);
            dados.velocidade.terrestre = match ? parseInt(match[1]) : 9;
        } else if (campo.type === 'number') {
            dados[nomeCampo] = parseFloat(campo.value) || 0;
        } else {
            dados[nomeCampo] = campo.value;
        }
    });
    
    return dados;
}
```

### Layout Compacto (monstro.html)

O template de monstros usa layout compacto em linha única:

```html
<div class="ficha-monstro-compacta">
    <!-- Header: Nome | PV | CA | ND | Desloc -->
    <div class="monstro-header-row">
        <input data-campo="nome" placeholder="Nome">
        <div class="stat-mini"><label>PV</label><input data-campo="hp_medio"></div>
        <div class="stat-mini"><label>CA</label><input data-campo="ca"></div>
        <div class="stat-mini"><label>ND</label><input data-campo="nd"></div>
        <div class="stat-mini"><label>Desloc.</label><input data-campo="velocidade_str"></div>
    </div>
    
    <!-- Atributos em linha -->
    <div class="atributos-monstro-row">
        {% for attr, sigla in atributos %}
        <div class="attr-monstro-box">
            <span class="attr-sigla">{{ sigla }}</span>
            <span class="attr-mod-grande">{{ mod }}</span>  <!-- Modificador grande -->
            <input class="attr-valor-input" data-campo="atributos.{{ attr }}">  <!-- Valor pequeno -->
        </div>
        {% endfor %}
    </div>
    
    <!-- Ações dinâmicas -->
    <div class="acoes-compactas">
        <div id="lista-acoes-monstro">
            <!-- .acao-linha com nome/ataque/dano -->
        </div>
        <button onclick="adicionarAcaoMonstro()">+ Ação</button>
    </div>
</div>
```

---

## 3. Instâncias de Monstros (Combate)

### Conceito
- **Monstro** = Template no bestiário
- **Instância** = Cópia específica em combate

### Rotas

| Método | Rota | Função |
|--------|------|--------|
| POST | `/fichas/api/monstro/instancia` | `api_criar_instancia_monstro()` |
| GET | `/fichas/api/monstro/instancia/<id>` | `api_obter_instancia_monstro(id)` |
| PATCH | `/fichas/api/monstro/instancia/<id>` | `api_atualizar_instancia_monstro(id)` |

### Criação de Instância

```python
# InstanciaMonstroRepository.criar_instancia()
def criar_instancia(cls, monstro_id, nome, sessao_id=None):
    # Busca template do monstro
    monstro = MonstroRepository.get_by_id(monstro_id)
    
    # Cria instância com HP inicial
    dados = {
        'monstro_id': monstro_id,
        'sessao_id': sessao_id,
        'nome': nome or f"{monstro['nome']} #{proxima_sequencia}",
        'hp_maximo': monstro['hp_medio'],
        'hp_atual': monstro['hp_medio'],
        'ca': monstro['ca']
    }
    
    return cls.insert(dados)
```

---

## 4. Repository Pattern

### BaseRepository (database.py)

```python
class BaseRepository:
    table_name = ""
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]:
        with get_connection() as conn:
            cursor = conn.execute(
                f"SELECT * FROM {cls.table_name} WHERE id = ?", (id,)
            )
            return dict_from_row(cursor.fetchone())
    
    @classmethod
    def get_all(cls, where: str = None, params: tuple = None) -> List[Dict]:
        with get_connection() as conn:
            sql = f"SELECT * FROM {cls.table_name}"
            if where:
                sql += f" WHERE {where}"
            cursor = conn.execute(sql, params or ())
            return [dict_from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def insert(cls, data: Dict) -> int:
        with get_connection() as conn:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            sql = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})"
            cursor = conn.execute(sql, tuple(data.values()))
            return cursor.lastrowid
    
    @classmethod
    def update(cls, id: int, data: Dict) -> bool:
        with get_connection() as conn:
            sets = ", ".join([f"{k} = ?" for k in data.keys()])
            sql = f"UPDATE {cls.table_name} SET {sets}, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?"
            conn.execute(sql, (*data.values(), id))
            return True
    
    @classmethod
    def delete(cls, id: int) -> bool:
        with get_connection() as conn:
            conn.execute(f"DELETE FROM {cls.table_name} WHERE id = ?", (id,))
            return True
```

### Repositórios Específicos

```python
class PersonagemRepository(BaseRepository):
    table_name = "personagens"
    
    @classmethod
    def criar(cls, dados: Dict) -> Dict:
        dados_db = cls._prepare_for_db(dados)
        id = cls.insert(dados_db)
        return cls.get_by_id(id)
    
    @staticmethod
    def _prepare_for_db(dados: Dict) -> Dict:
        """Serializa campos JSON para armazenamento"""
        json_fields = ['atributos', 'pericias_proficientes', ...]
        result = {}
        for k, v in dados.items():
            if k in json_fields and not isinstance(v, str):
                result[k] = json_dumps(v)
            else:
                result[k] = v
        return result
    
    @staticmethod
    def _parse_json_fields(data: Dict):
        """Deserializa campos JSON após leitura"""
        json_fields = ['atributos', 'pericias_proficientes', ...]
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                data[field] = json_loads_safe(data[field], default)


class MonstroRepository(BaseRepository):
    table_name = "monstros"
    # Similar ao PersonagemRepository
```

---

## 5. Tratamento de Erros

### Backend (API)

```python
@fichas_bp.route('/api/monstro', methods=['POST'])
def api_criar_monstro():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados não recebidos'}), 400
        if not data.get('nome'):
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        
        resultado = MonstroRepository.criar(data)
        return jsonify(resultado)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500
```

### Frontend (JS)

```javascript
async function criarMonstro() {
    const dados = coletarDadosMonstro();
    
    // Validação no cliente
    if (!dados.nome || dados.nome.trim() === '') {
        mostrarNotificacao('❌ Nome é obrigatório', 'danger');
        return;
    }
    
    try {
        const response = await fetch('/fichas/api/monstro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        
        const resultado = await response.json();
        
        if (response.ok && resultado.id) {
            mostrarNotificacao('✅ Criado!', 'success');
            window.location.href = `/fichas/monstro/${resultado.id}`;
        } else {
            console.error('Erro da API:', resultado);
            mostrarNotificacao('❌ ' + (resultado.erro || 'Erro'), 'danger');
        }
    } catch (error) {
        console.error('Erro:', error);
        mostrarNotificacao('❌ Erro de conexão', 'danger');
    }
}
```

---

## 6. Notificações

```javascript
// Função global em base.js
function mostrarNotificacao(mensagem, tipo = 'info') {
    // tipo: success, danger, warning, info
    const container = document.getElementById('notificacoes') || criarContainer();
    
    const notif = document.createElement('div');
    notif.className = `notificacao notificacao-${tipo}`;
    notif.textContent = mensagem;
    container.appendChild(notif);
    
    setTimeout(() => notif.remove(), 3000);
}
```

---

## 7. APIs do Sistema

### API de Dados (Rolagem)

```javascript
// POST /api/dados/rolar
// Body: { expressao: "2d6+3" }
// Response: { expressao, dados: [4, 2], soma: 6, modificador: 3, total: 9 }

const resultado = await API.post('/api/dados/rolar', { expressao: '1d20+5' });
```

### API de Personagens

```javascript
// GET /fichas/api/personagem/{id}
// Response: { id, nome, hp_atual, hp_maximo, atributos, armas, percepcao_passiva, ... }

// PUT /fichas/api/personagem/{id}
// Body: { ...dados completos }

// PATCH /fichas/api/personagem/{id}
// Body: { campo: valor } - atualização parcial

// Dano/Cura
// POST /api/personagens/{id}/dano   Body: { dano: 10 }
// POST /api/personagens/{id}/curar  Body: { quantidade: 5 }
// Response inclui: hp_atual, hp_maximo, sucesso_morte, falha_morte
```

### API de Instâncias de Monstros

```javascript
// POST /fichas/api/monstro/instancia
// Body: { monstro_id, nome?, sessao_id? }

// GET /fichas/api/monstro/instancia/{id}

// PATCH /fichas/api/monstro/instancia/{id}
// Body: { hp_atual, condicoes, ... }

// Dano/Cura
// POST /api/monstros/instancias/{id}/dano  Body: { dano: 10 }
// POST /api/monstros/instancias/{id}/curar Body: { quantidade: 5 }
```

### API de Sessão

```javascript
// POST /sessao/api/log
// Body: { tipo, mensagem, dados: {} }
// Registra ação no log do servidor
```

### Objeto API Global (base.js)

```javascript
const API = {
    async get(url) {
        const response = await fetch(url);
        return response.json();
    },
    
    async post(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async patch(url, data) {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }
};
```
