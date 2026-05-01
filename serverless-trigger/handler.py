import json
import os
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
BOOT_STAGE_RE = re.compile(r"^\[BOOT\]\s+([A-Za-z0-9_]+)\s+([0-9]+)\s+ticks$")
BOOT_START_RE = re.compile(r"^\[BOOT\]\s+start=([0-9]+)$")


def _default_xv6_root() -> Path:
    env_root = os.environ.get("XV6_ROOT")
    if env_root:
        return Path(env_root)

    local_parent = THIS_DIR.parent
    if (local_parent / "kernel" / "kernel").exists():
        return local_parent

    return THIS_DIR / "xv6"


def _decode_maybe_bytes(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _prepare_mutable_fs(base_fs_path: Path) -> Path:
    tmp_dir = Path(os.environ.get("XV6_TMPDIR", "/tmp"))
    tmp_dir.mkdir(parents=True, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(prefix="xv6-fs-", suffix=".img", dir=tmp_dir)
    os.close(fd)
    mutable_fs_path = Path(temp_path)
    shutil.copy2(base_fs_path, mutable_fs_path)
    return mutable_fs_path


def _build_qemu_command(kernel_path: Path, fs_path: Path) -> list[str]:
    qemu_bin = os.environ.get("QEMU_BIN", "qemu-system-riscv64")
    memory = os.environ.get("XV6_MEMORY", "64M")
    cpus = os.environ.get("XV6_CPUS", "1")

    return [
        qemu_bin,
        "-machine",
        "virt",
        "-bios",
        "none",
        "-kernel",
        str(kernel_path),
        "-m",
        memory,
        "-smp",
        cpus,
        "-nographic",
        "-monitor",
        "none",
        "-global",
        "virtio-mmio.force-legacy=false",
        "-drive",
        f"file={fs_path},if=none,format=raw,id=x0",
        "-device",
        "virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0",
    ]


def _parse_boot_metrics(output: str, tick_hz: int) -> dict[str, Any]:
    stage_ticks: dict[str, int] = {}
    boot_start_tick = None

    for line in output.splitlines():
        start_match = BOOT_START_RE.match(line.strip())
        if start_match:
            boot_start_tick = int(start_match.group(1))
            continue

        stage_match = BOOT_STAGE_RE.match(line.strip())
        if stage_match:
            stage_ticks[stage_match.group(1)] = int(stage_match.group(2))

    metrics: dict[str, Any] = {
        "tick_hz": tick_hz,
        "boot_start_tick": boot_start_tick,
        "stage_ticks": stage_ticks,
        "stage_ms": {
            stage: (ticks / tick_hz) * 1000 for stage, ticks in stage_ticks.items()
        },
        "boot_completed": "total_kernel" in stage_ticks,
    }
    if "total_kernel" in stage_ticks:
        metrics["total_kernel_ms"] = (stage_ticks["total_kernel"] / tick_hz) * 1000
    return metrics


def _terminate_process(process: subprocess.Popen) -> int | None:
    if process.poll() is not None:
        return process.returncode

    process.terminate()
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=1)
    return process.returncode


def _run_qemu(cmd: list[str], timeout_sec: float, env: dict[str, str]) -> tuple[str, str, bool, int | None, bool]:
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    assert process.stdout is not None
    assert process.stderr is not None

    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, data="stdout")
    selector.register(process.stderr, selectors.EVENT_READ, data="stderr")

    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    start = time.time()
    timed_out = False
    stopped_after_boot = False
    stop_after_boot = os.environ.get("XV6_STOP_ON_BOOT", "1") == "1"
    grace_after_boot_sec = float(os.environ.get("XV6_BOOT_GRACE_SEC", "0.05"))
    boot_seen_at = None

    try:
        while True:
            if process.poll() is not None:
                break

            now = time.time()
            if now - start >= timeout_sec:
                timed_out = True
                break

            if boot_seen_at is not None and now - boot_seen_at >= grace_after_boot_sec:
                stopped_after_boot = True
                break

            events = selector.select(timeout=0.1)
            for key, _ in events:
                chunk = os.read(key.fileobj.fileno(), 4096)
                if not chunk:
                    try:
                        selector.unregister(key.fileobj)
                    except Exception:
                        pass
                    continue

                if key.data == "stdout":
                    stdout_chunks.append(chunk)
                    combined_stdout = b"".join(stdout_chunks).decode("utf-8", errors="replace")
                    if stop_after_boot and boot_seen_at is None and "[BOOT] total_kernel" in combined_stdout:
                        boot_seen_at = time.time()
                else:
                    stderr_chunks.append(chunk)

        return_code = _terminate_process(process)

        # Drain any remaining buffered output after terminate/exit.
        while True:
            events = selector.select(timeout=0)
            if not events:
                break
            for key, _ in events:
                chunk = os.read(key.fileobj.fileno(), 4096)
                if not chunk:
                    try:
                        selector.unregister(key.fileobj)
                    except Exception:
                        pass
                    continue
                if key.data == "stdout":
                    stdout_chunks.append(chunk)
                else:
                    stderr_chunks.append(chunk)
    finally:
        selector.close()

    stdout = b"".join(stdout_chunks).decode("utf-8", errors="replace")
    stderr = b"".join(stderr_chunks).decode("utf-8", errors="replace")
    return stdout, stderr, timed_out, return_code, stopped_after_boot


