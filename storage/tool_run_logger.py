import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT / "outputs"
TOOL_RUN_LOG_PATH = OUTPUTS_DIR / "tool_runs.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_existing_logs() -> List[Dict[str, Any]]:
    if not TOOL_RUN_LOG_PATH.exists():
        return []

    with open(TOOL_RUN_LOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        return []

    return data


def save_logs(logs: List[Dict[str, Any]]) -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(TOOL_RUN_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


def next_tool_run_id(logs: List[Dict[str, Any]]) -> str:
    return f"TOOL-{len(logs) + 1:06d}"


def extract_evidence_refs(result: Dict[str, Any]) -> List[str]:
    refs = result.get("evidence_refs", [])

    if isinstance(refs, list):
        return refs

    return []


def log_tool_run(
    tool_name: str,
    status: str,
    started_at: str,
    completed_at: str,
    duration_ms: int,
    input_summary: Dict[str, Any],
    output_summary: Dict[str, Any],
    evidence_refs: List[str] | None = None,
    error: str | None = None,
) -> Dict[str, Any]:
    logs = load_existing_logs()

    log_entry = {
        "tool_run_id": next_tool_run_id(logs),
        "tool_name": tool_name,
        "status": status,
        "started_at": started_at,
        "completed_at": completed_at,
        "duration_ms": duration_ms,
        "input_summary": input_summary,
        "output_summary": output_summary,
        "evidence_refs": evidence_refs or [],
        "error": error,
    }

    logs.append(log_entry)
    save_logs(logs)

    return log_entry


def run_logged_tool(
    tool_name: str,
    tool_func,
    *args,
    input_summary: Dict[str, Any] | None = None,
    **kwargs,
) -> Dict[str, Any]:
    started_at = utc_now_iso()
    start = time.perf_counter()

    try:
        result = tool_func(*args, **kwargs)
        completed_at = utc_now_iso()
        duration_ms = int((time.perf_counter() - start) * 1000)

        output_summary = {
            "result_status": result.get("status"),
            "finding": result.get("finding"),
            "total_events": result.get("total_events"),
            "sector": result.get("sector"),
            "tool": result.get("tool"),
        }

        log_entry = log_tool_run(
            tool_name=tool_name,
            status="success",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            input_summary=input_summary or {},
            output_summary=output_summary,
            evidence_refs=extract_evidence_refs(result),
            error=None,
        )

        result["_tool_run_id"] = log_entry["tool_run_id"]
        return result

    except Exception as exc:
        completed_at = utc_now_iso()
        duration_ms = int((time.perf_counter() - start) * 1000)

        log_tool_run(
            tool_name=tool_name,
            status="error",
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            input_summary=input_summary or {},
            output_summary={},
            evidence_refs=[],
            error=str(exc),
        )

        raise