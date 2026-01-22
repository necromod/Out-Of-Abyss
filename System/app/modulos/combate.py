"""
Módulo de Combate - Sistema de combate D&D 5e
Gerencia turnos, ações, ataques e cálculos de combate
"""

from typing import Dict, List, Any, Optional
from uuid import uuid4
from datetime import datetime
from .dados import rolar_expressao, rolar_com_vantagem, rolar_com_desvantagem


class Acao:
    """Representa uma ação executada no combate"""
    
    def __init__(self, dados: Dict[str, Any]):
        self.id = str(uuid4())
        self.timestamp = datetime.now().isoformat()
        
        self.atacante_id = dados.get('atacante_id')
        self.atacante_nome = dados.get('atacante_nome', 'Desconhecido')
        self.alvo_id = dados.get('alvo_id')
        self.alvo_nome = dados.get('alvo_nome', 'Desconhecido')
        
        self.tipo = dados.get('tipo')  # ataque, magia, habilidade, etc
        self.nome = dados.get('nome', '')
        
        # Resultados
        self.rolagem_ataque = dados.get('rolagem_ataque')
        self.acertou = dados.get('acertou', False)
        self.critico = dados.get('critico', False)
        self.falha_critica = dados.get('falha_critica', False)
        
        self.dano = dados.get('dano', 0)
        self.tipo_dano = dados.get('tipo_dano')
        self.dano_detalhes = dados.get('dano_detalhes', {})
        
        # Efeitos adicionais
        self.efeitos = dados.get('efeitos', [])
        
        # Valores que podem ser sobrescritos
        self.sobrescrito = False
        self.valores_originais = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'atacante_id': self.atacante_id,
            'atacante_nome': self.atacante_nome,
            'alvo_id': self.alvo_id,
            'alvo_nome': self.alvo_nome,
            'tipo': self.tipo,
            'nome': self.nome,
            'rolagem_ataque': self.rolagem_ataque,
            'acertou': self.acertou,
            'critico': self.critico,
            'falha_critica': self.falha_critica,
            'dano': self.dano,
            'tipo_dano': self.tipo_dano,
            'dano_detalhes': self.dano_detalhes,
            'efeitos': self.efeitos,
            'sobrescrito': self.sobrescrito
        }


class Turno:
    """Representa um turno de combate"""
    
    def __init__(self, numero: int, participante_id: str, participante_nome: str):
        self.numero = numero
        self.participante_id = participante_id
        self.participante_nome = participante_nome
        self.acoes: List[Acao] = []
        self.finalizado = False
    
    def adicionar_acao(self, acao: Acao):
        self.acoes.append(acao)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'numero': self.numero,
            'participante_id': self.participante_id,
            'participante_nome': self.participante_nome,
            'acoes': [a.to_dict() for a in self.acoes],
            'finalizado': self.finalizado
        }


