"""
Repositórios de Dados - Acesso rápido ao SQLite
Cada repositório gerencia uma entidade específica
"""

from typing import Dict, List, Any, Optional
from .database import (
    get_connection, BaseRepository, 
    json_loads_safe, json_dumps, dict_from_row
)


# ==================== PERSONAGENS ====================

class PersonagemRepository(BaseRepository):
    table_name = "personagens"
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]:
        """Retorna personagem com campos JSON parseados"""
        data = super().get_by_id(id)
        if data:
            cls._parse_json_fields(data)
        return data
    
    @classmethod
    def get_all_ativos(cls) -> List[Dict]:
        """Retorna todos os personagens ativos"""
        results = cls.get_all(where="ativo = 1")
        for r in results:
            cls._parse_json_fields(r)
        return results
    
    @classmethod
    def criar(cls, dados: Dict) -> Dict:
        """Cria um novo personagem"""
        # Prepara campos JSON
        dados_db = cls._prepare_for_db(dados)
        id = cls.insert(dados_db)
        return cls.get_by_id(id)
    
    @classmethod
    def atualizar(cls, id: int, dados: Dict) -> Dict:
        """Atualiza um personagem"""
        dados_db = cls._prepare_for_db(dados)
        cls.update(id, dados_db)
        return cls.get_by_id(id)
    
    @classmethod
    def atualizar_campo(cls, id: int, campo: str, valor: Any) -> Dict:
        """Atualiza um campo específico"""
        # Se for campo JSON, precisa carregar, modificar e salvar
        json_fields = ['atributos', 'pericias_proficientes', 'pericias_expertise', 
                       'salvaguardas_proficientes', 'espacos_magia', 'espacos_usados',
                       'magias_conhecidas', 'magias_preparadas', 'equipamento', 
                       'armas', 'condicoes']
        
        if '.' in campo:
            # Campo aninhado como "atributos.forca"
            partes = campo.split('.')
            campo_base = partes[0]
            subcampo = partes[1]
            
            personagem = cls.get_by_id(id)
            if personagem and campo_base in personagem:
                obj = personagem[campo_base]
                if isinstance(obj, dict):
                    obj[subcampo] = valor
                    return cls.atualizar(id, {campo_base: obj})
        
        if campo in json_fields and not isinstance(valor, str):
            valor = json_dumps(valor)
        
        cls.update(id, {campo: valor})
        return cls.get_by_id(id)
    
    @classmethod
    def aplicar_dano(cls, id: int, dano: int) -> Dict:
        """Aplica dano ao personagem"""
        with get_connection() as conn:
            # Primeiro pega HP atual e temporário
            cursor = conn.execute(
                "SELECT hp_atual, hp_temporario FROM personagens WHERE id = ?", 
                (id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            
            hp_atual = row['hp_atual']
            hp_temp = row['hp_temporario']
            
            # Primeiro consome HP temporário
            if hp_temp > 0:
                if dano <= hp_temp:
                    conn.execute(
                        "UPDATE personagens SET hp_temporario = ? WHERE id = ?",
                        (hp_temp - dano, id)
                    )
                    return cls.get_by_id(id)
                else:
                    dano -= hp_temp
                    hp_temp = 0
            
            # Depois aplica no HP normal
            novo_hp = max(0, hp_atual - dano)
            conn.execute(
                "UPDATE personagens SET hp_atual = ?, hp_temporario = ? WHERE id = ?",
                (novo_hp, hp_temp, id)
            )
            
        return cls.get_by_id(id)
    
    @classmethod
    def curar(cls, id: int, quantidade: int) -> Dict:
        """Cura o personagem e reseta testes de morte se HP > 0"""
        with get_connection() as conn:
            # Cura e reseta testes de morte
            conn.execute(
                """UPDATE personagens 
                   SET hp_atual = MIN(hp_maximo, hp_atual + ?),
                       sucesso_morte = CASE WHEN hp_atual + ? > 0 THEN 0 ELSE sucesso_morte END,
                       falha_morte = CASE WHEN hp_atual + ? > 0 THEN 0 ELSE falha_morte END
                   WHERE id = ?""",
                (quantidade, quantidade, quantidade, id)
            )
        return cls.get_by_id(id)
    
    @staticmethod
    def _parse_json_fields(data: Dict):
        """Parse campos JSON do banco para dicts/lists"""
        json_fields = ['atributos', 'pericias_proficientes', 'pericias_expertise',
                       'salvaguardas_proficientes', 'espacos_magia', 'espacos_usados',
                       'magias_conhecidas', 'magias_preparadas', 'equipamento',
                       'equipamentos', 'armas', 'condicoes', 'moedas', 'dados_vida_tipos']
        
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                default = {} if field in ('espacos_magia', 'espacos_usados', 'atributos', 'moedas') else []
                data[field] = json_loads_safe(data[field], default)
    
    @staticmethod
    def _prepare_for_db(dados: Dict) -> Dict:
        """Prepara dados para inserção no banco"""
        json_fields = ['atributos', 'pericias_proficientes', 'pericias_expertise',
                       'salvaguardas_proficientes', 'espacos_magia', 'espacos_usados',
                       'magias_conhecidas', 'magias_preparadas', 'equipamento',
                       'equipamentos', 'armas', 'condicoes', 'moedas', 'dados_vida_tipos']
        
        result = {}
        for k, v in dados.items():
            if k in json_fields and not isinstance(v, str):
                result[k] = json_dumps(v)
            else:
                result[k] = v
        return result


# ==================== MONSTROS ====================

class MonstroRepository(BaseRepository):
    table_name = "monstros"
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]:
        data = super().get_by_id(id)
        if data:
            cls._parse_json_fields(data)
        return data
    
    @classmethod
    def get_all(cls, where: str = None, params: tuple = None) -> List[Dict]:
        results = super().get_all(where, params)
        for r in results:
            cls._parse_json_fields(r)
        return results
    
    @classmethod
    def buscar_por_nome(cls, nome: str) -> List[Dict]:
        """Busca monstros por nome (parcial)"""
        return cls.get_all(where="nome LIKE ?", params=(f"%{nome}%",))
    
    @classmethod
    def buscar_por_nd(cls, nd_min: float, nd_max: float) -> List[Dict]:
        """Busca monstros por faixa de ND"""
        return cls.get_all(where="nd >= ? AND nd <= ?", params=(nd_min, nd_max))
    
    @classmethod
    def criar(cls, dados: Dict) -> Dict:
        dados_db = cls._prepare_for_db(dados)
        id = cls.insert(dados_db)
        return cls.get_by_id(id)
    
    @classmethod
    def atualizar(cls, id: int, dados: Dict) -> Dict:
        """Atualiza um monstro (prepara campos JSON)"""
        dados_db = cls._prepare_for_db(dados)
        # Update sem atualizado_em (tabela monstros não tem esse campo)
        with get_connection() as conn:
            sets = ", ".join([f"{k} = ?" for k in dados_db.keys()])
            sql = f"UPDATE {cls.table_name} SET {sets} WHERE id = ?"
            conn.execute(sql, (*dados_db.values(), id))
        return cls.get_by_id(id)
    
    @staticmethod
    def _parse_json_fields(data: Dict):
        json_fields = ['atributos', 'velocidade', 'salvaguardas', 'pericias',
                       'resistencias', 'imunidades_dano', 'imunidades_condicao',
                       'vulnerabilidades', 'sentidos', 'idiomas', 'habilidades',
                       'acoes', 'acoes_bonus', 'reacoes', 'acoes_lendarias']
        
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                default = {} if field in ['atributos', 'velocidade', 'salvaguardas', 'pericias', 'sentidos'] else []
                data[field] = json_loads_safe(data[field], default)
    
    @staticmethod
    def _prepare_for_db(dados: Dict) -> Dict:
        json_fields = ['atributos', 'velocidade', 'salvaguardas', 'pericias',
                       'resistencias', 'imunidades_dano', 'imunidades_condicao',
                       'vulnerabilidades', 'sentidos', 'idiomas', 'habilidades',
                       'acoes', 'acoes_bonus', 'reacoes', 'acoes_lendarias']
        
        result = {}
        for k, v in dados.items():
            if k in json_fields and not isinstance(v, str):
                result[k] = json_dumps(v)
            else:
                result[k] = v
        return result


# ==================== INSTÂNCIAS DE MONSTROS ====================

class InstanciaMonstroRepository(BaseRepository):
    table_name = "monstros_instancias"
    
    @classmethod
    def update(cls, id: int, dados: Dict) -> bool:
        """Atualiza instância, tratando campos JSON"""
        # Prepara campos JSON
        json_fields = ['condicoes', 'acoes_usadas']
        prepared = {}
        for k, v in dados.items():
            if k in json_fields and not isinstance(v, str):
                prepared[k] = json_dumps(v)
            else:
                prepared[k] = v
        return super().update(id, prepared)
    
    @classmethod
    def criar_instancia(cls, monstro_id: int, nome: str, sessao_id: int = None) -> Dict:
        """Cria uma instância de monstro para combate"""
        monstro = MonstroRepository.get_by_id(monstro_id)
        if not monstro:
            return None
        
        # Calcula HP (usa médio ou rola)
        from .dados import rolar_expressao
        hp = monstro.get('hp_medio') or rolar_expressao(monstro.get('hp_formula', '1d8'))['total']
        
        dados = {
            'monstro_id': monstro_id,
            'sessao_id': sessao_id,
            'nome': nome or monstro['nome'],
            'hp_maximo': hp,
            'hp_atual': hp,
            'ca': monstro['ca'],
            'condicoes': '[]',
            'acoes_usadas': '{}'
        }
        
        id = cls.insert(dados)
        return cls.get_completo(id)
    
    @classmethod
    def get_completo(cls, id: int) -> Optional[Dict]:
        """Retorna instância com dados do monstro base"""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT i.*, m.nome as monstro_nome, m.tipo, m.tamanho, m.nd, m.xp,
                       m.atributos, m.velocidade, m.resistencias, m.imunidades_dano,
                       m.vulnerabilidades, m.habilidades, m.acoes, m.acoes_bonus,
                       m.reacoes, m.acoes_lendarias
                FROM monstros_instancias i
                JOIN monstros m ON i.monstro_id = m.id
                WHERE i.id = ?
            """, (id,))
            row = cursor.fetchone()
            if row:
                data = dict_from_row(row)
                # Parse JSON fields
                for field in ['condicoes', 'acoes_usadas', 'atributos', 'velocidade',
                              'resistencias', 'imunidades_dano', 'vulnerabilidades',
                              'habilidades', 'acoes', 'acoes_bonus', 'reacoes', 'acoes_lendarias']:
                    if field in data and isinstance(data[field], str):
                        data[field] = json_loads_safe(data[field], [] if field not in ['atributos', 'velocidade', 'acoes_usadas'] else {})
                return data
            return None
    
    @classmethod
    def get_ativos_sessao(cls, sessao_id: int) -> List[Dict]:
        """Retorna todas as instâncias ativas de uma sessão"""
        results = cls.get_all(where="sessao_id = ? AND ativo = 1", params=(sessao_id,))
        return [cls.get_completo(r['id']) for r in results]
    
    @classmethod
    def aplicar_dano(cls, id: int, dano: int, tipo_dano: str = None) -> Dict:
        """Aplica dano considerando resistências/vulnerabilidades"""
        instancia = cls.get_completo(id)
        if not instancia:
            return None
        
        dano_final = dano
        
        if tipo_dano:
            if tipo_dano in instancia.get('imunidades_dano', []):
                dano_final = 0
            elif tipo_dano in instancia.get('resistencias', []):
                dano_final = dano // 2
            elif tipo_dano in instancia.get('vulnerabilidades', []):
                dano_final = dano * 2
        
        novo_hp = max(0, instancia['hp_atual'] - dano_final)
        morto = 1 if novo_hp == 0 else 0
        
        with get_connection() as conn:
            conn.execute(
                "UPDATE monstros_instancias SET hp_atual = ?, morto = ? WHERE id = ?",
                (novo_hp, morto, id)
            )
        
        return cls.get_completo(id)
    
    @classmethod
    def curar(cls, id: int, quantidade: int) -> Dict:
        with get_connection() as conn:
            conn.execute(
                "UPDATE monstros_instancias SET hp_atual = MIN(hp_maximo, hp_atual + ?), morto = 0 WHERE id = ?",
                (quantidade, id)
            )
        return cls.get_completo(id)


# ==================== NPCs ====================

class NPCRepository(BaseRepository):
    table_name = "npcs"
    
    @classmethod
    def _parse_json_fields(cls, data: Dict) -> None:
        """Parseia campos JSON do NPC"""
        json_fields = ['atributos', 'acoes']
        for field in json_fields:
            if field in data and data[field]:
                data[field] = json_loads_safe(data[field], default=[])
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[Dict]:
        """Retorna NPC com campos JSON parseados"""
        data = super().get_by_id(id)
        if data:
            cls._parse_json_fields(data)
        return data
    
    @classmethod
    def get_all(cls, where: str = None, params: tuple = None) -> List[Dict]:
        """Retorna todos os NPCs com campos JSON parseados"""
        results = super().get_all(where, params)
        for r in results:
            cls._parse_json_fields(r)
        return results
    
    @classmethod
    def get_conhecidos(cls) -> List[Dict]:
        """Retorna NPCs que o grupo já conhece"""
        return cls.get_all(where="conhecido = 1 AND vivo = 1")
    
    @classmethod
    def get_por_localizacao(cls, local: str) -> List[Dict]:
        """Busca NPCs por localização"""
        return cls.get_all(where="localizacao LIKE ?", params=(f"%{local}%",))


# ==================== SESSÕES ====================

class SessaoRepository(BaseRepository):
    table_name = "sessoes"
    
    @classmethod
    def criar_sessao(cls, numero: int, titulo: str = None) -> Dict:
        from datetime import datetime
        dados = {
            'numero': numero,
            'data': datetime.now().strftime('%Y-%m-%d'),
            'titulo': titulo or f"Sessão {numero}"
        }
        id = cls.insert(dados)
        return cls.get_by_id(id)
    
    @classmethod
    def get_ultima(cls) -> Optional[Dict]:
        """Retorna a última sessão"""
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM sessoes ORDER BY numero DESC LIMIT 1"
            )
            return dict_from_row(cursor.fetchone())


# ==================== LOG DE AÇÕES ====================

class AcaoLogRepository(BaseRepository):
    table_name = "acoes_log"
    
    @classmethod
    def registrar(cls, dados: Dict) -> Dict:
        """Registra uma ação no log"""
        # Prepara campos JSON
        if 'rolagem_ataque' in dados and not isinstance(dados['rolagem_ataque'], str):
            dados['rolagem_ataque'] = json_dumps(dados['rolagem_ataque'])
        if 'dano_detalhes' in dados and not isinstance(dados['dano_detalhes'], str):
            dados['dano_detalhes'] = json_dumps(dados['dano_detalhes'])
        if 'efeitos' in dados and not isinstance(dados['efeitos'], str):
            dados['efeitos'] = json_dumps(dados['efeitos'])
        if 'valores_originais' in dados and not isinstance(dados['valores_originais'], str):
            dados['valores_originais'] = json_dumps(dados['valores_originais'])
        
        id = cls.insert(dados)
        return cls.get_by_id(id)
    
    @classmethod
    def get_por_sessao(cls, sessao_id: int) -> List[Dict]:
        """Retorna todas as ações de uma sessão"""
        return cls.get_all(where="sessao_id = ?", params=(sessao_id,))
    
    @classmethod
    def get_por_combate(cls, combate_id: int) -> List[Dict]:
        """Retorna todas as ações de um combate"""
        return cls.get_all(where="combate_id = ?", params=(combate_id,))
    
    @classmethod
    def get_por_entidade(cls, tipo: str, id: int) -> List[Dict]:
        """Retorna todas as ações de uma entidade (como atacante)"""
        return cls.get_all(
            where="atacante_tipo = ? AND atacante_id = ?",
            params=(tipo, id)
        )
    
    @classmethod
    def estatisticas_personagem(cls, personagem_id: int) -> Dict:
        """Retorna estatísticas de um personagem"""
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_ataques,
                    SUM(CASE WHEN acertou = 1 THEN 1 ELSE 0 END) as acertos,
                    SUM(CASE WHEN critico = 1 THEN 1 ELSE 0 END) as criticos,
                    SUM(CASE WHEN falha_critica = 1 THEN 1 ELSE 0 END) as falhas_criticas,
                    SUM(dano) as dano_total,
                    AVG(dano) as dano_medio
                FROM acoes_log
                WHERE atacante_tipo = 'personagem' AND atacante_id = ? AND tipo_acao = 'ataque'
            """, (personagem_id,))
            return dict_from_row(cursor.fetchone())


