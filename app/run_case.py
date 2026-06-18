import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from mcp_server.tools import (
    get_case_manifest,
    get_power_event_summary,
    get_water_event_summary,
    get_network_attack_evidence,
    get_endpoint_evidence,
    get_dependency_summary,
)
from mcp_server.timeline_builder import build_case_timeline
from mcp_server.claim_validator import validate_case_claims
from mcp_server.self_correction import build_self_correction_trace
from mcp_server.case_loader import load_ground_truth
from storage.tool_run_logger import run_logged_tool
from mcp_server.report_generator import (
    build_final_report_json,
    build_final_report_markdown,
)
from mcp_server.accuracy_report import (
    build_accuracy_report_json,
    build_accuracy_report_markdown,
)
from mcp_server.response_planner import (
    build_response_plan,
    build_response_plan_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT / "outputs"

FINDINGS_PATH = OUTPUTS_DIR / "findings.json"
TIMELINE_PATH = OUTPUTS_DIR / "timeline.json"
CLAIMS_PATH = OUTPUTS_DIR / "claims.json"
SELF_CORRECTION_PATH = OUTPUTS_DIR / "self_correction_trace.json"
FINAL_REPORT_JSON_PATH = OUTPUTS_DIR / "final_report.json"
FINAL_REPORT_MD_PATH = OUTPUTS_DIR / "final_report.md"
ACCURACY_REPORT_JSON_PATH = OUTPUTS_DIR / "accuracy_report.json"
ACCURACY_REPORT_MD_PATH = OUTPUTS_DIR / "accuracy_report.md"
RESPONSE_PLAN_JSON_PATH = OUTPUTS_DIR / "response_plan.json"
RESPONSE_PLAN_MD_PATH = OUTPUTS_DIR / "response_plan.md"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build_finding_record(
    finding_id: str,
    source_tool_result: Dict[str, Any],
    title: str,
    claim: str,
    status: str,
    confidence: float,
) -> Dict[str, Any]:
    return {
        "finding_id": finding_id,
        "title": title,
        "claim": claim,
        "status": status,
        "confidence": confidence,
        "source_tool": source_tool_result.get("tool"),
        "tool_run_id": source_tool_result.get("_tool_run_id"),
        "sector": source_tool_result.get("sector"),
        "finding": source_tool_result.get("finding"),
        "evidence_refs": source_tool_result.get("evidence_refs", []),
        "summary": {
            key: value
            for key, value in source_tool_result.items()
            if key
            in [
                "total_events",
                "attack_event_count",
                "natural_event_count",
                "normal_event_count",
                "water_anomaly_event_count",
                "high_severity_event_count",
                "defense_evasion_event_count",
                "power_to_water_dependency_count",
            ]
        },
    }


def run_case(case_dir: str = "data/sample_case_power_water_cascade") -> Dict[str, Any]:
    started_at = utc_now_iso()

    manifest = run_logged_tool(
        "get_case_manifest",
        get_case_manifest,
        case_dir,
        input_summary={"case_dir": case_dir},
    )

    power = run_logged_tool(
        "get_power_event_summary",
        get_power_event_summary,
        case_dir,
        input_summary={"case_dir": case_dir, "file_key": "power_events"},
    )

    water = run_logged_tool(
        "get_water_event_summary",
        get_water_event_summary,
        case_dir,
        input_summary={
            "case_dir": case_dir,
            "file_keys": ["water_treatment_events", "water_distribution_events"],
        },
    )

    network = run_logged_tool(
        "get_network_attack_evidence",
        get_network_attack_evidence,
        case_dir,
        input_summary={"case_dir": case_dir, "file_key": "network_events"},
    )

    endpoint = run_logged_tool(
        "get_endpoint_evidence",
        get_endpoint_evidence,
        case_dir,
        input_summary={"case_dir": case_dir, "file_key": "endpoint_events"},
    )

    dependency = run_logged_tool(
        "get_dependency_summary",
        get_dependency_summary,
        case_dir,
        input_summary={"case_dir": case_dir, "file_key": "dependency_graph"},
    )

    tool_results = {
        "manifest": manifest,
        "power": power,
        "water": water,
        "network": network,
        "endpoint": endpoint,
        "dependency": dependency,
    }

    findings: List[Dict[str, Any]] = [
        build_finding_record(
            finding_id="FIND-PWR-001",
            source_tool_result=power,
            title="Power evidence summary",
            claim="Power-grid evidence exists and must be evaluated before attributing downstream water impact.",
            status="CONFIRMED" if power.get("total_events", 0) > 0 else "UNSUPPORTED",
            confidence=0.75,
        ),
        build_finding_record(
            finding_id="FIND-WTR-001",
            source_tool_result=water,
            title="Water evidence summary",
            claim="Water utility operational evidence exists and must be checked for anomaly or attack indicators.",
            status="CONFIRMED" if water.get("total_events", 0) > 0 else "UNSUPPORTED",
            confidence=0.75,
        ),
        build_finding_record(
            finding_id="FIND-NET-001",
            source_tool_result=network,
            title="Network / Modbus evidence summary",
            claim="Network evidence is available to evaluate whether direct PLC or Modbus attack activity is supported.",
            status="CONFIRMED" if network.get("total_events", 0) > 0 else "UNSUPPORTED",
            confidence=0.72,
        ),
        build_finding_record(
            finding_id="FIND-END-001",
            source_tool_result=endpoint,
            title="Endpoint forensic evidence summary",
            claim="Endpoint evidence contains host-level activity relevant to the incident investigation.",
            status="CONFIRMED"
            if endpoint.get("defense_evasion_event_count", 0) > 0
            else "PARTIALLY_CONFIRMED",
            confidence=0.82
            if endpoint.get("defense_evasion_event_count", 0) > 0
            else 0.60,
        ),
        build_finding_record(
            finding_id="FIND-DEP-001",
            source_tool_result=dependency,
            title="Power-to-water dependency summary",
            claim="A dependency path exists from a power asset to a water utility asset.",
            status="CONFIRMED"
            if dependency.get("power_to_water_dependency_count", 0) > 0
            else "UNSUPPORTED",
            confidence=0.88
            if dependency.get("power_to_water_dependency_count", 0) > 0
            else 0.30,
        ),
    ]

    timeline = build_case_timeline(tool_results)
    claims = validate_case_claims(findings, tool_results)

    self_correction_trace = build_self_correction_trace(
        findings=findings,
        claims=claims,
        timeline=timeline,
        tool_results=tool_results,
    )

    response_plan = build_response_plan(
        findings=findings,
        claims=claims,
        tool_results=tool_results,
    )

    response_plan_md = build_response_plan_markdown(response_plan)

    investigation_summary = {
        "case_id": manifest.get("case_id"),
        "case_name": manifest.get("case_name"),
        "case_type": manifest.get("case_type"),
        "started_at": started_at,
        "completed_at": utc_now_iso(),
        "status": "success",
        "classification_hint": "POWER_TO_WATER_CASCADE"
        if dependency.get("power_to_water_dependency_count", 0) > 0
        else "INSUFFICIENT_EVIDENCE",
        "tool_results": tool_results,
        "findings": findings,
        "timeline": timeline,
        "claims": claims,
        "self_correction_trace": self_correction_trace,
        "response_plan": response_plan,
        "notes": [
            "This is a deterministic local case run.",
            "Each finding is linked to the tool run that produced it.",
            "This is not yet the final autonomous Protocol SIFT run.",
        ],
    }

    final_report = build_final_report_json(investigation_summary)
    final_report_md = build_final_report_markdown(final_report)

    ground_truth = load_ground_truth(case_dir)
    accuracy_report = build_accuracy_report_json(
        ground_truth=ground_truth,
        claims=claims,
        final_report=final_report,
    )
    accuracy_report_md = build_accuracy_report_markdown(accuracy_report)

    investigation_summary["final_report"] = final_report
    investigation_summary["accuracy_report"] = accuracy_report

    save_json(FINDINGS_PATH, investigation_summary)
    save_json(TIMELINE_PATH, timeline)
    save_json(CLAIMS_PATH, claims)
    save_json(SELF_CORRECTION_PATH, self_correction_trace)
    save_json(FINAL_REPORT_JSON_PATH, final_report)
    save_text(FINAL_REPORT_MD_PATH, final_report_md)
    save_json(ACCURACY_REPORT_JSON_PATH, accuracy_report)
    save_text(ACCURACY_REPORT_MD_PATH, accuracy_report_md)
    save_json(RESPONSE_PLAN_JSON_PATH, response_plan)
    save_text(RESPONSE_PLAN_MD_PATH, response_plan_md)

    return investigation_summary


def main():
    result = run_case()

    print("[OK] Case run completed")
    print(f"[OK] Findings saved to: {FINDINGS_PATH}")
    print(f"[OK] Timeline saved to: {TIMELINE_PATH}")
    print(f"[OK] Claims saved to: {CLAIMS_PATH}")
    print(f"[OK] Self-correction trace saved to: {SELF_CORRECTION_PATH}")
    print(f"[OK] Final report JSON saved to: {FINAL_REPORT_JSON_PATH}")
    print(f"[OK] Final report Markdown saved to: {FINAL_REPORT_MD_PATH}")
    print(f"[OK] Accuracy report JSON saved to: {ACCURACY_REPORT_JSON_PATH}")
    print(f"[OK] Accuracy report Markdown saved to: {ACCURACY_REPORT_MD_PATH}")
    print(f"✅ Response plan JSON saved to: {RESPONSE_PLAN_JSON_PATH}")
    print(f"✅ Response plan Markdown saved to: {RESPONSE_PLAN_MD_PATH}")

    print(f"Case: {result['case_id']} - {result['case_name']}")
    print(f"Classification hint: {result['classification_hint']}")
    print(f"Findings: {len(result['findings'])}")
    print(f"Timeline events: {len(result['timeline'])}")
    print(f"Claims: {len(result['claims'])}")
    print(f"Self-correction steps: {len(result['self_correction_trace']['steps'])}")
    print(f"Response actions: {len(result['response_plan']['recommended_actions'])}")

    accuracy = result["accuracy_report"]["summary"]["accuracy"]
    print(f"Accuracy: {accuracy}")

    for finding in result["findings"]:
        print(
            f"- {finding['finding_id']} | {finding['status']} | "
            f"{finding['title']} | tool_run={finding['tool_run_id']}"
        )


if __name__ == "__main__":
    main()