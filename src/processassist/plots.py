"""Three exploratory plots for the TEP training data."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from processassist.data import ID_COLUMNS, load_tep  # noqa: E402

FAULT_START_TRAIN = 20  # fault introduced at 1 h; samples every 3 min
PLOT_DIR = Path("docs/plots")


def measurement_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c not in ID_COLUMNS]


def plot_run_comparison(
    normal: pd.DataFrame, faulty: pd.DataFrame, fault: int, run: int, variable: str, out: Path
) -> Path:
    """Plot 1: one variable in one normal run against the same run with a fault."""
    n = normal[normal["simulationRun"] == run]
    f = faulty[(faulty["faultNumber"] == fault) & (faulty["simulationRun"] == run)]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(n["sample"], n[variable], label="fault-free")
    ax.plot(f["sample"], f[variable], label=f"fault {fault}")
    ax.axvline(FAULT_START_TRAIN, color="grey", linestyle="--", label="fault introduced (1 h)")
    ax.set(xlabel="sample (3 min)", ylabel=variable, title=f"{variable}: run {run}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_distribution(
    normal: pd.DataFrame, faulty: pd.DataFrame, fault: int, variable: str, out: Path
) -> Path:
    """Plot 2: distribution of one variable, fault-free vs after the fault starts."""
    f = faulty[(faulty["faultNumber"] == fault) & (faulty["sample"] > FAULT_START_TRAIN)]
    n = normal[normal["sample"] > FAULT_START_TRAIN]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(n[variable], bins=60, alpha=0.6, density=True, label="fault-free")
    ax.hist(f[variable], bins=60, alpha=0.6, density=True, label=f"fault {fault}")
    ax.set(xlabel=variable, ylabel="density", title=f"{variable} distribution")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_correlation(normal: pd.DataFrame, out: Path) -> Path:
    """Plot 3: correlation matrix of all process variables, fault-free data."""
    corr = normal[measurement_columns(normal)].corr()
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set(title="Correlation of process variables (fault-free)")
    ax.set_xlabel("variable index")
    ax.set_ylabel("variable index")
    fig.colorbar(im, ax=ax, label="correlation")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main() -> None:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    normal = load_tep("TEP_FaultFree_Training")
    faulty = load_tep("TEP_Faulty_Training")
    print(plot_run_comparison(normal, faulty, 1, 1, "xmeas_1", PLOT_DIR / "01_xmeas1_run1.png"))
    print(plot_distribution(normal, faulty, 1, "xmeas_1", PLOT_DIR / "02_xmeas1_distribution.png"))
    print(plot_correlation(normal, PLOT_DIR / "03_correlation.png"))


if __name__ == "__main__":
    main()
