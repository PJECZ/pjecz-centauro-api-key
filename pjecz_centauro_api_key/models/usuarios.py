"""
Usuarios, modelos
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Usuario(Base, UniversalMixin):
    """Usuario"""

    # Nombre de la tabla
    __tablename__ = "usuarios"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    email: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    nombres: Mapped[str] = mapped_column(String(256))
    apellido_paterno: Mapped[str] = mapped_column(String(256))
    apellido_materno: Mapped[str] = mapped_column(String(256))
    api_key: Mapped[Optional[str]] = mapped_column(String(128))
    api_key_expiracion: Mapped[Optional[datetime]]
