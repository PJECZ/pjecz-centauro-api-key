"""
Usuarios
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..settings import Settings, get_settings
from ..schemas.usuarios import UsuarioOut

usuarios = APIRouter(prefix="/api/v1/usuarios")


@usuarios.get("/", response_model=UsuarioOut)
async def paginado_usuarios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """Obtener usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return UsuarioOut(
        email=settings.user_email,
        nombres=settings.user_nombres,
        apellido_paterno=settings.user_apellido_paterno,
        apellido_materno=settings.user_apellido_materno,
    )
