"""
Órdenes, modelos
"""

from datetime import datetime
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin

class Orden(Base, UniversalMixin):
    """Orden"""

    # Nombre de la tabla
    __tablename__ = "ordenes"

    # Clave primaria
    id: Mapped[int] = mapped_column("id", primary_key=True)

    # Columnas
    causa: Mapped[str] = mapped_column(String(50))
    firmante: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(50))
    fecha_registro: Mapped[Optional[datetime]]
    estatus: Mapped[str] = mapped_column(String(30))
    expediente: Mapped[Optional[str]] = mapped_column(String(30))
    imputado: Mapped[Optional[str]] = mapped_column(String(500))

    # Hijo
    respuestas_firmas: Mapped[List["RespuestaFirma"]] = relationship("RespuestaFirma", back_populates="orden")

    def __repr__(self):
        """Representación"""
        return f"<Orden {self.id}>"
