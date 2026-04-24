## Dataset de viviendas (ML1)

### Opción A (recomendada para clase): dataset sintético
Genera un CSV con 200–500 filas con columnas:
- m2, habitaciones, banos, zona, antiguedad, precio

Así todo el mundo entrena el mismo día sin depender de descargas.

### Opción B: dataset real (Comunidad de Madrid)
Mira `../docs/conseguir-dataset-CAM.md`.

### Nota
Este repo ignora por defecto `data/*.csv` para evitar subir datos personales o grandes ficheros.
Si queréis versionar un CSV de ejemplo pequeño, quitad la regla del `.gitignore`.