def handler(event, context):
    start_time = time.time()
    xv6_root = _default_xv6_root()
    kernel_path = Path(os.environ.get("XV6_KERNEL", xv6_root / "kernel" / "kernel"))
    fs_path = Path(os.environ.get("XV6_FS", xv6_root / "fs.img"))
    timeout_sec = float(os.environ.get("XV6_BOOT_TIMEOUT_SEC", "5"))
    log_limit = int(os.environ.get("XV6_LOG_LIMIT", "500"))
    tick_hz = int(os.environ.get("XV6_TICK_HZ", "10000000"))

    response_body = {
        "message": "xv6 triggered",
        "xv6_root": str(xv6_root),
        "kernel_path": str(kernel_path),
        "base_fs_path": str(fs_path),
    }

    if not kernel_path.exists() or not fs_path.exists():
        missing = []
        if not kernel_path.exists():
            missing.append(str(kernel_path))
        if not fs_path.exists():
            missing.append(str(fs_path))

        end_time = time.time()
        response_body.update(
            {
                "error": "missing xv6 artifacts",
                "missing_paths": missing,
                "execution_time_ms": (end_time - start_time) * 1000,
            }
        )
        return {"statusCode": 500, "body": response_body}

    mutable_fs_path = _prepare_mutable_fs(fs_path)
    response_body["mutable_fs_path"] = str(mutable_fs_path)

    cmd = _build_qemu_command(kernel_path, mutable_fs_path)
    stdout = ""
    stderr = ""
    timed_out = False
    return_code = None
    stopped_after_boot = False
    child_env = os.environ.copy()
    child_env.setdefault("TMPDIR", "/tmp")

    try:
        stdout, stderr, timed_out, return_code, stopped_after_boot = _run_qemu(
            cmd,
            timeout_sec,
            child_env,
        )
    except Exception as exc:
        stderr = str(exc)

    end_time = time.time()

    try:
        mutable_fs_path.unlink(missing_ok=True)
    except OSError:
        pass

    response_body.update(
        {
            "execution_time_ms": (end_time - start_time) * 1000,
            "qemu_command": cmd,
            "timeout_sec": timeout_sec,
            "timed_out": timed_out,
            "return_code": return_code,
            "stopped_after_boot": stopped_after_boot,
            "stdout_excerpt": stdout[:log_limit],
            "stderr_excerpt": stderr[:log_limit],
            "boot_metrics": _parse_boot_metrics(stdout, tick_hz),
        }
    )

    return {"statusCode": 200, "body": response_body}


if __name__ == "__main__":
    print(json.dumps(handler({}, None), indent=2))
