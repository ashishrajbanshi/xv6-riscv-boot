import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name) for name in fieldnames})


def summarize(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "min": None, "max": None}
    return {
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
    }


def bool_from_text(text: str, needle: str) -> bool:
    return needle in (text or "")


def xv6_root_from_env() -> Path:
    env_root = os.environ.get("XV6_ROOT")
    if env_root:
        return Path(env_root)
    return THIS_DIR.parent


def read_kernel_constants(xv6_root: Path) -> dict[str, str | None]:
    param_h = xv6_root / "kernel" / "param.h"
    memlayout_h = xv6_root / "kernel" / "memlayout.h"

    constants = {
        "NPROC": None,
        "NCPU": None,
        "MAXOPBLOCKS": None,
        "NBUF": None,
        "PHYSTOP": None,
    }

    if param_h.exists():
        text = param_h.read_text(encoding="utf-8", errors="replace")
        for key in ("NPROC", "NCPU", "MAXOPBLOCKS", "NBUF"):
            match = re.search(rf"#define\s+{key}\s+(.+)", text)
            if match:
                constants[key] = match.group(1).strip()

    if memlayout_h.exists():
        text = memlayout_h.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"#define\s+PHYSTOP\s+(.+)", text)
        if match:
            constants["PHYSTOP"] = match.group(1).strip()

    return constants


def runtime_config() -> dict[str, str]:
    return {
        "XV6_MEMORY": os.environ.get("XV6_MEMORY", "128M"),
        "XV6_CPUS": os.environ.get("XV6_CPUS", "1"),
        "XV6_BOOT_TIMEOUT_SEC": os.environ.get("XV6_BOOT_TIMEOUT_SEC", "5"),
        "XV6_LOG_LIMIT": os.environ.get("XV6_LOG_LIMIT", "500"),
        "XV6_TICK_HZ": os.environ.get("XV6_TICK_HZ", "10000000"),
        "XV6_STOP_ON_BOOT": os.environ.get("XV6_STOP_ON_BOOT", "1"),
        "XV6_BOOT_GRACE_SEC": os.environ.get("XV6_BOOT_GRACE_SEC", "0.05"),
    }
