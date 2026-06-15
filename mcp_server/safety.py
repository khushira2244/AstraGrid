from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASE_DIR = ROOT / "data" / "sample_case_power_water_cascade"


class SafetyError(Exception):
    """Raised when a path or operation violates AstraGrid read-only safety rules."""


def resolve_case_path(case_dir: str | None = None) -> Path:
    """
    Resolve the case directory safely.

    Rules:
    - Default case is data/sample_case_power_water_cascade
    - Path must exist
    - Path must stay inside the AstraGrid project folder
    """
    target = Path(case_dir) if case_dir else DEFAULT_CASE_DIR
    target = target.resolve()

    root = ROOT.resolve()

    if root not in target.parents and target != root:
        raise SafetyError(f"Case path is outside project root: {target}")

    if not target.exists():
        raise SafetyError(f"Case path does not exist: {target}")

    if not target.is_dir():
        raise SafetyError(f"Case path is not a directory: {target}")

    return target


def safe_file_path(case_path: Path, relative_path: str) -> Path:
    """
    Resolve a case file safely.

    Prevents path traversal like ../../../secret.txt.
    """
    file_path = (case_path / relative_path).resolve()

    if case_path.resolve() not in file_path.parents and file_path != case_path.resolve():
        raise SafetyError(f"File path escapes case directory: {file_path}")

    if not file_path.exists():
        raise SafetyError(f"Required case file does not exist: {file_path}")

    if not file_path.is_file():
        raise SafetyError(f"Expected a file, got: {file_path}")

    return file_path