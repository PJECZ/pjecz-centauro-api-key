"""
Respuestas-Firmas, esquemas
"""

from pydantic import BaseModel, ConfigDict


class RespuestaFirmaOut(BaseModel):
    """Esquema para entregar respuesta-firma"""

    orden_id: int | None
    url_descarga: str | None
    causa: str | None
    firmante: str | None
    tipo: str | None
    imputado: str | None
    model_config = ConfigDict(from_attributes=True)
