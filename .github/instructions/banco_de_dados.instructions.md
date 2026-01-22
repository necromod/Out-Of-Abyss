---
applyTo: "**/*.py,**/*.sql,**/database*,**/repositories*,**/db_init*"
---

# Estrutura do Banco de Dados - Out of the Abyss System

SQLite com WAL mode | Arquivo: `System/data/campaign.db`

---

## Configuração do SQLite

```python
# Pragmas aplicados em toda conexão (database.py)
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging
conn.execute("PRAGMA synchronous = NORMAL")
```

---

## Tabelas Principais

### 1. `personagens` - Fichas de PCs

| Coluna | Tipo | Padrão | Descrição |
|--------|------|--------|-----------|
| `id` | INTEGER | AUTO | PK |
| `nome` | TEXT | NOT NULL | Nome do personagem |
| `jogador` | TEXT | | Nome do jogador |
| `raca` | TEXT | | Raça do personagem |
| `classe` | TEXT | | Classe principal |
| `nivel` | INTEGER | 1 | Nível atual |
| `antecedente` | TEXT | | Antecedente |
| `alinhamento` | TEXT | | Alinhamento moral |
| `atributos` | TEXT/JSON | `{forca:10,...}` | 6 atributos |
| `hp_maximo` | INTEGER | 10 | HP máximo |
| `hp_atual` | INTEGER | 10 | HP atual |
| `hp_temporario` | INTEGER | 0 | HP temporário |
| `ca` | INTEGER | 10 | Classe de Armadura |
| `ca_bonus` | INTEGER | 0 | Bônus de CA |
| `velocidade` | TEXT | '9m' | Velocidade de movimento |
| `iniciativa_bonus` | INTEGER | 0 | Bônus de iniciativa |
| `inspiracao` | INTEGER | 0 | Pontos de inspiração |
| `pericias_proficientes` | TEXT/JSON | `[]` | Lista de perícias |
| `pericias_expertise` | TEXT/JSON | `[]` | Perícias com expertise |
| `salvaguardas_proficientes` | TEXT/JSON | `[]` | Salvaguardas proficientes |
| `dados_vida` | TEXT | '1d8' | Dado de vida base |
| `dados_vida_restantes` | INTEGER | 1 | Dados de vida disponíveis |
| `dados_vida_tipos` | TEXT/JSON | `[{qtd,faces}]` | Para multiclasse |
| `conjurador` | INTEGER | 0 | Se é conjurador |
| `atributo_conjuracao` | TEXT | | INT/SAB/CAR |
| `espacos_magia` | TEXT/JSON | `{}` | Slots por nível |
| `espacos_usados` | TEXT/JSON | `{}` | Slots gastos |
| `magias_conhecidas` | TEXT/JSON | `[]` | Lista de magias |
| `magias_preparadas` | TEXT/JSON | `[]` | Magias preparadas |
| `equipamento` | TEXT/JSON | `[]` | Lista de itens (legado) |
| `equipamentos` | TEXT/JSON | `[]` | Lista de equipamentos |
| `armas` | TEXT/JSON | `[]` | Lista de armas |
| `moedas` | TEXT/JSON | `{pc,pp,pe,po,pl}` | Dinheiro |
| `bonus_proficiencia` | INTEGER | 2 | Bônus de proficiência |
| `proficiencias` | TEXT | | Proficiências gerais |
| `linguas` | TEXT | | Idiomas conhecidos |
| `caracteristicas` | TEXT | | Características de classe/raça |
| `personalidade` | TEXT | | Traços de personalidade |
| `ideais` | TEXT | | Ideais |
| `vinculos` | TEXT | | Vínculos |
| `defeitos` | TEXT | | Defeitos |
| `condicoes` | TEXT/JSON | `[]` | Condições ativas |
| `notas` | TEXT | | Notas livres |
| `ativo` | INTEGER | 1 | Se está ativo |
| `sucesso_morte` | INTEGER | 0 | Sucessos em death saves |
| `falha_morte` | INTEGER | 0 | Falhas em death saves |
| `criado_em` | TEXT | TIMESTAMP | Data criação |
| `atualizado_em` | TEXT | TIMESTAMP | Última atualização |

