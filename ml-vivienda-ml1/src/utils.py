from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"


def ensure_dirs() -> None:
    """Crea carpetas necesarias si no existen."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
