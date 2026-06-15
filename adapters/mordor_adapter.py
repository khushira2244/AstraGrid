import json
from pathlib import Path
from typing import Dict, List, Any


ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = ROOT / "configs" / "column_maps" / "mordor_endpoint.json"
OUTPUT_PATH = ROOT / "data" / "processed" / "endpoint_events.json"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_lines(file_path: Path) -> List[Dict[str, Any]]:
    events = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))

    return events


def infer_endpoint_signals(event: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
    signals = []

    message = str(event.get("Message", ""))
    event_id = event.get("EventID")

    patterns = config["important_event_patterns"]

    if event_id == patterns["audit_log_cleared"]["event_id"]:
        signals.append("audit_log_cleared")
        signals.append("possible_defense_evasion")

    for keyword in patterns["powershell_activity"]["message_keywords"]:
        if keyword.lower() in message.lower():
            signals.append("powershell_activity")
            break

    for keyword in patterns["process_or_command_activity"]["message_keywords"]:
        if keyword.lower() in message.lower():
            signals.append("process_or_command_activity")
            break

    return list(set(signals))


def event_type_from_signals(signals: List[str]) -> str:
    if "audit_log_cleared" in signals:
        return "endpoint_audit_log_cleared"
    if "powershell_activity" in signals:
        return "endpoint_powershell_activity"
    if "process_or_command_activity" in signals:
        return "endpoint_command_execution"
    return "endpoint_security_event"


def severity_from_signals(signals: List[str]) -> str:
    if "possible_defense_evasion" in signals:
        return "high"
    if "powershell_activity" in signals:
        return "medium"
    if "process_or_command_activity" in signals:
        return "medium"
    return "low"


def confidence_from_signals(signals: List[str]) -> float:
    if "possible_defense_evasion" in signals:
        return 0.86
    if "powershell_activity" in signals:
        return 0.78
    if "process_or_command_activity" in signals:
        return 0.72
    return 0.55


def build_event(
    row_id: int,
    source_file: str,
    raw_event: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    signals = infer_endpoint_signals(raw_event, config)

    return {
        "event_id": f"END-{row_id:06d}",
        "timestamp": raw_event.get("@timestamp") or raw_event.get("TimeCreated"),
        "sector": "endpoint",
        "source_dataset": config["dataset_id"],
        "asset": raw_event.get("Hostname", "unknown_host"),
        "event_type": event_type_from_signals(signals),
        "severity": severity_from_signals(signals),
        "confidence": confidence_from_signals(signals),
        "label": "endpoint_event",
        "endpoint": {
            "hostname": raw_event.get("Hostname"),
            "event_id": raw_event.get("EventID"),
            "source_name": raw_event.get("SourceName"),
            "channel": raw_event.get("Channel"),
            "level": raw_event.get("Level"),
            "message": raw_event.get("Message"),
            "signals": signals,
        },
        "evidence_ref": {
            "source_file": source_file,
            "row_id": row_id,
            "columns": config["normalized_event_mapping"]["evidence_sources"],
        },
    }


def convert_mordor_file(file_path: Path, max_events: int = 500) -> List[Dict[str, Any]]:
    config = load_config()

    raw_events = load_json_lines(file_path)
    raw_events = raw_events[:max_events]

    events = []

    for idx, raw_event in enumerate(raw_events):
        event = build_event(
            row_id=idx,
            source_file=file_path.name,
            raw_event=raw_event,
            config=config,
        )
        events.append(event)

    return events


def main():
    config = load_config()

    raw_folder = ROOT / config["raw_folder"]
    file_path = raw_folder / config["primary_file"]

    if not file_path.exists():
        raise FileNotFoundError(f"Mordor endpoint file not found: {file_path}")

    print(f"Reading Mordor endpoint file: {file_path}")

    events = convert_mordor_file(file_path, max_events=500)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    print(f"Generated {len(events)} endpoint events")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()