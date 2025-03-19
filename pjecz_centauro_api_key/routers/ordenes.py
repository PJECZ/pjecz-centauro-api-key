"""
Órdenes
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import UsuarioInDB, get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_string
from ..models.ordenes import Orden
from ..schemas.ordenes import OrdenOut

ordenes = APIRouter(prefix="/api/v1/ordenes")


@ordenes.get("/", response_model=CustomPage[OrdenOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Obtener órdenes"""
    if current_user.permissions.get("ORDENES", 0) < 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Orden).order_by(Orden.id.desc()))
