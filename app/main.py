from fastapi import FastAPI
#from app.routers import indicadores
from app.routers.indicadores import router as indicadores_router

app = FastAPI(
    title="API de Indicadores Académicos",
    description="Consulta de indicadores institucionales",
    version="1.0"
)

app.include_router(indicadores_router)