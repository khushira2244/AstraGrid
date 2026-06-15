import json
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = ROOT / "configs" / "column_maps" / "batadal.json"
OUTPUT_PATH = ROOT / "data" / "processed" / "batadal_events.json"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_columns_by_prefix(df: pd.DataFrame, prefixes: List[str]) -> List[str]:
    cols = []
    for col in df.columns:
        if any(str(col).startswith(prefix) for prefix in prefixes):
            cols.append(col)
    return cols


def get_existing_columns(df: pd.DataFrame, columns: List[str]) -> List[str]:
    return [col for col in columns if col in df.columns]


def severity_from_label(label: str) -> str:
    if label == "1":
        return "high"
    return "low"


def confidence_from_label(label: str) -> float:
    if label == "1":
        return 0.88
    return 0.60


def build_event(
    row_id: int,
    source_file: str,
    timestamp: Any,
    label: str,
    config: Dict[str, Any],
    evidence_columns: Dict[str, List[str]],
) -> Dict[str, Any]:
    event_type = config["normalized_event_mapping"]["event_type_from_label"].get(
        label, "water_distribution_unknown_event"
    )

    return {
        "event_id": f"BATADAL-{row_id:06d}",
        "timestamp": str(timestamp),
        "sector": "water",
        "source_dataset": config["dataset_id"],
        "asset": config["normalized_event_mapping"]["asset_scope"],
        "event_type": event_type,
        "severity": severity_from_label(label),
        "confidence": confidence_from_label(label),
        "label": label,
        "evidence_ref": {
            "source_file": source_file,
            "row_id": row_id,
            "column_groups": evidence_columns,
        },
    }


def convert_batadal_file(file_path: Path, max_rows: int = 500) -> List[Dict[str, Any]]:
    config = load_config()

    df = pd.read_csv(file_path, nrows=max_rows)

    label_col = config["label"]["column"]
    time_col = config["time"]["column"]

    tank_cols = get_columns_by_prefix(
        df, config["column_groups"]["tank_levels"]["include_prefixes"]
    )
    pump_flow_cols = get_columns_by_prefix(
        df, config["column_groups"]["pump_flows"]["include_prefixes"]
    )
    pump_status_cols = get_columns_by_prefix(
        df, config["column_groups"]["pump_status"]["include_prefixes"]
    )
    valve_cols = get_existing_columns(
        df, config["column_groups"]["valve_flow_status"]["columns"]
    )
    pressure_cols = get_columns_by_prefix(
        df, config["column_groups"]["pressure_measurements"]["include_prefixes"]
    )

    evidence_columns = {
        "tank_levels": tank_cols,
        "pump_flows": pump_flow_cols,
        "pump_status": pump_status_cols,
        "valve_flow_status": valve_cols,
        "pressure_measurements": pressure_cols,
        "label": [label_col],
        "timestamp": [time_col],
    }

    events = []

    for idx, row in df.iterrows():
        label = str(row[label_col])
        timestamp = row[time_col]

        event = build_event(
            row_id=int(idx),
            source_file=file_path.name,
            timestamp=timestamp,
            label=label,
            config=config,
            evidence_columns=evidence_columns,
        )
        events.append(event)

    return events


def main():
    config = load_config()

    raw_folder = ROOT / config["raw_folder"]
    file_path = raw_folder / config["primary_file"]

    if not file_path.exists():
        raise FileNotFoundError(f"BATADAL file not found: {file_path}")

    print(f"Reading BATADAL file: {file_path}")

    events = convert_batadal_file(file_path, max_rows=500)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    print(f"Generated {len(events)} BATADAL events")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()