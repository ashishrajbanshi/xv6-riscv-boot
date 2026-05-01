import argparse
import json
import time
from pathlib import Path
from typing import Any

from experiment_utils import (
    bool_from_text,
    ensure_dir,
    read_kernel_constants,
    runtime_config,
    summarize,
    utc_timestamp,
    write_csv,
    write_json,
    xv6_root_from_env,
)
from handler import handler


def run_once() -> dict[str, Any]:
    result = handler({}, None)
    body = result["body"]
    metrics = body.get("boot_metrics", {})
    stage_ms = metrics.get("stage_ms", {})
    stdout_excerpt = body.get("stdout_excerpt", "")
    return {
        "status_code": result.get("statusCode"),
        "execution_time_ms": body.get("execution_time_ms"),
        "timed_out": body.get("timed_out"),
        "return_code": body.get("return_code"),
        "stopped_after_boot": body.get("stopped_after_boot"),
        "boot_completed": metrics.get("boot_completed", False),
        "total_kernel_ticks": metrics.get("stage_ticks", {}).get("total_kernel"),
        "total_kernel_ms": metrics.get("total_kernel_ms"),
        "kinit_ms": stage_ms.get("kinit"),
        "vm_init_ms": stage_ms.get("vm_init"),
        "procinit_ms": stage_ms.get("procinit"),
        "userinit_ms": stage_ms.get("userinit"),
        "panic": bool_from_text(stdout_excerpt, "panic:"),
        "stdout_excerpt": stdout_excerpt,
        "stderr_excerpt": body.get("stderr_excerpt", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure xv6 boot timing via the trigger handler.")
    parser.add_argument("--runs", type=int, default=5, help="Number of trigger runs.")
    parser.add_argument("--pause-ms", type=int, default=0, help="Pause between runs.")
    parser.add_argument("--json", action="store_true", help="Emit full JSON results.")
    parser.add_argument("--label", default="local-trigger", help="Experiment label used in saved filenames.")
    parser.add_argument(
        "--output-dir",
        default="experiments/results/local",
        help="Directory for JSON and CSV outputs.",
    )
    args = parser.parse_args()

    runs: list[dict] = []
    for index in range(args.runs):
        run = run_once()
        run["run"] = index + 1
        runs.append(run)
        if args.pause_ms and index + 1 < args.runs:
            time.sleep(args.pause_ms / 1000)

    successful_boots = [run for run in runs if run.get("boot_completed")]
    trigger_times = [run["execution_time_ms"] for run in runs if run.get("execution_time_ms") is not None]
    kernel_times = [run["total_kernel_ms"] for run in successful_boots if run.get("total_kernel_ms") is not None]
    xv6_root = xv6_root_from_env()
    kernel_constants = read_kernel_constants(xv6_root)
    stamp = utc_timestamp()
    output_dir = ensure_dir(Path(args.output_dir))
    base_name = f"{stamp}_{args.label}"
    json_path = output_dir / f"{base_name}.json"
    csv_path = output_dir / f"{base_name}.csv"

    summary = {
        "created_at_utc": stamp,
        "label": args.label,
        "xv6_root": str(xv6_root),
        "runs": args.runs,
        "successful_boots": len(successful_boots),
        "runtime_config": runtime_config(),
        "kernel_constants": kernel_constants,
        "trigger_time_ms": summarize(trigger_times),
        "kernel_boot_ms": summarize(kernel_times),
        "results": runs,
    }

    rows = []
    for run in runs:
        rows.append(
            {
                "run": run["run"],
                "status_code": run["status_code"],
                "execution_time_ms": run["execution_time_ms"],
                "total_kernel_ticks": run["total_kernel_ticks"],
                "total_kernel_ms": run["total_kernel_ms"],
                "kinit_ms": run["kinit_ms"],
                "vm_init_ms": run["vm_init_ms"],
                "procinit_ms": run["procinit_ms"],
                "userinit_ms": run["userinit_ms"],
                "boot_completed": run["boot_completed"],
                "timed_out": run["timed_out"],
                "return_code": run["return_code"],
                "stopped_after_boot": run["stopped_after_boot"],
                "panic": run["panic"],
            }
        )

    write_json(json_path, summary)
    write_csv(
        csv_path,
        rows,
        [
            "run",
            "status_code",
            "execution_time_ms",
            "total_kernel_ticks",
            "total_kernel_ms",
            "kinit_ms",
            "vm_init_ms",
            "procinit_ms",
            "userinit_ms",
            "boot_completed",
            "timed_out",
            "return_code",
            "stopped_after_boot",
            "panic",
        ],
    )

    if args.json:
        print(f"saved_json={json_path}")
        print(f"saved_csv={csv_path}")
        print(json.dumps(summary, indent=2))
        return

    print(f"saved_json={json_path}")
    print(f"saved_csv={csv_path}")
    print(f"runs={summary['runs']} successful_boots={summary['successful_boots']}")
    if trigger_times:
        print(
            "trigger_time_ms "
            f"mean={summary['trigger_time_ms']['mean']:.3f} "
            f"min={summary['trigger_time_ms']['min']:.3f} "
            f"max={summary['trigger_time_ms']['max']:.3f}"
        )
    if kernel_times:
        print(
            "kernel_boot_ms "
            f"mean={summary['kernel_boot_ms']['mean']:.3f} "
            f"min={summary['kernel_boot_ms']['min']:.3f} "
            f"max={summary['kernel_boot_ms']['max']:.3f}"
        )

    for run in runs:
        print(
            f"run={run['run']} status={run['status_code']} "
            f"trigger_ms={run['execution_time_ms']:.3f} "
            f"kernel_ms={run['total_kernel_ms']} "
            f"return_code={run['return_code']} timed_out={run['timed_out']} "
            f"boot_completed={run['boot_completed']} panic={run['panic']}"
        )


if __name__ == "__main__":
    main()
