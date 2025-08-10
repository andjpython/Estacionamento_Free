#!/usr/bin/env python3
"""
Health check para o Render
Verifica se a aplicação está funcionando corretamente
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from db import engine
    
    # Testar conexão com o banco
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        if result.scalar() == 1:
            print("✅ Health check: OK")
            sys.exit(0)
        else:
            print("❌ Health check: Falha no banco")
            sys.exit(1)
            
except Exception as e:
    print(f"❌ Health check: Erro - {e}")
    sys.exit(1)
