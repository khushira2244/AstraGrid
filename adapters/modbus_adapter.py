import json
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = ROOT / "configs" / "column_maps" / "modbus_syn_flood.json"
OUTPUT_PATH = ROOT / "data" / "processed" / "network_events.json"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


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


def infer_network_signal(row: pd.Series) -> List[str]:
    signals = []

    protocol = str(row.get("Protocol", ""))
    info = str(row.get("Info", ""))

    if "Modbus" in protocol:
        signals.append("modbus_tcp_protocol")

    if "Query" in info:
        signals.append("modbus_query")

    if "Response" in info:
        signals.append("modbus_response")

    if "Func" in info:
        signals.append("modbus_function_code_present")

    if "Write Single Register" in info:
        signals.append("write_single_register")

    if "Read Holding Registers" in info:
        signals.append("read_holding_registers")

    if "[SYN]" in info:
        signals.append("tcp_syn")

    if "[SYN, ACK]" in info:
        signals.append("tcp_syn_ack")

    if "[ACK]" in info:
        signals.append("tcp_ack")

    return signals


def build_event(
    row_id: int,
    source_file: str,
    row: pd.Series,
    label: str,
    config: Dict[str, Any],
    evidence_columns: Dict[str, List[str]],
) -> Dict[str, Any]:
    event_type = config["normalized_event_mapping"]["event_type_from_label"].get(
        label, "network_unknown_event"
    )

    return {
        "event_id": f"NET-{row_id:06d}",
        "timestamp": str(row.get("Time")),
        "sector": "network",
        "source_dataset": config["dataset_id"],
        "asset": config["normalized_event_mapping"]["asset_scope"],
        "event_type": event_type,
        "severity": severity_from_label(label),
        "confidence": confidence_from_label(label),
        "label": label,
        "network": {
            "source": str(row.get("Source")),
            "destination": str(row.get("Destination")),
            "protocol": str(row.get("Protocol")),
            "length": int(row.get("Length")) if pd.notna(row.get("Length")) else None,
            "info": str(row.get("Info")),
            "signals": infer_network_signal(row),
        },
        "evidence_ref": {
            "source_file": source_file,
            "row_id": row_id,
            "column_groups": evidence_columns,
        },
    }


def convert_modbus_file(file_path: Path, max_rows: int = 1000) -> List[Dict[str, Any]]:
    config = load_config()

    df = pd.read_csv(file_path, nrows=max_rows)
    df.columns = df.columns.str.strip()

    label_col = config["label"]["column"]

    network_identity_cols = get_existing_columns(
        df, config["column_groups"]["network_identity"]["columns"]
    )
    protocol_cols = get_existing_columns(
        df, config["column_groups"]["protocol_evidence"]["columns"]
    )

    evidence_columns = {
        "network_identity": network_identity_cols,
        "protocol_evidence": protocol_cols,
        "label": [label_col],
        "time": [config["time"]["column"]],
    }

    events = []

    for idx, row in df.iterrows():
        label = str(row[label_col])

        event = build_event(
            row_id=int(idx),
            source_file=file_path.name,
            row=row,
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
        raise FileNotFoundError(f"Modbus file not found: {file_path}")

    print(f"Reading Modbus network file: {file_path}")

    events = convert_modbus_file(file_path, max_rows=1000)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    print(f"Generated {len(events)} network events")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()