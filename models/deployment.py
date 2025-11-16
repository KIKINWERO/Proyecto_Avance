import pickle
import pandas as pd
import numpy as np
import pickle
from scipy.stats import randint, uniform

# Preprocesamiento y Pipeline
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
# ¡Importaciones clave para el transformador personalizado!
from sklearn.base import BaseEstimator, TransformerMixin

# Modelo
from xgboost import XGBClassifier

import pickle

SRC_PATH = '/content/drive/MyDrive/Pregrado - Posgrado - Trabajo/Maestría - Inteligencia Artificial Aplicada/11. MLOps/1. Primera etapa de proyecto/Modelado/obesity_estimation_original.csv'
MODEL_PATH = 'xgboost_model_artifacts.pkl'

with open(MODEL_PATH, 'rb') as f:
    artifacts = pickle.load(f)

model = artifacts['model']
label_encoder = artifacts['label_encoder']

df_raw = pd.read_csv(SRC_PATH, sep=None, engine="python", encoding="utf-8")

# 1. Predecir las clases numéricas
pred_numeric = model.predict(df_raw)

# 2. Predecir las probabilidades (si las necesitas)
pred_proba = model.predict_proba(df_raw)

# 3. Decodificar a etiquetas legibles

pred_labels = label_encoder.inverse_transform(pred_numeric)
