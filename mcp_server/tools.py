from collections import Counter
from typing import Any, Dict, List

from mcp_server.case_loader import (
    load_case_manifest,
    load_events,
    load_dependency_graph,
    load_ground_truth,
)


def _top_event_refs(events: List[Dict[str, Any]], limit: int = 10) -> List[str]:
    refs = []
    for event in events[:limit]:
        event_id = event.get("event_id")
        if event_id:
            refs.append(event_id)
    return refs


def _count_by(events: List[Dict[str, Any]], field: str) -> Dict[str, int]:
    return dict(Counter(str(event.get(field, "unknown")) for event in events))


def get_case_manifest(case_dir: str | None = None) -> Dict[str, Any]:
    manifest = load_case_manifest(case_dir)
    ground_truth = load_ground_truth(case_dir)

    return {
        "status": "success",
        "tool": "get_case_manifest",
        "case_id": manifest.get("case_id"),
        "case_name": manifest.get("case_name"),
        "case_type": manifest.get("case_type"),
        "case_goal": manifest.get("case_goal"),
        "read_only": manifest.get("read_only", True),
        "files": manifest.get("files", {}),
        "expected_classification": ground_truth.get("expected_classification"),
        "expected_agent_behavior": manifest.get("expected_agent_behavior", []),
    }


def get_power_event_summary(case_dir: str | None = None) -> Dict[str, Any]:
    events = load_events("power_events", case_dir)

    attack_events = [e for e in events if e.get("event_type") == "power_cyber_attack"]
    natural_events = [e for e in events if e.get("event_type") == "power_natural_disturbance"]
    normal_events = [e for e in events if e.get("event_type") == "power_normal_operation"]

    suspicious = attack_events or natural_events

    return {
        "status": "success",
        "tool": "get_power_event_summary",
        "sector": "power",
        "total_events": len(events),
        "event_type_counts": _count_by(events, "event_type"),
        "severity_counts": _count_by(events, "severity"),
        "attack_event_count": len(attack_events),
        "natural_event_count": len(natural_events),
        "normal_event_count": len(normal_events),
        "finding": "power_event_detected" if suspicious else "no_power_attack_in_loaded_sample",
        "evidence_refs": _top_event_refs(suspicious[:10]),
        "sample_refs": _top_event_refs(events[:5]),
        "note": "This tool returns normalized power evidence only; it does not inspect or modify raw data.",
    }


def get_water_event_summary(case_dir: str | None = None) -> Dict[str, Any]:
    treatment_events = load_events("water_treatment_events", case_dir)
    distribution_events = load_events("water_distribution_events", case_dir)

    all_water = treatment_events + distribution_events

    attack_like = [
        e for e in all_water
        if "attack" in str(e.get("event_type", "")).lower()
        or str(e.get("severity", "")).lower() == "high"
    ]

    return {
        "status": "success",
        "tool": "get_water_event_summary",
        "sector": "water",
        "total_events": len(all_water),
        "treatment_event_count": len(treatment_events),
        "distribution_event_count": len(distribution_events),
        "event_type_counts": _count_by(all_water, "event_type"),
        "severity_counts": _count_by(all_water, "severity"),
        "water_anomaly_event_count": len(attack_like),
        "finding": "water_anomaly_detected" if attack_like else "no_water_attack_in_loaded_sample",
        "evidence_refs": _top_event_refs(attack_like[:10]),
        "sample_refs": _top_event_refs(all_water[:5]),
        "note": "This combines SWaT treatment and BATADAL distribution normalized events.",
    }


def get_network_attack_evidence(case_dir: str | None = None) -> Dict[str, Any]:
    events = load_events("network_events", case_dir)

    attack_events = [
        e for e in events
        if e.get("event_type") == "network_modbus_syn_flood_attack"
        or str(e.get("label")) == "1"
        or str(e.get("severity")).lower() == "high"
    ]

    protocol_counts = Counter(
        str(e.get("network", {}).get("protocol", "unknown")) for e in events
    )

    signal_counts = Counter()
    for event in events:
        for signal in event.get("network", {}).get("signals", []):
            signal_counts[signal] += 1

    return {
        "status": "success",
        "tool": "get_network_attack_evidence",
        "sector": "network",
        "total_events": len(events),
        "attack_event_count": len(attack_events),
        "protocol_counts": dict(protocol_counts),
        "signal_counts": dict(signal_counts),
        "finding": "network_attack_evidence_present" if attack_events else "no_network_attack_in_loaded_sample",
        "evidence_refs": _top_event_refs(attack_events[:10]),
        "sample_refs": _top_event_refs(events[:5]),
        "note": "This tool summarizes Modbus/TCP normalized network evidence.",
    }


def get_endpoint_evidence(case_dir: str | None = None) -> Dict[str, Any]:
    events = load_events("endpoint_events", case_dir)

    high_events = [e for e in events if str(e.get("severity")).lower() == "high"]
    defense_evasion = [
        e for e in events
        if "possible_defense_evasion" in e.get("endpoint", {}).get("signals", [])
        or e.get("event_type") == "endpoint_audit_log_cleared"
    ]

    event_id_counts = Counter(
        str(e.get("endpoint", {}).get("event_id", "unknown")) for e in events
    )

    signal_counts = Counter()
    for event in events:
        for signal in event.get("endpoint", {}).get("signals", []):
            signal_counts[signal] += 1

    return {
        "status": "success",
        "tool": "get_endpoint_evidence",
        "sector": "endpoint",
        "total_events": len(events),
        "high_severity_event_count": len(high_events),
        "defense_evasion_event_count": len(defense_evasion),
        "event_id_counts": dict(event_id_counts),
        "signal_counts": dict(signal_counts),
        "finding": "endpoint_defense_evasion_evidence_present" if defense_evasion else "no_endpoint_defense_evasion_in_loaded_sample",
        "evidence_refs": _top_event_refs(defense_evasion[:10]),
        "sample_refs": _top_event_refs(events[:5]),
        "note": "This tool summarizes normalized Mordor endpoint evidence.",
    }


def get_dependency_summary(case_dir: str | None = None) -> Dict[str, Any]:
    graph = load_dependency_graph(case_dir)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    power_to_water_edges = [
        e for e in edges
        if e.get("relationship") == "supplies_power_to"
        and "WATER" in str(e.get("to", ""))
    ]

    return {
        "status": "success",
        "tool": "get_dependency_summary",
        "case_id": graph.get("case_id"),
        "graph_type": graph.get("graph_type"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "power_to_water_dependency_count": len(power_to_water_edges),
        "power_to_water_dependencies": power_to_water_edges,
        "finding": "power_to_water_dependency_present" if power_to_water_edges else "no_power_to_water_dependency_found",
    }