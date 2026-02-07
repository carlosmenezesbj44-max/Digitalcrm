import sys
sys.path.insert(0, r'c:\Users\menezes\OneDrive\Documentos\DigitalcodeCRM\crm_provedor')

from crm_modules.usuarios.service import UsuarioService
from crm_core.db.base import get_db_session

db = get_db_session()
try:
    s = UsuarioService(db)
    r = s.autenticar('admin', 'senha123456', '127.0.0.1')
    print(r.access_token)
finally:
    db.close()
