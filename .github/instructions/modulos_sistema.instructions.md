---
applyTo: "**"
---

# Módulos do Sistema - Referência Rápida

Descrição de cada módulo Python e seu propósito.

---

## 1. database.py

**Caminho:** `app/modulos/database.py`

**Responsabilidades:**
- Conexão com SQLite
- Context manager `get_connection()`
- Inicialização de tabelas `init_database()`
- Classe base `BaseRepository` para CRUD
- Funções de serialização JSON

**Funções Principais:**

```python
# Conexão
from app.modulos.database import get_connection
with get_connection() as conn:
    cursor = conn.execute("SELECT * FROM tabela")

# Conversão de Row para Dict
from app.modulos.database import dict_from_row
data = dict_from_row(cursor.fetchone())

# JSON
from app.modulos.database import json_dumps, json_loads_safe
json_str = json_dumps({"key": "value"})
obj = json_loads_safe(json_str, default={})

# Inicialização
from app.modulos.database import init_database
init_database()  # Cria todas as tabelas
```

**BaseRepository:**
```python
class BaseRepository:
    table_name = ""
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]
    
    @classmethod
    def get_all(cls, where: str = None, params: tuple = None) -> List[Dict]
    
    @classmethod
    def insert(cls, data: Dict) -> int  # Retorna ID inserido
    
    @classmethod
    def update(cls, id: int, data: Dict) -> bool
    
    @classmethod
    def delete(cls, id: int) -> bool
```

---

## 2. repositories.py

**Caminho:** `app/modulos/repositories.py`

**Responsabilidades:**
- Repositórios específicos por entidade
- Parse/prepare de campos JSON
- Métodos de busca especializados

**Classes:**

### PersonagemRepository
```python
from app.modulos.repositories import PersonagemRepository

# Criar
p = PersonagemRepository.criar({'nome': 'Guerreiro', 'classe': 'Guerreiro'})

# Buscar
p = PersonagemRepository.get_by_id(1)
todos = PersonagemRepository.get_all_ativos()

# Atualizar
PersonagemRepository.atualizar(1, {'hp_atual': 25})
PersonagemRepository.atualizar_campo(1, 'atributos.forca', 18)

# Combate
PersonagemRepository.aplicar_dano(1, 10)
PersonagemRepository.curar(1, 5)

# Campos JSON tratados automaticamente:
# atributos, pericias_proficientes, pericias_expertise,
# salvaguardas_proficientes, armas, equipamentos, moedas,
# espacos_magia, espacos_usados, magias_conhecidas, magias_preparadas,
# dados_vida_tipos, condicoes

# Estrutura de armas (formato novo):
# [{ nome, bonus, dados[], tipo }]
```

### MonstroRepository
```python
from app.modulos.repositories import MonstroRepository

# CRUD básico
m = MonstroRepository.criar({'nome': 'Goblin', 'nd': 0.25})
m = MonstroRepository.get_by_id(1)
todos = MonstroRepository.get_all()

# Buscas
MonstroRepository.buscar_por_nome('gob')  # Busca parcial
MonstroRepository.buscar_por_nd(0, 2)     # Faixa de ND
```

### InstanciaMonstroRepository
```python
from app.modulos.repositories import InstanciaMonstroRepository

# Criar instância para combate
inst = InstanciaMonstroRepository.criar_instancia(
    monstro_id=1, 
    nome='Goblin #1',
    sessao_id=1
)

# Obter com dados do template
inst = InstanciaMonstroRepository.get_completo(inst_id)
```

### NpcRepository
```python
from app.modulos.repositories import NpcRepository

npc = NpcRepository.criar({'nome': 'Mercador', 'localizacao': 'Cidade'})
npcs = NpcRepository.get_all()
```

### SessaoRepository
```python
from app.modulos.repositories import SessaoRepository

sessao = SessaoRepository.criar_sessao()  # Auto-incrementa número
atual = SessaoRepository.get_sessao_atual()
```

---

## 3. regras_base.py

**Caminho:** `app/modulos/regras_base.py`

**Responsabilidades:**
- Cálculos D&D 5e
- Modificadores de atributos
- Bônus de proficiência
- Classe de Armadura

**Funções:**

