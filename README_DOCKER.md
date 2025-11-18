# Guía de Containerización con Docker

Esta guía te ayudará a ejecutar la API de Predicción de Niveles de Obesidad usando Docker y Docker Compose.

## 📋 Requisitos Previos

### 1. Instalar Docker Desktop

**Para Windows:**

1. Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop/
2. Asegúrate de tener:
   - Windows 10/11 64-bit (versión Pro, Enterprise o Education)
   - WSL 2 habilitado
   - Virtualización habilitada en BIOS
3. Instala Docker Desktop y reinicia tu computadora
4. Verifica la instalación abriendo PowerShell o CMD y ejecutando:

```bash
docker --version
docker-compose --version
```

Deberías ver las versiones instaladas.

### 2. Verificar que WSL 2 está habilitado

En PowerShell (como Administrador):

```powershell
wsl --install
```

Si ya tienes WSL, verifica la versión:

```powershell
wsl --list --verbose
```

Asegúrate de que la versión sea 2.

## 🚀 Inicio Rápido

### Opción 1: Usando Docker Compose (Recomendado)

1. **Abre PowerShell o CMD** en la carpeta raíz del proyecto:
   ```bash
   cd C:\Users\rarme\Proyecto_Avance
   ```

2. **Construye y ejecuta el contenedor:**
   ```bash
   docker-compose up -d
   ```

   El flag `-d` ejecuta el contenedor en segundo plano (detached mode).

3. **Verifica que está corriendo:**
   ```bash
   docker-compose ps
   ```

4. **Accede a la API:**
   - API: http://localhost:8000
   - Documentación Swagger: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc

### Opción 2: Usando Docker directamente

1. **Construye la imagen:**
   ```bash
   docker build -t obesity-api:latest .
   ```

2. **Ejecuta el contenedor:**
   ```bash
   docker run -d --name obesity-api -p 8000:8000 obesity-api:latest
   ```

3. **Verifica que está corriendo:**
   ```bash
   docker ps
   ```

## 📝 Comandos Útiles

### Ver logs del contenedor

```bash
# Con Docker Compose
docker-compose logs -f

# Con Docker directamente
docker logs -f obesity-api
```

### Detener el contenedor

```bash
# Con Docker Compose
docker-compose down

# Con Docker directamente
docker stop obesity-api
docker rm obesity-api
```

### Reiniciar el contenedor

```bash
# Con Docker Compose
docker-compose restart

# Con Docker directamente
docker restart obesity-api
```

### Reconstruir la imagen (después de cambios)

```bash
# Con Docker Compose
docker-compose up -d --build

# Con Docker directamente
docker build -t obesity-api:latest .
docker stop obesity-api
docker rm obesity-api
docker run -d --name obesity-api -p 8000:8000 obesity-api:latest
```

### Ver el estado del contenedor

```bash
# Con Docker Compose
docker-compose ps

# Con Docker directamente
docker ps -a
```

### Ejecutar comandos dentro del contenedor

```bash
# Con Docker Compose
docker-compose exec api bash

# Con Docker directamente
docker exec -it obesity-api bash
```

## 🧪 Probar la API

### 1. Verificar que la API está funcionando

Abre tu navegador o usa curl:

```bash
curl http://localhost:8000/
```

