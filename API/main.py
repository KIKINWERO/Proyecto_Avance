"""Aplicación principal FastAPI para la API de predicción de obesidad."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from API.routers import router
from API import __version__

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Predicción de Niveles de Obesidad",
    description="API REST para predecir niveles de obesidad basado en hábitos alimenticios y condición física",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(router, prefix="/api/v1", tags=["predictions"])


@app.on_event("startup")
async def startup_event():
    """Evento ejecutado al iniciar la aplicación."""
    logger.info("Iniciando API de Predicción de Niveles de Obesidad")
    logger.info(f"Versión: {__version__}")
    # TODO: Cargar modelo aquí cuando esté disponible
    logger.warning("Modelo no cargado - usando función dummy")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento ejecutado al cerrar la aplicación."""
    logger.info("Cerrando API de Predicción de Niveles de Obesidad")


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "API de Predicción de Niveles de Obesidad",
        "version": __version__,
        "docs": "/docs",
        "redoc": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "API.main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info",
    )