```python
from app.modulos.regras_base import (
    calcular_modificador,
    calcular_bonus_proficiencia,
    calcular_ca_base,
    calcular_iniciativa
)

# Modificador: (valor - 10) // 2
mod = calcular_modificador(16)  # +3

# Bônus de proficiência por nível
bonus = calcular_bonus_proficiencia(5)  # +3

# CA base
ca = calcular_ca_base(14)  # 10 + mod_des = 12

# Iniciativa
init = calcular_iniciativa(14, bonus_extra=2)  # mod_des + bonus
```

---

## 4. regras_dnd_data.py

**Caminho:** `app/modulos/regras_dnd_data.py`

**Responsabilidades:**
- Dados estáticos D&D 5e
- Popular tabelas de raças, classes, perícias
- Condições do D&D

**Uso:**
```python
from app.modulos.regras_dnd_data import popular_regras_dnd

# Popula tabelas: racas, classes, pericias, condicoes_dnd
popular_regras_dnd()
```

---

## 5. db_init.py

**Caminho:** `app/modulos/db_init.py`

**Responsabilidades:**
- Popular dados iniciais
- Monstros do Underdark
- NPCs da campanha Out of the Abyss
- Configurações padrão

**Uso:**
```python
from app.modulos.db_init import inicializar_banco

# Cria tabelas e popula dados iniciais
inicializar_banco()
```

---

## 6. dados.py

**Caminho:** `app/modulos/dados.py`

**Responsabilidades:**
- Rolagem de dados
- Parser de expressões (2d6+3)
- Registro de rolagens

**Funções:**
```python
from app.modulos.dados import rolar, rolar_expressao

# Rolar dados simples
resultado = rolar(6)  # 1d6

# Rolar expressão complexa
resultado = rolar_expressao('2d6+3')
# Retorna: {'expressao': '2d6+3', 'dados': [4, 2], 'soma': 6, 'modificador': 3, 'total': 9}

# Com vantagem/desvantagem
resultado = rolar_expressao('1d20', vantagem=True)
```

---

## 7. combate.py

**Caminho:** `app/modulos/combate.py`

**Responsabilidades:**
- Gerenciamento de combate
- Ordem de iniciativa
- Controle de turnos

**Classes:**
```python
from app.modulos.combate import GerenciadorCombate

combate = GerenciadorCombate(sessao_id=1)

# Adicionar participantes
combate.adicionar_participante('personagem', 1, iniciativa=15)
combate.adicionar_participante('monstro_instancia', 5, iniciativa=12)

# Controle
combate.iniciar()
combate.proximo_turno()
atual = combate.get_turno_atual()
combate.finalizar()
```

---

## 8. acoes.py

**Caminho:** `app/modulos/acoes.py`

**Responsabilidades:**
- Resolução de ações de combate
- Ataques
- Aplicação de dano/cura

**Funções:**
```python
from app.modulos.acoes import realizar_ataque, aplicar_dano

# Ataque
resultado = realizar_ataque(
    atacante_tipo='personagem',
    atacante_id=1,
    alvo_tipo='monstro_instancia',
    alvo_id=5,
    bonus_ataque=5,
    expressao_dano='1d8+3'
)

# Dano direto
aplicar_dano(tipo='monstro_instancia', id=5, dano=10)
```

---

## 9. condicoes.py

**Caminho:** `app/modulos/condicoes.py`

**Responsabilidades:**
- Gerenciamento de condições D&D
- Aplicar/remover condições
- Efeitos mecânicos

**Funções:**
```python
from app.modulos.condicoes import aplicar_condicao, remover_condicao, get_condicoes

# Aplicar condição
aplicar_condicao(tipo='personagem', id=1, condicao='envenenado')

# Remover
remover_condicao(tipo='personagem', id=1, condicao='envenenado')

# Listar ativas
condicoes = get_condicoes(tipo='personagem', id=1)
```

---

## Blueprints (routes/)

### main.py
- `/` - Página inicial
- `/config` - Configurações

### fichas.py
- `/fichas/personagens` - Lista de PCs
- `/fichas/personagem/<id>` - Ficha de PC
- `/fichas/monstros` - Bestiário
- `/fichas/monstro/<id>` - Ficha de monstro
- `/fichas/npcs` - Lista de NPCs
- `/fichas/api/*` - APIs JSON

### sessao.py
- `/sessao` - Tela de sessão
- `/sessao/api/*` - APIs de sessão

### combate.py
- `/combate` - Tela de combate
- `/combate/api/*` - APIs de combate

