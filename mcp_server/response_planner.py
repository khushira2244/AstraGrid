from datetime import datetime, timezone
from typing import Any, Dict, List


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_response_plan(
    findings: List[Dict[str, Any]],
    claims: List[Dict[str, Any]],
    tool_results: Dict[str, Any],
) -> Dict[str, Any]:
    claim_by_id = {claim.get("claim_id"): claim for claim in claims}

    direct_water_claim = claim_by_id.get("CLAIM-004", {})
    cascade_claim = claim_by_id.get("CLAIM-005", {})

    power = tool_results.get("power", {})
    water = tool_results.get("water", {})
    network = tool_results.get("network", {})
    endpoint = tool_results.get("endpoint", {})
    dependency = tool_results.get("dependency", {})

    return {
        "response_plan_id": "RESP-ASTRAGRID-001",
        "case_id": tool_results.get("manifest", {}).get("case_id", "ASTRAGRID-001"),
        "generated_at": utc_now_iso(),
        "response_mode": "safe_autonomous_recommendation",
        "automation_boundary": (
            "AstraGrid recommends response actions but does not perform destructive "
            "or operational infrastructure changes without human approval."
        ),
        "incident_classification": (
            "POWER_TO_WATER_CASCADE"
            if dependency.get("power_to_water_dependency_count", 0) > 0
            else "INSUFFICIENT_EVIDENCE"
        ),
        "key_reasoning": {
            "initial_hypothesis": "Direct water cyberattack",
            "corrected_hypothesis": (
                "Power-to-water cascade is plausible; direct water attack is unsupported"
            ),
            "direct_water_attack_status": direct_water_claim.get("status", "UNKNOWN"),
            "cascade_status": cascade_claim.get("status", "UNKNOWN"),
            "why_not_direct_water_attack": (
                "Water evidence exists, but the current evidence does not prove a direct "
                "PLC or SCADA command path causing the water anomaly."
            ),
            "why_cascade_response": (
                "Power evidence, water evidence, and a dependency path from "
                "POWER_SUBSTATION_01 to WATER_PUMP_STATION_03 support a cautious "
                "power-to-water cascade response posture."
            ),
        },
        "recommended_actions": [
            {
                "action_id": "RESP-001",
                "category": "evidence_preservation",
                "priority": "critical",
                "action": "Preserve AstraGrid outputs, raw case files, and tool-run logs.",
                "reason": "Investigation conclusions are evidence-backed and must remain auditable.",
                "approval_required": False,
                "related_tools": ["all"],
            },
            {
                "action_id": "RESP-002",
                "category": "power_triage",
                "priority": "high",
                "action": "Verify POWER_SUBSTATION_01 status and review power-side event window.",
                "reason": "Power-grid evidence is confirmed and may explain downstream water impact.",
                "approval_required": False,
                "related_tools": [power.get("tool")],
                "tool_run_ids": [power.get("_tool_run_id")],
                "evidence_refs": power.get("evidence_refs", []),
            },
            {
                "action_id": "RESP-003",
                "category": "water_operations",
                "priority": "high",
                "action": "Notify water operations that the anomaly may be downstream cascade impact.",
                "reason": "Water evidence is confirmed, but direct water cyberattack is unsupported.",
                "approval_required": False,
                "related_tools": [water.get("tool")],
                "tool_run_ids": [water.get("_tool_run_id")],
                "evidence_refs": water.get("evidence_refs", []),
            },
            {
                "action_id": "RESP-004",
                "category": "network_monitoring",
                "priority": "medium",
                "action": "Increase monitoring on Modbus/TCP and OT network paths.",
                "reason": "Network attack indicators are present, but direct water command-path causation is not proven.",
                "approval_required": False,
                "related_tools": [network.get("tool")],
                "tool_run_ids": [network.get("_tool_run_id")],
                "evidence_refs": network.get("evidence_refs", []),
            },
            {
                "action_id": "RESP-005",
                "category": "endpoint_forensics",
                "priority": "high",
                "action": "Preserve and review endpoint evidence related to audit log clearing.",
                "reason": "Endpoint defense-evasion evidence is confirmed.",
                "approval_required": False,
                "related_tools": [endpoint.get("tool")],
                "tool_run_ids": [endpoint.get("_tool_run_id")],
                "evidence_refs": endpoint.get("evidence_refs", []),
            },
            {
                "action_id": "RESP-006",
                "category": "dependency_coordination",
                "priority": "high",
                "action": "Coordinate power and water teams around the dependency path POWER_SUBSTATION_01 to WATER_PUMP_STATION_03.",
                "reason": "Dependency graph confirms that the power asset supplies the water pump station.",
                "approval_required": False,
                "related_tools": [dependency.get("tool")],
                "tool_run_ids": [dependency.get("_tool_run_id")],
            },
        ],
        "human_approval_required": [
            {
                "action": "Isolate endpoint workstation from production networks.",
                "reason": "Could affect operations and requires owner approval.",
            },
            {
                "action": "Change firewall or OT network rules.",
                "reason": "Could disrupt industrial communications.",
            },
            {
                "action": "Modify PLC, SCADA, pump, valve, or substation operations.",
                "reason": "Physical process impact requires human operator approval.",
            },
            {
                "action": "Declare direct water cyberattack attribution.",
                "reason": "Current evidence does not support this claim.",
            },
        ],
        "actions_not_recommended": [
            {
                "action": "Do not claim attacker country attribution.",
                "reason": "No threat-intelligence or attribution evidence is loaded.",
            },
            {
                "action": "Do not classify the case as proven direct water cyberattack.",
                "reason": "No direct PLC or SCADA water command path is proven.",
            },
            {
                "action": "Do not perform automatic shutdown of water or power infrastructure.",
                "reason": "High-impact physical actions require human approval.",
            },
        ],
        "response_summary": (
            "AstraGrid recommends a cautious cascade response: preserve evidence, "
            "verify power-side impact, notify water operations, monitor OT network activity, "
            "review endpoint defense evasion, and require human approval before disruptive actions."
        ),
    }


