# Guía de Testing - Proyecto MLOps Obesidad

Esta guía te ayudará a ejecutar las pruebas del proyecto paso a paso. Está diseñada para ser clara y fácil de seguir, incluso si no tienes mucha experiencia con testing.

## 📋 Tabla de Contenidos

1. [Preparación del Entorno](#1-preparación-del-entorno)
2. [Estructura de Tests](#2-estructura-de-tests)
3. [Pruebas Unitarias](#3-pruebas-unitarias)
4. [Pruebas de Integración](#4-pruebas-de-integración)
5. [Ejecutar las Pruebas](#5-ejecutar-las-pruebas)
6. [Solución de Problemas](#6-solución-de-problemas)

---

## 1. Preparación del Entorno

### Paso 1.1: Verificar que tienes Conda instalado

Abre una terminal (PowerShell en Windows, Terminal en Mac/Linux) y escribe:

```bash
conda --version
```

Si ves un número de versión (ej: `conda 23.x.x`), estás listo. Si no, necesitas instalar Conda primero.

### Paso 1.2: Activar el entorno conda "mlops"

En la terminal, ejecuta:

```bash
conda activate mlops
```

**Nota para Windows PowerShell:** Si te da error, usa este comando en su lugar:
```powershell
C:\Users\rarme\anaconda3\envs\mlops\python.exe --version
```

Si ves la versión de Python, el entorno existe. Si no, necesitas crearlo primero.

### Paso 1.3: Navegar a la carpeta del proyecto

En la terminal, ve a la carpeta raíz del proyecto:

```bash
cd C:\Users\rarme\Proyecto_Avance
```

**Verificación:** Deberías ver archivos como `requirements.txt`, `README.md`, y carpetas como `API/`, `mlops_obesidad/`, `tests/`.

### Paso 1.4: Instalar las dependencias

Con el entorno conda activado, ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará todas las bibliotecas necesarias, incluyendo `pytest` que usamos para las pruebas.

**Tiempo estimado:** 2-5 minutos dependiendo de tu conexión a internet.

**Verificación:** Al final deberías ver algo como "Successfully installed..." sin errores.

---

## 2. Estructura de Tests

### ¿Dónde están los tests?

Todos los tests están en la carpeta **`tests/`** en la raíz del proyecto:

```
Proyecto_Avance/
└── tests/
    ├── test_data.py              # Tests de datos (ejemplo básico)
    ├── test_preprocessing.py     # Tests del módulo de preprocesamiento
    ├── test_inference.py         # Tests del módulo de inferencia
    ├── test_api_services.py      # Tests de los servicios de la API
    └── test_api_integration.py   # Tests de integración de la API
```

### Convención de nombres

- Todos los archivos de test deben empezar con `test_`
- Todas las funciones de test deben empezar con `test_`
- Ejemplo: `test_model_loader.py` contiene la función `test_load_model()`

---

## 3. Pruebas Unitarias

Las pruebas unitarias verifican que cada función individual funcione correctamente.

### 3.1. Tests del Módulo de Preprocesamiento

**Ubicación:** `tests/test_preprocessing.py`

Estos tests verifican que el transformador `DataCleanerTransformer` funcione correctamente.

**Qué se prueba:**
- Que el transformador limpie valores nulos correctamente
- Que recorte espacios en strings
- Que elimine columnas completamente vacías

**Cómo ejecutarlo:**
```bash
pytest tests/test_preprocessing.py -v
```

El `-v` significa "verbose" (detallado) y te mostrará más información.

### 3.2. Tests del Módulo de Inferencia

**Ubicación:** `tests/test_inference.py`

Estos tests verifican que el módulo de inferencia funcione correctamente.

**Qué se prueba:**
- Que el modelo se pueda cargar correctamente
- Que la conversión de request a DataFrame funcione
- Que las predicciones se generen correctamente

**Cómo ejecutarlo:**
```bash
pytest tests/test_inference.py -v
```

**Nota importante:** Estos tests requieren que el archivo `models/xgboost_model_artifacts.pkl` exista.

### 3.3. Tests de los Servicios de la API

**Ubicación:** `tests/test_api_services.py`

Estos tests verifican las funciones de los servicios de la API.

**Qué se prueba:**
- Que `real_predict()` funcione correctamente
- Que `dummy_predict()` funcione como fallback
- Que las respuestas tengan el formato correcto

**Cómo ejecutarlo:**
```bash
pytest tests/test_api_services.py -v
```

---

## 4. Pruebas de Integración

Las pruebas de integración verifican que varios componentes trabajen juntos correctamente.

### 4.1. Tests de Integración de la API

**Ubicación:** `tests/test_api_integration.py`

Estos tests verifican que la API completa funcione end-to-end.

**Qué se prueba:**
- Que el endpoint `/api/v1/predict` responda correctamente
- Que las validaciones de entrada funcionen
- Que los errores se manejen apropiadamente

**Cómo ejecutarlo:**

**Paso 1:** Abre una terminal y inicia la API:
```bash
conda activate mlops
cd C:\Users\rarme\Proyecto_Avance
python run_api.py
```

Deberías ver mensajes como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Paso 2:** Abre OTRA terminal (deja la primera corriendo) y ejecuta:
```bash
conda activate mlops
cd C:\Users\rarme\Proyecto_Avance
pytest tests/test_api_integration.py -v
```

**Nota:** La API debe estar corriendo para que estos tests funcionen.

---

## 5. Ejecutar las Pruebas

### 5.1. Ejecutar TODOS los tests

Para ejecutar todos los tests de una vez:

```bash
pytest tests/ -v
```

Esto ejecutará todos los archivos `test_*.py` en la carpeta `tests/`.

### 5.2. Ejecutar un test específico

Si quieres ejecutar solo una función de test específica:

```bash
pytest tests/test_inference.py::test_load_model -v
```

Esto ejecutará solo la función `test_load_model` del archivo `test_inference.py`.

### 5.3. Ver más detalles

Para ver información más detallada sobre qué se está probando:

```bash
pytest tests/ -v -s
```

El `-s` muestra los mensajes de print() y logs.

### 5.4. Ver cobertura de código

Para ver qué porcentaje del código está siendo probado:

```bash
pytest tests/ --cov=mlops_obesidad --cov=API --cov-report=html
```

Esto generará un reporte HTML en `htmlcov/index.html` que puedes abrir en tu navegador.

---

## 6. Solución de Problemas

### Problema 1: "ModuleNotFoundError: No module named 'pytest'"

**Solución:**
```bash
pip install pytest
```

O reinstala todas las dependencias:
```bash
pip install -r requirements.txt
```

### Problema 2: "ModuleNotFoundError: No module named 'mlops_obesidad'"

**Solución:** Asegúrate de estar en la carpeta raíz del proyecto:
```bash
cd C:\Users\rarme\Proyecto_Avance
```

### Problema 3: "FileNotFoundError: El archivo del modelo no existe"

**Solución:** Verifica que el archivo `models/xgboost_model_artifacts.pkl` exista. Si no existe, necesitas el modelo entrenado.

### Problema 4: "AttributeError: Can't get attribute 'DataCleanerTransformer'"

**Solución:** Esto significa que el módulo de preprocesamiento no se está importando correctamente. Verifica que:
1. El archivo `mlops_obesidad/preprocessing/transformers.py` exista
2. El archivo `mlops_obesidad/preprocessing/__init__.py` exista

### Problema 5: Los tests de integración fallan con "Connection refused"

**Solución:** La API no está corriendo. Sigue estos pasos:

1. Abre una terminal y ejecuta:
   ```bash
   conda activate mlops
   cd C:\Users\rarme\Proyecto_Avance
   python run_api.py
   ```

2. Espera a ver el mensaje "Uvicorn running on http://127.0.0.1:8000"

3. En otra terminal, ejecuta los tests de integración

### Problema 6: "InconsistentVersionWarning" de scikit-learn

**Solución:** El modelo requiere scikit-learn 1.6.1. Instala la versión correcta:
```bash
pip install scikit-learn==1.6.1
```

---

## 📝 Checklist de Testing

Usa este checklist para asegurarte de que todo esté funcionando:

- [ ] Entorno conda "mlops" activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Estoy en la carpeta raíz del proyecto (`C:\Users\rarme\Proyecto_Avance`)
- [ ] El archivo `models/xgboost_model_artifacts.pkl` existe
- [ ] Los tests unitarios pasan: `pytest tests/test_preprocessing.py -v`
- [ ] Los tests de inferencia pasan: `pytest tests/test_inference.py -v`
- [ ] Los tests de servicios pasan: `pytest tests/test_api_services.py -v`
- [ ] La API se puede iniciar: `python run_api.py`
- [ ] Los tests de integración pasan: `pytest tests/test_api_integration.py -v`

---

## 🎯 Resumen de Comandos Rápidos

```bash
# 1. Activar entorno
conda activate mlops

# 2. Ir a la carpeta del proyecto
cd C:\Users\rarme\Proyecto_Avance

# 3. Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# 4. Ejecutar todos los tests
pytest tests/ -v

# 5. Ejecutar tests específicos
pytest tests/test_inference.py -v

# 6. Iniciar la API (para tests de integración)
python run_api.py
```

---

## 📚 Recursos Adicionales

- **Documentación de pytest:** https://docs.pytest.org/
- **Documentación de la API:** Ver `API/README.md`
- **Guía de integración:** Ver `API/INTEGRACION_MODELO.md`

---

## ❓ ¿Necesitas Ayuda?

Si encuentras problemas que no están en esta guía:

1. Revisa los mensajes de error cuidadosamente
2. Verifica que estés en la carpeta correcta
3. Asegúrate de que el entorno conda esté activado
4. Revisa que todas las dependencias estén instaladas
5. Consulta con el equipo de desarrollo

---

**Última actualización:** Noviembre 2025

