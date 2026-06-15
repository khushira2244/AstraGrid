import json
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = ROOT / "configs" / "column_maps" / "power_msu_ornl.json"
OUTPUT_PATH = ROOT / "data" / "processed" / "power_events.json"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_pmu_columns(df: pd.DataFrame, config: Dict[str, Any]) -> List[str]:
    rules = config["column_groups"]["pmu_measurements"]["rules"]
    prefixes = rules.get("include_prefixes", [])
    exact = rules.get("include_exact", [])

    cols = []
    for col in df.columns:
        if col in exact or any(str(col).startswith(prefix) for prefix in prefixes):
            cols.append(col)

    return cols


def get_existing_columns(df: pd.DataFrame, columns: List[str]) -> List[str]:
    return [col for col in columns if col in df.columns]


def severity_from_label(label: str) -> str:
    if label == "Attack":
        return "high"
    if label == "Natural":
        return "medium"
    return "low"


def confidence_from_label(label: str) -> float:
    if label == "Attack":
        return 0.90
    if label == "Natural":
        return 0.75
    return 0.60


def build_event(
    row_id: int,
    source_file: str,
    label: str,
    config: Dict[str, Any],
    evidence_columns: Dict[str, List[str]],
) -> Dict[str, Any]:
    event_type = config["normalized_event_mapping"]["event_type_from_label"].get(
        label, "power_unknown_event"
    )

    return {
        "event_id": f"PWR-{row_id:06d}",
        "timestamp": None,
        "sector": "power",
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


def convert_power_file(file_path: Path, max_rows: int = 500) -> List[Dict[str, Any]]:
    config = load_config()

    df = pd.read_csv(file_path, nrows=max_rows)
    label_col = config["label"]["column"]

    pmu_cols = get_pmu_columns(df, config)
    control_cols = get_existing_columns(
        df, config["column_groups"]["control_panel_logs"]["columns"]
    )
    relay_cols = get_existing_columns(
        df, config["column_groups"]["relay_logs"]["columns"]
    )
    snort_cols = get_existing_columns(
        df, config["column_groups"]["snort_ids_logs"]["columns"]
    )

    evidence_columns = {
        "pmu_measurements": pmu_cols[:10],  # keep refs small for output
        "control_panel_logs": control_cols,
        "relay_logs": relay_cols,
        "snort_ids_logs": snort_cols,
        "label": [label_col],
    }

    events = []

    for idx, row in df.iterrows():
        label = str(row[label_col])
        event = build_event(
            row_id=int(idx),
            source_file=file_path.name,
            label=label,
            config=config,
            evidence_columns=evidence_columns,
        )
        events.append(event)

    return events


def main():
    config = load_config()
    raw_folder = ROOT / config["raw_folder"]

    files = sorted(raw_folder.glob(config["file_pattern"]))

    if not files:
        raise FileNotFoundError(f"No power CSV files found in {raw_folder}")

    # Start with data2.csv if available, otherwise first CSV
    preferred = raw_folder / "data2.csv"
    file_path = preferred if preferred.exists() else files[0]

    print(f"Reading power file: {file_path}")

    events = convert_power_file(file_path, max_rows=500)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    print(f"Generated {len(events)} power events")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()