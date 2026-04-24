# Cómo conseguir un dataset de la Comunidad de Madrid (guía práctica)

## Resumen
La Comunidad de Madrid publica conjuntos de datos en su **Catálogo de Datos Abiertos (CKAN)** y muchos aparecen también en `datos.gob.es`.

## Fuentes principales (comparativa)
| **Fuente** | **Cobertura** | **Formatos** | **Acceso** |
|---|---:|---|---|
| **Catálogo Comunidad de Madrid (CKAN)** | Toda la Comunidad | CSV; JSON; ZIP | Descarga directa; API CKAN. |
| **datos.gob.es** | Agregador nacional | CSV; JSON | Fichas con enlaces directos y licencia (p. ej. CC BY 4.0). |
| **Portal Comunidad de Madrid (web)** | Información y API | CSV; JSON | Buscador y documentación del catálogo. |

## Pasos prácticos
1. **Buscar** en el Catálogo (https://datos.comunidad.madrid) o en `datos.gob.es` con palabras clave: `viviendas`, `transacciones`, `AVS`.
2. **Revisar ficha técnica**: columnas, frecuencia, licencia.
3. **Descarga**: usar el enlace `download` del recurso (CSV/JSON) o la API CKAN para automatizar.
4. **Preprocesado**: normalizar columnas, filtrar por municipio/distrito, guardar copia con fecha.

## Ejemplo de descarga rápida (plantilla)
```bash
curl -L -o viviendas_cam.csv "https://datos.comunidad.madrid/dataset/.../download/viviendas.csv"
```
