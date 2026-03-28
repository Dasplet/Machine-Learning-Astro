from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay


def plot_confusion_matrix(cm, labels, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cm = np.array(cm)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    plt.title("Matriz de confusión - KNN")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_clusters_vs_real_classes(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    scatter1 = axes[0].scatter(df["g"], df["r"], c=df["cluster"])
    axes[0].set_title("Clusters KMeans")
    axes[0].set_xlabel("g")
    axes[0].set_ylabel("r")

    class_codes = df["class"].astype("category").cat.codes
    scatter2 = axes[1].scatter(df["g"], df["r"], c=class_codes)
    axes[1].set_title("Clases reales")
    axes[1].set_xlabel("g")
    axes[1].set_ylabel("r")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_redshift_prediction(y_true, y_pred, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(6, 5))
    plt.scatter(y_true, y_pred, alpha=0.7)
    plt.xlabel("Redshift real")
    plt.ylabel("Redshift predicho")
    plt.title("Regresión lineal: real vs predicho")

    min_val = min(min(y_true), min(y_pred))
    max_val = max(max(y_true), max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()