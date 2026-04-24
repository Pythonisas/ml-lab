## Dataset de viviendas (ML1)

### Opción A (recomendada para clase): dataset sintético
Genera un CSV con 200–500 filas con columnas:
- m2, habitaciones, banos, zona, antiguedad, precio

Comando:
```bash
cd ml-vivienda-ml1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/generate_dataset.py --out data/viviendas.csv --n 300 --seed 42
```

### Opción B: dataset real (Comunidad de Madrid)
Mira `../docs/conseguir-dataset-CAM.md`.

### Nota
Este repo ignora por defecto `data/*.csv` para evitar subir datos personales o grandes ficheros.
Si queréis versionar un CSV de ejemplo pequeño, quitad la regla del `.gitignore`.
