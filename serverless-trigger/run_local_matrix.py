import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from experiment_utils import ensure_dir


THIS_DIR = Path(__file__).resolve().parent


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_saved_paths(output: str) -> dict[str, str]:
    saved: dict[str, str] = {}
    for line in output.splitlines():
        if line.startswith("saved_json="):
            saved["json"] = line.split("=", 1)[1].strip()
        elif line.startswith("saved_csv="):
            saved["csv"] = line.split("=", 1)[1].strip()
    return saved


def append_text(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def run_step(
    *,
    step_name: str,
    argv: list[str],
    env: dict[str, str],
    log_path: Path,
    cwd: Path,
) -> dict[str, Any]:
    started = time.time()
    append_text(
        log_path,
        f"\n## {step_name}\n"
        f"- started_utc: {now_utc()}\n"
        f"- cwd: `{cwd}`\n"
        f"- command: `{' '.join(argv)}`\n"
        f"- env: `{json.dumps({k: env[k] for k in sorted(env) if k.startswith('XV6_')}, sort_keys=True)}`\n\n",
    )

    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    duration_ms = (time.time() - started) * 1000

    append_text(
        log_path,
        f"### stdout\n```text\n{result.stdout}```\n"
        f"### stderr\n```text\n{result.stderr}```\n"
        f"- exit_code: `{result.returncode}`\n"
        f"- duration_ms: `{duration_ms:.3f}`\n",
    )

    saved = parse_saved_paths(result.stdout)
    if saved:
        append_text(log_path, f"- saved_outputs: `{json.dumps(saved, sort_keys=True)}`\n")

    return {
        "step_name": step_name,
        "argv": argv,
        "env": {k: env[k] for k in sorted(env) if k.startswith("XV6_")},
        "returncode": result.returncode,
        "duration_ms": duration_ms,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "saved_outputs": saved,
    }


def start_server(env: dict[str, str], cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, "serve.py"],
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def stop_server(process: subprocess.Popen, log_path: Path) -> None:
    process.terminate()
    try:
        stdout, _ = process.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, _ = process.communicate(timeout=2)
    append_text(
        log_path,
        "\n### server_output\n```text\n"
        + (stdout or "")
        + "```\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local xv6 measurement matrix and keep a step log.")
    parser.add_argument("--runs", type=int, default=5, help="Runs per measurement command.")
    parser.add_argument("--cpus", default="1", help="Value for XV6_CPUS.")
    parser.add_argument("--timeout-sec", default="5", help="Value for XV6_BOOT_TIMEOUT_SEC.")
    parser.add_argument(
        "--memories",
        default="32M,64M,128M",
        help="Comma-separated XV6_MEMORY values.",
    )
    parser.add_argument(
        "--skip-http",
        action="store_true",
        help="Only run direct local trigger measurements, not the HTTP /noop and /trigger endpoints.",
    )
    parser.add_argument(
        "--track-root",
        default="experiments/tracks",
        help="Directory for the run log and manifest.",
    )
    args = parser.parse_args()

    memories = [item.strip() for item in args.memories.split(",") if item.strip()]
    stamp = stamp_utc()
    track_dir = ensure_dir(Path(args.track_root) / f"{stamp}_local_matrix")
    log_path = track_dir / "steps.md"
    manifest_path = track_dir / "manifest.json"

    append_text(
        log_path,
        "# Local Matrix Track\n\n"
        f"- created_at_utc: `{now_utc()}`\n"
        f"- runs_per_measurement: `{args.runs}`\n"
        f"- memories: `{memories}`\n"
        f"- include_http: `{not args.skip_http}`\n",
    )

    steps: list[dict[str, Any]] = []

    for memory in memories:
        base_env = os.environ.copy()
        base_env["XV6_MEMORY"] = memory
        base_env["XV6_CPUS"] = args.cpus
        base_env["XV6_BOOT_TIMEOUT_SEC"] = args.timeout_sec

        steps.append(
            run_step(
                step_name=f"local-trigger-{memory}",
                argv=[
                    sys.executable,
                    "measure_boot.py",
                    "--runs",
                    str(args.runs),
                    "--label",
                    f"matrix_local_{memory.lower()}",
                ],
                env=base_env,
                log_path=log_path,
                cwd=THIS_DIR,
            )
        )

        if args.skip_http:
            continue

        append_text(
            log_path,
            f"\n## start-http-server-{memory}\n"
            f"- started_utc: {now_utc()}\n"
            f"- env: `{json.dumps({'XV6_MEMORY': memory, 'XV6_CPUS': args.cpus}, sort_keys=True)}`\n",
        )
        server = start_server(base_env, THIS_DIR)
        time.sleep(1)

        try:
            steps.append(
                run_step(
                    step_name=f"http-noop-{memory}",
                    argv=[
                        sys.executable,
                        "measure_http.py",
                        "--url",
                        "http://127.0.0.1:8080/noop",
                        "--runs",
                        str(args.runs),
                        "--label",
                        f"matrix_noop_{memory.lower()}",
                    ],
                    env=base_env,
                    log_path=log_path,
                    cwd=THIS_DIR,
                )
            )

            steps.append(
                run_step(
                    step_name=f"http-trigger-{memory}",
                    argv=[
                        sys.executable,
                        "measure_http.py",
                        "--url",
                        "http://127.0.0.1:8080/trigger",
                        "--runs",
                        str(args.runs),
                        "--label",
                        f"matrix_trigger_{memory.lower()}",
                    ],
                    env=base_env,
                    log_path=log_path,
                    cwd=THIS_DIR,
                )
            )
        finally:
            stop_server(server, log_path)

    manifest = {
        "created_at_utc": now_utc(),
        "runs": args.runs,
        "memories": memories,
        "cpus": args.cpus,
        "timeout_sec": args.timeout_sec,
        "include_http": not args.skip_http,
        "track_dir": str(track_dir),
        "steps": steps,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"track_log={log_path}")
    print(f"track_manifest={manifest_path}")


if __name__ == "__main__":
    main()
