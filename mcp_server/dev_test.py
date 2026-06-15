import json

from mcp_server.tools import (
    get_case_manifest,
    get_power_event_summary,
    get_water_event_summary,
    get_network_attack_evidence,
    get_endpoint_evidence,
    get_dependency_summary,
)
from storage.tool_run_logger import run_logged_tool


def print_result(title, result):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(json.dumps(result, indent=2)[:4000])


def main():
    case_dir = "data/sample_case_power_water_cascade"

    print_result(
        "CASE MANIFEST",
        run_logged_tool(
            "get_case_manifest",
            get_case_manifest,
            case_dir,
            input_summary={"case_dir": case_dir},
        ),
    )

    print_result(
        "POWER SUMMARY",
        run_logged_tool(
            "get_power_event_summary",
            get_power_event_summary,
            case_dir,
            input_summary={"case_dir": case_dir, "file_key": "power_events"},
        ),
    )

    print_result(
        "WATER SUMMARY",
        run_logged_tool(
            "get_water_event_summary",
            get_water_event_summary,
            case_dir,
            input_summary={
                "case_dir": case_dir,
                "file_keys": ["water_treatment_events", "water_distribution_events"],
            },
        ),
    )

    print_result(
        "NETWORK EVIDENCE",
        run_logged_tool(
            "get_network_attack_evidence",
            get_network_attack_evidence,
            case_dir,
            input_summary={"case_dir": case_dir, "file_key": "network_events"},
        ),
    )

    print_result(
        "ENDPOINT EVIDENCE",
        run_logged_tool(
            "get_endpoint_evidence",
            get_endpoint_evidence,
            case_dir,
            input_summary={"case_dir": case_dir, "file_key": "endpoint_events"},
        ),
    )

    print_result(
        "DEPENDENCY SUMMARY",
        run_logged_tool(
            "get_dependency_summary",
            get_dependency_summary,
            case_dir,
            input_summary={"case_dir": case_dir, "file_key": "dependency_graph"},
        ),
    )

    print("\n✅ Local MCP tool foundation test completed successfully.")
    print("✅ Tool execution logs written to outputs/tool_runs.json")


if __name__ == "__main__":
    main()

