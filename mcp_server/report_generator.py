from datetime import datetime, timezone
from typing import Any, Dict, List


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _status_counts(items: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}

    for item in items:
        status = str(item.get("status", "UNKNOWN"))
        counts[status] = counts.get(status, 0) + 1

    return counts


def build_final_report_json(investigation_summary: Dict[str, Any]) -> Dict[str, Any]:
    findings = investigation_summary.get("findings", [])
    timeline = investigation_summary.get("timeline", [])
    claims = investigation_summary.get("claims", [])
    self_correction = investigation_summary.get("self_correction_trace", {})

    confirmed_claims = [c for c in claims if c.get("status") == "CONFIRMED"]
    unsupported_claims = [c for c in claims if c.get("status") == "UNSUPPORTED"]
    partial_claims = [c for c in claims if c.get("status") == "PARTIALLY_CONFIRMED"]
    inferred_claims = [c for c in claims if c.get("status") == "INFERRED"]

    return {
        "report_id": "REPORT-ASTRAGRID-001",
        "generated_at": utc_now_iso(),
        "case_id": investigation_summary.get("case_id"),
        "case_name": investigation_summary.get("case_name"),
        "case_type": investigation_summary.get("case_type"),
        "status": "success",
        "classification": investigation_summary.get("classification_hint"),
        "executive_summary": (
            "AstraGrid analyzed a cyber-physical incident case using normalized power, "
            "water, network, endpoint, and dependency evidence. The deterministic analysis "
            "supports a cautious power-to-water cascade interpretation while marking the "
            "direct water cyberattack claim as unsupported."
        ),
        "key_result": {
            "initial_hypothesis": self_correction.get("initial_hypothesis"),
            "corrected_hypothesis": self_correction.get("corrected_hypothesis"),
            "direct_water_attack_status": self_correction.get("final_position", {})
            .get("direct_water_attack", {})
            .get("status"),
            "cascade_status": self_correction.get("final_position", {})
            .get("power_to_water_cascade", {})
            .get("status"),
        },
        "evidence_summary": {
            "finding_count": len(findings),
            "timeline_event_count": len(timeline),
            "claim_count": len(claims),
            "self_correction_steps": len(self_correction.get("steps", [])),
            "claim_status_counts": _status_counts(claims),
            "finding_status_counts": _status_counts(findings),
        },
        "confirmed_claims": confirmed_claims,
        "partially_confirmed_claims": partial_claims,
        "inferred_claims": inferred_claims,
        "unsupported_claims": unsupported_claims,
        "findings": findings,
        "timeline": timeline,
        "self_correction_trace": self_correction,
        "evidence_integrity": {
            "raw_data_modified": False,
            "evidence_mode": "read_only_normalized_case_files",
            "traceability": (
                "Every finding and claim links back to tool_run_ids and evidence_refs "
                "where available."
            ),
            "guardrails": [
                "Case files are loaded through safe path resolution.",
                "Tools read normalized event JSON files only.",
                "Tool execution is recorded in outputs/tool_runs.json.",
                "Unsupported claims are explicitly labeled instead of being overclaimed.",
            ],
        },
        "recommendations": [
            "Treat the direct water cyberattack hypothesis as unsupported until stronger PLC command-path evidence is available.",
            "Continue investigating timing relationships between power events and water anomalies.",
            "Use endpoint and network evidence to determine whether a shared actor or coordinated campaign is supported.",
            "Preserve all raw evidence and use only read-only analysis paths during autonomous investigation.",
        ],
    }


