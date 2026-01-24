# 🗡️ Fuga do Abismo - Sistema de Mestragem D&D 5e

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Flask-3.0+-green?logo=flask" />
  <img src="https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite" />
  <img src="https://img.shields.io/badge/D%26D-5e-red" />
  <img src="https://img.shields.io/badge/License-GPL%20v3-blue" />
</p>

Sistema web local para auxiliar na mestragem de **Dungeons & Dragons 5ª Edição**, desenvolvido especificamente para a campanha **Fuga do Abismo**, mas adaptável para qualquer aventura.

## 📖 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Módulos do Sistema](#-módulos-do-sistema)
- [API REST](#-api-rest)
- [Padrões e Convenções](#-padrões-e-convenções)
- [Regras D&D 5e Implementadas](#-regras-dd-5e-implementadas)
- [Testes Automatizados](#-testes-automatizados)
- [Bugs Conhecidos](#-bugs-conhecidos)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Visão Geral

Este sistema foi criado para **acelerar e organizar** as sessões de RPG, permitindo ao mestre:

- Gerenciar fichas de **personagens**, **monstros** e **NPCs**
- Controlar **combates** com iniciativa, turnos e rounds
- Aplicar **efeitos e condições** D&D 5e com contagem de turnos
- **Rolar ataques automaticamente** com detecção de crítico/falha
- Manter **log de combate** persistente por sessão
- Usar **widgets flutuantes** arrastáveis para organizar informações

O foco é na **agilidade durante a sessão** — edição em tempo real, auto-save, e interface otimizada para uso com mouse.

---

## ✨ Funcionalidades

### 📋 Gerenciamento de Fichas

| Recurso | Descrição |
|---------|-----------|
| **Personagens** | Ficha completa D&D 5e com atributos, perícias, magias, equipamentos |
| **Monstros** | Bestiário com ações, atributos, ND e criação de instâncias para combate |
| **NPCs** | Fichas simplificadas com relacionamentos e status |
| **Auto-save** | Todas as alterações são salvas automaticamente |
| **Observações** | Campo destacado para anotações em cada ficha |
| **Cards Compactos** | Listas visuais com atributos, stats e ações em destaque |

**Novidade**: Listas de personagens, monstros e NPCs agora exibem **cards compactos** com:
- Grid de 6 atributos (FOR, DES, CON, INT, SAB, CAR) com modificadores calculados
- Stats principais (HP/CA para personagens, ND para monstros, status para NPCs)
- Preview de ataques/ações mais importantes
- Cores e badges visuais (nível, ND, status de NPC)
- Alertas de HP baixo/crítico para personagens

### ⚔️ Sistema de Combate

| Recurso | Descrição |
|---------|-----------|
| **Iniciativa** | Rolagem automática (1d20 + mod DES), editável por clique |
| **Turnos** | Controle de ordem com destaque visual do turno atual |
| **Contador Inteligente** | Funciona com 0, 1 ou múltiplos participantes |
| **Ataques** | Clique para rolar d20 + bônus, detecta crítico (20) e falha (1) |
| **Dano** | Rolagem automática com tipos de dano coloridos |
| **Crítico** | Dobra automaticamente os dados de dano 🎯 |
| **Testes de Morte** | Aparecem quando HP ≤ 0, marca "💀 MORTO" com 3 falhas |
| **Dano/Cura Rápida** | Botões para aplicar valores diretamente |

**Novidade**: Sistema de turnos agora funciona corretamente mesmo sem participantes ou com apenas 1 combatente, incrementando o contador a cada clique.

### 🖼️ Cenários e Mapas

| Recurso | Descrição |
|---------|-----------|
| **Drag-and-Drop** | Arraste imagens diretamente para a tela de sessão |
| **Upload Automático** | Imagens são salvas em `Imagens/Cenários/` |
| **Modal de Seleção** | Galeria com thumbnails de todos os cenários |
| **Persistência** | Cenário atual é salvo e restaurado entre sessões |
| **Formatos** | Suporta PNG, JPG, JPEG, WEBP, GIF |
| **Duplicatas** | Sistema adiciona sufixo numérico automaticamente |

**Novidade**: Sistema completo de cenários com drag-and-drop, modal de seleção visual e persistência automática.

### 🎭 Efeitos e Condições D&D 5e

Todas as 15 condições do Livro do Jogador + tipos de dano persistentes:

- Agarrado, Amedrontado, Atordoado, Caído, Cego
- Enfeitiçado, Envenenado, Incapacitado, Inconsciente, Invisível
- Paralisado, Petrificado, Restringido, Surdo, Exaustão (6 níveis)
- Danos contínuos: Ácido, Ígneo, Venenoso, etc.

Cada efeito pode ter:
- **Contador de turnos** (decrementa automaticamente)
- **Descrição opcional** (ex: "Magia Sleep do mago")
- **Tooltip** quando commouse em cima mostra regras do efeito

### 🖼️ Widgets Flutuantes

| Widget | Função |
|--------|--------|
| **Ficha de Personagem** | Mini-ficha com HP, CA, atributos, ações, efeitos |
| **Ficha de Monstro** | Instância com HP individual, ações rápidas |
| **Iniciativa** | Ordem de turnos com controles |
| **Log de Combate** | Histórico de ações (horário no hover) |
| **Dados** | Rolador de expressões (2d6+3, 1d20, etc.) |

Recursos dos widgets:
- **Arrastar** pelo header
- **Redimensionar** pelos cantos
- **Minimizar** com botão
- **Fechar** com X ou middle-click no header
- **Posicionamento inteligente** (não sobrepõe outros)

### 📜 Sistema de Sessões

- **Persistência automática** em arquivos JSON
- **Histórico de sessões** com dropdown na navbar
- **Restauração de estado** (widgets, combate, log)
- **Nova sessão automática** quando a data muda
- **Save automático** a cada 10 segundos

### 🎲 Tipos de Dano

13 tipos com cores e ícones visuais:

| Tipo | Cor | Descrição |
|------|-----|-----------|
| 🧪 Ácido | Verde-amarelo | Corrosão química |
| 🔨 Contundente | Marrom | Impacto físico |
| ⚔️ Cortante | Prata | Lâminas e cortes |
| ⚡ Elétrico | Azul claro | Choque e raios |
| 💫 Energético | Roxo | Força mágica pura |
| ❄️ Gélido | Azul gelo | Frio extremo |
| 🔥 Ígneo | Vermelho | Fogo e calor |
| 💀 Necrótico | Índigo | Energia vital |
| 🗡️ Perfurante | Cinza | Perfuração |
| 🧠 Psíquico | Orquídea | Dano mental |
| ✨ Radiante | Dourado | Luz divina |
| 🌩️ Trovejante | Azul royal | Ondas sonoras |
| ☠️ Venenoso | Verde limão | Toxinas |

---

## 📁 Estrutura do Projeto

```
System/
├── main.py                 # Entry point - inicia o servidor Flask
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
│
├── app/                    # Aplicação Flask
│   ├── __init__.py         # Factory create_app()
│   ├── config.py           # Configurações (debug, secret_key, etc.)
│   │
│   ├── modulos/            # Lógica de negócio
│   │   ├── database.py     # Conexão SQLite + BaseRepository
│   │   ├── db_init.py      # Inicialização e população do banco
│   │   ├── repositories.py # Repositórios (Personagem, Monstro, NPC, Sessao)
│   │   ├── regras_base.py  # Cálculos D&D (modificadores, CA, bônus)
│   │   ├── regras_dnd_data.py # Dados estáticos (raças, classes, perícias)
│   │   ├── combate.py      # Motor de combate
│   │   ├── acoes.py        # Ações de combate (ataque, dano)
│   │   ├── condicoes.py    # Gerenciamento de condições
│   │   └── dados.py        # Rolagem de dados e expressões
│   │
│   ├── routes/             # Blueprints Flask (rotas)
│   │   ├── main.py         # / e /config
│   │   ├── fichas.py       # /fichas/* (personagens, monstros, NPCs)
│   │   ├── api.py          # /api/* (dados, regras)
│   │   ├── sessao.py       # /sessao/* (gerenciamento de sessões)
│   │   └── combate.py      # /combate/* (rotas de combate)
│   │
│   └── static/             # Arquivos estáticos
│       ├── css/
│       │   ├── base.css    # Estilos globais, tema, variáveis
│       │   ├── fichas.css  # Fichas de personagem
│       │   ├── monstros.css # Fichas de monstro
│       │   ├── sessao.css  # Tela de sessão, widgets, combate
│       │   └── widgets.css # Sistema de widgets
│       │
│       └── js/
│           ├── base.js     # Utilitários, API, modais, notificações
│           ├── fichas.js   # CRUD de fichas, auto-save, point buy
│           ├── sessao.js   # Combate, efeitos, ataques, turnos
│           └── widgets.js  # Classes Widget e WidgetManager
│
├── templates/              # Templates Jinja2
│   ├── base.html           # Layout base com navbar
│   ├── index.html          # Página inicial
│   ├── config.html         # Configurações
│   ├── erro.html           # Página de erro
│   │
│   ├── fichas/
│   │   ├── personagem.html # Ficha completa de PC
│   │   ├── monstro.html    # Ficha de monstro
│   │   ├── npc.html        # Ficha de NPC
│   │   ├── lista_personagens.html  # Cards compactos com atributos/stats
│   │   ├── lista_monstros.html     # Cards compactos com ND/ações
│   │   └── lista_npcs.html         # Cards compactos com status/local
│   │
│   ├── sessao/
│   │   └── tela_sessao.html # Tela principal de sessão + drag-drop
│   │
│   └── widgets/
│       ├── ficha_personagem.html
│       └── ficha_monstro.html
│
├── data/                   # Dados persistentes
│   ├── campaign.db         # Banco SQLite (gerado automaticamente)
│   ├── personagens.json    # Backup/export
│   └── sessoes/            # Arquivos de sessão
│       ├── indice_sessoes.json
│       ├── sessao_1.json
│       └── ...
│
├── config/                 # Scripts de inicialização
│   ├── run_system.bat
│   └── run_system.ps1
│
└── tests/                  # Testes automatizados
    ├── __init__.py
    └── test_sistema_completo.py  # Suite completa (87 testes)
```

**Pastas Externas ao System**:
```
Imagens/
└── Cenários/              # Mapas e cenários de sessão (auto-criada)
    ├── Caverna.png
    ├── Mercado_Noite.png
    └── ...
```

---

## 🛠️ Tecnologias

### Backend
- **Python 3.10+** - Linguagem principal
- **Flask 3.0+** - Framework web
- **SQLite 3** - Banco de dados local (modo WAL)
- **Jinja2** - Engine de templates

### Frontend
- **HTML5** - Estrutura semântica
- **CSS3** - Variáveis CSS, Grid, Flexbox
- **JavaScript ES6+** - Vanilla JS, async/await, classes
- **Fetch API** - Requisições assíncronas

### Padrões
- **Repository Pattern** - Acesso a dados
- **Blueprint Pattern** - Organização de rotas Flask
- **BEM-like** - Nomenclatura CSS

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonar o repositório)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/necromod/Out-Of-Abyss.git
cd Out-Of-Abyss/System
```

2. **Crie um ambiente virtual**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o sistema**
```bash
python main.py
```

5. **Acesse no navegador**
```
http://127.0.0.1:5000
```

### Estrutura de Dependências

```txt
Flask>=3.0.0
```

O sistema usa bibliotecas padrão do Python para o restante (sqlite3, json, datetime, etc.).

---

## 📖 Como Usar

### Página Inicial
- Acesse `http://127.0.0.1:5000`
- Use a navbar para navegar entre Personagens, Monstros, NPCs e Sessão

### Criando um Personagem
1. Vá em **Fichas > Personagens**
2. Clique em **+ Novo Personagem**
3. Preencha os dados (nome, raça, classe, atributos)
4. Use **Point Buy** ou distribua manualmente
5. O sistema salva automaticamente

### Adicionando Monstros
1. Vá em **Fichas > Monstros**
2. Clique em **+ Novo Monstro**
3. Preencha as informações básicas
4. Adicione ações com **+ Adicionar Ação**

### Usando a Tela de Sessão
1. Vá em **Sessão**
2. Use os botões na navbar para adicionar widgets:
   - 👤 Ficha de Personagem
   - 👹 Adicionar Monstro
   - ⏱️ Iniciativa
   - 📜 Log de Combate
   - 🎲 Dados
   - 🗺️ Selecionar Cenário

### Adicionando Cenários
1. **Arraste** uma imagem diretamente para a tela de sessão, ou
2. Clique no botão **🗺️** na navbar
3. Selecione um cenário da galeria
4. O cenário é persistido e restaurado nas próximas sessões
5. Clique no **✕** para remover o cenário

### Iniciando Combate
1. Adicione criaturas clicando no botão ⚔️ em cada widget
2. Clique no botão de combate na navbar
3. O sistema rola iniciativa automaticamente
4. Use **Próximo** para avançar turnos
   - Funciona mesmo sem participantes ou com apenas 1

### Rolando Ataques
1. Clique no botão de ataque no widget da criatura
2. O sistema rola 1d20 + bônus
3. Em caso de acerto, rola o dano automaticamente
4. Crítico (20) dobra os dados de dano
5. Falha crítica (1) não rola dano

### Aplicando Efeitos
1. Clique em **+ Efeito** no widget
2. Selecione a condição
3. Defina a duração em turnos (0 = permanente)
4. Opcional: adicione descrição

---

## 🧩 Módulos do Sistema

### database.py
Gerencia conexão com SQLite e provê a classe `BaseRepository`:
- `get_connection()` - Context manager para conexões
- `dict_from_row()` - Converte Row para Dict
- `json_dumps/loads_safe()` - Serialização JSON segura

### repositories.py
Repositórios para cada entidade:
- `PersonagemRepository` - CRUD + campos JSON complexos
- `MonstroRepository` - Bestiário com buscas
- `InstanciaMonstroRepository` - Monstros em combate
- `NpcRepository` - NPCs da campanha
- `SessaoRepository` - Gerenciamento de sessões

### regras_base.py
Cálculos D&D 5e:
- `calcular_modificador(valor)` - (valor - 10) // 2
- `calcular_bonus_proficiencia(nivel)` - 2 + ((nivel-1)//4)
- `calcular_ca_base(mod_destreza)` - 10 + mod

### dados.py
Rolagem de dados:
- `rolar(faces)` - Rola um dado
- `rolar_expressao(expr)` - Parseia "2d6+3", retorna detalhes

### sessao.js
Estado e lógica de combate:
- `SessaoState` - Estado global da sessão (turnos, widgets, mapa)
- `CONDICOES_DND` - 15 condições + tipos de dano
- `proximoTurno()` - Avança turno (0, 1 ou N participantes)
- `aplicarCenario()` - Carrega imagem de cenário na tela
- `restaurarEstado()` - Restaura sessão salva (widgets, combate, mapa)
- `rolarAtaque()` - Ataque com crítico/falha
- `adicionarEfeito()` - Sistema de efeitos
- `proximoTurno()` - Avança combate

### widgets.js
Sistema de widgets flutuantes:
- `Widget` - Classe base (arrastar, redimensionar, minimizar)
- `WidgetManager` - Gerencia instâncias, salva/restaura estado

---

## 🔌 API REST

### Personagens
```
GET    /fichas/api/personagens          # Lista todos
GET    /fichas/api/personagem/:id       # Obtém um
POST   /fichas/api/personagem           # Cria novo
PUT    /fichas/api/personagem/:id       # Atualiza completo
PATCH  /fichas/api/personagem/:id       # Atualiza parcial
DELETE /fichas/api/personagem/:id       # Remove
```

### Monstros
```
GET    /api/monstros                    # Lista todos
GET    /fichas/api/monstro/:id          # Obtém um
POST   /fichas/api/monstro              # Cria novo
PUT    /fichas/api/monstro/:id          # Atualiza
POST   /fichas/api/monstro/instancia    # Cria instância para combate
PATCH  /fichas/api/monstro/instancia/:id # Atualiza instância
```

### Sessão
```
GET    /sessao/api/sessao/atual         # Sessão atual
POST   /sessao/api/sessao/nova          # Cria nova sessão
PUT    /sessao/api/sessao/:id           # Salva estado
GET    /sessao/api/sessao/:id           # Carrega sessão
GET    /sessao/api/sessoes              # Lista todas
```

### Dados
```
POST   /api/dados/rolar                 # {expressao: "2d6+3"}
GET    /api/regras/dnd                  # Dados de regras D&D
```

---

## 📐 Padrões e Convenções

### Python
```python
# Tipagem quando possível
def funcao(param: str, opcional: int = 0) -> Dict[str, Any]:

# Docstrings em funções públicas
"""Descrição breve da função."""

# snake_case para funções e variáveis
def calcular_modificador(valor):

# PascalCase para classes
class PersonagemRepository(BaseRepository):
```

### JavaScript
```javascript
// camelCase para funções
function rolarAtaque(event, nomeAtacante, ...) { }

// UPPER_SNAKE_CASE para constantes
const CONDICOES_DND = { ... };

// async/await para requisições
async function salvarPersonagem() {
    const response = await API.post('/api/...', dados);
}
```

### CSS
```css
/* Variáveis globais no :root */
:root {
    --ficha-bg: #1a1a2e;
    --ficha-accent: #e94560;
}

/* BEM-like para componentes */
.widget-personagem-conteudo { }
.widget-personagem-header { }
.btn-acao { }
```

### Banco de Dados
- Tabelas em plural snake_case: `personagens`, `monstros`
- Colunas em snake_case: `hp_atual`, `bonus_proficiencia`
- Campos complexos em JSON: `atributos`, `armas`, `condicoes`

---

## 🎲 Regras D&D 5e Implementadas

### Cálculos Automáticos
- **Modificador de atributo**: (valor - 10) // 2
- **Bônus de proficiência**: 2 + ((nível - 1) // 4)
- **Percepção Passiva**: 10 + mod SAB (+ proficiência se aplicável)
- **Iniciativa**: 1d20 + mod DES

### Sistema de Ataque
- Rola 1d20 + bônus de ataque
- **Crítico (20)**: Dobra todos os dados de dano
- **Falha Crítica (1)**: Ataque erra automaticamente

### Testes de Morte
- Aparecem quando HP ≤ 0
- 3 sucessos = estabiliza
- 3 falhas = morre
- Botão de reset disponível

### Condições
Todas as 15 condições do PHB com:
- Descrição das regras
- Contador de turnos (decrementa a cada turno)
- Remoção automática quando expira

---

## � Testes Automatizados

O sistema inclui uma suite completa de testes em `tests/test_sistema_completo.py`.

### Executando os Testes

```bash
# Na raiz do projeto (Out Of Abyss/)
# Ativar ambiente virtual primeiro
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac

# Rodar todos os testes
python -m pytest System/tests/test_sistema_completo.py -v

# Rodar apenas uma classe de testes
python -m pytest System/tests/test_sistema_completo.py::TestAPIRest -v

# Rodar com relatório resumido
python -m pytest System/tests/test_sistema_completo.py --tb=short
```

### Classes de Teste

| Classe | Testes | Descrição |
|--------|--------|-----------|
| **TestRegrasDnD** | 6 | Modificadores, bônus de proficiência, CA, iniciativa, percepção passiva |
| **TestRolagemDados** | 7 | d6, d20, d100, expressões complexas, críticos |
| **TestRepositorios** | 17 | CRUD de personagens, monstros, instâncias, NPCs |
| **TestAPIRest** | 15 | Endpoints GET/POST/PUT/DELETE |
| **TestRotasPaginas** | 9 | Páginas HTML (listas, fichas, sessão) |
| **TestValidacaoDados** | 5 | Validação de atributos, níveis, ND, expressões |
| **TestFluxosCompletos** | 3 | Criar→editar→deletar, combate, sessão |
| **TestEstruturaArquivos** | 11 | Verificação de arquivos e pastas necessários |
| **TestIntegridadeBanco** | 4 | Tabelas e colunas SQLite |
| **TestBugsConhecidos** | 2 | Documenta bugs descobertos |
| **TestWidgetsInterface** | 3 | Widgets de sessão |
| **TestPerformance** | 3 | Tempo de resposta (< 2s) |

**Total: 87 testes** (83 passam, 4 pulados por bugs conhecidos)

### Requisitos para Testes

```bash
pip install pytest requests
```

O servidor Flask **deve estar rodando** em `http://127.0.0.1:5000` para os testes de API e páginas funcionarem.

### Cobertura dos Testes

Os testes cobrem:
- ✅ Regras D&D 5e (cálculos matemáticos)
- ✅ Rolagem de dados (expressões, críticos)
- ✅ Repositórios (CRUD completo)
- ✅ API REST (todos os endpoints principais)
- ✅ Páginas HTML (status codes)
- ✅ Validação de dados
- ✅ Fluxos completos de uso
- ✅ Estrutura de arquivos do projeto
- ✅ Integridade do banco de dados
- ✅ Performance básica

---

## 🎨 Visual e UX

### Cards Compactos
Todas as listas de entidades usam o mesmo padrão visual:
- **Personagens**: Header com nível, grid de atributos 6 cols, stats (HP/CA/PP), lista de armas
- **Monstros**: Header com ND, grid de atributos 6 cols, stats (CA/HP/XP), lista de ações
- **NPCs**: Header com status badge, local, descrição, relacionamento, tags (morto/vivo)

### Sistema de Cores
- **Aliado** (NPC): Verde (#4ade80)
- **Hostil** (NPC): Vermelho (#ef4444)
- **Neutro** (NPC): Amarelo (#fbbf24)
- **HP Crítico** (≤25%): Vermelho com gradiente
- **HP Baixo** (≤50%): Amarelo com gradiente
- **ND Lendário**: Roxo (#8b5cf6)
- **ND Muito Alto**: Vermelho (#dc2626)
- **ND Alto**: Laranja (#ea580c)
- **ND Médio**: Amarelo (#ca8a04)

---

## 🐛 Bugs Conhecidos

Os seguintes bugs foram identificados durante os testes e estão documentados:

### BUG #1: Coluna `atualizado_em` faltando em `monstros_instancias`

**Localização:** `app/modulos/database.py` (linha ~678)

**Problema:** O método `BaseRepository.update()` sempre tenta atualizar a coluna `atualizado_em`, mas a tabela `monstros_instancias` não possui essa coluna.

**Impacto:** Falha ao atualizar instâncias de monstros via `InstanciaMonstroRepository.update()`.

**Workaround:** Use `atualizar_campo()` ou métodos específicos ao invés de `update()` genérico.

**Correção pendente:** Adicionar coluna `atualizado_em` na tabela `monstros_instancias` ou modificar `BaseRepository.update()` para verificar se a coluna existe.

### BUG #2: Templates de Widget assumem atributos como inteiros

**Localização:** `templates/widgets/ficha_personagem.html` (linha ~39)

**Problema:** O template faz operação aritmética `(personagem.atributos[attr] - 10) // 2`, mas quando os atributos são armazenados como strings no JSON, ocorre TypeError.

**Impacto:** Widgets de personagem podem falhar ao carregar se os atributos não forem convertidos para inteiros.

**Workaround:** Garantir que os atributos sejam salvos como inteiros no banco, não como strings.

**Correção pendente:** Adicionar filtro Jinja2 `|int` ou converter no backend antes de enviar ao template.

### Status dos Bugs

| Bug | Severidade | Status |
|-----|------------|--------|
| #1 | Média | Documentado, workaround disponível |
| #2 | Baixa | Documentado, workaround disponível |

Os testes marcam esses bugs como **skipped** ao invés de falhar, para não bloquear a execução da suite de testes.

---

## �🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes

---

## 📄 Licença

Este projeto está licenciado sob a **GNU General Public License v3.0** - veja o arquivo [LICENSE](../LICENSE).

### O que isso significa:

✅ **Você PODE:**
- Usar o software para qualquer propósito
- Modificar o código fonte
- Distribuir cópias
- Distribuir versões modificadas

⚠️ **Você DEVE:**
- Incluir o código fonte ao distribuir
- Manter a mesma licença GPL v3 em derivados
- Documentar mudanças feitas no código
- Incluir o aviso de copyright original

❌ **Você NÃO PODE:**
- Usar em software proprietário/fechado
- Sublicenciar sob outra licença
- Responsabilizar o autor por danos

```
Fuga do Abismo - Sistema de Mestragem D&D 5e
Copyright (C) 2026 necromod

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

---

## 🙏 Agradecimentos

- **Wizards of the Coast** - Por D&D 5e e a campanha Out of the Abyss
- **Comunidade de RPG** - Pela inspiração
- **Flask** - Framework web incrível

---

<p align="center">
  <strong>Boas aventuras no Underdark! 🕯️</strong>
</p>