Deberías recibir:
```json
{
  "message": "API de Predicción de Niveles de Obesidad",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### 2. Probar el endpoint de predicción

**Con PowerShell (Windows):**

```powershell
$body = @{
    Gender = "Female"
    Age = 21.0
    Height = 1.62
    Weight = 64.0
    family_history_with_overweight = "yes"
    FAVC = "no"
    FCVC = 2.0
    NCP = 3.0
    CAEC = "Sometimes"
    SMOKE = "no"
    CH2O = 2.0
    SCC = "no"
    FAF = 0.0
    TUE = 1.0
    CALC = "no"
    MTRANS = "Public_Transportation"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/predict" -Method POST -Body $body -ContentType "application/json"
```

**Con curl (si está instalado):**

```bash
curl -X POST "http://localhost:8000/api/v1/predict" `
  -H "Content-Type: application/json" `
  -d "{\"Gender\":\"Female\",\"Age\":21.0,\"Height\":1.62,\"Weight\":64.0,\"family_history_with_overweight\":\"yes\",\"FAVC\":\"no\",\"FCVC\":2.0,\"NCP\":3.0,\"CAEC\":\"Sometimes\",\"SMOKE\":\"no\",\"CH2O\":2.0,\"SCC\":\"no\",\"FAF\":0.0,\"TUE\":1.0,\"CALC\":\"no\",\"MTRANS\":\"Public_Transportation\"}"
```

**Con Python:**

```python
import requests

url = "http://localhost:8000/api/v1/predict"
data = {
    "Gender": "Female",
    "Age": 21.0,
    "Height": 1.62,
    "Weight": 64.0,
    "family_history_with_overweight": "yes",
    "FAVC": "no",
    "FCVC": 2.0,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "SMOKE": "no",
    "CH2O": 2.0,
    "SCC": "no",
    "FAF": 0.0,
    "TUE": 1.0,
    "CALC": "no",
    "MTRANS": "Public_Transportation"
}

response = requests.post(url, json=data)
print(response.json())
```

### 3. Acceder a la documentación interactiva

Abre tu navegador y ve a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Desde ahí puedes probar la API directamente desde la interfaz web.

## 🔍 Verificar el Health Check

El contenedor incluye un health check automático. Puedes verificar el estado:

```bash
# Con Docker Compose
docker-compose ps

# Con Docker directamente
docker inspect --format='{{.State.Health.Status}}' obesity-api
```

El estado debería ser `healthy` después de unos segundos.

## 🐛 Solución de Problemas

### Problema 1: "Cannot connect to the Docker daemon"

**Solución:**
1. Asegúrate de que Docker Desktop esté ejecutándose
2. Verifica que WSL 2 esté habilitado
3. Reinicia Docker Desktop

### Problema 2: "Port 8000 is already in use"

**Solución:**
1. Detén cualquier proceso que esté usando el puerto 8000
2. O cambia el puerto en `docker-compose.yml`:
   ```yaml
   ports:
     - "8001:8000"  # Usa 8001 en lugar de 8000
   ```

### Problema 3: "Model not found" o errores al cargar el modelo

**Solución:**
1. Verifica que el archivo `models/xgboost_model_artifacts.pkl` exista
2. Verifica los logs del contenedor:
   ```bash
   docker-compose logs api
   ```

### Problema 4: El contenedor se detiene inmediatamente

**Solución:**
1. Revisa los logs:
   ```bash
   docker-compose logs api
   ```
2. Verifica que todas las dependencias estén en `requirements.txt`
3. Asegúrate de que el modelo esté en la carpeta `models/`

### Problema 5: "Build failed" al construir la imagen

**Solución:**
1. Verifica que estás en la carpeta raíz del proyecto
2. Asegúrate de que `requirements.txt` existe y es válido
3. Revisa los logs de construcción:
   ```bash
   docker-compose build --no-cache
   ```

### Problema 6: Errores de permisos en Windows

**Solución:**
1. Ejecuta PowerShell o CMD como Administrador
2. Asegúrate de que Docker Desktop tenga permisos adecuados
3. Verifica la configuración de WSL 2

## 📦 Estructura de Archivos Docker

```
Proyecto_Avance/
├── Dockerfile              # Configuración de la imagen Docker
├── .dockerignore           # Archivos a ignorar en el build
├── docker-compose.yml      # Configuración de Docker Compose
├── README_DOCKER.md        # Esta guía
├── requirements.txt        # Dependencias de Python
├── models/                 # Modelo incluido en la imagen
│   └── xgboost_model_artifacts.pkl
├── API/                    # Código de la API
├── mlops_obesidad/         # Código del proyecto
└── logs/                   # Logs (montado como volumen)
```

## 🔐 Consideraciones de Seguridad

1. **Usuario no-root**: El contenedor se ejecuta como usuario no-root (`appuser`)
2. **Health checks**: El contenedor incluye health checks para monitoreo
3. **Variables de entorno**: Puedes agregar variables de entorno en `docker-compose.yml` para configuración sensible

## 🚀 Despliegue en Producción

Para producción, considera:

1. **Usar un registro de imágenes**: Docker Hub, AWS ECR, Google Container Registry
2. **Variables de entorno**: Mover configuraciones sensibles a variables de entorno
3. **Logging**: Configurar logging centralizado
4. **Monitoreo**: Integrar con sistemas de monitoreo (Prometheus, Grafana)
5. **Escalado**: Usar Docker Swarm o Kubernetes para múltiples instancias
6. **HTTPS**: Configurar un reverse proxy (nginx) con certificados SSL

## 📚 Recursos Adicionales

- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [Docker Desktop para Windows](https://docs.docker.com/desktop/windows/)
- [Documentación de la API](API/README.md)

## ❓ ¿Necesitas Ayuda?

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs -f`
2. Verifica que Docker Desktop esté corriendo
3. Asegúrate de que WSL 2 esté habilitado
4. Consulta la documentación oficial de Docker

---

**Última actualización:** Noviembre 2025

