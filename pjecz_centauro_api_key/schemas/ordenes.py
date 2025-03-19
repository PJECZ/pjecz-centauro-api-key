"""
Órdenes, esquemas
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrdenOut(BaseModel):
    """Esquema para entregar documentos"""

    id: int
    causa: str
    firmante: str
    tipo: str
    fecha_registro: datetime | None
    estatus: str
    expediente: str | None
    imputado: str | None
    model_config = ConfigDict(from_attributes=True)
