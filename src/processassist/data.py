"""Download the TEP files from Harvard Dataverse and convert them to Parquet."""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

DOI = "doi:10.7910/DVN/6C3JR1"
BASE = "https://dataverse.harvard.edu"
RAW_DIR = Path("data/raw")
PARQUET_DIR = Path("data/parquet")

# Start with the two training files; add the testing files when you need them (they are large).
DEFAULT_FILES = ("TEP_FaultFree_Training.RData", "TEP_Faulty_Training.RData")

ID_COLUMNS = ("faultNumber", "simulationRun", "sample")


def list_remote_files() -> dict[str, int]:
    """Return {filename: file id} for the latest dataset version."""
    query = urllib.parse.urlencode({"persistentId": DOI})
    url = f"{BASE}/api/datasets/:persistentId/versions/:latest/files?{query}"
    with urllib.request.urlopen(url, timeout=60) as resp:  # noqa: S310
        payload = json.load(resp)
    return {f["dataFile"]["filename"]: f["dataFile"]["id"] for f in payload["data"]}


def download(filenames: tuple[str, ...] = DEFAULT_FILES, dest: Path = RAW_DIR) -> list[Path]:
    """Download the named files into ``dest`` (skips files already present)."""
    dest.mkdir(parents=True, exist_ok=True)
    remote = list_remote_files()
    paths: list[Path] = []
    for name in filenames:
        if name not in remote:
            raise KeyError(f"{name} not found on Dataverse. Available: {sorted(remote)}")
        target = dest / name
        if not target.exists():
            url = f"{BASE}/api/access/datafile/{remote[name]}"
            print(f"Downloading {name} ...")
            urllib.request.urlretrieve(url, target)  # noqa: S310
        paths.append(target)
    return paths


def tidy(df: pd.DataFrame) -> pd.DataFrame:
    """Give the id columns compact integer types and the measurements float32."""
    out = df.copy()
    for col in ID_COLUMNS:
        out[col] = out[col].astype("int16")
    value_cols = [c for c in out.columns if c not in ID_COLUMNS]
    out[value_cols] = out[value_cols].astype("float32")
    return out


def rdata_to_parquet(rdata_path: Path, out_dir: Path = PARQUET_DIR) -> Path:
    """Convert one .RData file (holding a single dataframe) to Parquet."""
    import pyreadr  # imported here so tests that skip RData do not need it

    result = pyreadr.read_r(str(rdata_path))
    if len(result) != 1:
        raise ValueError(f"Expected one object in {rdata_path}, found {list(result)}")
    df = tidy(next(iter(result.values())))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{rdata_path.stem}.parquet"
    df.to_parquet(out_path, index=False)
    return out_path


def load_tep(name: str, parquet_dir: Path = PARQUET_DIR) -> pd.DataFrame:
    """Load a converted file, e.g. ``load_tep("TEP_FaultFree_Training")``."""
    return pd.read_parquet(parquet_dir / f"{name}.parquet")


def main() -> None:
    parser = argparse.ArgumentParser(description="TEP data helper")
    parser.add_argument("action", choices=["download", "convert", "all"])
    args = parser.parse_args()
    if args.action in ("download", "all"):
        download()
    if args.action in ("convert", "all"):
        for name in DEFAULT_FILES:
            print("Wrote", rdata_to_parquet(RAW_DIR / name))


if __name__ == "__main__":
    main()