**Estrutura JSON de Atributos:**
```json
{
  "forca": 10,
  "destreza": 10,
  "constituicao": 10,
  "inteligencia": 10,
  "sabedoria": 10,
  "carisma": 10
}
```

**Estrutura JSON de Armas:**
```json
[
  {
    "nome": "Espada Longa",
    "ataque": "+5",
    "dano": "1d8+3 cort."
  }
]
```

**Estrutura JSON de Moedas:**
```json
{
  "pc": 0,   // Peças de cobre
  "pp": 0,   // Peças de prata
  "pe": 0,   // Peças de electrum
  "po": 0,   // Peças de ouro
  "pl": 0    // Peças de platina
}
```

---

### 2. `monstros` - Bestiário (Templates)

| Coluna | Tipo | Padrão | Descrição |
|--------|------|--------|-----------|
| `id` | INTEGER | AUTO | PK |
| `nome` | TEXT | NOT NULL | Nome do monstro |
| `tipo` | TEXT | 'aberração' | Tipo de criatura |
| `tamanho` | TEXT | 'Médio' | Miúdo/Pequeno/Médio/Grande/Enorme/Colossal |
| `alinhamento` | TEXT | | Alinhamento |
| `nd` | REAL | 0 | Nível de Desafio |
| `xp` | INTEGER | 0 | XP ao derrotar |
| `atributos` | TEXT/JSON | `{...}` | 6 atributos |
| `ca` | INTEGER | 10 | Classe de Armadura |
| `ca_tipo` | TEXT | | Tipo de armadura |
| `hp_formula` | TEXT | '1d8' | Fórmula de HP |
| `hp_medio` | INTEGER | | HP médio calculado |
| `velocidade` | TEXT/JSON | `{terrestre:9}` | Velocidades |
| `salvaguardas` | TEXT/JSON | `{}` | Bônus em salvaguardas |
| `pericias` | TEXT/JSON | `{}` | Bônus em perícias |
| `resistencias` | TEXT/JSON | `[]` | Resistências a dano |
| `imunidades_dano` | TEXT/JSON | `[]` | Imunidades a dano |
| `imunidades_condicao` | TEXT/JSON | `[]` | Imunidades a condições |
| `vulnerabilidades` | TEXT/JSON | `[]` | Vulnerabilidades |
| `sentidos` | TEXT/JSON | `{}` | Sentidos especiais |
| `percepcao_passiva` | INTEGER | 10 | Percepção passiva |
| `idiomas` | TEXT/JSON | `[]` | Idiomas |
| `habilidades` | TEXT/JSON | `[]` | Habilidades especiais |
| `acoes` | TEXT/JSON | `[]` | Ações principais |
| `acoes_bonus` | TEXT/JSON | `[]` | Ações bônus |
| `reacoes` | TEXT/JSON | `[]` | Reações |
| `acoes_lendarias` | TEXT/JSON | `[]` | Ações lendárias |
| `fonte` | TEXT | 'Livro do Mestre' | Livro de origem |
| `imagem` | TEXT | | Caminho da imagem |
| `notas` | TEXT | | Notas do mestre |
| `criado_em` | TEXT | TIMESTAMP | Data criação |

**Estrutura JSON de Velocidade:**
```json
{
  "terrestre": 9,
  "escalada": 9,
  "voo": 18,
  "natacao": 9
}
```

**Estrutura JSON de Ações:**
```json
[
  {
    "nome": "Mordida",
    "tipo": "ataque",
    "ataque_tipo": "corpo",
    "bonus": 5,
    "alcance": "1,5m",
    "alvos": "1",
    "dano": "1d8+3",
    "tipo_dano": "perfurante",
    "extra": "CD 12 CON ou envenenado"
  },
  {
    "nome": "Multiataques",
    "tipo": "especial",
    "descricao": "Faz dois ataques de garra."
  }
]
```

**Estrutura JSON de Habilidades:**
```json
[
  {
    "nome": "Visão no Escuro",
    "descricao": "Enxerga em escuridão até 18m."
  }
]
```

---

