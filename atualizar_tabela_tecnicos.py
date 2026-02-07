import sys
import os
sys.path.append(os.path.dirname(__file__))

from crm_core.db.base import engine
from crm_modules.tecnicos.models import TecnicoModel

# Deletar a tabela antiga
TecnicoModel.__table__.drop(engine, checkfirst=True)
print("[OK] Tabela antiga deletada")

# Criar a tabela nova
TecnicoModel.__table__.create(engine, checkfirst=True)
print("[OK] Tabela nova criada com sucesso!")
