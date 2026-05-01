# Project Changes

This repository extends xv6-riscv for a measurement study of boot-time latency and cold-start behavior on QEMU/RISC-V. The changes are experimental rather than general-purpose xv6 features. They add boot-stage instrumentation, configurable boot paths, and a local HTTP trigger harness used to measure xv6 as the OS-initialization component of a serverless-style cold start.

## Kernel Instrumentation

The main measurement change is in `kernel/main.c`. The kernel now reads the RISC-V `time` CSR around major initialization stages and prints machine-readable lines such as:

```text
[BOOT] kinit         ... ticks
[BOOT] vm_init       ... ticks
[BOOT] procinit      ... ticks
[BOOT] userinit      ... ticks
[BOOT] total_kernel  ... ticks
```

These lines are the primary source for per-stage boot measurements. They are also parsed by the Python trigger harness under `serverless-trigger/`.

`user/init.c` was also changed to print when user-space `/init` is reached. This supports observation of the user handoff, while the kernel-side measurements focus on initialization through `total_kernel`.

## Boot Configuration Experiments

Several kernel constants and boot paths were changed to support controlled experiments:

- `kernel/memlayout.h`: `PHYSTOP` was changed from 128 MB to 64 MB in the current working configuration. This controls how much physical memory `kinit()` scans and directly affects boot time.
- `kernel/param.h`: `NPROC`, `NCPU`, and `MAXOPBLOCKS` were reduced for experiments on process-table size, CPU count, and buffer-cache/log size.
- `Makefile`: added `OPT` so compiler optimization level can be varied, and added `NODISK` support to build/run xv6 without attaching the VirtIO disk.
- `kernel/file.c`: moved file-system and disk initialization behind a lazy first-use path in `filealloc()`.
- `kernel/start.c` and `kernel/main.c`: deferred timer interrupt arming until just before `scheduler()` so timer interrupts do not fire during the measured boot path.
- `kernel/main.c` and `kernel/uart.c`: disabled selected device/interrupt paths for experiments that study whether unused devices affect boot latency.
- `kernel/entry.S`: added explanatory comments around early stack setup; this is documentation-only and does not change behavior.

The committed source reflects the current experimental configuration. Some earlier measurements were collected by rebuilding xv6 with different values of `PHYSTOP`, CPU count, `NPROC`, `MAXOPBLOCKS`, `NODISK`, and `OPT`.

## Serverless Trigger Harness

The `serverless-trigger/` directory contains a local trigger harness used to evaluate request-driven xv6 boot:

- `handler.py` launches QEMU, boots xv6, watches for `[BOOT] total_kernel`, parses boot metrics, and returns JSON.
- `serve.py` exposes HTTP endpoints.
- `noop_handler.py` implements `/noop`, a no-op baseline used to estimate local HTTP overhead.
- `measure_boot.py`, `measure_http.py`, and `run_local_matrix.py` collect repeated measurements and save JSON/CSV outputs.

The completed measurements use local trigger and local HTTP results. Docker and Cloud Run support files are included as deployment support for future work, but Docker/Cloud Run experiment results have not been collected yet.

## Experiment Outputs

Saved measurement artifacts live under:

- `serverless-trigger/experiments/results/local/`
- `serverless-trigger/experiments/results/http/`
- `serverless-trigger/experiments/tracks/`

The HTTP matrix results are the source for the `/noop` and `/trigger` latency analysis. The track logs record the exact commands and environment variables used for the matrix run.

These changes should be understood as an experimental measurement setup, not as a production xv6 configuration.