# ==================== ROLAGENS ====================

class RolagemRepository(BaseRepository):
    table_name = "rolagens"
    
    @classmethod
    def registrar(cls, dados: Dict) -> Dict:
        if 'dados' in dados and not isinstance(dados['dados'], str):
            dados['dados'] = json_dumps(dados['dados'])
        id = cls.insert(dados)
        return cls.get_by_id(id)


# ==================== COMBATES ====================

class CombateRepository(BaseRepository):
    table_name = "combates"
    
    @classmethod
    def criar(cls, sessao_id: int, nome: str = None) -> Dict:
        dados = {
            'sessao_id': sessao_id,
            'nome': nome,
            'ativo': 1
        }
        id = cls.insert(dados)
        return cls.get_by_id(id)
    
    @classmethod
    def get_ativo(cls) -> Optional[Dict]:
        """Retorna o combate ativo"""
        results = cls.get_all(where="ativo = 1")
        if results:
            data = results[0]
            if 'ordem_iniciativa' in data:
                data['ordem_iniciativa'] = json_loads_safe(data['ordem_iniciativa'], [])
            return data
        return None
    
    @classmethod
    def atualizar_iniciativa(cls, id: int, ordem: List[Dict]) -> Dict:
        with get_connection() as conn:
            conn.execute(
                "UPDATE combates SET ordem_iniciativa = ? WHERE id = ?",
                (json_dumps(ordem), id)
            )
        return cls.get_by_id(id)
    
    @classmethod
    def finalizar(cls, id: int) -> Dict:
        with get_connection() as conn:
            conn.execute(
                "UPDATE combates SET ativo = 0, finalizado = 1, finalizado_em = CURRENT_TIMESTAMP WHERE id = ?",
                (id,)
            )
        return cls.get_by_id(id)
