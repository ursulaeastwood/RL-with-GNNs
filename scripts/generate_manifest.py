import yaml
from pathlib import Path
from itertools import product
from typing import Any
import copy


def load_yaml(path: str | Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
def save_yaml(obj: Any, path: str | Path ):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False)  


def set_dotted(cfg: dict, dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    cur = cfg
    for part in parts[:-1]:
        if part not in cur or not isinstance(cur[part], dict):
            cur[part] = {}
        cur = cur[part]
    cur[parts[-1]] = value

def main():
    base = load_yaml("config/base.yaml")
    sweep = load_yaml("config/sweep.yaml")

    seeds = sweep["seeds"]
    params = sweep["parameters"]

    keys = list(params.keys())
    values = [params[k] for k in keys]

    manifest = []
    experiment_dir = Path("generated/experiments")
    experiment_dir.mkdir(parents=True, exist_ok=True)

    for exp_idx, combo in enumerate(product(*values)):
        exp_cfg = copy.deepcopy(base)

        for key, value in zip(keys, combo):
            set_dotted(exp_cfg, key, value)

        experiment_id = f"exp_{exp_idx:04d}"
        exp_cfg["experiment"] = {
            "id": experiment_id,
        }

        config_path = experiment_dir / f"{experiment_id}.yaml"
        save_yaml(exp_cfg, config_path)

        for seed in seeds:
            manifest.append(
                {
                    "experiment": experiment_id,
                    "seed": seed,
                    "config": str(config_path),
                }
            )

    save_yaml({"runs": manifest}, "generated/manifest.yaml")

if __name__ == "__main__":
    main()


        
