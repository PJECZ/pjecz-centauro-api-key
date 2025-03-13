"""
Usuarios, esquemas
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsuarioOut(BaseModel):
    """Esquema para entregar usuarios"""

    email: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    model_config = ConfigDict(from_attributes=True)


class UsuarioInDB(UsuarioOut):
    """Usuario en base de datos"""

    username: str
    permissions: dict
    hashed_password: str
    disabled: bool
    api_key: str
    api_key_expiracion: datetime
