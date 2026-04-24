# Práctica ML 1 — Predicción de precios de vivienda (Regresión) — Versión mejorada

## Objetivo
Construir un mini‑sistema reproducible que estime el **precio** de una vivienda a partir de características simples y que se pueda ejecutar desde la terminal.

## Entregables
- `ml-vivienda/` con la estructura indicada.
- `src/train.py`, `src/predict.py`, `src/features.py`, `src/utils.py`.
- `data/viviendas.csv` (ejemplo 200–500 filas) y `README.org`.
- `models/model.joblib` y `models/metadata.json` (al entrenar).

## Requisitos
- Python 3.10+, `venv`.
- `pandas`, `scikit-learn`, `joblib`.
- `requirements.txt` con versiones fijas.

## Flujo recomendado
1. **Carga y validación**: comprobar existencia del archivo, columnas obligatorias `m2,habitaciones,banos,zona,antiguedad,precio`, tipos y nulos.
2. **EDA breve**: distribuciones, outliers, correlaciones, histograma de `precio`.
3. **Preprocesado**:
   - Numéricas: `SimpleImputer(strategy='median')`, opcional `StandardScaler`.
   - Categóricas: `OneHotEncoder(handle_unknown='ignore')`.
   - Pipeline: `ColumnTransformer` + `Pipeline`.
   - **Considerar** `log(precio)` si `precio` está sesgado.
4. **Modelado**:
   - `LinearRegression` (baseline) y `RandomForestRegressor`.
   - Añadir `Ridge` como alternativa.
   - Hiperparámetros con `RandomizedSearchCV` (opcional).
5. **Evaluación**:
   - `train_test_split` (80/20, `random_state`).
   - CV 5‑fold; reportar **MAE**, **RMSE**, **R²** (media ± std).
6. **Persistencia y metadata**:
   - Guardar modelo ganador con `joblib`.
   - Crear `models/metadata.json` con fecha, versión sklearn, features, métricas.
7. **Predict CLI**:
   - `argparse` + `input()` fallback; validar entradas; manejar categorías desconocidas.

## Buenas prácticas y rúbrica añadida
- Manejo de errores y logging.
- Tests mínimos: carga CSV, pipeline transforma, predict con ejemplo.
- README con comandos de ejemplo y resultados reproducibles.

## Comandos de ejemplo
```bash
python src/train.py --data data/viviendas.csv --out models/model.joblib --random-state 42
python src/predict.py --m2 75 --habitaciones 3 --banos 2 --zona centro --antiguedad 10
```
