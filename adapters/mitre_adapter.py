import json
from pathlib import Path
from typing import Dict, List, Any, Optional


ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = ROOT / "configs" / "column_maps" / "mitre_attack.json"
OUTPUT_PATH = ROOT / "data" / "processed" / "mitre_techniques.json"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_stix_objects(file_path: Path) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("objects", [])


def get_technique_id(obj: Dict[str, Any]) -> Optional[str]:
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack" and ref.get("external_id"):
            return ref.get("external_id")
    return None


def get_tactics(obj: Dict[str, Any]) -> List[str]:
    phases = obj.get("kill_chain_phases", [])
    return [phase.get("phase_name") for phase in phases if phase.get("phase_name")]


def normalize_technique(obj: Dict[str, Any], domain: str) -> Optional[Dict[str, Any]]:
    if obj.get("type") != "attack-pattern":
        return None

    if obj.get("revoked") is True or obj.get("x_mitre_deprecated") is True:
        return None

    technique_id = get_technique_id(obj)

    if not technique_id:
        return None

    return {
        "technique_id": technique_id,
        "name": obj.get("name"),
        "domain": domain,
        "tactics": get_tactics(obj),
        "description": obj.get("description", ""),
        "platforms": obj.get("x_mitre_platforms", []),
        "is_subtechnique": obj.get("x_mitre_is_subtechnique", False),
        "mitre_version": obj.get("x_mitre_version"),
        "stix_id": obj.get("id"),
    }


def extract_domain_techniques(file_path: Path, domain: str) -> List[Dict[str, Any]]:
    objects = load_stix_objects(file_path)
    techniques = []

    for obj in objects:
        normalized = normalize_technique(obj, domain)
        if normalized:
            techniques.append(normalized)

    return techniques


def main():
    config = load_config()

    raw_folder = ROOT / config["raw_folder"]

    ics_file = raw_folder / config["files"]["ics"]
    enterprise_file = raw_folder / config["files"]["enterprise"]

    if not ics_file.exists():
        raise FileNotFoundError(f"MITRE ICS file not found: {ics_file}")

    if not enterprise_file.exists():
        raise FileNotFoundError(f"MITRE Enterprise file not found: {enterprise_file}")

    print(f"Reading MITRE ICS: {ics_file}")
    ics_techniques = extract_domain_techniques(ics_file, domain="ics")

    print(f"Reading MITRE Enterprise: {enterprise_file}")
    enterprise_techniques = extract_domain_techniques(enterprise_file, domain="enterprise")

    all_techniques = ics_techniques + enterprise_techniques

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_techniques, f, indent=2)

    print(f"ICS techniques: {len(ics_techniques)}")
    print(f"Enterprise techniques: {len(enterprise_techniques)}")
    print(f"Total techniques saved: {len(all_techniques)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()