class SistemaCombate:
    """Sistema principal de gerenciamento de combate"""
    
    def __init__(self):
        self.ativo = False
        self.rodada = 0
        self.turno_atual = 0
        
        # Ordem de iniciativa: lista de {id, nome, iniciativa, tipo}
        self.ordem_iniciativa: List[Dict[str, Any]] = []
        
        # Histórico de turnos
        self.turnos: List[Turno] = []
        
        # Log de ações (todas as ações do combate)
        self.log: List[Acao] = []
        
        # Pilha de desfazer
        self._pilha_desfazer: List[Dict[str, Any]] = []
    
    def iniciar(self, participantes: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Inicia um novo combate"""
        self.ativo = True
        self.rodada = 1
        self.turno_atual = 0
        self.ordem_iniciativa = participantes or []
        self.turnos = []
        self.log = []
        self._pilha_desfazer = []
        
        return {
            'sucesso': True,
            'mensagem': 'Combate iniciado',
            'rodada': self.rodada,
            'participantes': len(self.ordem_iniciativa)
        }
    
    def definir_iniciativa(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Define ou atualiza a ordem de iniciativa"""
        participantes = dados.get('participantes', [])
        
        # Ordena por iniciativa (maior primeiro)
        self.ordem_iniciativa = sorted(
            participantes,
            key=lambda x: (x.get('iniciativa', 0), x.get('desempate', 0)),
            reverse=True
        )
        
        return {
            'sucesso': True,
            'ordem': self.ordem_iniciativa
        }
    
    def obter_ordem(self) -> Dict[str, Any]:
        """Retorna a ordem de iniciativa atual"""
        return {
            'rodada': self.rodada,
            'turno_atual': self.turno_atual,
            'ativo': self.ativo,
            'ordem': self.ordem_iniciativa,
            'participante_atual': self.ordem_iniciativa[self.turno_atual] if self.ordem_iniciativa else None
        }
    
    def proximo_turno(self) -> Dict[str, Any]:
        """Avança para o próximo turno"""
        if not self.ordem_iniciativa:
            return {'sucesso': False, 'erro': 'Nenhum participante na iniciativa'}
        
        self.turno_atual += 1
        
        # Se passou por todos, nova rodada
        if self.turno_atual >= len(self.ordem_iniciativa):
            self.turno_atual = 0
            self.rodada += 1
        
        participante = self.ordem_iniciativa[self.turno_atual]
        
        return {
            'sucesso': True,
            'rodada': self.rodada,
            'turno': self.turno_atual,
            'participante': participante
        }
    
    def turno_anterior(self) -> Dict[str, Any]:
        """Volta para o turno anterior"""
        if not self.ordem_iniciativa:
            return {'sucesso': False, 'erro': 'Nenhum participante na iniciativa'}
        
        self.turno_atual -= 1
        
        if self.turno_atual < 0:
            if self.rodada > 1:
                self.rodada -= 1
                self.turno_atual = len(self.ordem_iniciativa) - 1
            else:
                self.turno_atual = 0
        
        participante = self.ordem_iniciativa[self.turno_atual]
        
        return {
            'sucesso': True,
            'rodada': self.rodada,
            'turno': self.turno_atual,
            'participante': participante
        }
    
    def executar_acao(self, atacante_id: str, alvo_id: str, tipo_acao: str, detalhes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma ação de combate
        
        tipo_acao: 'ataque', 'magia', 'habilidade', 'desengajar', 'correr', 'esquivar', 'ajudar', 'esconder'
        """
        resultado = {
            'atacante_id': atacante_id,
            'atacante_nome': detalhes.get('atacante_nome', 'Atacante'),
            'alvo_id': alvo_id,
            'alvo_nome': detalhes.get('alvo_nome', 'Alvo'),
            'tipo': tipo_acao,
            'nome': detalhes.get('nome', tipo_acao)
        }
        
        if tipo_acao == 'ataque':
            resultado.update(self._executar_ataque(detalhes))
        elif tipo_acao == 'magia':
            resultado.update(self._executar_magia(detalhes))
        elif tipo_acao in ['desengajar', 'correr', 'esquivar', 'ajudar', 'esconder']:
            resultado.update({'sucesso': True, 'descricao': f'{tipo_acao.capitalize()} executado'})
        else:
            resultado.update(self._executar_acao_generica(detalhes))
        
        # Cria registro da ação
        acao = Acao(resultado)
        self.log.append(acao)
        
        # Salva estado para desfazer
        self._pilha_desfazer.append({
            'tipo': 'acao',
            'acao_id': acao.id,
            'dados': resultado
        })
        
        return {'sucesso': True, 'acao': acao.to_dict()}
    
    def _executar_ataque(self, detalhes: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula um ataque"""
        bonus_ataque = detalhes.get('bonus_ataque', 0)
        ca_alvo = detalhes.get('ca_alvo', 10)
        vantagem = detalhes.get('vantagem', False)
        desvantagem = detalhes.get('desvantagem', False)
        dano_expressao = detalhes.get('dano', '1d6')
        tipo_dano = detalhes.get('tipo_dano', 'cortante')
        
        # Rolagem de ataque
        if vantagem and not desvantagem:
            rolagem = rolar_com_vantagem(bonus_ataque)
        elif desvantagem and not vantagem:
            rolagem = rolar_com_desvantagem(bonus_ataque)
        else:
            rolagem = rolar_expressao(f'1d20+{bonus_ataque}')
        
        total_ataque = rolagem['total']
        critico = rolagem.get('critico', False)
        falha_critica = rolagem.get('falha_critica', False)
        
        # Verifica acerto
        acertou = False
        if critico:
            acertou = True
        elif falha_critica:
            acertou = False
        elif total_ataque >= ca_alvo:
            acertou = True
        
        # Calcula dano se acertou
        dano_total = 0
        dano_detalhes = {}
        
        if acertou:
            dano_result = rolar_expressao(dano_expressao)
            dano_total = dano_result['total']
            
            # Dano crítico: dobra os dados
            if critico:
                dano_extra = rolar_expressao(dano_expressao)
                dano_total += dano_extra['soma_dados']  # Só dados, não modificador
                dano_detalhes['critico_extra'] = dano_extra['soma_dados']
            
            dano_detalhes['rolagem'] = dano_result
        
        return {
            'rolagem_ataque': rolagem,
            'total_ataque': total_ataque,
            'ca_alvo': ca_alvo,
            'acertou': acertou,
            'critico': critico,
            'falha_critica': falha_critica,
            'dano': dano_total,
            'tipo_dano': tipo_dano,
            'dano_detalhes': dano_detalhes
        }
    
    def _executar_magia(self, detalhes: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma magia"""
        nome_magia = detalhes.get('nome', 'Magia')
        nivel = detalhes.get('nivel', 0)
        cd_salvaguarda = detalhes.get('cd_salvaguarda')
        tipo_salvaguarda = detalhes.get('tipo_salvaguarda')
        dano_expressao = detalhes.get('dano')
        tipo_dano = detalhes.get('tipo_dano')
        efeitos = detalhes.get('efeitos', [])
        
        resultado = {
            'nome': nome_magia,
            'nivel': nivel,
            'efeitos': efeitos
        }
        
        # Se tem salvaguarda
        if cd_salvaguarda and tipo_salvaguarda:
            resultado['cd_salvaguarda'] = cd_salvaguarda
            resultado['tipo_salvaguarda'] = tipo_salvaguarda
        
        # Se causa dano
        if dano_expressao:
            dano_result = rolar_expressao(dano_expressao)
            resultado['dano'] = dano_result['total']
            resultado['tipo_dano'] = tipo_dano
            resultado['dano_detalhes'] = dano_result
        
        return resultado
    
    def _executar_acao_generica(self, detalhes: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma ação genérica"""
        return {
            'descricao': detalhes.get('descricao', 'Ação executada'),
            'efeitos': detalhes.get('efeitos', [])
        }
    
    def desfazer_ultima_acao(self) -> Dict[str, Any]:
        """Desfaz a última ação"""
        if not self._pilha_desfazer:
            return {'sucesso': False, 'erro': 'Nada para desfazer'}
        
        ultimo = self._pilha_desfazer.pop()
        
        # Remove do log
        acao_id = ultimo.get('acao_id')
        self.log = [a for a in self.log if a.id != acao_id]
        
        return {
            'sucesso': True,
            'desfeito': ultimo
        }
    
    def sobrescrever_resultado(self, acao_id: str, novos_valores: Dict[str, Any]) -> Dict[str, Any]:
        """Permite ao mestre sobrescrever qualquer resultado"""
        for acao in self.log:
            if acao.id == acao_id:
                # Salva valores originais
                if not acao.sobrescrito:
                    acao.valores_originais = {
                        'acertou': acao.acertou,
                        'dano': acao.dano,
                        'critico': acao.critico
                    }
                
                # Aplica novos valores
                for campo, valor in novos_valores.items():
                    if hasattr(acao, campo):
                        setattr(acao, campo, valor)
                
                acao.sobrescrito = True
                
                return {
                    'sucesso': True,
                    'acao': acao.to_dict()
                }
        
        return {'sucesso': False, 'erro': 'Ação não encontrada'}
    
    def obter_log(self) -> List[Dict[str, Any]]:
        """Retorna o log completo do combate"""
        return {
            'combate_ativo': self.ativo,
            'rodada': self.rodada,
            'turno': self.turno_atual,
            'total_acoes': len(self.log),
            'acoes': [a.to_dict() for a in self.log]
        }
    
    def finalizar(self) -> Dict[str, Any]:
        """Finaliza o combate"""
        resumo = {
            'rodadas_totais': self.rodada,
            'acoes_totais': len(self.log),
            'log': self.obter_log()
        }
        
        self.ativo = False
        self.rodada = 0
        self.turno_atual = 0
        self.ordem_iniciativa = []
        
        return {
            'sucesso': True,
            'mensagem': 'Combate finalizado',
            'resumo': resumo
        }
