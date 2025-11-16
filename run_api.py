"""Script para ejecutar la API de predicción de obesidad."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "API.main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info",
    )

