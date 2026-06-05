# Fuga do Abismo — Sistema de Mestragem D&D 5e

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Flask-3.0+-green?logo=flask" />
  <img src="https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite" />
  <img src="https://img.shields.io/badge/D%26D-5e-red" />
  <img src="https://img.shields.io/badge/versão-0.1.0-informational" />
  <img src="https://img.shields.io/badge/License-GPL%20v3-blue" />
</p>

Aplicação web local para auxiliar a mestragem de **Dungeons & Dragons 5ª Edição**, desenvolvida para a campanha **Fuga do Abismo**. Roda inteiramente no navegador sem conexão com internet — dados ficam no seu computador.

---

## Índice

- [Visão Geral](#visão-geral)
- [Instalação](#instalação)
- [Ferramentas Disponíveis](#ferramentas-disponíveis)
- [Status de Implementação](#status-de-implementação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API REST](#api-rest)
- [Regras D&D 5e Implementadas](#regras-dd-5e-implementadas)
- [Testes](#testes)
- [Bugs Conhecidos](#bugs-conhecidos)
- [Changelog](#changelog)
- [Licença](#licença)

---

## Visão Geral

O sistema foi criado para **acelerar e organizar sessões de RPG** sem depender de ferramentas online. O mestre gerencia tudo em uma única tela: fichas abertas como widgets flutuantes, combate com iniciativa e turnos, notas de sessão, mapas e log de ações — tudo persistido automaticamente.

**Stack:** Python 3.10+ · Flask 3 · SQLite (WAL) · Vanilla JS/HTML/CSS

---

## Instalação

```powershell
# 1. Clone
git clone https://github.com/necromod/Out-Of-Abyss.git
cd Out-Of-Abyss

# 2. Ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # Linux/Mac

# 3. Dependências
pip install -r System/requirements.txt

# 4. Inicia o servidor (abre o navegador automaticamente)
python System/main.py
```

Acesse em: `http://127.0.0.1:5000`

> O banco de dados SQLite é criado automaticamente em `System/data/campaign.db` na primeira execução.

### Executar testes

```powershell
# Com o servidor rodando em outro terminal:
python -m pytest System/tests/test_sistema_completo.py -v

# Testes específicos (sem precisar do servidor):
python -m pytest System/tests/test_sistema_completo.py -v -k "not APIRest and not Paginas and not Fluxos and not Widgets and not Performance"
```

---

## Ferramentas Disponíveis

### Fichas de Personagem ✅

Ficha completa D&D 5e acessível em **Fichas → Personagens**.

- Atributos (FOR, DES, CON, INT, SAB, CAR) com modificadores calculados automaticamente
- HP máximo / atual / temporário com alertas de HP baixo e crítico
- Classe de Armadura, Iniciativa, Deslocamento, Percepção Passiva
- Proficiência em perícias e salvaguardas
- Espaços de magia por nível (campos disponíveis, sem controle de uso — veja [não implementado](#não-implementadas-ou-incompletas))
- Inventário com armas e equipamentos
- Testes de morte (3 sucessos / 3 falhas)
- Auto-save a cada alteração
- Criação com Point Buy ou distribuição livre de atributos

> **Melhoria pendente:** seletor de raça/classe deveria preencher automaticamente os bônus de atributo, idiomas e proficiências. Atualmente o mestre preenche tudo manualmente.

---

### Fichas de Monstro ✅

Bestiário gerenciado em **Fichas → Monstros**.

- Atributos completos, ND, XP, tipo, tamanho
- Resistências, imunidades e vulnerabilidades a tipos de dano
- Habilidades, ações, ações bônus, reações e ações lendárias
- **Instâncias de combate**: cada monstro pode ser instanciado com HP individual para uso em sessão
- Busca por nome e por faixa de ND
- Auto-save

> **Melhoria pendente:** não há importação de dados externos (D&D Beyond, Open5e, etc.). Todos os monstros devem ser cadastrados manualmente.

---

### Fichas de NPC ✅

NPCs da campanha em **Fichas → NPCs**.

- Nome, descrição, localização, relacionamento com o grupo
- Status: vivo/morto, conhecido/desconhecido pelo grupo
- HP máximo/atual com botões de dano e cura rápida
- Auto-save por campo individual (edição inline)

> **Melhoria pendente:** widget de NPC na tela de sessão é básico — mostra nome, HP e descrição, mas não exibe ações ou outras estatísticas de combate completas.

---

### Sistema de Combate ✅

Acessado pela tela de **Sessão**, botão ⚔️.

- Rolagem automática de iniciativa (1d20 + mod DES) para cada participante
- Ordem de turnos com destaque visual do turno atual
- Botão **Próximo Turno** (funciona com 0, 1 ou múltiplos participantes)
- Ataques com rolagem 1d20 + bônus — detecta crítico (20) e falha crítica (1)
- Crítico dobra automaticamente todos os dados de dano
- 13 tipos de dano com resistências/imunidades/vulnerabilidades aplicadas automaticamente
- Dano e cura rápida via input flutuante ao clicar nos botões de HP
- Testes de morte para personagens com HP ≤ 0

> **Melhoria pendente:** não há suporte a ações bônus, reações ou ações lendárias com contadores automáticos por turno. O controle é manual pelo mestre.

---

### Condições D&D 5e ✅

Aplicadas via botão **+ Efeito** em qualquer widget de criatura.

Todas as 15 condições do Player's Handbook:
Agarrado · Amedrontado · Atordoado · Caído · Cego · Enfeitiçado · Envenenado · Incapacitado · Inconsciente · Invisível · Paralisado · Petrificado · Restringido · Surdo · Exaustão (6 níveis)

Mais danos persistentes (ácido, ígneo, venenoso, etc.) com contador de turnos.

- Cada condição tem tooltip com as regras do PHB
- Duração em turnos — decrementa automaticamente com o avanço de turno
- Duração 0 = permanente (remove manualmente)

---

### Widgets Flutuantes ✅

Disponíveis na barra superior da tela de **Sessão**.

| Widget | Botão | Função |
|---|---|---|
| Ficha de Personagem | 👤 | Mini-ficha com HP, CA, atributos, ações rápidas, efeitos |
| Ficha de Monstro | 👹 | Instância de combate com HP individual, ações, resistências |
| Ficha de NPC | (menu NPCs) | HP, descrição, ações básicas |
| Iniciativa | ⏱️ | Ordem de turnos com controle de round |
| Log de Combate | 📜 | Histórico de ações com horário no hover |
| Rolador de Dados | 🎲 | Expressões livres: `2d6+3`, `1d20`, `4d8-2` |
| Notas de Sessão | 📝 | Notas persistidas em banco com múltiplos campos de texto |

Recursos de todos os widgets:
- Arrastar pelo header
- Redimensionar pelos cantos/bordas
- Minimizar / Fechar (ou middle-click no header para fechar)
- **Pop-out `↗️`**: abre o widget em janela externa independente do navegador

---

### Notas de Sessão ✅

Acessadas pelo botão **📝 Notas** na navbar da tela de sessão.

- Crie quantas notas quiser, cada uma com título e múltiplos campos de texto
- Auto-save ao digitar (debounce de 1,2 s)
- Ajuste de tamanho de fonte por campo (A− / A+)
- Adicione campos ilimitados com **+ Adicionar Campo**
- Dropdown mostra todas as notas criadas; ícone ✓ indica notas já abertas

**Janela externa (pop-out):** clicar em `↗️` abre a nota em uma janela dedicada completamente funcional — edição de título, campos, adição de campos e auto-save — sem depender da janela principal.

> **Não implementado ainda:** links entre notas (botão 🔗 existe, mas mostra "será implementado em breve").

---

### Cenários e Mapas ✅

Acessados pelo botão **🗺️** na navbar ou arrastando uma imagem para a tela.

- **Drag-and-drop**: arraste qualquer imagem (PNG, JPG, WEBP, GIF) diretamente para a tela
- **Galeria de seleção**: modal com thumbnails dos cenários já salvos
- Imagens salvas em `Imagens/Cenários/` com sufixo numérico para evitar duplicatas
- Cenário atual persiste entre sessões (salvo no estado da sessão)
- Clique no ✕ para remover o cenário da tela

---

### Sistema de Sessões ✅

- Estado completo salvo automaticamente a cada 10 segundos em `System/data/sessoes/`
- Dropdown na navbar lista todas as sessões para restauração
- Ao restaurar, widgets, posições, combate ativo e cenário são recuperados
- Cada sessão tem número sequencial e título

---

## Status de Implementação

### Totalmente Funcionais ✅

| Ferramenta | Observação |
|---|---|
| CRUD de Personagens | Completo com Point Buy |
| CRUD de Monstros | Completo com instâncias de combate |
| CRUD de NPCs | Completo |
| Combate com iniciativa e turnos | Completo |
| Condições D&D 5e (15 + danos contínuos) | Completo |
| Widgets flutuantes (arrastar, redimensionar, pop-out) | Completo |
| Notas de sessão com janela externa | Completo (v0.1.0) |
| Cenários / mapas com drag-and-drop | Completo |
| Log de combate | Completo |
| Rolador de dados com expressões | Completo |
| Auto-save em todas as fichas e notas | Completo |
| Persistência de sessão (JSON) | Completo |
| Suite de 87 testes automatizados | 56 passam offline, 31 requerem servidor |

### Precisam de Melhorias ⚠️

| Ferramenta | Problema |
|---|---|
| Widget de NPC | Exibe só HP e descrição; sem ações de combate completas |
| Ficha de Personagem — raça/classe | Seleção não preenche bônus/proficiências automaticamente |
| Fichas de Monstro — importação | Cadastro 100% manual; sem importação de fontes externas |
| Sistema de turnos — ações por turno | Sem contador automático de ação, ação bônus e reação |
| Exaustão | Condição registrável, mas os penais dos 6 níveis não são aplicados automaticamente |
| Tela de sessão — layout | Widgets não têm snapping a grade nem salvamento de posição entre sessões |

### Não Implementadas ou Incompletas ❌

| Recurso | Situação |
|---|---|
| Links entre notas | Botão 🔗 presente, funcionalidade não implementada |
| Controle de espaços de magia | Campos existem na ficha, sem controle de uso/recuperação por descanso |
| Controle de recursos de classe | Sem rastreio de Pontos de Ki, Fúria, Usos de Canalização, etc. |
| Ações lendárias com contador | Campo cadastrado no monstro, sem lógica de 3 ações/round |
| Importação de bestiário externo | Sem suporte a Open5e API, D&D Beyond ou JSON de terceiros |
| Modo multi-mestre / rede local | Aplicação é single-user localhost |
| Sons e alertas sonoros | Sem feedback de áudio para críticos, morte, etc. |

---

## Estrutura do Projeto

```
Out-Of-Abyss/
├── CHANGELOG.md
├── README.md
├── LICENSE
│
├── System/
│   ├── main.py                     # Entry point (abre http://127.0.0.1:5000)
│   ├── requirements.txt            # Flask e dependências
│   │
│   ├── app/
│   │   ├── __init__.py             # Factory create_app()
│   │   ├── config.py               # Caminhos, SECRET_KEY, REGRAS_ATIVAS
│   │   │
│   │   ├── modulos/
│   │   │   ├── database.py         # SQLite + BaseRepository + migrações
│   │   │   ├── repositories.py     # CRUD por entidade (Personagem, Monstro, NPC…)
│   │   │   ├── regras_base.py      # Cálculos D&D (modificadores, CA, proficiência)
│   │   │   ├── regras_dnd_data.py  # Dados estáticos — raças, classes, perícias (67 KB)
│   │   │   ├── combate.py          # Motor de combate
│   │   │   ├── acoes.py            # Resolução de ataques e dano
│   │   │   ├── condicoes.py        # 15 condições PHB com contadores
│   │   │   ├── dados.py            # Parser de expressões de dados ("2d6+3")
│   │   │   └── regras/             # Livros opcionais (Xanathar, Tasha, etc.)
│   │   │
│   │   ├── routes/
│   │   │   ├── main.py             # GET /, /config, /notas/<id>
│   │   │   ├── fichas.py           # /fichas/* — páginas e API de fichas
│   │   │   ├── api.py              # /api/* — endpoints JSON gerais
│   │   │   ├── sessao.py           # /sessao/* — estado e persistência de sessão
│   │   │   └── combate.py          # /combate/* — ações de combate
│   │   │
│   │   └── static/
│   │       ├── css/
│   │       │   ├── base.css        # Variáveis globais, tema, reset
│   │       │   ├── fichas.css      # Fichas de personagem/monstro/NPC
│   │       │   ├── sessao.css      # Tela de sessão, combate, widgets
│   │       │   └── widgets.css     # Sistema de widgets flutuantes
│   │       └── js/
│   │           ├── base.js         # Utilitários, cliente API, modais, notificações
│   │           ├── fichas.js       # CRUD de fichas, auto-save, Point Buy (77 KB)
│   │           ├── sessao.js       # Combate, notas, widgets de sessão (193 KB)
│   │           └── widgets.js      # Classe Widget + pop-out + comunicação cross-window
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── config.html
│   │   ├── fichas/                 # personagem, monstro, npc, listas
│   │   ├── sessao/                 # tela_sessao.html
│   │   ├── widgets/                # ficha_personagem, ficha_monstro, ficha_npc
│   │   └── notas/
│   │       └── janela.html         # Página standalone para nota em janela externa
│   │
│   ├── data/
│   │   ├── campaign.db             # SQLite (gerado automaticamente)
│   │   └── sessoes/                # Estado de cada sessão em JSON
│   │
│   └── tests/
│       └── test_sistema_completo.py  # 87 testes em 12 classes
│
└── Imagens/
    └── Cenários/                   # Mapas de batalha (criada automaticamente)
```

---

## API REST

### Personagens
```
GET    /fichas/api/personagens          Lista todos
GET    /fichas/api/personagem/:id       Obtém um
POST   /fichas/api/personagem           Cria
PATCH  /fichas/api/personagem/:id       Atualiza
DELETE /fichas/api/personagem/:id       Remove
PATCH  /fichas/api/personagem/:id/campo Atualiza campo individual
```

### Monstros
```
GET    /api/monstros                    Lista (suporta ?nome= e ?nd_min= &nd_max=)
GET    /fichas/api/monstro/:id          Obtém um
POST   /fichas/api/monstro              Cria
PATCH  /fichas/api/monstro/:id          Atualiza
DELETE /fichas/api/monstro/:id          Remove
POST   /fichas/api/monstro/instancia    Cria instância de combate
GET    /fichas/api/monstro/instancia/:id Obtém instância com dados do monstro base
PATCH  /fichas/api/monstro/instancia/:id Atualiza instância
```

### NPCs
```
GET    /api/npcs                        Lista (suporta ?conhecidos=1 e ?local=)
GET    /api/npcs/:id                    Obtém um
PATCH  /api/npcs/:id                    Atualiza (com serialização correta de JSON)
POST   /api/npcs                        Cria
POST   /api/npcs/:id/dano               Aplica dano
POST   /api/npcs/:id/curar              Cura
```

### Notas de Sessão
```
GET    /api/notas                       Lista todas
GET    /api/notas/:id                   Obtém uma
POST   /api/notas                       Cria
PATCH  /api/notas/:id                   Atualiza (título, campos, links, posição)
DELETE /api/notas/:id                   Remove
GET    /notas/:id                       Página standalone de edição
```

### Sessão e Dados
```
GET    /sessao/api/atual                Sessão atual
GET    /sessao/api/lista                Lista de sessões
POST   /api/dados/rolar                 Rola dados {expressao: "2d6+3"}
GET    /api/dnd/regras-completas        Todos os dados D&D em uma requisição
GET    /api/dnd/racas                   Raças disponíveis
GET    /api/dnd/classes                 Classes disponíveis
GET    /api/dnd/pericias                Perícias
```

---

## Regras D&D 5e Implementadas

| Regra | Status |
|---|---|
| Modificador de atributo `(val − 10) ÷ 2` | ✅ |
| Bônus de proficiência por nível | ✅ |
| Percepção Passiva `10 + mod SAB` | ✅ |
| Iniciativa `1d20 + mod DES` | ✅ |
| Ataque crítico (20 natural — dobra dados) | ✅ |
| Falha crítica (1 natural) | ✅ |
| Testes de morte (3 sucessos / 3 falhas) | ✅ |
| 15 condições PHB com duração em turnos | ✅ |
| 13 tipos de dano | ✅ |
| Resistências / Imunidades / Vulnerabilidades | ✅ |
| Point Buy para criação de personagem | ✅ |
| Exaustão (6 níveis) — registro | ✅ penalidades automáticas |
| Espaços de magia — campos | ✅ controle de uso/recuperação |
| Ações lendárias — cadastro | ✅ contador automático por round |
| Recursos de classe (Ki, Fúria…) | ❌ |

---

## Testes

```
Suite: System/tests/test_sistema_completo.py
Total: 87 testes em 12 classes
```

| Classe | Testes | Requer servidor |
|---|---|---|
| TestRegrasDnD | 17 | Não |
| TestRolagemDados | 7 | Não |
| TestRepositorios | 9 | Não |
| TestValidacaoDados | 5 | Não |
| TestEstruturaArquivos | 11 | Não |
| TestIntegridadeBanco | 4 | Não |
| TestBugsConhecidos | 2 | Não |
| TestAPIRest | 13 | Sim |
| TestRotasPaginas | 9 | Sim |
| TestFluxosCompletos | 3 | Sim |
| TestWidgetsInterface | 3 | Sim |
| TestPerformance | 3 | Sim |

**56 passam sem servidor · 31 requerem `python System/main.py` rodando**

---

## Bugs Conhecidos

| # | Local | Descrição | Severidade |
|---|---|---|---|
| #1 | `database.py` `BaseRepository.update()` | Tenta atualizar coluna `atualizado_em` em `monstros_instancias`, que não possui essa coluna. Workaround: use os métodos específicos da instância. | Média |
| #2 | `templates/widgets/ficha_personagem.html` | Template faz aritmética em atributos assumindo `int`; se gravados como string causa `TypeError`. | Baixa |

> Todos os bugs críticos identificados na revisão de 2026-06-05 foram corrigidos na v0.1.0. Ver [CHANGELOG](CHANGELOG.md).

---

## Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para o histórico completo de versões.

Versão atual: **0.1.0**

---

## Licença

**GNU General Public License v3.0** — veja [LICENSE](LICENSE).

Você pode usar, modificar e distribuir livremente desde que mantenha o código-fonte aberto e a mesma licença em obras derivadas.

---

<p align="center">Boas aventuras no Underdark! 🕯️</p>
