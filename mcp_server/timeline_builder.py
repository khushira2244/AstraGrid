from typing import Any, Dict, List


def build_timeline_event(
    order: int,
    phase: str,
    title: str,
    sector: str,
    status: str,
    description: str,
    source_tool: str,
    tool_run_id: str | None,
    evidence_refs: List[str] | None = None,
) -> Dict[str, Any]:
    return {
        "order": order,
        "phase": phase,
        "title": title,
        "sector": sector,
        "status": status,
        "description": description,
        "source_tool": source_tool,
        "tool_run_id": tool_run_id,
        "evidence_refs": evidence_refs or [],
    }


def build_case_timeline(tool_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    power = tool_results["power"]
    water = tool_results["water"]
    network = tool_results["network"]
    endpoint = tool_results["endpoint"]
    dependency = tool_results["dependency"]

    timeline = [
        build_timeline_event(
            order=1,
            phase="initial_triage",
            title="Endpoint forensic evidence checked",
            sector="endpoint",
            status="CONFIRMED"
            if endpoint.get("defense_evasion_event_count", 0) > 0
            else "PARTIALLY_CONFIRMED",
            description=(
                "The agent checks host-level forensic evidence first to identify "
                "possible compromise or defense-evasion activity."
            ),
            source_tool=endpoint.get("tool"),
            tool_run_id=endpoint.get("_tool_run_id"),
            evidence_refs=endpoint.get("evidence_refs", []),
        ),
        build_timeline_event(
            order=2,
            phase="power_investigation",
            title="Power-grid evidence checked",
            sector="power",
            status="CONFIRMED" if power.get("total_events", 0) > 0 else "UNSUPPORTED",
            description=(
                "The agent evaluates normalized power-grid evidence before assuming "
                "that the downstream water issue is a direct cyberattack."
            ),
            source_tool=power.get("tool"),
            tool_run_id=power.get("_tool_run_id"),
            evidence_refs=power.get("evidence_refs", []),
        ),
        build_timeline_event(
            order=3,
            phase="water_investigation",
            title="Water utility evidence checked",
            sector="water",
            status="CONFIRMED" if water.get("total_events", 0) > 0 else "UNSUPPORTED",
            description=(
                "The agent checks water-treatment and water-distribution evidence "
                "for operational anomaly or direct attack indicators."
            ),
            source_tool=water.get("tool"),
            tool_run_id=water.get("_tool_run_id"),
            evidence_refs=water.get("evidence_refs", []),
        ),
        build_timeline_event(
            order=4,
            phase="network_investigation",
            title="Network / Modbus evidence checked",
            sector="network",
            status="CONFIRMED" if network.get("total_events", 0) > 0 else "UNSUPPORTED",
            description=(
                "The agent checks Modbus/TCP network evidence to decide whether "
                "direct PLC or water-side attack activity is supported."
            ),
            source_tool=network.get("tool"),
            tool_run_id=network.get("_tool_run_id"),
            evidence_refs=network.get("evidence_refs", []),
        ),
        build_timeline_event(
            order=5,
            phase="dependency_reasoning",
            title="Power-to-water dependency checked",
            sector="cross_sector",
            status="CONFIRMED"
            if dependency.get("power_to_water_dependency_count", 0) > 0
            else "UNSUPPORTED",
            description=(
                "The agent checks the dependency graph to determine whether a "
                "power event could plausibly cascade into water utility impact."
            ),
            source_tool=dependency.get("tool"),
            tool_run_id=dependency.get("_tool_run_id"),
            evidence_refs=dependency.get("evidence_refs", []),
        ),
        build_timeline_event(
            order=6,
            phase="corrected_hypothesis",
            title="Initial direct-water-attack hypothesis corrected",
            sector="reasoning",
            status="PARTIALLY_CONFIRMED",
            description=(
                "Because a power-to-water dependency exists and direct water attack "
                "evidence is not yet independently proven, the agent should avoid "
                "claiming a direct water cyberattack and instead classify the case "
                "as a plausible power-to-water cascade."
            ),
            source_tool="reasoning_synthesis",
            tool_run_id=None,
            evidence_refs=[],
        ),
    ]

    return timeline