### api.py
- APIs gerais e utilitárias

---

## Estrutura de Static

### CSS
| Arquivo | Uso |
|---------|-----|
| `base.css` | Estilos globais, variáveis, layout base |
| `fichas.css` | Fichas de personagem, atributos, HP |
| `monstros.css` | Fichas de monstro, layout compacto |
| `sessao.css` | Tela de sessão, iniciativa, efeitos, testes de morte |
| `widgets.css` | Componentes de widgets flutuantes |

### JS
| Arquivo | Uso |
|---------|-----|
| `base.js` | Funções globais, notificações, utilitários |
| `fichas.js` | CRUD de personagens, coleta de dados, auto-save, iniciativa |
| `sessao.js` | Lógica de sessão, combate, turnos, efeitos D&D 5e |
| `widgets.js` | Classe Widget e WidgetManager, arrastar, redimensionar |

---

## 10. widgets.js

**Caminho:** `app/static/js/widgets.js`

**Responsabilidades:**
- Classe `Widget` - Blocos flutuantes
- Classe `WidgetManager` - Gerenciamento de widgets
- Arrastar, redimensionar, minimizar, fechar
- Middle-click no header fecha widget

**Classes Principais:**
```javascript
class Widget {
    constructor(options) { }
    criar() { }           // Cria elemento DOM
    setupDrag(header) { } // Configura arraste
    fechar() { }          // Remove widget
    minimizar() { }       // Toggle minimizado
    setConteudo(html) { } // Atualiza conteúdo
    trazerParaFrente() { }
}

class WidgetManager {
    criar(options) { }    // Cria novo widget
    remover(id) { }       // Remove widget
    salvarEstado() { }    // Serializa para salvar
    restaurarEstado() { } // Restaura de salvamento
}
```

---

## 11. sessao.js

**Caminho:** `app/static/js/sessao.js`

**Responsabilidades:**
- Estado da sessão (`SessaoState`)
- Sistema de combate (turnos, rounds)
- Sistema de ataques com rolagem automática
- Condições D&D 5e (`CONDICOES_DND`)
- Widgets de personagem/monstro
- Dano/cura rápida
- Testes de morte
- Log de combate formatado

**Estado Global:**
```javascript
const SessaoState = {
    combateAtivo: false,
    ordemTurnos: [],    // [{tipo, id, nome, iniciativa, modDestreza, efeitos}]
    turnoAtual: 0,
    roundAtual: 0,      // 0 = fora de combate, 1+ = em combate
    contadorMonstros: {},
    logCombate: []      // Histórico de ações
};
```

**Funções Principais:**
```javascript
// Combate
iniciarCombate()          // Inicia combate, ordena turnos
proximoTurno()            // Avança turno, incrementa round se necessário
finalizarCombate()        // Encerra combate
adicionarAosTurnos(tipo, id, nome, iniciativa, modDestreza)
editarIniciativa(event, index)

// Ataques (rola automaticamente ao clicar)
rolarAtaque(event, nomeAtacante, nomeAtaque, bonusAtaque, dados, tipoDano)
// Rola 1d20+bonus, detecta crítico/falha, rola dano (dobrado em crit)

// Log de Combate
adicionarLogCombate(mensagem, tipo)  // tipo: info, ataque, crit, fumble, dano, cura
atualizarWidgetLog()

// Widgets de ficha
carregarPersonagemWidget(widgetId, personagemId)
gerarHTMLPersonagemWidget(p)  // Inclui PP: 👁{percepcaoPassiva}
atualizarWidgetCriatura(tipo, id, dadosAtualizados)

// Dano/Cura
abrirDanoRapido(event, id, nome, tipo)
abrirCuraRapida(event, id, nome, tipo)

// Efeitos D&D 5e
abrirModalEfeito(event, tipo, id)  // Modal com style="display: flex;"
adicionarEfeito(tipo, id)
removerEfeito(btn)  // Recebe o botão clicado
atualizarContadoresEfeitos()  // Decrementa turnos, remove expirados

// Testes de Morte
marcarTesteMorte(event, id, tipo, valor)
```

**Constante de Condições:**
```javascript
const CONDICOES_DND = {
    'agarrado': { nome: 'Agarrado', descricao: '...' },
    'amedrontado': { nome: 'Amedrontado', descricao: '...' },
    // ... todas as 15 condições D&D 5e
};
```

