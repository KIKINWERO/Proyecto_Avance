# Imagen base: Python 3.10 slim para reducir tamaño
FROM python:3.10-slim

# Metadatos de la imagen
LABEL maintainer="Equipo 7 MLOPs MNA"
LABEL description="API de Predicción de Niveles de Obesidad - MLOps"
LABEL version="1.0.0"

# Variables de entorno para optimizar Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes Python
# (XGBoost y scikit-learn pueden necesitar compiladores)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Limpiar compiladores después de instalar dependencias (reducir tamaño)
RUN apt-get purge -y --auto-remove \
        build-essential \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar código de la aplicación y modelo
COPY --chown=appuser:appuser . .

# Cambiar a usuario no-root
USER appuser

# Exponer puerto de la API
EXPOSE 8000

# Health check para verificar que la API está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1

# Comando para ejecutar la API
# Usar 0.0.0.0 para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "8000"]

