from typing import Any, Dict, List


def build_claim(
    claim_id: str,
    claim: str,
    status: str,
    confidence: float,
    reason: str,
    evidence_refs: List[str] | None = None,
    tool_run_ids: List[str] | None = None,
    related_findings: List[str] | None = None,
) -> Dict[str, Any]:
    return {
        "claim_id": claim_id,
        "claim": claim,
        "status": status,
        "confidence": confidence,
        "reason": reason,
        "evidence_refs": evidence_refs or [],
        "tool_run_ids": tool_run_ids or [],
        "related_findings": related_findings or [],
    }


def validate_case_claims(
    findings: List[Dict[str, Any]],
    tool_results: Dict[str, Any],
) -> List[Dict[str, Any]]:
    power = tool_results["power"]
    water = tool_results["water"]
    network = tool_results["network"]
    endpoint = tool_results["endpoint"]
    dependency = tool_results["dependency"]

    power_has_events = power.get("total_events", 0) > 0
    water_has_events = water.get("total_events", 0) > 0
    network_has_direct_attack = network.get("attack_event_count", 0) > 0
    endpoint_has_evasion = endpoint.get("defense_evasion_event_count", 0) > 0
    power_to_water_dependency = dependency.get("power_to_water_dependency_count", 0) > 0

    claims = [
        build_claim(
            claim_id="CLAIM-001",
            claim="Power-grid evidence exists in the case.",
            status="CONFIRMED" if power_has_events else "UNSUPPORTED",
            confidence=0.85 if power_has_events else 0.2,
            reason=(
                "The power evidence tool loaded normalized power events from the case."
                if power_has_events
                else "No normalized power events were loaded."
            ),
            evidence_refs=power.get("evidence_refs", []) or power.get("sample_refs", []),
            tool_run_ids=[power.get("_tool_run_id")] if power.get("_tool_run_id") else [],
            related_findings=["FIND-PWR-001"],
        ),
        build_claim(
            claim_id="CLAIM-002",
            claim="Water utility evidence exists in the case.",
            status="CONFIRMED" if water_has_events else "UNSUPPORTED",
            confidence=0.85 if water_has_events else 0.2,
            reason=(
                "The water evidence tool loaded normalized water-treatment and water-distribution events."
                if water_has_events
                else "No normalized water events were loaded."
            ),
            evidence_refs=water.get("evidence_refs", []) or water.get("sample_refs", []),
            tool_run_ids=[water.get("_tool_run_id")] if water.get("_tool_run_id") else [],
            related_findings=["FIND-WTR-001"],
        ),
        build_claim(
            claim_id="CLAIM-003",
            claim="Endpoint defense-evasion evidence exists.",
            status="CONFIRMED" if endpoint_has_evasion else "UNSUPPORTED",
            confidence=0.88 if endpoint_has_evasion else 0.3,
            reason=(
                "Endpoint evidence includes defense-evasion indicators such as audit log clearing."
                if endpoint_has_evasion
                else "Endpoint evidence did not contain defense-evasion indicators."
            ),
            evidence_refs=endpoint.get("evidence_refs", []),
            tool_run_ids=[endpoint.get("_tool_run_id")] if endpoint.get("_tool_run_id") else [],
            related_findings=["FIND-END-001"],
        ),
        build_claim(
            claim_id="CLAIM-004",
            claim="Direct water cyberattack is proven.",
            status="UNSUPPORTED",
            confidence=0.25,
            reason=(
                "The case contains water evidence and network evidence, but the current deterministic analysis "
                "does not independently prove that a direct cyber command caused the water anomaly. "
                "The agent should avoid overclaiming direct water attack."
            ),
            evidence_refs=network.get("evidence_refs", []),
            tool_run_ids=[
                tool_id
                for tool_id in [water.get("_tool_run_id"), network.get("_tool_run_id")]
                if tool_id
            ],
            related_findings=["FIND-WTR-001", "FIND-NET-001"],
        ),
        build_claim(
            claim_id="CLAIM-005",
            claim="A power-to-water cascade is plausible.",
            status="PARTIALLY_CONFIRMED"
            if power_has_events and water_has_events and power_to_water_dependency
            else "UNSUPPORTED",
            confidence=0.82
            if power_has_events and water_has_events and power_to_water_dependency
            else 0.35,
            reason=(
                "Power evidence, water evidence, and a dependency path from power to water are present. "
                "This supports a plausible cascade hypothesis, while direct causation still requires stronger temporal proof."
                if power_has_events and water_has_events and power_to_water_dependency
                else "Required power, water, or dependency evidence is missing."
            ),
            evidence_refs=(
                (power.get("evidence_refs", []) or power.get("sample_refs", [])[:3])
                + (water.get("evidence_refs", []) or water.get("sample_refs", [])[:3])
            ),
            tool_run_ids=[
                tool_id
                for tool_id in [
                    power.get("_tool_run_id"),
                    water.get("_tool_run_id"),
                    dependency.get("_tool_run_id"),
                ]
                if tool_id
            ],
            related_findings=["FIND-PWR-001", "FIND-WTR-001", "FIND-DEP-001"],
        ),
        build_claim(
            claim_id="CLAIM-006",
            claim="The case should be classified as a coordinated multi-sector attack.",
            status="INFERRED" if network_has_direct_attack and endpoint_has_evasion else "UNSUPPORTED",
            confidence=0.55 if network_has_direct_attack and endpoint_has_evasion else 0.25,
            reason=(
                "Network attack evidence and endpoint defense-evasion evidence are both present, but coordination "
                "requires stronger shared actor, timing, or command-path evidence."
                if network_has_direct_attack and endpoint_has_evasion
                else "Available evidence is insufficient to classify this as a coordinated multi-sector attack."
            ),
            evidence_refs=(network.get("evidence_refs", []) + endpoint.get("evidence_refs", []))[:10],
            tool_run_ids=[
                tool_id
                for tool_id in [network.get("_tool_run_id"), endpoint.get("_tool_run_id")]
                if tool_id
            ],
            related_findings=["FIND-NET-001", "FIND-END-001"],
        ),
    ]

    return claims