### 3. `monstros_instancias` - Monstros em Combate

| Coluna | Tipo | Padrão | Descrição |
|--------|------|--------|-----------|
| `id` | INTEGER | AUTO | PK |
| `monstro_id` | INTEGER | NOT NULL | FK → monstros |
| `sessao_id` | INTEGER | | FK → sessoes |
| `nome` | TEXT | NOT NULL | Nome da instância |
| `hp_maximo` | INTEGER | NOT NULL | HP máximo |
| `hp_atual` | INTEGER | NOT NULL | HP atual |
| `ca` | INTEGER | | CA (pode ser diferente) |
| `condicoes` | TEXT/JSON | `[]` | Condições ativas |
| `concentrando` | TEXT | | Magia em concentração |
| `notas_combate` | TEXT | | Notas de combate |
| `acoes_usadas` | TEXT/JSON | `{}` | Controle de recargas |
| `ativo` | INTEGER | 1 | Se está ativo |
| `morto` | INTEGER | 0 | Se foi morto |
| `criado_em` | TEXT | TIMESTAMP | Data criação |

---

### 4. `npcs` - NPCs da Campanha

| Coluna | Tipo | Padrão | Descrição |
|--------|------|--------|-----------|
| `id` | INTEGER | AUTO | PK |
| `nome` | TEXT | NOT NULL | Nome do NPC |
| `titulo` | TEXT | | Título/cargo |
| `raca` | TEXT | | Raça |
| `classe` | TEXT | | Classe |
| `ocupacao` | TEXT | | Ocupação |
| `localizacao` | TEXT | | Localização atual |
| `descricao` | TEXT | | Descrição física |
| `personalidade` | TEXT | | Personalidade |
| `hp_maximo` | INTEGER | | HP máximo |
| `hp_atual` | INTEGER | | HP atual |
| `ca` | INTEGER | 10 | Classe de Armadura |
| `monstro_id` | INTEGER | | FK → monstros (se usar stats de monstro) |
| `alinhamento` | TEXT | 'neutro' | amigável/indiferente/hostil |
| `aliado` | INTEGER | 0 | Se é aliado |
| `hostil` | INTEGER | 0 | Se é hostil |
| `neutro` | INTEGER | 1 | Se é neutro |
| `vivo` | INTEGER | 1 | Se está vivo |
| `conhecido` | INTEGER | 0 | Se o grupo conhece |
| `imagem` | TEXT | | Caminho da imagem |
| `notas` | TEXT | | Notas do mestre |
| `criado_em` | TEXT | TIMESTAMP | Data criação |
| `atualizado_em` | TEXT | TIMESTAMP | Última atualização |

---

### 5. `sessoes` - Controle de Sessões

| Coluna | Tipo | Padrão | Descrição |
|--------|------|--------|-----------|
| `id` | INTEGER | AUTO | PK |
| `numero` | INTEGER | NOT NULL | Número da sessão |
| `data` | TEXT | NOT NULL | Data da sessão |
| `titulo` | TEXT | | Título da sessão |
| `resumo` | TEXT | | Resumo da sessão |
| `duracao_minutos` | INTEGER | | Duração |
| `criado_em` | TEXT | TIMESTAMP | Data criação |
| `atualizado_em` | TEXT | TIMESTAMP | Última atualização |

---

### 6. `combates` - Rastreamento de Combates

| Coluna | Tipo | Padrão | Descrição |
|--------|------|--------|-----------|
| `id` | INTEGER | AUTO | PK |
| `sessao_id` | INTEGER | | FK → sessoes |
| `nome` | TEXT | | Nome do combate |
| `rodada` | INTEGER | 1 | Rodada atual |
| `turno_atual` | INTEGER | 0 | Índice do turno |
| `ordem_iniciativa` | TEXT/JSON | `[]` | Ordem de combate |
| `ativo` | INTEGER | 0 | Se está em andamento |
| `finalizado` | INTEGER | 0 | Se foi finalizado |
| `iniciado_em` | TEXT | TIMESTAMP | Quando iniciou |
| `finalizado_em` | TEXT | | Quando finalizou |

---

