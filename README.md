# Proyecto MLOps - Estimación de Niveles de Obesidad

## Caso de Uso

Este repositorio contiene un proyecto de machine learning realizado en la material de "Operaciones de aprendizaje automático" de la Maestría en Inteligencia Artificial Aplicada, enfocado en estimar los niveles de obesidad en individuos basándose en sus hábitos alimenticios y condición física. El dataset incluye información de individuos de México, Perú y Colombia, con 2,111 registros y 16 características.

El proyecto tiene como objetivo clasificar a los individuos en diferentes categorías de obesidad:
- Peso Insuficiente
- Peso Normal  
- Sobrepeso Nivel I
- Sobrepeso Nivel II
- Obesidad Tipo I
- Obesidad Tipo II
- Obesidad Tipo III

El dataset fue obtenido del UCI Machine Learning Repository y contiene tanto datos sintéticos (77%) generados usando Weka y el filtro SMOTE, como datos reales (23%) recolectados a través de una plataforma web.

**Referencia del Dataset:** [Estimation of Obesity Levels Based On Eating Habits and Physical Condition](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)

## Estructura del Proyecto

```
project-name/
├── LICENSE                    # Licencia de código abierto
├── Makefile                   # Comandos de conveniencia
├── README.md                  # Documentación principal del proyecto
├── data/                      # Directorio de datos
│   ├── external/              # Datos de fuentes externas
│   ├── interim/               # Datos intermedios transformados
│   ├── processed/             # Datasets finales para modelado
│   └── raw/                   # Datos originales inmutables
├── docs/                      # Documentación del proyecto
├── mlops/                     # Código fuente del paquete Python
│   ├── __init__.py
│   ├── config.py              # Variables de configuración
│   ├── dataset.py             # Scripts para descargar/generar datos
│   ├── features.py            # Código para crear características
│   ├── plots.py               # Código para visualizaciones
│   └── modeling/              # Código relacionado con modelado
│       ├── __init__.py
│       ├── predict.py         # Código para inferencia del modelo
│       └── train.py           # Código para entrenar modelos
├── models/                    # Modelos entrenados y serializados
├── notebooks/                 # Jupyter notebooks
├── references/                # Diccionarios de datos, manuales, etc.
├── reports/                   # Análisis generados
│   └── figures/               # Gráficos y figuras generadas
├── pyproject.toml             # Configuración del proyecto
├── requirements.txt           # Dependencias de Python
└── setup.cfg                  # Configuración para flake8
```