def build_response_plan_markdown(response_plan: Dict[str, Any]) -> str:
    lines = []

    lines.append("# AstraGrid Autonomous Response Plan")
    lines.append("")
    lines.append(f"Response plan ID: {response_plan.get('response_plan_id')}")
    lines.append(f"Case ID: {response_plan.get('case_id')}")
    lines.append(f"Generated at: {response_plan.get('generated_at')}")
    lines.append(f"Response mode: {response_plan.get('response_mode')}")
    lines.append("")
    lines.append("## Automation Boundary")
    lines.append("")
    lines.append(response_plan.get("automation_boundary", ""))
    lines.append("")
    lines.append("## Key Reasoning")
    lines.append("")
    reasoning = response_plan.get("key_reasoning", {})
    for key, value in reasoning.items():
        lines.append(f"- **{key}**: {value}")
    lines.append("")
    lines.append("## Recommended Safe Actions")
    lines.append("")

    for action in response_plan.get("recommended_actions", []):
        lines.append(f"### {action.get('action_id')} — {action.get('category')}")
        lines.append(f"- Priority: {action.get('priority')}")
        lines.append(f"- Action: {action.get('action')}")
        lines.append(f"- Reason: {action.get('reason')}")
        lines.append(f"- Approval required: {action.get('approval_required')}")
        if action.get("tool_run_ids"):
            lines.append(f"- Tool run IDs: {action.get('tool_run_ids')}")
        if action.get("evidence_refs"):
            lines.append(f"- Evidence refs: {action.get('evidence_refs')}")
        lines.append("")

    lines.append("## Human Approval Required")
    lines.append("")
    for item in response_plan.get("human_approval_required", []):
        lines.append(f"- {item.get('action')} — {item.get('reason')}")
    lines.append("")

    lines.append("## Actions Not Recommended")
    lines.append("")
    for item in response_plan.get("actions_not_recommended", []):
        lines.append(f"- {item.get('action')} — {item.get('reason')}")
    lines.append("")

    lines.append("## Response Summary")
    lines.append("")
    lines.append(response_plan.get("response_summary", ""))

    return "\n".join(lines)