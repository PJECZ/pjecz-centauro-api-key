"""
Authentications
"""

import re
from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from hashids import Hashids
from starlette.status import HTTP_403_FORBIDDEN
from unidecode import unidecode

from ..models.usuarios import Usuario
from ..schemas.usuarios import UsuarioInDB
from ..settings import Settings, get_settings
from .exceptions import MyAuthenticationError

API_KEY_REGEXP = r"^\w+\.\w+\.\w+$"


def get_user(usuario_id: int, settings: Annotated[Settings, Depends(get_settings)]) -> Optional[UsuarioInDB]:
    """Consultar el usuario"""

    # Convertir el texto de palabras separadas por comas en un diccionario
    permissions = {}
    for key in settings.user_permissions.split(","):
        permissions[key.upper()] = 1

    # Convertir a tiempo la fecha de expiración de la API key
    try:
        api_key_expiracion = datetime.strptime("%Y-%m-%d", settings.user_api_key_expiracion)
    except ValueError:
        api_key_expiracion = datetime.now() + timedelta(days=30)

    # Entregar
    if settings:
        return UsuarioInDB(
            id=usuario_id,
            email=settings.user_email,
            nombres=settings.user_nombres,
            apellido_paterno=settings.user_apellido_paterno,
            apellido_materno=settings.user_apellido_materno,
            username=settings.user_email,
            permissions=permissions,
            hashed_password=settings.user_hashed_password,
            disabled=settings.user_disabled == "1",
            api_key=settings.user_api_key,
            api_key_expiracion=api_key_expiracion,
        )
    return None


def authenticate_user(api_key: str, settings: Annotated[Settings, Depends(get_settings)]) -> UsuarioInDB:
    """Autentificar un usuario por su api_key"""

    # Validar con expresión regular
    api_key = unidecode(api_key)
    if re.match(API_KEY_REGEXP, api_key) is None:
        raise MyAuthenticationError("No paso la validación por expresión regular")

    # Separar el ID, el email y la cadena aleatoria del api_key
    api_key_id, api_key_email, _ = api_key.split(".")

    # Decodificar el ID
    usuario_id = Usuario.decode_id(api_key_id)
    if usuario_id is None:
        raise MyAuthenticationError("No se pudo descifrar el ID")

    # Consultar
    usuario = get_user(usuario_id, settings)
    if usuario is None:
        raise MyAuthenticationError("No se encontró el usuario")

    # Validar el api_key
    if usuario.api_key != api_key:
        raise MyAuthenticationError("No es igual la api_key al dato en la base de datos")

    # Validar el email
    if api_key_email != Hashids(salt=usuario.email, min_length=8).encode(1):
        raise MyAuthenticationError("No coincide el correo electrónico")

    # Validar el tiempo de expiración
    if usuario.api_key_expiracion < datetime.now():
        raise MyAuthenticationError("No vigente porque ya expiró")

    # Validad que sea activo
    if usuario.disabled:
        raise MyAuthenticationError("No es activo este usuario porque fue eliminado")

    # Entregar
    return usuario


async def get_current_active_user(
    api_key: Annotated[str, Depends(APIKeyHeader(name="X-Api-Key"))],
    settings: Annotated[Settings, Depends(get_settings)],
) -> UsuarioInDB:
    """Obtener el usuario activo actual"""

    # Try-except
    try:
        usuario = authenticate_user(api_key, settings)
    except MyAuthenticationError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(error)) from error

    # Entregar
    return usuario
