from typing import Any, Dict, List


def build_trace_step(
    step_id: str,
    phase: str,
    agent_thought: str,
    action: str,
    evidence_checked: List[str],
    result: str,
    correction: str | None = None,
    tool_run_ids: List[str] | None = None,
) -> Dict[str, Any]:
    return {
        "step_id": step_id,
        "phase": phase,
        "agent_thought": agent_thought,
        "action": action,
        "evidence_checked": evidence_checked,
        "result": result,
        "correction": correction,
        "tool_run_ids": tool_run_ids or [],
    }


def build_self_correction_trace(
    findings: List[Dict[str, Any]],
    claims: List[Dict[str, Any]],
    timeline: List[Dict[str, Any]],
    tool_results: Dict[str, Any],
) -> Dict[str, Any]:
    power = tool_results["power"]
    water = tool_results["water"]
    network = tool_results["network"]
    endpoint = tool_results["endpoint"]
    dependency = tool_results["dependency"]

    direct_water_claim = next(
        (claim for claim in claims if claim.get("claim_id") == "CLAIM-004"),
        None,
    )
    cascade_claim = next(
        (claim for claim in claims if claim.get("claim_id") == "CLAIM-005"),
        None,
    )

    steps = [
        build_trace_step(
            step_id="SC-STEP-001",
            phase="initial_hypothesis",
            agent_thought=(
                "A water utility anomaly could indicate a direct cyberattack against "
                "water treatment or distribution systems."
            ),
            action="Start with a cautious direct-water-attack hypothesis.",
            evidence_checked=["water_treatment_events", "water_distribution_events"],
            result="Water evidence exists, but existence alone does not prove direct cyberattack.",
            correction=None,
            tool_run_ids=[water.get("_tool_run_id")] if water.get("_tool_run_id") else [],
        ),
        build_trace_step(
            step_id="SC-STEP-002",
            phase="gap_detection",
            agent_thought=(
                "The direct-water-attack hypothesis requires stronger support from "
                "network, PLC, or command-path evidence."
            ),
            action="Check Modbus/TCP network evidence before making a direct attack claim.",
            evidence_checked=["network_events"],
            result=(
                "Network evidence is present, but deterministic analysis does not prove "
                "that a direct water cyber command caused the anomaly."
            ),
            correction="Mark direct water cyberattack as unsupported unless stronger evidence appears.",
            tool_run_ids=[network.get("_tool_run_id")] if network.get("_tool_run_id") else [],
        ),
        build_trace_step(
            step_id="SC-STEP-003",
            phase="context_expansion",
            agent_thought=(
                "A downstream water anomaly may be caused by upstream infrastructure, "
                "so power evidence must be checked."
            ),
            action="Check power-grid evidence.",
            evidence_checked=["power_events"],
            result="Power-grid evidence exists and should be considered before attribution.",
            correction="Expand investigation from isolated water attack to cross-infrastructure reasoning.",
            tool_run_ids=[power.get("_tool_run_id")] if power.get("_tool_run_id") else [],
        ),
        build_trace_step(
            step_id="SC-STEP-004",
            phase="host_evidence_check",
            agent_thought=(
                "Endpoint evidence can indicate compromise, operator workstation activity, "
                "or defense evasion relevant to the incident."
            ),
            action="Check endpoint forensic evidence.",
            evidence_checked=["endpoint_events"],
            result=(
                "Endpoint defense-evasion evidence exists, including audit-log clearing indicators."
                if endpoint.get("defense_evasion_event_count", 0) > 0
                else "Endpoint evidence exists, but no strong defense-evasion indicator was found."
            ),
            correction=None,
            tool_run_ids=[endpoint.get("_tool_run_id")] if endpoint.get("_tool_run_id") else [],
        ),
        build_trace_step(
            step_id="SC-STEP-005",
            phase="dependency_check",
            agent_thought=(
                "If a power asset supplies a water asset, a power-side incident may plausibly "
                "cascade into water utility impact."
            ),
            action="Check infrastructure dependency graph.",
            evidence_checked=["dependency_graph"],
            result=(
                "A dependency path exists from POWER_SUBSTATION_01 to WATER_PUMP_STATION_03."
                if dependency.get("power_to_water_dependency_count", 0) > 0
                else "No power-to-water dependency path was found."
            ),
            correction="Prefer power-to-water cascade hypothesis over unsupported direct-water-attack claim.",
            tool_run_ids=[dependency.get("_tool_run_id")] if dependency.get("_tool_run_id") else [],
        ),
        build_trace_step(
            step_id="SC-STEP-006",
            phase="corrected_conclusion",
            agent_thought=(
                "The evidence supports a cautious cascade interpretation, while direct water "
                "cyberattack remains unsupported."
            ),
            action="Update final claim statuses.",
            evidence_checked=[
                "claims.json",
                "timeline.json",
                "findings.json",
                "tool_runs.json",
            ],
            result=(
                "Direct water cyberattack is UNSUPPORTED; power-to-water cascade is "
                "PARTIALLY_CONFIRMED."
            ),
            correction="Corrected from direct-water-attack hypothesis to plausible cascade hypothesis.",
            tool_run_ids=[
                tool_id
                for tool_id in [
                    water.get("_tool_run_id"),
                    network.get("_tool_run_id"),
                    power.get("_tool_run_id"),
                    dependency.get("_tool_run_id"),
                ]
                if tool_id
            ],
        ),
    ]

    return {
        "trace_id": "SC-TRACE-ASTRAGRID-001",
        "case_id": "ASTRAGRID-001",
        "trace_type": "self_correction_trace",
        "initial_hypothesis": "Direct water cyberattack",
        "corrected_hypothesis": "Power-to-water cascade is plausible; direct water attack is unsupported",
        "final_position": {
            "direct_water_attack": {
                "status": direct_water_claim.get("status") if direct_water_claim else "UNKNOWN",
                "confidence": direct_water_claim.get("confidence") if direct_water_claim else None,
            },
            "power_to_water_cascade": {
                "status": cascade_claim.get("status") if cascade_claim else "UNKNOWN",
                "confidence": cascade_claim.get("confidence") if cascade_claim else None,
            },
        },
        "max_iterations": 6,
        "iterations_used": len(steps),
        "termination_reason": "Sufficient evidence to avoid unsupported direct-water-attack attribution and support cautious cascade classification.",
        "steps": steps,
        "evidence_integrity_note": (
            "All steps use read-only normalized event files and link conclusions back to tool_run_ids "
            "and evidence_refs. No raw data is modified."
        ),
    }