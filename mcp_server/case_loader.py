import json
from pathlib import Path
from typing import Any, Dict, List

from mcp_server.safety import resolve_case_path, safe_file_path


def load_json_file(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_case_manifest(case_dir: str | None = None) -> Dict[str, Any]:
    case_path = resolve_case_path(case_dir)
    manifest_path = safe_file_path(case_path, "case_manifest.json")
    return load_json_file(manifest_path)


def load_case_file(file_key: str, case_dir: str | None = None) -> Any:
    case_path = resolve_case_path(case_dir)
    manifest = load_case_manifest(str(case_path))

    files = manifest.get("files", {})

    if file_key not in files:
        raise KeyError(f"File key not found in manifest: {file_key}")

    relative_path = files[file_key]["path"]
    file_path = safe_file_path(case_path, relative_path)

    return load_json_file(file_path)


def load_events(file_key: str, case_dir: str | None = None) -> List[Dict[str, Any]]:
    data = load_case_file(file_key, case_dir)

    if not isinstance(data, list):
        raise TypeError(f"Expected list of events for {file_key}, got {type(data)}")

    return data


def load_dependency_graph(case_dir: str | None = None) -> Dict[str, Any]:
    data = load_case_file("dependency_graph", case_dir)

    if not isinstance(data, dict):
        raise TypeError("dependency_graph must be a JSON object")

    return data


def load_ground_truth(case_dir: str | None = None) -> Dict[str, Any]:
    data = load_case_file("ground_truth", case_dir)

    if not isinstance(data, dict):
        raise TypeError("ground_truth must be a JSON object")

    return data