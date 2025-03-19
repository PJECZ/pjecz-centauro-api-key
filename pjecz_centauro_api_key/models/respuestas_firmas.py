"""
Respuestas-Firmas, modelos
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class RespuestaFirma(Base, UniversalMixin):
    """RespuestaFirma"""

    # Nombre de la tabla
    __tablename__ = "tbl_respuestafirma"

    # Clave primaria
    id: Mapped[int] = mapped_column("idrespuestafirmaPrimaria", primary_key=True)

    # Clave foránea
    orden_id: Mapped[int] = mapped_column("folio", ForeignKey("ordenes.id"))
    orden: Mapped["Orden"] = relationship(back_populates="respuestas_firmas")

    # Columnas
    url_descarga: Mapped[Optional[str]] = mapped_column("urlDescarga")

    @property
    def causa(self):
        """Causa"""
        return self.orden.causa

    @property
    def firmante(self):
        """Firmante"""
        return self.orden.firmante

    @property
    def tipo(self):
        """Tipo"""
        return self.orden.tipo

    @property
    def imputado(self):
        """Imputado"""
        return self.orden.imputado

    def __repr__(self):
        """Representación"""
        return f"<RespuestaFirma {self.id}>"
