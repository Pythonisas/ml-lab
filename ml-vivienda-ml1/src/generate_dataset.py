#!/usr/bin/env python3
"""Generador de dataset sintético para ML1 (viviendas).

Crea un CSV con columnas:
- m2, habitaciones, banos, zona, antiguedad, precio

Uso:
  python3 src/generate_dataset.py --out data/viviendas.csv --n 300 --seed 42

Notas:
- Los precios se generan con una "fórmula" simple + ruido, para que haya
  estructura aprendible por los modelos.
- No representa el mercado real.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd


ZONAS = ["centro", "norte", "sur", "este", "oeste"]


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def sample_row(rng: random.Random) -> dict:
    zona = rng.choice(ZONAS)

    # Distribuciones simples (no perfectas, pero razonables)
    m2 = clamp(rng.gauss(85, 28), 25, 180)

    # habitaciones correlacionadas con m2
    if m2 < 45:
        habitaciones = rng.choice([1, 1, 2])
    elif m2 < 80:
        habitaciones = rng.choice([2, 2, 3])
    elif m2 < 120:
        habitaciones = rng.choice([3, 3, 4])
    else:
        habitaciones = rng.choice([4, 4, 5])

    # baños correlacionados con habitaciones
    if habitaciones <= 2:
        banos = rng.choice([1, 1, 2])
    elif habitaciones == 3:
        banos = rng.choice([1, 2, 2])
    else:
        banos = rng.choice([2, 2, 3])

    antiguedad = int(clamp(rng.gauss(25, 18), 0, 80))

    # Precio base por zona (€/m2 aproximado, inventado)
    euro_m2 = {
        "centro": 4200,
        "norte": 3600,
        "oeste": 3300,
        "este": 3000,
        "sur": 2700,
    }[zona]

    # Ajustes simples
    ajuste_banos = (banos - 1) * 12000
    ajuste_antiguedad = -(antiguedad * 650)  # cuanto más viejo, algo menos

    # Precio determinista aproximado
    precio = euro_m2 * m2 + ajuste_banos + ajuste_antiguedad

    # Ruido (mercado: no todo se explica por estas 5 columnas)
    ruido = rng.gauss(0, 18000)
    precio = precio + ruido

    # Evitar precios absurdos
    precio = clamp(precio, 45000, 900000)

    # Redondeo a enteros para “sensación” de precio real
    precio = int(round(precio / 100.0) * 100)

    return {
        "m2": round(m2, 1),
        "habitaciones": int(habitaciones),
        "banos": int(banos),
        "zona": zona,
        "antiguedad": int(antiguedad),
        "precio": precio,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, help="Ruta de salida CSV")
    p.add_argument("--n", type=int, default=300, help="Número de filas")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    rows = [sample_row(rng) for _ in range(args.n)]

    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)

    print(f"OK: generado {len(df)} filas en {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
