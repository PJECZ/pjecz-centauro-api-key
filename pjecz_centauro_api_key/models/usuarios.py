"""
Usuarios, modelos
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class Usuario(Base, UniversalMixin):
    """Usuario"""

    # Nombre de la tabla
    __tablename__ = "usuarios"

    # Clave primaria
    id: Mapped[int] = mapped_column("idRegistro", primary_key=True)

    # Columnas
    nombre: Mapped[str] = mapped_column("nombre", String(256))
    tipo_usuario: Mapped[str] = mapped_column("tipoUsuario", String(256))
    # api_key: Mapped[Optional[str]] = mapped_column(String(128))
    # api_key_expiracion: Mapped[Optional[datetime]]

    @property
    def permissions(self) -> dict:
        """Entrega un diccionario con todos los permisos"""
        return {
            "ORDENES": 1,
            "USUARIOS": 1,
        }

    def __repr__(self):
        """Representación"""
        return f"<Usuario {self.nombre}>"
