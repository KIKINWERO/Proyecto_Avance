# Proyecto MLOps - Estimación de Niveles de Obesidad

## Caso de Uso

Este repositorio contiene un proyecto de machine learning enfocado en estimar los niveles de obesidad en individuos basándose en sus hábitos alimenticios y condición física. El dataset incluye información de individuos de México, Perú y Colombia, con 2,111 registros y 16 características.

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
├─ data/
│  ├─ raw/           # Datos originales, inmutables
│  ├─ interim/       # Transformaciones intermedias de datos
│  └─ processed/     # Datasets finales y canónicos para modelado
├─ notebooks/        # Jupyter notebooks para exploración y análisis
├─ src/
│  ├─ data/          # Scripts de procesamiento de datos
│  ├─ features/      # Código de ingeniería de características
│  ├─ models/        # Entrenamiento y evaluación de modelos
│  └─ visualization/ # Utilidades de graficación y visualización
├─ models/           # Artefactos de modelos entrenados
├─ reports/          # Reportes de análisis generados y documentación
├─ dvc.yaml          # Configuración de Data Version Control
├─ requirements.txt  # Dependencias de Python
└─ README.md         # Documentación del proyecto
```
