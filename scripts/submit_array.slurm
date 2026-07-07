#!/bin/bash

#SBATCH --job-name="gnn-rl-sweep"
#SBATCH --time=02:00:00
#SBATCH --mem=8G
#SBATCH --partition=orchid
#SBATCH --account=orchid
#SBATCH --qos=orchid
#SBATCH --gres=gpu:1
#SBATCH -o logs/slurm/%A_%a.out
#SBATCH -e logs/slurm/%A_%a.err

MANIFEST=generated/manifest.yaml

read CONFIG SEED < <(
python - "$MANIFEST" "$SLURM_ARRAY_TASK_ID" <<'PY'
import sys
import yaml

manifest = sys.argv[1]
idx = int(sys.argv[2])

with open(manifest) as f:
    runs = yaml.safe_load(f)["runs"]

run = runs[idx]
print(run["config"], run["seed"])
PY
)

echo "Running config ${CONFIG} seed ${SEED}"

uv run scripts/train_worker.py --config "$CONFIG" --seed "$SEED"