### 7. `acoes_log` - Histórico de Ações

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER | PK |
| `sessao_id` | INTEGER | FK → sessoes |
| `combate_id` | INTEGER | FK → combates |
| `rodada` | INTEGER | Rodada da ação |
| `atacante_tipo` | TEXT | personagem/monstro/npc |
| `atacante_id` | INTEGER | ID do atacante |
| `atacante_nome` | TEXT | Nome do atacante |
| `alvo_tipo` | TEXT | Tipo do alvo |
| `alvo_id` | INTEGER | ID do alvo |
| `alvo_nome` | TEXT | Nome do alvo |
| `tipo_acao` | TEXT | ataque/magia/habilidade |
| `nome_acao` | TEXT | Nome da ação |
| `rolagem_ataque` | TEXT | Expressão rolada |
| `total_ataque` | INTEGER | Total do ataque |
| `ca_alvo` | INTEGER | CA do alvo |
| `acertou` | INTEGER | Se acertou |
| `critico` | INTEGER | Se foi crítico |
| `falha_critica` | INTEGER | Se foi falha crítica |
| `dano` | INTEGER | Dano causado |
| `tipo_dano` | TEXT | Tipo de dano |
| `dano_detalhes` | TEXT | Detalhes do dano |
| `cd_salvaguarda` | INTEGER | CD da salvaguarda |
| `tipo_salvaguarda` | TEXT | Atributo da salvaguarda |
| `resultado_salvaguarda` | INTEGER | Resultado da rolagem |
| `passou_salvaguarda` | INTEGER | Se passou |
| `efeitos` | TEXT/JSON | Efeitos aplicados |
| `sobrescrito` | INTEGER | Se foi alterado pelo mestre |
| `valores_originais` | TEXT | Valores antes da alteração |
| `timestamp` | TEXT | Momento da ação |

---

### 8. `configuracoes` - Configurações do Sistema

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `chave` | TEXT | PK - Nome da config |
| `valor` | TEXT | Valor da config |
| `atualizado_em` | TEXT | Última atualização |

**Configurações Padrão:**
- `regras_xanathar`: '0'
- `regras_tasha`: '0'
- `regras_underdark`: '1'
- `usar_fome_sede`: '1'
- `usar_exaustao_underdark`: '1'
- `tema`: 'escuro'
- `auto_save`: '1'
- `intervalo_save`: '30'

---

### 9. Tabelas de Regras D&D

#### `racas`
Raças jogáveis com modificadores de atributos e habilidades.

#### `classes`
Classes com dados de vida, proficiências, etc.

#### `pericias`
Lista de perícias com atributos associados.

#### `condicoes_dnd`
Condições do D&D 5e com descrições e efeitos mecânicos.

---

## Funções de Acesso (database.py)

### Conexão
```python
from app.modulos.database import get_connection

with get_connection() as conn:
    cursor = conn.execute("SELECT * FROM personagens")
    rows = cursor.fetchall()
```

### Utilitários JSON
```python
from app.modulos.database import json_dumps, json_loads_safe

# Serializar para DB
json_str = json_dumps({"forca": 10, "destreza": 14})

# Deserializar do DB
obj = json_loads_safe(json_str, default={})
```

### Dict from Row
```python
from app.modulos.database import dict_from_row

row = cursor.fetchone()
data = dict_from_row(row)  # Converte sqlite3.Row para dict
```

---

## Índices Recomendados

```sql
CREATE INDEX idx_personagens_ativo ON personagens(ativo);
CREATE INDEX idx_monstros_nd ON monstros(nd);
CREATE INDEX idx_monstros_instancias_sessao ON monstros_instancias(sessao_id);
CREATE INDEX idx_npcs_vivo ON npcs(vivo);
CREATE INDEX idx_acoes_log_sessao ON acoes_log(sessao_id);
CREATE INDEX idx_acoes_log_combate ON acoes_log(combate_id);
```

---

## Migrações

Quando adicionar colunas:
```python
# Em database.py ou db_init.py
try:
    conn.execute("ALTER TABLE tabela ADD COLUMN nova_coluna TEXT DEFAULT ''")
except:
    pass  # Coluna já existe
```
