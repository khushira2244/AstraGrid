from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


CASE_DIR_DEFAULT = "data/sample_case_power_water_cascade"
WADI_CONFIG_DEFAULT = "configs/column_maps/wadi_optional.json"
OUTPUT_DIR_DEFAULT = "outputs"


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _write_markdown(path: Path, report: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    summary = report.get("summary", {})
    claim_boundaries = report.get("claim_boundaries", {})
    wadi = report.get("wadi_optional_adapter", {})

    lines: List[str] = [
        "# Context Integrity Report",
        "",
        f"Case: **{report.get('case_id', 'UNKNOWN')}**",
        "",
        "## Principle",
        "",
        report.get(
            "principle",
            "No cyber-physical claim should be promoted without validated infrastructure context.",
        ),
        "",
        "## Summary",
        "",
        f"- Overall context status: **{summary.get('overall_context_status')}**",
        f"- Water treatment context: **{summary.get('water_treatment_context')}**",
        f"- Water distribution context: **{summary.get('water_distribution_context')}**",
        f"- WADI optional adapter: **{summary.get('wadi_optional_adapter')}**",
        f"- Sensor context: **{summary.get('sensor_context')}**",
        f"- Actuator context: **{summary.get('actuator_context')}**",
        f"- Timestamp context: **{summary.get('timestamp_context')}**",
        f"- Dependency context: **{summary.get('dependency_context')}**",
        f"- Direct command path context: **{summary.get('direct_command_path_context')}**",
        "",
        "## Claim Boundaries",
        "",
        f"- Direct water cyberattack: **{claim_boundaries.get('direct_water_cyberattack')}**",
        f"- Power-to-water cascade: **{claim_boundaries.get('power_to_water_cascade')}**",
        f"- Attacker country attribution: **{claim_boundaries.get('attacker_country_attribution')}**",
        f"- Destructive response: **{claim_boundaries.get('destructive_response')}**",
        "",
        "## WADI Optional Adapter",
        "",
        f"- Dataset: **{wadi.get('dataset_name')}**",
        f"- Adapter status: **{wadi.get('status')}**",
        f"- Backend role: **{wadi.get('backend_role')}**",
        f"- Raw folder: `{wadi.get('raw_folder')}`",
        f"- Primary file: `{wadi.get('primary_file')}`",
        f"- Normal file: `{wadi.get('normal_file')}`",
        "",
        "## Checks",
        "",
    ]

    for check in report.get("checks", []):
        lines.extend(
            [
                f"### {check.get('check')}",
                f"- Status: **{check.get('status')}**",
                f"- Evidence: {check.get('evidence')}",
                f"- Meaning: {check.get('meaning')}",
                "",
            ]
        )

    lines.extend(
        [
            "## Final Context Decision",
            "",
            report.get("final_decision", ""),
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def _has_events(events: Any) -> bool:
    return isinstance(events, list) and len(events) > 0


def _has_column_groups(events: Any) -> bool:
    if not isinstance(events, list) or not events:
        return False

    first_event = events[0]
    evidence_ref = first_event.get("evidence_ref", {}) if isinstance(first_event, dict) else {}
    column_groups = evidence_ref.get("column_groups", {}) if isinstance(evidence_ref, dict) else {}

    return isinstance(column_groups, dict) and len(column_groups) > 0


def _has_timestamps(events: Any) -> bool:
    if not isinstance(events, list) or not events:
        return False

    return any(isinstance(event, dict) and bool(event.get("timestamp")) for event in events)


def _dependency_path_present(dependency_graph: Any) -> bool:
    if isinstance(dependency_graph, list):
        for item in dependency_graph:
            if not isinstance(item, dict):
                continue

            relationship = str(item.get("relationship", "")).lower()
            source = str(item.get("from", item.get("source", ""))).lower()
            target = str(item.get("to", item.get("target", ""))).lower()

            if "power" in source and "water" in target:
                return True

            if "supplies_power" in relationship:
                return True

    if isinstance(dependency_graph, dict):
        text = json.dumps(dependency_graph).lower()
        return "power" in text and "water" in text and "supplies" in text

    return False


def _wadi_status(wadi_config: Dict[str, Any]) -> str:
    inspection = wadi_config.get("inspection_result", {})
    status = inspection.get("status")

    if status:
        return str(status)

    if wadi_config.get("dataset_id") and wadi_config.get("column_groups"):
        return "specification_ready"

    return "missing"


def _wadi_has_sensor_groups(wadi_config: Dict[str, Any]) -> bool:
    column_groups = wadi_config.get("column_groups", {})
    sensors = column_groups.get("sensors", {})
    keywords = sensors.get("include_keywords", [])

    return isinstance(keywords, list) and len(keywords) > 0


def _wadi_has_actuator_groups(wadi_config: Dict[str, Any]) -> bool:
    column_groups = wadi_config.get("column_groups", {})
    actuators = column_groups.get("actuators", {})
    keywords = actuators.get("include_keywords", [])

    return isinstance(keywords, list) and len(keywords) > 0


def _wadi_has_label(wadi_config: Dict[str, Any]) -> bool:
    label = wadi_config.get("label", {})
    return bool(label.get("column")) and isinstance(label.get("classes"), dict)


def _wadi_has_time(wadi_config: Dict[str, Any]) -> bool:
    time = wadi_config.get("time", {})
    return bool(time.get("date_column")) and bool(time.get("time_column"))


def build_context_integrity_report(
    case_dir: str = CASE_DIR_DEFAULT,
    wadi_config_path: str = WADI_CONFIG_DEFAULT,
    output_dir: str = OUTPUT_DIR_DEFAULT,
    save: bool = True,
) -> Dict[str, Any]:
    case_path = Path(case_dir)
    wadi_path = Path(wadi_config_path)

    water_treatment_events = _read_json(case_path / "water_treatment_events.json", [])
    water_distribution_events = _read_json(case_path / "water_distribution_events.json", [])
    dependency_graph = _read_json(case_path / "dependency_graph.json", [])
    case_manifest = _read_json(case_path / "case_manifest.json", {})
    wadi_config = _read_json(wadi_path, {})

    case_id = case_manifest.get("case_id") or case_manifest.get("id") or "ASTRAGRID-001"

    water_treatment_present = _has_events(water_treatment_events)
    water_distribution_present = _has_events(water_distribution_events)
    batadal_column_groups_present = _has_column_groups(water_distribution_events)
    water_timestamps_present = _has_timestamps(water_treatment_events) or _has_timestamps(
        water_distribution_events
    )

    dependency_present = _dependency_path_present(dependency_graph)

    wadi_adapter_status = _wadi_status(wadi_config)
    wadi_config_present = wadi_adapter_status != "missing"
    wadi_sensor_context = _wadi_has_sensor_groups(wadi_config)
    wadi_actuator_context = _wadi_has_actuator_groups(wadi_config)
    wadi_label_context = _wadi_has_label(wadi_config)
    wadi_time_context = _wadi_has_time(wadi_config)

    # Important forensic boundary:
    # Existing water evidence and WADI context do not prove direct PLC/SCADA command path.
    direct_command_path_present = False

    checks: List[Dict[str, Any]] = [
        {
            "check": "water_treatment_context",
            "status": "PRESENT" if water_treatment_present else "MISSING",
            "evidence": "water_treatment_events.json",
            "meaning": "SWaT-style water treatment evidence is available for the case.",
        },
        {
            "check": "water_distribution_context",
            "status": "PRESENT" if water_distribution_present else "MISSING",
            "evidence": "water_distribution_events.json",
            "meaning": "BATADAL-style water distribution evidence is available for the case.",
        },
        {
            "check": "batadal_column_group_context",
            "status": "PRESENT" if batadal_column_groups_present else "MISSING",
            "evidence": "water_distribution_events.json evidence_ref.column_groups",
            "meaning": "Tank, pump, valve, pressure, label, and timestamp groups are mapped.",
        },
        {
            "check": "wadi_optional_adapter",
            "status": "ACCEPTED" if wadi_config_present else "MISSING",
            "evidence": wadi_config_path,
            "meaning": "WADI is available as an optional large water-distribution adapter specification.",
        },
        {
            "check": "wadi_sensor_context",
            "status": "PRESENT" if wadi_sensor_context else "MISSING",
            "evidence": "configs/column_maps/wadi_optional.json column_groups.sensors",
            "meaning": "WADI sensor keyword groups are defined for large-scale water distribution context.",
        },
        {
            "check": "wadi_actuator_context",
            "status": "PRESENT" if wadi_actuator_context else "MISSING",
            "evidence": "configs/column_maps/wadi_optional.json column_groups.actuators",
            "meaning": "WADI actuator/control keyword groups are defined.",
        },
        {
            "check": "wadi_label_context",
            "status": "PRESENT" if wadi_label_context else "MISSING",
            "evidence": "configs/column_maps/wadi_optional.json label",
            "meaning": "WADI normal/attack label mapping is defined.",
        },
        {
            "check": "timestamp_context",
            "status": "PRESENT" if water_timestamps_present and wadi_time_context else "PARTIAL",
            "evidence": "case water timestamps + WADI date/time config",
            "meaning": "Timestamp fields exist for comparing windows across evidence layers.",
        },
        {
            "check": "dependency_context",
            "status": "CONFIRMED" if dependency_present else "MISSING",
            "evidence": "dependency_graph.json",
            "meaning": "A power-to-water dependency path is available for cascade reasoning.",
        },
        {
            "check": "direct_plc_or_scada_command_path",
            "status": "UNSUPPORTED" if not direct_command_path_present else "PRESENT",
            "evidence": "No direct command-path proof found in the loaded water context.",
            "meaning": "Water evidence does not automatically prove a direct water cyberattack.",
        },
    ]

    missing_count = sum(1 for check in checks if check["status"] == "MISSING")
    partial_count = sum(1 for check in checks if check["status"] == "PARTIAL")
    unsupported_count = sum(1 for check in checks if check["status"] == "UNSUPPORTED")

    if missing_count == 0 and partial_count == 0:
        overall_status = "STRONG"
    elif missing_count <= 1:
        overall_status = "PARTIAL"
    else:
        overall_status = "WEAK"

    direct_water_attack_status = "UNSUPPORTED"
    cascade_status = "PARTIALLY_CONFIRMED" if dependency_present and water_distribution_present else "INSUFFICIENT_CONTEXT"

    report: Dict[str, Any] = {
        "status": "success",
        "case_id": case_id,
        "layer": "context_integrity",
        "principle": "No direct attack or cascade claim should be promoted without validated infrastructure context.",
        "summary": {
            "overall_context_status": overall_status,
            "water_treatment_context": "PRESENT" if water_treatment_present else "MISSING",
            "water_distribution_context": "PRESENT" if water_distribution_present else "MISSING",
            "wadi_optional_adapter": wadi_adapter_status,
            "sensor_context": "PRESENT" if batadal_column_groups_present or wadi_sensor_context else "MISSING",
            "actuator_context": "PRESENT" if wadi_actuator_context else "MISSING",
            "timestamp_context": "PRESENT" if water_timestamps_present and wadi_time_context else "PARTIAL",
            "dependency_context": "CONFIRMED" if dependency_present else "MISSING",
            "direct_command_path_context": "UNSUPPORTED",
        },
        "claim_boundaries": {
            "direct_water_cyberattack": direct_water_attack_status,
            "power_to_water_cascade": cascade_status,
            "attacker_country_attribution": "NOT_SUPPORTED",
            "destructive_response": "HUMAN_APPROVAL_REQUIRED",
        },
        "wadi_optional_adapter": {
            "dataset_id": wadi_config.get("dataset_id"),
            "dataset_name": wadi_config.get("dataset_name"),
            "status": wadi_adapter_status,
            "backend_role": wadi_config.get("backend_role"),
            "raw_folder": wadi_config.get("raw_folder"),
            "primary_file": wadi_config.get("primary_file"),
            "normal_file": wadi_config.get("normal_file"),
            "label_column": wadi_config.get("label", {}).get("column"),
            "inspection_result": wadi_config.get("inspection_result", {}),
        },
        "checks": checks,
        "final_decision": (
            "AstraGrid treats WADI as an optional large-scale water-distribution adapter "
            "and uses it to strengthen context integrity. The existing case supports water "
            "context and a power-to-water dependency path, but direct water cyberattack remains "
            "UNSUPPORTED because no direct PLC/SCADA command path is proven."
        ),
    }

    if save:
        output_path = Path(output_dir)
        _write_json(output_path / "context_integrity_report.json", report)
        _write_markdown(output_path / "context_integrity_report.md", report)

    return report


if __name__ == "__main__":
    result = build_context_integrity_report()
    print("[OK] Context integrity report generated")
    print(json.dumps(result.get("summary", {}), indent=2))