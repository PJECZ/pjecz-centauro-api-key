"""
Respuestas-Firmas
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
from ..schemas.respuestas_firmas import RespuestaFirmaOut

respuestas_firmas = APIRouter(prefix="/api/v1/respuestas_firmas")


@respuestas_firmas.get("/", response_model=CustomPage[RespuestaFirmaOut])
async def paginado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    imputado: str = None,
    tipo: str = None,
):
    """Obtener órdenes"""
    if current_user.permissions.get("ORDENES", 0) < 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = (
        database.query(RespuestaFirma).
        join(Orden, Orden.folio == RespuestaFirma.orden_id).
        order_by(Orden.id.desc())
    )
    if imputado is not None:
        consulta = consulta.filter(Orden.imputado.contains(imputado))
    if tipo is not None:
        consulta = consulta.filter(Orden.tipo == tipo)
    return paginate(consulta)
