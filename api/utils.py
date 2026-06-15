import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
CASE_DIR = BASE_DIR / "data" / "sample_case_power_water_cascade"


def read_json_file(file_path: Path) -> Any:
    if not file_path.exists():
        return {
            "status": "missing",
            "message": f"File not found: {file_path.name}",
            "path": str(file_path),
        }

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        return {
            "status": "error",
            "message": f"Invalid JSON in {file_path.name}",
            "error": str(error),
        }


def read_text_file(file_path: Path) -> dict:
    if not file_path.exists():
        return {
            "status": "missing",
            "message": f"File not found: {file_path.name}",
            "path": str(file_path),
        }

    try:
        return {
            "status": "success",
            "file_name": file_path.name,
            "content": file_path.read_text(encoding="utf-8"),
        }
    except Exception as error:
        return {
            "status": "error",
            "message": f"Could not read {file_path.name}",
            "error": str(error),
        }


def output_json(file_name: str) -> Any:
    return read_json_file(OUTPUTS_DIR / file_name)


def output_markdown(file_name: str) -> dict:
    return read_text_file(OUTPUTS_DIR / file_name)


def case_json(file_name: str) -> Any:
    return read_json_file(CASE_DIR / file_name)


def build_case_summary() -> dict:
    manifest = case_json("case_manifest.json")
    claims = output_json("claims.json")
    findings = output_json("findings.json")
    timeline = output_json("timeline.json")
    tool_runs = output_json("tool_runs.json")

    return {
        "status": "success",
        "case": manifest,
        "counts": {
            "claims": len(claims) if isinstance(claims, list) else 0,
            "findings": (
                            len(findings.get("findings", []))
                            if isinstance(findings, dict)
                            else len(findings)
                            if isinstance(findings, list)
                            else 0
                        ),
            "timeline_events": len(timeline) if isinstance(timeline, list) else 0,
            "tool_runs": len(tool_runs) if isinstance(tool_runs, list) else 0,
        },
        "result": {
            "expected_main_result": "Direct water cyberattack unsupported; power-to-water cascade partially confirmed"
        },
    }