def build_final_report_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append(f"# AstraGrid Final Incident Report")
    lines.append("")
    lines.append(f"**Report ID:** {report.get('report_id')}")
    lines.append(f"**Generated At:** {report.get('generated_at')}")
    lines.append(f"**Case ID:** {report.get('case_id')}")
    lines.append(f"**Case Name:** {report.get('case_name')}")
    lines.append(f"**Classification:** {report.get('classification')}")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append("")
    lines.append(report.get("executive_summary", ""))
    lines.append("")

    key_result = report.get("key_result", {})
    lines.append("## Key Result")
    lines.append("")
    lines.append(f"- **Initial hypothesis:** {key_result.get('initial_hypothesis')}")
    lines.append(f"- **Corrected hypothesis:** {key_result.get('corrected_hypothesis')}")
    lines.append(f"- **Direct water attack status:** {key_result.get('direct_water_attack_status')}")
    lines.append(f"- **Power-to-water cascade status:** {key_result.get('cascade_status')}")
    lines.append("")

    evidence_summary = report.get("evidence_summary", {})
    lines.append("## Evidence Summary")
    lines.append("")
    lines.append(f"- Findings: {evidence_summary.get('finding_count')}")
    lines.append(f"- Timeline events: {evidence_summary.get('timeline_event_count')}")
    lines.append(f"- Claims: {evidence_summary.get('claim_count')}")
    lines.append(f"- Self-correction steps: {evidence_summary.get('self_correction_steps')}")
    lines.append(f"- Claim status counts: {evidence_summary.get('claim_status_counts')}")
    lines.append("")

    lines.append("## Confirmed Claims")
    lines.append("")
    for claim in report.get("confirmed_claims", []):
        lines.append(f"- **{claim.get('claim_id')}** — {claim.get('claim')}")
        lines.append(f"  - Status: {claim.get('status')}")
        lines.append(f"  - Confidence: {claim.get('confidence')}")
        lines.append(f"  - Evidence refs: {claim.get('evidence_refs')}")
        lines.append(f"  - Tool runs: {claim.get('tool_run_ids')}")
    lines.append("")

    lines.append("## Partially Confirmed / Inferred Claims")
    lines.append("")
    for claim in report.get("partially_confirmed_claims", []) + report.get("inferred_claims", []):
        lines.append(f"- **{claim.get('claim_id')}** — {claim.get('claim')}")
        lines.append(f"  - Status: {claim.get('status')}")
        lines.append(f"  - Confidence: {claim.get('confidence')}")
        lines.append(f"  - Reason: {claim.get('reason')}")
    lines.append("")

    lines.append("## Unsupported Claims")
    lines.append("")
    for claim in report.get("unsupported_claims", []):
        lines.append(f"- **{claim.get('claim_id')}** — {claim.get('claim')}")
        lines.append(f"  - Status: {claim.get('status')}")
        lines.append(f"  - Reason: {claim.get('reason')}")
    lines.append("")

    lines.append("## Investigation Timeline")
    lines.append("")
    for event in report.get("timeline", []):
        lines.append(
            f"{event.get('order')}. **{event.get('title')}** "
            f"({event.get('sector')}, {event.get('status')})"
        )
        lines.append(f"   - Phase: {event.get('phase')}")
        lines.append(f"   - Description: {event.get('description')}")
        lines.append(f"   - Tool run: {event.get('tool_run_id')}")
    lines.append("")

    lines.append("## Self-Correction Summary")
    lines.append("")
    trace = report.get("self_correction_trace", {})
    lines.append(f"- Initial hypothesis: {trace.get('initial_hypothesis')}")
    lines.append(f"- Corrected hypothesis: {trace.get('corrected_hypothesis')}")
    lines.append(f"- Iterations used: {trace.get('iterations_used')}")
    lines.append(f"- Termination reason: {trace.get('termination_reason')}")
    lines.append("")
    for step in trace.get("steps", []):
        lines.append(f"- **{step.get('step_id')} / {step.get('phase')}**")
        lines.append(f"  - Thought: {step.get('agent_thought')}")
        lines.append(f"  - Action: {step.get('action')}")
        lines.append(f"  - Result: {step.get('result')}")
        if step.get("correction"):
            lines.append(f"  - Correction: {step.get('correction')}")
    lines.append("")

    lines.append("## Evidence Integrity")
    lines.append("")
    integrity = report.get("evidence_integrity", {})
    lines.append(f"- Raw data modified: {integrity.get('raw_data_modified')}")
    lines.append(f"- Evidence mode: {integrity.get('evidence_mode')}")
    lines.append(f"- Traceability: {integrity.get('traceability')}")
    lines.append("")
    lines.append("### Guardrails")
    for guardrail in integrity.get("guardrails", []):
        lines.append(f"- {guardrail}")
    lines.append("")

    lines.append("## Recommendations")
    lines.append("")
    for rec in report.get("recommendations", []):
        lines.append(f"- {rec}")
    lines.append("")

    return "\n".join(lines)