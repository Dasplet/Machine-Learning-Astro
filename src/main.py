from pathlib import Path
import json

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from src.data_utils import (
    load_dataset,
    basic_dataset_checks,
    FEATURES_REGRESSION,
    TARGET_REGRESSION
)
from src.models import (
    run_classification,
    run_regression,
    run_clustering,
    save_json
)
from src.plots import (
    plot_confusion_matrix,
    plot_clusters_vs_real_classes,
    plot_redshift_prediction
)

DATA_PATH = Path("data/sdss_sample.csv")
OUTPUT_DIR = Path("outputs")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_dataset(DATA_PATH)

    checks = basic_dataset_checks(df)
    save_json(checks, OUTPUT_DIR / "dataset_checks.json")

    # Clasificación
    classification_metrics = run_classification(df)
    save_json(classification_metrics, OUTPUT_DIR / "classification_metrics.json")

    plot_confusion_matrix(
        classification_metrics["confusion_matrix"],
        classification_metrics["labels"],
        OUTPUT_DIR / "classification_confusion_matrix.png"
    )

    # Regresión
    regression_metrics = run_regression(df)
    save_json(regression_metrics, OUTPUT_DIR / "regression_metrics.json")

    # Reentreno sencillo para gráfica real vs predicho
    X = df[FEATURES_REGRESSION]
    y = df[TARGET_REGRESSION]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42
    )
    reg_model = LinearRegression()
    reg_model.fit(X_train, y_train)
    y_pred = reg_model.predict(X_test)

    plot_redshift_prediction(
        y_test.values,
        y_pred,
        OUTPUT_DIR / "regression_real_vs_predicted.png"
    )

    # Clustering
    clustering_metrics, clustered_df = run_clustering(df)
    save_json(clustering_metrics, OUTPUT_DIR / "clustering_metrics.json")

    plot_clusters_vs_real_classes(
        clustered_df,
        OUTPUT_DIR / "clustering_vs_real_classes.png"
    )

    # Resumen general
    summary = {
        "dataset_rows": int(df.shape[0]),
        "dataset_columns": int(df.shape[1]),
        "classification_accuracy": classification_metrics["accuracy"],
        "regression_mse": regression_metrics["mse"],
        "regression_r2": regression_metrics["r2"],
        "clustering_inertia": clustering_metrics["inertia"]
    }
    save_json(summary, OUTPUT_DIR / "summary.json")

    with open(OUTPUT_DIR / "run.log", "w", encoding="utf-8") as f:
        f.write("Pipeline ejecutado correctamente.\n")
        f.write(json.dumps(summary, indent=4, ensure_ascii=False))

    print("Proceso finalizado. Revisa la carpeta outputs/.")


if __name__ == "__main__":
    main()