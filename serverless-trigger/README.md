# xv6 Serverless Trigger

This package wraps the parent `xv6-riscv` build in a container image so a serverless platform can cold-start Python, load QEMU, and boot xv6 inside the function container.

## Current status

The completed measurements in this repository are local trigger and local HTTP measurements. The Docker and Cloud Run files are included as deployment support for future serverless experiments, but Docker/Cloud Run experiment results have not been collected yet.

## What changed from the generic example

The parent tree is `xv6-riscv`, not the older x86 xv6 layout. That means the correct boot artifact is `kernel/kernel`, and the correct emulator is `qemu-system-riscv64`. There is no `xv6.img` in this repository.

## Files

- `handler.py`: core trigger logic that runs QEMU and returns a boot-log excerpt plus timing.
- `noop_handler.py`: baseline function for measuring provider and container overhead without QEMU.
- `serve.py`: tiny HTTP wrapper for Cloud Run or local container testing.
- `measure_boot.py`: repeats the trigger locally, saves JSON/CSV, and summarizes both end-to-end trigger time and parsed xv6 boot time.
- `measure_http.py`: measures `/noop` or `/trigger` over HTTP and saves JSON/CSV for container or serverless runs.
- `run_local_matrix.py`: runs a larger local matrix and keeps a step-by-step log under `experiments/tracks/`.
- `experiment_utils.py`: shared helpers for saved results and configuration metadata.
- `Dockerfile`: custom image that installs QEMU and copies the prebuilt xv6 artifacts from the parent directory.
- `experiments/`: saved result layout and workflow notes.
- `deploy/cloudrun/`: exact Cloud Run deployment and cold-start measurement steps.

At invocation time, `handler.py` copies the bundled `fs.img` into `/tmp` before booting QEMU. That is intentional: many serverless runtimes expose the container image as read-only and only allow writes under `/tmp`.

## Build the image

Build from `serverless-trigger/`, but use the parent xv6 directory as the Docker build context so Docker can see `kernel/kernel` and `fs.img`:

```bash
docker build -f serverless-trigger/Dockerfile -t xv6-trigger ..
```

If you need fresh artifacts first:

```bash
make -C .. kernel/kernel fs.img
```

## Run locally

```bash
docker run --rm -p 8080:8080 xv6-trigger
```

Trigger the xv6 boot:

```bash
curl http://localhost:8080/trigger
```

Measure the no-op baseline:

```bash
curl http://localhost:8080/noop
```

Health check:

```bash
curl http://localhost:8080/healthz
```

## Useful environment variables

- `XV6_BOOT_TIMEOUT_SEC`: how long to let QEMU run before it is killed and the current boot log is returned.
- `XV6_MEMORY`: QEMU guest memory, such as `128M` or `1024M`.
- `XV6_CPUS`: guest CPU count. Use `1` for cleaner cold-start comparisons.
- `XV6_LOG_LIMIT`: maximum number of log characters returned in the response.
- `XV6_TMPDIR`: writable directory used for the per-invocation mutable copy of `fs.img`.

## Local non-container test

From this directory:

```bash
python3 handler.py
```

That uses the existing local `../kernel/kernel` and `../fs.img` by default.

To run repeated measurements:

```bash
python3 measure_boot.py --runs 5 --label local_default
```

For machine-readable output:

```bash
python3 measure_boot.py --runs 5 --json
```

Each run is saved automatically under `experiments/results/local/` as both JSON and CSV.

To measure a running HTTP endpoint:

```bash
python3 measure_http.py --url http://localhost:8080/noop --runs 5 --label noop_local
python3 measure_http.py --url http://localhost:8080/trigger --runs 5 --label trigger_local
```

Those runs are saved under `experiments/results/http/`.

For directory layout and the recommended experiment workflow, see `experiments/README.md`.

To run a larger local matrix and keep a step log:

```bash
python3 run_local_matrix.py --runs 5
```

For Cloud Run deployment and true serverless cold-start measurement steps, see `deploy/cloudrun/README.md`.
