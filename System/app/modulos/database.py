"""
Módulo de Banco de Dados - SQLite Local
Performance: consultas em 1-5ms
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'campaign.db')


def get_db_path():
    """Retorna o caminho do banco de dados"""
    return DB_PATH


@contextmanager
def get_connection():
    """Context manager para conexão com o banco"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retorna dicts ao invés de tuples
    conn.execute("PRAGMA foreign_keys = ON")  # Habilita foreign keys
    conn.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging (mais rápido)
    conn.execute("PRAGMA synchronous = NORMAL")  # Balance entre segurança e velocidade
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def dict_from_row(row) -> Optional[Dict]:
    """Converte sqlite3.Row para dict"""
    if row is None:
        return None
    return dict(row)


def migrate_database():
    """Executa migrações do banco de dados para adicionar novas colunas"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verifica e adiciona coluna 'fonte' em racas
        try:
            cursor.execute("SELECT fonte FROM racas LIMIT 1")
        except sqlite3.OperationalError:
            print("[MIGRATION] Adicionando coluna 'fonte' em racas...")
            cursor.execute("ALTER TABLE racas ADD COLUMN fonte TEXT DEFAULT 'PHB'")
        
        # Verifica e adiciona coluna 'fonte' em classes
        try:
            cursor.execute("SELECT fonte FROM classes LIMIT 1")
        except sqlite3.OperationalError:
            print("[MIGRATION] Adicionando coluna 'fonte' em classes...")
            cursor.execute("ALTER TABLE classes ADD COLUMN fonte TEXT DEFAULT 'PHB'")
        
        conn.commit()


def init_database():
    """Inicializa o banco de dados com todas as tabelas"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # ==================== SESSÕES ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER NOT NULL,
                data TEXT NOT NULL,
                titulo TEXT,
                resumo TEXT,
                duracao_minutos INTEGER,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ==================== PERSONAGENS (PCs) ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                jogador TEXT,
                raca TEXT,
                classe TEXT,
                nivel INTEGER DEFAULT 1,
                antecedente TEXT,
                alinhamento TEXT,
                
                -- Atributos (armazenados como JSON para flexibilidade)
                atributos TEXT DEFAULT '{"forca":10,"destreza":10,"constituicao":10,"inteligencia":10,"sabedoria":10,"carisma":10}',
                
                -- Combate
                hp_maximo INTEGER DEFAULT 10,
                hp_atual INTEGER DEFAULT 10,
                hp_temporario INTEGER DEFAULT 0,
                ca INTEGER DEFAULT 10,
                ca_bonus INTEGER DEFAULT 0,
                velocidade TEXT DEFAULT '9m',
                iniciativa_bonus INTEGER DEFAULT 0,
                inspiracao INTEGER DEFAULT 0,
                
                -- Proficiências (JSON arrays)
                pericias_proficientes TEXT DEFAULT '[]',
                pericias_expertise TEXT DEFAULT '[]',
                salvaguardas_proficientes TEXT DEFAULT '[]',
                
                -- Dados de vida
                dados_vida TEXT DEFAULT '1d8',
                dados_vida_restantes INTEGER DEFAULT 1,
                
                -- Magia (JSON)
                conjurador INTEGER DEFAULT 0,
                atributo_conjuracao TEXT,
                espacos_magia TEXT DEFAULT '{}',
                espacos_usados TEXT DEFAULT '{}',
                magias_conhecidas TEXT DEFAULT '[]',
                magias_preparadas TEXT DEFAULT '[]',
                
                -- Equipamento (JSON)
                equipamento TEXT DEFAULT '[]',
                equipamentos TEXT DEFAULT '[]',
                armas TEXT DEFAULT '[]',
                moedas TEXT DEFAULT '{"pc":0,"pp":0,"pe":0,"po":0,"pl":0}',
                
                -- Proficiências
                bonus_proficiencia INTEGER DEFAULT 2,
                proficiencias TEXT,
                linguas TEXT,
                
                -- Personalidade
                caracteristicas TEXT,
                personalidade TEXT,
                ideais TEXT,
                vinculos TEXT,
                defeitos TEXT,
                
                -- Dados de vida (JSON para multiclasse)
                dados_vida_tipos TEXT DEFAULT '[{"qtd":1,"faces":8}]',
                
                -- Estado
                condicoes TEXT DEFAULT '[]',
                notas TEXT,
                ativo INTEGER DEFAULT 1,
                
                -- Morte
                sucesso_morte INTEGER DEFAULT 0,
                falha_morte INTEGER DEFAULT 0,
                
                -- Percepção Passiva (calculado: 10 + mod sabedoria)
                percepcao_passiva INTEGER DEFAULT 10,
                
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ==================== MONSTROS (Templates) ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monstros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT DEFAULT 'aberração',
                tamanho TEXT DEFAULT 'Médio',
                alinhamento TEXT,
                nd REAL DEFAULT 0,
                xp INTEGER DEFAULT 0,
                
                -- Atributos
                atributos TEXT DEFAULT '{"forca":10,"destreza":10,"constituicao":10,"inteligencia":10,"sabedoria":10,"carisma":10}',
                
                -- Combate
                ca INTEGER DEFAULT 10,
                ca_tipo TEXT,
                hp_formula TEXT DEFAULT '1d8',
                hp_medio INTEGER,
                velocidade TEXT DEFAULT '{"terrestre":9}',
                
                -- Defesas (JSON)
                salvaguardas TEXT DEFAULT '{}',
                pericias TEXT DEFAULT '{}',
                resistencias TEXT DEFAULT '[]',
                imunidades_dano TEXT DEFAULT '[]',
                imunidades_condicao TEXT DEFAULT '[]',
                vulnerabilidades TEXT DEFAULT '[]',
                
                -- Sentidos
                sentidos TEXT DEFAULT '{}',
                percepcao_passiva INTEGER DEFAULT 10,
                idiomas TEXT DEFAULT '[]',
                
                -- Habilidades e Ações (JSON)
                habilidades TEXT DEFAULT '[]',
                acoes TEXT DEFAULT '[]',
                acoes_bonus TEXT DEFAULT '[]',
                reacoes TEXT DEFAULT '[]',
                acoes_lendarias TEXT DEFAULT '[]',
                
                -- Metadados
                fonte TEXT DEFAULT 'Livro do Mestre',
                imagem TEXT,
                notas TEXT,
                
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ==================== INSTÂNCIAS DE MONSTROS (em combate) ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monstros_instancias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monstro_id INTEGER NOT NULL,
                sessao_id INTEGER,
                nome TEXT NOT NULL,
                
                -- Estado de combate
                hp_maximo INTEGER NOT NULL,
                hp_atual INTEGER NOT NULL,
                ca INTEGER,
                condicoes TEXT DEFAULT '[]',
                concentrando TEXT,
                notas_combate TEXT,
                acoes_usadas TEXT DEFAULT '{}',
                
                -- Status
                ativo INTEGER DEFAULT 1,
                morto INTEGER DEFAULT 0,
                
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (monstro_id) REFERENCES monstros(id),
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
            )
        """)
        
        # ==================== NPCs ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS npcs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                titulo TEXT,
                raca TEXT,
                classe TEXT,
                ocupacao TEXT,
                localizacao TEXT,
                descricao TEXT,
                personalidade TEXT,
                
                -- Combate
                hp_maximo INTEGER,
                hp_atual INTEGER,
                ca INTEGER DEFAULT 10,
                monstro_id INTEGER,
                
                -- Relacionamentos (alinhamento com o grupo)
                alinhamento TEXT DEFAULT 'neutro',  -- amigável, indiferente, hostil
                aliado INTEGER DEFAULT 0,
                hostil INTEGER DEFAULT 0,
                neutro INTEGER DEFAULT 1,
                
                -- Status
                vivo INTEGER DEFAULT 1,
                conhecido INTEGER DEFAULT 0,
                
                imagem TEXT,
                notas TEXT,
                
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (monstro_id) REFERENCES monstros(id)
            )
        """)
        
        # ==================== COMBATES ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS combates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER,
                nome TEXT,
                rodada INTEGER DEFAULT 1,
                turno_atual INTEGER DEFAULT 0,
                
                -- Ordem de iniciativa (JSON)
                ordem_iniciativa TEXT DEFAULT '[]',
                
                -- Status
                ativo INTEGER DEFAULT 0,
                finalizado INTEGER DEFAULT 0,
                
                iniciado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                finalizado_em TEXT,
                
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
            )
        """)
        
        # ==================== LOG DE AÇÕES (histórico completo) ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS acoes_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER,
                combate_id INTEGER,
                rodada INTEGER,
                
                -- Participantes
                atacante_tipo TEXT,
                atacante_id INTEGER,
                atacante_nome TEXT,
                alvo_tipo TEXT,
                alvo_id INTEGER,
                alvo_nome TEXT,
                
                -- Ação
                tipo_acao TEXT NOT NULL,
                nome_acao TEXT,
                
                -- Resultados de ataque
                rolagem_ataque TEXT,
                total_ataque INTEGER,
                ca_alvo INTEGER,
                acertou INTEGER,
                critico INTEGER DEFAULT 0,
                falha_critica INTEGER DEFAULT 0,
                
                -- Dano
                dano INTEGER DEFAULT 0,
                tipo_dano TEXT,
                dano_detalhes TEXT,
                
                -- Salvaguarda
                cd_salvaguarda INTEGER,
                tipo_salvaguarda TEXT,
                resultado_salvaguarda INTEGER,
                passou_salvaguarda INTEGER,
                
                -- Efeitos
                efeitos TEXT DEFAULT '[]',
                
                -- Sobrescrição pelo mestre
                sobrescrito INTEGER DEFAULT 0,
                valores_originais TEXT,
                
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id),
                FOREIGN KEY (combate_id) REFERENCES combates(id)
            )
        """)
        
        # ==================== ROLAGENS DE DADOS ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rolagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER,
                combate_id INTEGER,
                
                -- Quem rolou
                entidade_tipo TEXT,
                entidade_id INTEGER,
                entidade_nome TEXT,
                
                -- Rolagem
                expressao TEXT NOT NULL,
                dados TEXT,
                soma_dados INTEGER,
                modificador INTEGER DEFAULT 0,
                total INTEGER NOT NULL,
                
                -- Tipo
                tipo TEXT,
                critico INTEGER DEFAULT 0,
                falha_critica INTEGER DEFAULT 0,
                
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id),
                FOREIGN KEY (combate_id) REFERENCES combates(id)
            )
        """)
        
        # ==================== NOTAS DE SESSÃO ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER,
                titulo TEXT,
                conteudo TEXT,
                categoria TEXT,
                
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
            )
        """)
        
        # ==================== CONFIGURAÇÕES ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ==================== RAÇAS D&D 5e ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS racas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                categoria TEXT DEFAULT 'Livro do Jogador',
                fonte TEXT DEFAULT 'PHB',
                
                -- Bônus
                bonus_atributos TEXT DEFAULT '{}',
                velocidade INTEGER DEFAULT 9,
                tamanho TEXT DEFAULT 'Médio',
                
                -- Proficiências e idiomas
                idiomas TEXT DEFAULT '[]',
                proficiencias_armas TEXT DEFAULT '[]',
                proficiencias_armaduras TEXT DEFAULT '[]',
                proficiencias_ferramentas TEXT DEFAULT '[]',
                pericias_bonus TEXT DEFAULT '[]',
                
                -- Características
                caracteristicas TEXT DEFAULT '[]',
                resistencias TEXT DEFAULT '[]',
                imunidades TEXT DEFAULT '[]',
                
                -- Escolhas pendentes
                atributos_escolha INTEGER DEFAULT 0,
                pericias_escolha INTEGER DEFAULT 0,
                idiomas_escolha INTEGER DEFAULT 0,
                pericias_opcoes TEXT DEFAULT '[]',
                
                -- Subraça
                subraca_de INTEGER,
                
                ativo INTEGER DEFAULT 1,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (subraca_de) REFERENCES racas(id)
            )
        """)
        
        # ==================== CLASSES D&D 5e ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                fonte TEXT DEFAULT 'PHB',
                
                -- Dados de vida
                dado_vida INTEGER NOT NULL,
                hp_primeiro_nivel TEXT,
                
                -- Salvaguardas
                salvaguardas_proficientes TEXT DEFAULT '[]',
                
                -- Proficiências
                armaduras TEXT DEFAULT '[]',
                armas TEXT DEFAULT '[]',
                ferramentas TEXT DEFAULT '[]',
                
                -- Perícias
                pericias_disponiveis TEXT DEFAULT '[]',
                qtd_pericias INTEGER DEFAULT 2,
                
                -- Características nível 1
                caracteristicas_nivel_1 TEXT DEFAULT '[]',
                
                -- Magia
                conjurador INTEGER DEFAULT 0,
                atributo_conjuracao TEXT,
                magias_conhecidas_nivel_1 INTEGER DEFAULT 0,
                truques_nivel_1 INTEGER DEFAULT 0,
                
                ativo INTEGER DEFAULT 1,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ==================== PERÍCIAS D&D 5e ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pericias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                nome_display TEXT NOT NULL,
                atributo_base TEXT NOT NULL,
                descricao TEXT
            )
        """)
        
        # ==================== IDIOMAS D&D 5e ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS idiomas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                tipo TEXT DEFAULT 'comum',
                falantes TEXT
            )
        """)
        
        # ==================== TIPOS DE CRIATURA D&D 5e ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipos_criatura (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                nome_display TEXT NOT NULL,
                descricao TEXT,
                exemplos TEXT
            )
        """)
        
        # ==================== ANTECEDENTES D&D 5e ====================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS antecedentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                
                -- Proficiências
                pericias TEXT DEFAULT '[]',
                ferramentas TEXT DEFAULT '[]',
                idiomas_escolha INTEGER DEFAULT 0,
                
                -- Equipamento inicial
                equipamento TEXT DEFAULT '[]',
                dinheiro_inicial TEXT,
                
                -- Características
                caracteristica_nome TEXT,
                caracteristica_descricao TEXT,
                
                -- Personalidade
                tracos_personalidade TEXT DEFAULT '[]',
                ideais TEXT DEFAULT '[]',
                vinculos TEXT DEFAULT '[]',
                defeitos TEXT DEFAULT '[]',
                
                ativo INTEGER DEFAULT 1,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ==================== ÍNDICES PARA PERFORMANCE ====================
        
        # Índices para tabelas de regras
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_racas_nome ON racas(nome)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_racas_categoria ON racas(categoria)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_classes_nome ON classes(nome)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pericias_atributo ON pericias(atributo_base)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tipos_criatura_nome ON tipos_criatura(nome)")
        
        # Índices para buscas frequentes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_personagens_nome ON personagens(nome)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_personagens_ativo ON personagens(ativo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_monstros_nome ON monstros(nome)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_monstros_nd ON monstros(nd)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_npcs_nome ON npcs(nome)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_npcs_vivo ON npcs(vivo)")
        
        # Índices para histórico
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_acoes_sessao ON acoes_log(sessao_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_acoes_combate ON acoes_log(combate_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_acoes_atacante ON acoes_log(atacante_tipo, atacante_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_acoes_alvo ON acoes_log(alvo_tipo, alvo_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rolagens_sessao ON rolagens(sessao_id)")
        
        # Índices para instâncias
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_instancias_sessao ON monstros_instancias(sessao_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_instancias_ativo ON monstros_instancias(ativo)")
        
        # ==================== MIGRAÇÕES ====================
        _executar_migracoes(cursor)
        
        conn.commit()
        print("✅ Banco de dados inicializado com sucesso!")


def _executar_migracoes(cursor):
    """Executa migrações para atualizar schema existente"""
    
    # Verifica e adiciona coluna percepcao_passiva em personagens
    cursor.execute("PRAGMA table_info(personagens)")
    colunas_personagens = [col[1] for col in cursor.fetchall()]
    
    if 'percepcao_passiva' not in colunas_personagens:
        print("[MIGRAÇÃO] Adicionando percepcao_passiva em personagens...")
        cursor.execute("ALTER TABLE personagens ADD COLUMN percepcao_passiva INTEGER DEFAULT 10")
        
        # Atualiza valores existentes baseado no modificador de sabedoria
        cursor.execute("SELECT id, atributos FROM personagens")
        for row in cursor.fetchall():
            id_p = row[0]
            atributos = json_loads_safe(row[1], {})
            sabedoria = atributos.get('sabedoria', 10)
            mod_sab = (sabedoria - 10) // 2
            percepcao_passiva = 10 + mod_sab
            cursor.execute("UPDATE personagens SET percepcao_passiva = ? WHERE id = ?", (percepcao_passiva, id_p))
        print(f"[MIGRAÇÃO] percepcao_passiva atualizada para personagens existentes")
    
    # Verifica e atualiza percepcao_passiva em monstros (se existir)
    cursor.execute("PRAGMA table_info(monstros)")
    colunas_monstros = [col[1] for col in cursor.fetchall()]
    
    if 'percepcao_passiva' in colunas_monstros:
        # Atualiza monstros existentes que tenham valor 0 ou default
        cursor.execute("SELECT id, atributos, percepcao_passiva FROM monstros WHERE percepcao_passiva = 0 OR percepcao_passiva = 10")
        for row in cursor.fetchall():
            id_m = row[0]
            atributos = json_loads_safe(row[1], {})
            sabedoria = atributos.get('sabedoria', 10)
            mod_sab = (sabedoria - 10) // 2
            percepcao_passiva = 10 + mod_sab
            if percepcao_passiva != row[2]:  # Só atualiza se for diferente do atual
                cursor.execute("UPDATE monstros SET percepcao_passiva = ? WHERE id = ?", (percepcao_passiva, id_m))
    
    # ==================== MIGRAÇÃO: campo observacoes ====================
    
    # Adiciona coluna observacoes em personagens
    cursor.execute("PRAGMA table_info(personagens)")
    colunas_personagens = [col[1] for col in cursor.fetchall()]
    
    if 'observacoes' not in colunas_personagens:
        print("[MIGRAÇÃO] Adicionando observacoes em personagens...")
        cursor.execute("ALTER TABLE personagens ADD COLUMN observacoes TEXT DEFAULT ''")
        print(f"[MIGRAÇÃO] observacoes adicionada em personagens")
    
    # Adiciona coluna observacoes em monstros
    if 'observacoes' not in colunas_monstros:
        print("[MIGRAÇÃO] Adicionando observacoes em monstros...")
        cursor.execute("ALTER TABLE monstros ADD COLUMN observacoes TEXT DEFAULT ''")
        print(f"[MIGRAÇÃO] observacoes adicionada em monstros")
    
    # Adiciona coluna observacoes em monstros_instancias
    cursor.execute("PRAGMA table_info(monstros_instancias)")
    colunas_instancias = [col[1] for col in cursor.fetchall()]
    
    if 'observacoes' not in colunas_instancias:
        print("[MIGRAÇÃO] Adicionando observacoes em monstros_instancias...")
        cursor.execute("ALTER TABLE monstros_instancias ADD COLUMN observacoes TEXT DEFAULT ''")
        print(f"[MIGRAÇÃO] observacoes adicionada em monstros_instancias")
    
    # ==================== MIGRAÇÃO: campo fonte em antecedentes ====================
    cursor.execute("PRAGMA table_info(antecedentes)")
    colunas_antecedentes = [col[1] for col in cursor.fetchall()]
    
    if 'fonte' not in colunas_antecedentes:
        print("[MIGRAÇÃO] Adicionando fonte em antecedentes...")
        cursor.execute("ALTER TABLE antecedentes ADD COLUMN fonte TEXT DEFAULT 'PHB'")
        print(f"[MIGRAÇÃO] fonte adicionada em antecedentes")


# ==================== HELPERS JSON ====================

def json_loads_safe(data: str, default=None):
    """Carrega JSON de forma segura"""
    if data is None:
        return default
    try:
        return json.loads(data)
    except:
        return default


def json_dumps(data) -> str:
    """Converte para JSON"""
    return json.dumps(data, ensure_ascii=False)


# ==================== CRUD GENÉRICO ====================

class BaseRepository:
    """Repositório base com operações CRUD"""
    
    table_name = ""
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]:
        with get_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {cls.table_name} WHERE id = ?", (id,))
            row = cursor.fetchone()
            return dict_from_row(row)
    
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
            
            # Verifica se a tabela tem coluna atualizado_em
            cursor = conn.execute(f"PRAGMA table_info({cls.table_name})")
            colunas = [row[1] for row in cursor.fetchall()]
            
            if 'atualizado_em' in colunas:
                sql = f"UPDATE {cls.table_name} SET {sets}, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?"
            else:
                sql = f"UPDATE {cls.table_name} SET {sets} WHERE id = ?"
            
            conn.execute(sql, (*data.values(), id))
            return True
    
    @classmethod
    def delete(cls, id: int) -> bool:
        with get_connection() as conn:
            conn.execute(f"DELETE FROM {cls.table_name} WHERE id = ?", (id,))
            return True


# Inicializa o banco ao importar o módulo
if not os.path.exists(DB_PATH):
    init_database()
