#!/usr/bin/env python
"""Script para verificar se os monstros foram adicionados corretamente"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.modulos.repositories import MonstroRepository

def verificar_monstros():
    print("=== Verificando Monstros Adicionados ===\n")
    
    monstros = MonstroRepository.get_all()
    monstros_underdark = [m for m in monstros if m.get('fonte') == 'Out of the Abyss']
    
    print(f"Total de monstros no sistema: {len(monstros)}")
    print(f"Monstros de Out of the Abyss: {len(monstros_underdark)}")
    print()
    
    print("Monstros adicionados:")
    for m in sorted(monstros_underdark, key=lambda x: x['nd']):
        print(f"  • {m['nome']} (ND {m['nd']})")
    
    print()
    print("🎯 Verificação concluída!")

if __name__ == "__main__":
    verificar_monstros()