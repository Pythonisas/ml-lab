#!/usr/bin/env python3
"""Práctica ML 1 — entrenamiento (ESQUELETO INCOMPLETO)

Uso:
  python3 src/train_incompleto.py --data data/viviendas.csv --save

Objetivo:
- Cargar + validar dataset
- EDA breve
- Preprocesar con Pipeline (imputer + OHE + scaler opcional)
- Entrenar varios modelos (baseline + más potente)
- Evaluar con MAE/RMSE/R² + CV(5)
- Guardar mejor modelo y metadata

Completa los huecos marcados con ___
"""

from __future__ import annotations

import argparse
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.features import CATEGORICAL, FEATURES, NUMERIC, TARGET
from src.utils import MODELS_DIR, ensure_dirs


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    missing = [c for c in (FEATURES + [TARGET]) if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {missing}")

    # Limpieza mínima
    df = df.dropna(subset=FEATURES + [TARGET]).copy()

    # Validaciones sencillas
    if (df["m2"] <= 0).any():
        raise ValueError("Hay filas con m2 <= 0")
    if (df[TARGET] <= 0).any():
        raise ValueError("Hay filas con precio <= 0")

    return df


def brief_eda(df: pd.DataFrame) -> None:
    print("\n=== EDA breve ===")
    print(df[NUMERIC + [TARGET]].describe().round(2))
    print("\nZonas (top):")
    print(df["zona"].value_counts().head(10))


def make_preprocessor(scale_numeric: bool) -> ColumnTransformer:
    num_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))

    numeric_pipe = Pipeline(steps=num_steps)

    cat_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, ___),  # NUMERIC
            ("cat", cat_pipe, ___),  # CATEGORICAL
        ]
    )


def eval_regression(y_true, y_pred) -> dict:
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    r2 = r2_score(y_true, y_pred)
    return {"mae": float(mae), "rmse": float(rmse), "r2": float(r2)}


def maybe_log_transform(y: pd.Series, use_log: bool):
    if not use_log:
        return y, None
    return y.apply(math.log), "log"


def maybe_inverse_transform(y_pred: pd.Series, transform: str | None) -> pd.Series:
    if transform is None:
        return y_pred
    if transform == "log":
        return y_pred.apply(math.exp)
    return y_pred


def train_one(model, X_train, y_train, preprocessor) -> Pipeline:
    pipe = Pipeline(steps=[("prep", preprocessor), ("model", model)])
    pipe.fit(X_train, y_train)
    return pipe


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--random-state", type=int, default=42)
    p.add_argument("--save", action="store_true")
    p.add_argument("--scale", action="store_true", help="Escalar numéricas (opcional)")
    p.add_argument("--log-target", action="store_true", help="Entrenar con log(precio) (opcional)")
    args = p.parse_args()

    csv_path = Path(args.data)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    ensure_dirs()

    df = load_data(csv_path)
    brief_eda(df)

    X = df[FEATURES]
    y_raw = df[TARGET]

    y, target_transform = maybe_log_transform(y_raw, args.log_target)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=args.random_state
    )

    preprocessor = make_preprocessor(scale_numeric=args.scale)

    candidates = {
        "linear_regression": LinearRegression(),
        "ridge": ___,  # Ridge(alpha=...)
        "random_forest": ___,  # RandomForestRegressor(...)
    }

    results = {}
    trained = {}

    for name, model in candidates.items():
        pipe = train_one(model, X_train, y_train, preprocessor)

        pred = pd.Series(pipe.predict(X_test))
        pred = maybe_inverse_transform(pred, target_transform)
        y_test_eval = maybe_inverse_transform(pd.Series(y_test), target_transform)

        metrics = eval_regression(y_test_eval, pred)

        cv_scores = cross_val_score(pipe, X, y, cv=5, scoring="neg_mean_absolute_error")
        cv_mae = (-cv_scores).mean()
        cv_std = (-cv_scores).std()

        results[name] = {
            "test": metrics,
            "cv_mae_mean": float(cv_mae),
            "cv_mae_std": float(cv_std),
        }
        trained[name] = pipe

    print("\n=== Resultados (menor MAE/RMSE es mejor; mayor R² es mejor) ===")
    for name, r in results.items():
        m = r["test"]
        print(
            f"- {name:16} | MAE={m['mae']:.2f} RMSE={m['rmse']:.2f} R²={m['r2']:.3f} "
            f"| CV_MAE={r['cv_mae_mean']:.2f}±{r['cv_mae_std']:.2f}"
        )

    best_name = min(results, key=lambda k: results[k]["test"]["rmse"])
    best_pipe = trained[best_name]

    print(f"\nMejor modelo (por RMSE en test): {best_name}")

    if args.save:
        model_path = MODELS_DIR / "model.joblib"
        joblib.dump(best_pipe, model_path)

        metadata = {
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "sklearn": sklearn.__version__,
            "best_model": best_name,
            "features": FEATURES,
            "target": TARGET,
            "target_transform": target_transform,
            "results": results,
            "random_state": args.random_state,
            "scale_numeric": bool(args.scale),
        }

        (MODELS_DIR / "metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding="utf-8"
        )
        print(f"Guardado: {model_path}")
        print(f"Guardado: {MODELS_DIR / 'metadata.json'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
