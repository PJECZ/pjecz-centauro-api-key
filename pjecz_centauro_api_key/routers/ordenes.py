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
from ..models.respuestas_firmas import RespuestaFirma
from ..schemas.ordenes import OrdenOut

ordenes = APIRouter(prefix="/api/v1/ordenes")


@ordenes.get("/", response_model=CustomPage[OrdenOut])
async def paginado_ordenes_aprehnsion(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    imputado: str = None,
):
    """Órdenes de Aprehensión"""
    if current_user.permissions.get("ORDENES", 0) < 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = (
        database.query(Orden).
        join(RespuestaFirma, Orden.id == RespuestaFirma.orden_id).
        order_by(Orden.id.desc())
    )
    if imputado is not None:
        consulta = consulta.filter(Orden.imputado.contains(imputado))
    consulta = consulta.filter(Orden.tipo == "Orden de Aprehensión")
    return paginate(consulta)
