"""
PJECZ Centauro API Key
"""

from fastapi import FastAPI

# Hazme un hola mundo con FastAPI
app = FastAPI(
    title="PJECZ Centauro API Key",
    description="API Key para el proyecto Centauro de PJECZ",
    docs_url=None,
)

@app.get("/")
async def root():
    """Mensaje de bienvenida"""
    return {"message": "Hello World"}
