from pathlib import Path
import pandas as pd
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

EXPERIMENT_NAME = "mis_node_ft_1"
BASE_PATH = Path("runs") / EXPERIMENT_NAME

def load_tensorboard_run(run_path: Path, seed: str) -> pd.DataFrame:
    ea = EventAccumulator(str(run_path))
    ea.Reload()

    rows = []
    for tag in ea.Tags().get("scalars", []):
        for event in ea.Scalars(tag):
            rows.append({
                "experiment": EXPERIMENT_NAME,
                "run": run_path.parent.name,   # e.g. "seed49"
                "metric": tag,
                "step": event.step,
                "value": event.value,
            })

    return pd.DataFrame(rows)


# Collect all run folders like runs/mis_node_ft_1/seed49/MaskablePPO_1
dfs = []
for seed_dir in BASE_PATH.glob("seed*"):
    run_path = seed_dir / "MaskablePPO_1"
    if run_path.exists():
        dfs.append(load_tensorboard_run(run_path, seed=seed_dir.name))

data = pd.concat(dfs, ignore_index=True)
data.to_csv(f"notebooks/{EXPERIMENT_NAME}_df.csv", index=False)