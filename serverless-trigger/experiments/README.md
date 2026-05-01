# Experiment Layout

This directory stores measurement outputs and the minimal metadata needed to explain each run.

## Results

- `results/local/`: local trigger runs gathered through `measure_boot.py`
- `results/http/`: HTTP endpoint runs gathered through `measure_http.py`

Each saved experiment produces:

- `*.json`: full structured summary, per-run details, and configuration metadata
- `*.csv`: flat table for plots and spreadsheet import

## Recommended workflow

### Local trigger measurements

Use this when you want to study QEMU launch plus xv6 boot on the current machine:

```bash
XV6_MEMORY=32M XV6_CPUS=1 python3 measure_boot.py --runs 10 --label local_32m
```

For a repeatable multi-configuration run with a step-by-step track log:

```bash
python3 run_local_matrix.py --runs 5
```

### Container or serverless endpoint measurements

Use this when the image is running behind HTTP, either locally with Docker, on Cloud Run, or on another platform:

```bash
python3 measure_http.py --url http://localhost:8080/noop --runs 10 --label noop_local
python3 measure_http.py --url http://localhost:8080/trigger --runs 10 --label trigger_local
```

For cold-start experiments, compare the saved `noop` and `trigger` outputs collected under the same platform settings.

## Tracks

- `tracks/`: timestamped markdown logs and manifests showing the exact commands used for a matrix or cloud measurement session

## Cloud deployment

For exact Cloud Run deployment and invocation steps, see `deploy/cloudrun/README.md`.
