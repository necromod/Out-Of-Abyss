# CHANGELOG

Todas as mudanças notáveis neste projeto serão documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/) — `MAJOR.MINOR.PATCH`.

---

## [0.1.0] — 2026-06-05

### Adicionado
- **Janela externa de Notas** (`/notas/<id>`): notas agora abrem em uma janela standalone completamente funcional via botão `↗️`, substituindo o pop-out genérico que era apenas um snapshot estático. A nova página possui edição de título, campos de texto com auto-save debounced, botões de tamanho de fonte por campo, adição de novos campos e indicador de status de salvamento (Salvando… / ✓ Salvo / ✗ Erro).
- **Rota `GET /notas/<id>`** em `main.py` para servir a página standalone de nota.
- **Template `templates/notas/janela.html`**: página auto-contida que consome a API `/api/notas/<id>` diretamente, sem dependência de `sessao.js` ou `widgets.js`.
- **`NPCRepository.atualizar()`**: novo método com serialização correta de campos JSON (`atributos`, `acoes`) ao salvar NPCs.
- **`CLAUDE.md`**: arquivo de contexto para Claude Code com comandos e arquitetura do projeto.

### Corrigido
- **CRÍTICO** — `PATCH /api/notas/<id>` com campos de posição (`posicao_x`, `posicao_y`, `largura`, `altura`) causava `TypeError` (HTTP 500) porque `atualizar_posicao()` recebia um dict onde esperava argumentos posicionais `(x, y)`. Corrigido usando `NotasSessaoRepository.update()` diretamente com os campos presentes. (`api.py`)
- **`POST /fichas/api/monstro/instancia`** com `monstro_id` inexistente retornava HTTP 200 com corpo `null`. Agora retorna HTTP 404 com mensagem de erro. (`fichas.py`)
- **Limpeza de teste `test_api_criar_instancia_monstro`** enviava `DELETE` para `/fichas/api/monstro/instancia/<id>` — rota que só aceita GET e PATCH — resultando em HTTP 405 e vazamento de linhas órfãs no banco a cada execução. Corrigido removendo a chamada de limpeza inválida. (`tests/test_sistema_completo.py`)
- **Serialização de JSON em NPCs**: `PATCH /api/npcs/<id>` chamava `NPCRepository.update()` direto, sem serializar campos `atributos`/`acoes`. Dados enviados como dict eram gravados como `repr()` Python, corrompendo esses campos. Agora chama `NPCRepository.atualizar()`. (`api.py`, `repositories.py`)

### Removido
- **Bloco "Rotas de compatibilidade"** em `api.py` (linhas 647–697): continha handlers GET duplicados para `/personagens`, `/monstros`, `/npcs` e `/npcs/<id>`, e um handler PATCH/PUT duplicado para `/npcs/<id>` — todos inacessíveis pois Flask registrava apenas os primeiros handlers de cada URL. Eliminado o risco de comportamento silenciosamente errado caso a ordem de registro mudasse.

### Melhorado
- **`criarWidgetNota`** em `sessao.js`: removidos ~40 chamadas de `console.log` de debug que poluíam o console durante uso normal. Método `abrirPopout` sobrescrito no nível de instância para usar `/notas/<id>` ao invés do pop-out genérico.

---

## [0.0.4] — 2026 (commits `90cf3f0`, `43db807`)

### Alterado
- Refatoração de mensagens de log: substituição de emojis (`✅`, `❌`, `📥`) por tags ASCII (`[OK]`, `[ERRO]`, `[INFO]`) em `main.py`, `database.py` e outros módulos para compatibilidade de terminal.
- Atualização de dados da sessão (sessao_3.json → sessao_4.json).

---

## [0.0.3] — 2026 (commit `8242926`)

### Adicionado
- **Sistema de pop-out de widgets**: botão `↗️` em todos os widgets abre uma janela flutuante externa com o conteúdo do widget, CSS do sistema e comunicação bidirecional com a janela pai (funções `rolarAtaque`, `toggleMenuResistencia`, etc.).
- Sistema local de dano/cura dentro do pop-out (não redireciona para a janela pai).

---

## [0.0.2] — 2026 (commit `0ef46c0`)

### Adicionado
- **Widget de NPC** com descrição editável e auto-save.
- **Sistema de notas da campanha**: widget flutuante de notas persistidas no banco SQLite, com múltiplos campos de texto, ajuste de fonte e auto-save.
- Dropdown de notas na navbar da tela de sessão.

---

## [0.0.1] — 2026 (commit `f9bd559`)

### Adicionado
- Versão inicial do **sistema de notas de sessão**: tabela `notas_sessao` no banco, repositório `NotasSessaoRepository`, endpoints REST `/api/notas`, e widget de nota com campos de texto livres.

---

> Para o histórico completo de commits, consulte `git log --oneline`.
