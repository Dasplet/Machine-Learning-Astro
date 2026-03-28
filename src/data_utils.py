from pathlib import Path
import pandas as pd


FEATURES_CLASSIFICATION = ["u", "g", "r", "i", "z", "redshift"]
FEATURES_REGRESSION = ["u", "g", "r", "i", "z"]
FEATURES_CLUSTERING = ["u", "g", "r", "i", "z"]
TARGET_CLASS = "class"
TARGET_REGRESSION = "redshift"


def load_dataset(csv_path: str | Path) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    df = pd.read_csv(path)

    required_cols = set(FEATURES_CLASSIFICATION + [TARGET_CLASS])
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")

    df = df.dropna(subset=list(required_cols)).copy()
    return df


def basic_dataset_checks(df: pd.DataFrame) -> dict:
    checks = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "null_values_total": int(df.isnull().sum().sum()),
        "has_required_columns": all(
            col in df.columns
            for col in FEATURES_CLASSIFICATION + [TARGET_CLASS]
        ),
        "class_distribution": df[TARGET_CLASS].value_counts().to_dict()
    }

    if checks["rows"] == 0:
        raise ValueError("El dataset quedó vacío luego de limpiar nulos.")

    return checks