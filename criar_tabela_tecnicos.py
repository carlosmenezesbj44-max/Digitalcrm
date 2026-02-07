import sys
import os
sys.path.append(os.path.dirname(__file__))

from crm_core.db.base import engine
from crm_modules.tecnicos.models import TecnicoModel

# Criar a tabela
TecnicoModel.__table__.create(engine, checkfirst=True)
print("[OK] Tabela 'tecnicos' criada com sucesso!")
