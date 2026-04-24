#!/usr/bin/env python3
"""Práctica ML 1 — predicción por terminal (ESQUELETO INCOMPLETO)

Uso (CLI):
  python3 src/predict_incompleto.py --m2 75 --habitaciones 3 --banos 2 --zona centro --antiguedad 10

Uso (interactivo):
  python3 src/predict_incompleto.py

Requisito:
  python3 src/train_incompleto.py --data data/viviendas.csv --save

Completa los huecos marcados con ___
"""

from __future__ import annotations

import argparse
import json
import math

import joblib
import pandas as pd

from src.features import FEATURES
from src.utils import MODELS_DIR


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--m2", type=float)
    p.add_argument("--habitaciones", type=int)
    p.add_argument("--banos", type=int)
    p.add_argument("--zona", type=str)
    p.add_argument("--antiguedad", type=int)
    return p.parse_args()


def ask(prompt: str, cast):
    while True:
        raw = input(prompt).strip()
        try:
            return cast(raw)
        except Exception:
            print("Valor inválido, prueba otra vez.")


def main() -> int:
    model_path = MODELS_DIR / "model.joblib"
    meta_path = MODELS_DIR / "metadata.json"

    if not model_path.exists():
        raise FileNotFoundError(
            "Falta models/model.joblib. Entrena con: python3 src/train_incompleto.py --data data/viviendas.csv --save"
        )

    model = joblib.load(model_path)

    meta = {}
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))

    args = parse_args()

    m2 = args.m2 if args.m2 is not None else ask("m2: ", float)
    hab = args.habitaciones if args.habitaciones is not None else ask("habitaciones: ", int)
    banos = args.banos if args.banos is not None else ask("banos: ", int)
    zona = args.zona if args.zona is not None else input("zona: ").strip().lower()
    antig = args.antiguedad if args.antiguedad is not None else ask("antiguedad: ", int)

    row = {
        "m2": m2,
        "habitaciones": hab,
        "banos": banos,
        "zona": zona,
        "antiguedad": antig,
    }

    X = pd.DataFrame([row], columns=___)  # FEATURES

    pred = pd.Series(model.predict(X))
    if meta.get("target_transform") == "log":
        pred = pred.apply(math.exp)

    print(f"Precio estimado: {pred.iloc[0]:,.2f} €")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
