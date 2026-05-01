# Matrix Summary

## Configurations

- `32M`, `XV6_CPUS=1`, `XV6_BOOT_TIMEOUT_SEC=5`, 5 runs
- `64M`, `XV6_CPUS=1`, `XV6_BOOT_TIMEOUT_SEC=5`, 5 runs
- `128M`, `XV6_CPUS=1`, `XV6_BOOT_TIMEOUT_SEC=5`, 5 runs

## Results

- `32M` direct trigger: 0 of 5 successful boots, all timed out
- `32M` HTTP `/noop`: round-trip mean `4.292 ms`
- `32M` HTTP `/trigger`: handler mean `5082.405 ms`, effectively timeout-bound

- `64M` direct trigger: trigger mean `275.284 ms`, kernel mean `102.293 ms`
- `64M` HTTP `/noop`: round-trip mean `3.858 ms`
- `64M` HTTP `/trigger`: round-trip mean `310.505 ms`, handler mean `305.587 ms`, kernel mean `117.605 ms`

- `128M` direct trigger: trigger mean `282.126 ms`, kernel mean `105.516 ms`
- `128M` HTTP `/noop`: round-trip mean `4.059 ms`
- `128M` HTTP `/trigger`: round-trip mean `298.194 ms`, handler mean `293.285 ms`, kernel mean `112.695 ms`

## Notes

- In this workspace, `32M` does not reliably reach `[BOOT] total_kernel` within the current timeout.
- Both `64M` and `128M` complete boot measurement consistently.
- Successful boots still end with the existing xv6 `panic: kerneltrap` after `total_kernel`.
- Detailed command history is in `steps.md`.
- Full per-run data is in `manifest.json` and the saved JSON/CSV files under `experiments/results/`.
