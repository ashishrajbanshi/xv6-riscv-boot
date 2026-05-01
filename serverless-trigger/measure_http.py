import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from experiment_utils import (
    bool_from_text,
    ensure_dir,
    runtime_config,
    summarize,
    utc_timestamp,
    write_csv,
    write_json,
)


def fetch_once(url: str, timeout_sec: float) -> dict[str, Any]:
    started = time.time()
    status = None
    error = None
    response_payload: dict[str, Any] | None = None

    try:
        with urllib.request.urlopen(url, timeout=timeout_sec) as response:
            status = response.status
            payload_text = response.read().decode("utf-8", errors="replace")
            response_payload = json.loads(payload_text)
    except urllib.error.HTTPError as exc:
        status = exc.code
        error = str(exc)
    except Exception as exc:
        error = str(exc)

    finished = time.time()

    body = (response_payload or {}).get("body", {})
    boot_metrics = body.get("boot_metrics", {})
    stage_ms = boot_metrics.get("stage_ms", {})
    stdout_excerpt = body.get("stdout_excerpt", "")

    return {
        "http_status": status,
        "roundtrip_ms": (finished - started) * 1000,
        "handler_status_code": (response_payload or {}).get("statusCode"),
        "handler_execution_time_ms": body.get("execution_time_ms"),
        "timed_out": body.get("timed_out"),
        "return_code": body.get("return_code"),
        "boot_completed": boot_metrics.get("boot_completed"),
        "total_kernel_ticks": boot_metrics.get("stage_ticks", {}).get("total_kernel"),
        "total_kernel_ms": boot_metrics.get("total_kernel_ms"),
        "kinit_ms": stage_ms.get("kinit"),
        "vm_init_ms": stage_ms.get("vm_init"),
        "procinit_ms": stage_ms.get("procinit"),
        "userinit_ms": stage_ms.get("userinit"),
        "panic": bool_from_text(stdout_excerpt, "panic:"),
        "stdout_excerpt": stdout_excerpt,
        "stderr_excerpt": body.get("stderr_excerpt", ""),
        "error": error,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure HTTP-facing xv6/noop cold-start endpoints.")
    parser.add_argument("--url", required=True, help="Full URL, for example http://localhost:8080/trigger")
    parser.add_argument("--runs", type=int, default=5, help="Number of requests.")
    parser.add_argument("--pause-ms", type=int, default=0, help="Pause between requests.")
    parser.add_argument("--timeout-sec", type=float, default=30.0, help="HTTP client timeout.")
    parser.add_argument("--label", default="http-trigger", help="Experiment label used in saved filenames.")
    parser.add_argument(
        "--output-dir",
        default="experiments/results/http",
        help="Directory for JSON and CSV outputs.",
    )
    args = parser.parse_args()

    runs: list[dict[str, Any]] = []
    for index in range(args.runs):
        run = fetch_once(args.url, args.timeout_sec)
        run["run"] = index + 1
        runs.append(run)
        if args.pause_ms and index + 1 < args.runs:
            time.sleep(args.pause_ms / 1000)

    roundtrip_values = [run["roundtrip_ms"] for run in runs if run.get("roundtrip_ms") is not None]
    handler_values = [
        run["handler_execution_time_ms"]
        for run in runs
        if run.get("handler_execution_time_ms") is not None
    ]
    kernel_values = [run["total_kernel_ms"] for run in runs if run.get("total_kernel_ms") is not None]

    stamp = utc_timestamp()
    output_dir = ensure_dir(Path(args.output_dir))
    base_name = f"{stamp}_{args.label}"
    json_path = output_dir / f"{base_name}.json"
    csv_path = output_dir / f"{base_name}.csv"

    summary = {
        "created_at_utc": stamp,
        "label": args.label,
        "url": args.url,
        "runs": args.runs,
        "runtime_config": runtime_config(),
        "roundtrip_ms": summarize(roundtrip_values),
        "handler_execution_time_ms": summarize(handler_values),
        "kernel_boot_ms": summarize(kernel_values),
        "results": runs,
    }

    rows = []
    for run in runs:
        rows.append(
            {
                "run": run["run"],
                "http_status": run["http_status"],
                "handler_status_code": run["handler_status_code"],
                "roundtrip_ms": run["roundtrip_ms"],
                "handler_execution_time_ms": run["handler_execution_time_ms"],
                "total_kernel_ticks": run["total_kernel_ticks"],
                "total_kernel_ms": run["total_kernel_ms"],
                "kinit_ms": run["kinit_ms"],
                "vm_init_ms": run["vm_init_ms"],
                "procinit_ms": run["procinit_ms"],
                "userinit_ms": run["userinit_ms"],
                "boot_completed": run["boot_completed"],
                "timed_out": run["timed_out"],
                "return_code": run["return_code"],
                "panic": run["panic"],
                "error": run["error"],
            }
        )

    write_json(json_path, summary)
    write_csv(
        csv_path,
        rows,
        [
            "run",
            "http_status",
            "handler_status_code",
            "roundtrip_ms",
            "handler_execution_time_ms",
            "total_kernel_ticks",
            "total_kernel_ms",
            "kinit_ms",
            "vm_init_ms",
            "procinit_ms",
            "userinit_ms",
            "boot_completed",
            "timed_out",
            "return_code",
            "panic",
            "error",
        ],
    )

    print(f"saved_json={json_path}")
    print(f"saved_csv={csv_path}")
    print(
        "roundtrip_ms "
        f"mean={summary['roundtrip_ms']['mean']:.3f} "
        f"min={summary['roundtrip_ms']['min']:.3f} "
        f"max={summary['roundtrip_ms']['max']:.3f}"
    )
    if handler_values:
        print(
            "handler_execution_time_ms "
            f"mean={summary['handler_execution_time_ms']['mean']:.3f} "
            f"min={summary['handler_execution_time_ms']['min']:.3f} "
            f"max={summary['handler_execution_time_ms']['max']:.3f}"
        )
    if kernel_values:
        print(
            "kernel_boot_ms "
            f"mean={summary['kernel_boot_ms']['mean']:.3f} "
            f"min={summary['kernel_boot_ms']['min']:.3f} "
            f"max={summary['kernel_boot_ms']['max']:.3f}"
        )


if __name__ == "__main__":
    main()
