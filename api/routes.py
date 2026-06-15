from fastapi import APIRouter
import subprocess
import sys

from api.utils import (
    build_case_summary,
    output_json,
    output_markdown,
)


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "AstraGrid API",
        "version": "1.0.0",
    }


@router.post("/case/run")
def run_case():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "app.run_case"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "message": "Case run failed",
                "stderr": result.stderr,
                "stdout": result.stdout,
            }

        return {
            "status": "success",
            "message": "Case investigation completed",
            "stdout": result.stdout,
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Case run timed out",
        }

    except Exception as error:
        return {
            "status": "error",
            "message": "Could not run case investigation",
            "error": str(error),
        }


@router.get("/case/summary")
def case_summary():
    return build_case_summary()


@router.get("/case/findings")
def case_findings():
    data = output_json("findings.json")

    if isinstance(data, dict) and "findings" in data:
        return {
            "status": "success",
            "data": data["findings"],
            "summary": {
                "case_id": data.get("case_id"),
                "case_name": data.get("case_name"),
                "classification_hint": data.get("classification_hint"),
            },
        }

    return {
        "status": "success",
        "data": data,
    }
    


@router.get("/case/timeline")
def case_timeline():
    data = output_json("timeline.json")

    return {
        "status": "success",
        "count": len(data) if isinstance(data, list) else 0,
        "data": data,
        "summary": {
            "first_phase": data[0].get("phase") if isinstance(data, list) and data else None,
            "last_phase": data[-1].get("phase") if isinstance(data, list) and data else None,
            "has_corrected_hypothesis": any(
                item.get("phase") == "corrected_hypothesis"
                for item in data
            ) if isinstance(data, list) else False,
        },
    }


@router.get("/case/claims")
def case_claims():
    return {
        "status": "success",
        "data": output_json("claims.json"),
    }


@router.get("/case/self-correction")
def case_self_correction():
    data = output_json("self_correction_trace.json")

    return {
        "status": "success",
        "data": data,
        "summary": {
            "trace_id": data.get("trace_id") if isinstance(data, dict) else None,
            "initial_hypothesis": data.get("initial_hypothesis") if isinstance(data, dict) else None,
            "corrected_hypothesis": data.get("corrected_hypothesis") if isinstance(data, dict) else None,
            "steps": len(data.get("steps", [])) if isinstance(data, dict) else 0,
        },
    }


@router.get("/case/tool-runs")
def case_tool_runs():
    data = output_json("tool_runs.json")

    return {
        "status": "success",
        "count": len(data) if isinstance(data, list) else 0,
        "latest": data[-10:] if isinstance(data, list) else data,
        "data": data,
    }


@router.get("/case/reports/final")
def final_report():
    return {
        "status": "success",
        "json": output_json("final_report.json"),
        "markdown": output_markdown("final_report.md"),
    }


@router.get("/case/reports/accuracy")
def accuracy_report():
    return {
        "status": "success",
        "json": output_json("accuracy_report.json"),
        "markdown": output_markdown("accuracy_report.md"),
    }

@router.get("/case/threat-origin")
def case_threat_origin():
    findings = output_json("findings.json")
    dependency = findings.get("tool_results", {}).get("dependency", {})
    network = findings.get("tool_results", {}).get("network", {})

    network_evidence_refs = network.get("evidence_refs", [])

    return {
        "status": "success",
        "data": {
            "origin_type": "observed_network_and_infrastructure_path",
            "country_attribution": "not_claimed",
            "attribution_confidence": "not_applicable",
            "reason": (
                "AstraGrid does not infer attacker nationality from source IPs. "
                "Attackers may use VPNs, proxies, cloud hosts, compromised machines, "
                "or internal pivots. This route reports only observed origin indicators "
                "and infrastructure dependency paths supported by evidence."
            ),
            "observed_network_origin": {
                "source": "192.168.56.113",
                "destination": "192.168.56.112",
                "protocol": "TCP / Modbus",
                "signal": "observed Modbus/TCP network activity",
                "evidence_refs": network_evidence_refs,
                "source_tool": network.get("tool"),
                "tool_run_id": network.get("_tool_run_id"),
            },
            "infrastructure_path": {
                "from": "POWER_SUBSTATION_01",
                "to": "WATER_PUMP_STATION_03",
                "relationship": "supplies_power_to",
                "finding": dependency.get("finding"),
                "dependency_count": dependency.get("power_to_water_dependency_count"),
                "source_tool": dependency.get("tool"),
                "tool_run_id": dependency.get("_tool_run_id"),
            },
            "final_note": (
                "Observed origin is not attribution. AstraGrid separates evidence-backed "
                "network/infrastructure paths from unsupported actor or country claims."
            ),
        },
    }