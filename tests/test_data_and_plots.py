from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from processassist.data import ID_COLUMNS, load_tep, tidy
from processassist.plots import plot_correlation, plot_distribution, plot_run_comparison


def make_frame(fault: int, runs: int = 2, samples: int = 60) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    rows = runs * samples
    df = pd.DataFrame(
        {
            "faultNumber": float(fault),
            "simulationRun": np.repeat(np.arange(1, runs + 1), samples).astype(float),
            "sample": np.tile(np.arange(1, samples + 1), runs).astype(float),
        }
    )
    for i in range(1, 6):
        df[f"xmeas_{i}"] = rng.normal(size=rows)
    return df


def test_tidy_sets_compact_types() -> None:
    out = tidy(make_frame(0))
    assert all(out[c].dtype == "int16" for c in ID_COLUMNS)
    assert out["xmeas_1"].dtype == "float32"


def test_parquet_round_trip(tmp_path: Path) -> None:
    df = tidy(make_frame(0))
    df.to_parquet(tmp_path / "TEP_FaultFree_Training.parquet", index=False)
    back = load_tep("TEP_FaultFree_Training", tmp_path)
    pd.testing.assert_frame_equal(df, back)


@pytest.fixture
def frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    return tidy(make_frame(0)), tidy(make_frame(1))


def test_plots_write_files(tmp_path: Path, frames: tuple[pd.DataFrame, pd.DataFrame]) -> None:
    normal, faulty = frames
    assert plot_run_comparison(normal, faulty, 1, 1, "xmeas_1", tmp_path / "a.png").exists()
    assert plot_distribution(normal, faulty, 1, "xmeas_1", tmp_path / "b.png").exists()
    assert plot_correlation(normal, tmp_path / "c.png").exists()


def test_rdata_to_parquet(tmp_path: Path) -> None:
    import pyreadr

    from processassist.data import rdata_to_parquet

    rdata = tmp_path / "TEP_FaultFree_Training.RData"
    pyreadr.write_rdata(str(rdata), make_frame(0), df_name="fault_free_training")
    out = rdata_to_parquet(rdata, tmp_path / "parquet")
    back = pd.read_parquet(out)
    assert len(back) == 120
    assert back["simulationRun"].dtype == "int16"
