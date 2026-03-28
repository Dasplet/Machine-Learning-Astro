import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

from src.data_utils import (
    FEATURES_CLASSIFICATION,
    FEATURES_REGRESSION,
    FEATURES_CLUSTERING,
    TARGET_CLASS,
    TARGET_REGRESSION
)


def save_json(data: dict, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def run_classification(df: pd.DataFrame) -> dict:
    X = df[FEATURES_CLASSIFICATION]
    y = df[TARGET_CLASS]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.30, random_state=42, stratify=y_encoded
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    metrics = {
        "model": "KNN",
        "k": 5,
        "features": FEATURES_CLASSIFICATION,
        "target": TARGET_CLASS,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "accuracy": float(acc),
        "confusion_matrix": cm.tolist(),
        "labels": label_encoder.classes_.tolist()
    }
    return metrics


def run_regression(df: pd.DataFrame) -> dict:
    X = df[FEATURES_REGRESSION]
    y = df[TARGET_REGRESSION]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "model": "LinearRegression",
        "features": FEATURES_REGRESSION,
        "target": TARGET_REGRESSION,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "mse": float(mse),
        "r2": float(r2),
        "coefficients": {
            feature: float(coef)
            for feature, coef in zip(FEATURES_REGRESSION, model.coef_)
        },
        "intercept": float(model.intercept_)
    }
    return metrics


def run_clustering(df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    X = df[FEATURES_CLUSTERING].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Se fija n_init para evitar diferencias entre versiones y mejorar reproducibilidad.
    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = model.fit_predict(X_scaled)

    clustered_df = df.copy()
    clustered_df["cluster"] = clusters

    metrics = {
        "model": "KMeans",
        "n_clusters": 3,
        "features": FEATURES_CLUSTERING,
        "inertia": float(model.inertia_),
        "cluster_sizes": (
            clustered_df["cluster"].value_counts().sort_index().to_dict()
        )
    }

    return metrics, clustered_df