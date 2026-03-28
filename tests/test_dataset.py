from pathlib import Path
import pandas as pd

from src.data_utils import load_dataset, basic_dataset_checks


DATA_PATH = Path("data/sdss_sample.csv")


def test_dataset_exists():
    assert DATA_PATH.exists(), "El dataset no existe en data/sdss_sample.csv"


def test_dataset_loads():
    df = load_dataset(DATA_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_required_columns():
    df = load_dataset(DATA_PATH)
    checks = basic_dataset_checks(df)
    assert checks["has_required_columns"] is True
    assert checks["rows"] > 0