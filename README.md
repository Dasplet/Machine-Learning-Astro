# Pipeline de Machine Learning reproducible con Docker y Jenkins usando datos astronómicos

## Descripción
Este proyecto implementa un pipeline de Machine Learning con tres tareas:

- Clasificación con KNN (k=5)
- Regresión lineal para predecir `redshift`
- Clustering con KMeans (3 clusters)

El proyecto guarda métricas y gráficas en `outputs/`, puede ejecutarse localmente y también dentro de Docker. Además, incorpora un `Jenkinsfile` para automatizar pruebas y ejecución.

## Estructura
- `src/`: código fuente
- `tests/`: pruebas básicas
- `data/`: dataset
- `outputs/`: resultados generados

## Ejecución local
```bash
pip install -r requirements.txt
python src/main.py