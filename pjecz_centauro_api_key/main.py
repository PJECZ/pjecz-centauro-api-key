"""
PJECZ Centauro API Key
"""

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers.ordenes import ordenes
from .routers.respuestas_firmas import respuestas_firmas
from .routers.usuarios import usuarios

app = FastAPI(
    title="PJECZ Centauro API Key",
    description="API Key para el proyecto Centauro de PJECZ",
    docs_url="/docs",
)

app.include_router(ordenes)
app.include_router(respuestas_firmas)
app.include_router(usuarios)

# Paginación
add_pagination(app)


@app.get("/")
async def root():
    """Mensaje de bienvenida"""
    return {"message": "Hola Mundo!"}
