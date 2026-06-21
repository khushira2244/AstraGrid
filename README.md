# AstraGrid


<img width="1672" height="941" alt="ChatGPT Image Jun 18, 2026, 10_37_57 AM" src="https://github.com/user-attachments/assets/9702f9c4-0583-4dae-8946-f179d9244df6" />



**AstraGrid** is a Protocol SIFT extension for autonomous cyber-physical incident response across power, water, network, endpoint, and infrastructure dependency evidence.

Live demo: [https://astragrid.netlify.app/](https://astragrid.netlify.app/)
Repository: [https://github.com/khushira2244/AstraGrid](https://github.com/khushira2244/AstraGrid)


## Important points after hackathon I kept changes on other branch.
These changes belongs to which I want to upgrad my product.
Upgrade Roadmap

Day 1 — WADI Integration
Large-scale water distribution scenario expansion.

Day 2–3 — MCP Integration
AstraGrid tools become Protocol SIFT / MCP-ready and visible in the frontend.

Day 4 — Multi-Case Support
Run multiple cyber-physical cases from one system.

Day 5 — MITRE ATT&CK ICS Mapping
Map OT/network/endpoint evidence to ATT&CK for ICS technique context.



---

## What AstraGrid Solves

Cyber-physical incidents are difficult because the first visible symptom is often not the root cause.

In the demo case, a water utility anomaly initially looks like a direct water cyberattack. AstraGrid checks the evidence across power, water, network, endpoint, and dependency layers, then corrects the conclusion:

```text
Initial hypothesis:
Direct water cyberattack

Corrected hypothesis:
Power-to-water cascade is plausible; direct water attack is unsupported
```

AstraGrid avoids overclaiming. It separates confirmed evidence from unsupported hypotheses and records every step with tool-run IDs, evidence references, reports, and execution logs.

---

## SANS SIFT / Protocol SIFT Alignment

AstraGrid is not only a web dashboard.

The project was designed to run inside the SANS SIFT Workstation case environment and support Protocol SIFT-style autonomous investigation.

AstraGrid adds a structured cyber-physical reasoning layer:

```text
SANS SIFT Workstation
→ Protocol SIFT / Claude Code
→ AstraGrid structured tools
→ Power + Water + Network + Endpoint + Dependency evidence
→ Findings
→ Timeline
→ Claim validation
→ Self-correction trace
→ Final report
→ Accuracy report
→ Tool-run audit logs
→ Frontend visualization
```

The frontend visualizes the outputs from the SIFT/agent investigation. It does not replace Protocol SIFT.

---

## Demo Case

### ASTRAGRID-001 — Power-to-Water Cascade Cyber-Physical Incident

Investigation question:

```text
Did a water utility anomaly come from a direct water cyberattack,
or was it downstream impact from a power-side incident?
```

AstraGrid checks:

* Power-grid telemetry
* Water treatment and water distribution evidence
* Modbus / OT network evidence
* Endpoint forensic evidence
* Infrastructure dependency graph
* Ground truth for accuracy evaluation

Final result:

```text
Classification: POWER_TO_WATER_CASCADE
Direct water cyberattack: UNSUPPORTED
Power-to-water cascade: PARTIALLY_CONFIRMED
Claim accuracy: 1.0
Self-correction steps: 6
Evidence integrity: maintained
Country attribution: not claimed
```

---

## Core Capabilities

### 1. Five Evidence Layers

AstraGrid checks each infrastructure layer in sequence:

```text
Power-grid telemetry
Water treatment and distribution evidence
Modbus / OT network evidence
Endpoint forensic evidence
Infrastructure dependency graph
```

### 2. Evidence-Backed Claim Validation

Every claim receives an explicit status:

```text
CONFIRMED
PARTIALLY_CONFIRMED
INFERRED
UNSUPPORTED
CONTRADICTED
```

### 3. Self-Correction

The system starts with a hypothesis, checks gaps, expands context, and revises the conclusion when evidence does not support the first answer.

Demo self-correction:

```text
Direct water cyberattack → UNSUPPORTED
Power-to-water cascade → PARTIALLY_CONFIRMED
```

### 4. Tool-Run Audit Trail

Every tool execution is logged with:

* tool name
* tool run ID
* timestamps
* input summary
* output summary
* evidence references
* status
* error field

### 5. Final Report and Accuracy Report

AstraGrid generates:

```text
outputs/final_report.json
outputs/final_report.md
outputs/accuracy_report.json
outputs/accuracy_report.md
```

The accuracy report compares generated claims against the demo ground truth.

---

## Structured Tools

AstraGrid currently includes these investigation tools:

```text
get_case_manifest
get_power_event_summary
get_water_event_summary
get_network_attack_evidence
get_endpoint_evidence
get_dependency_summary
```

These tools are MCP-ready and were designed for Protocol SIFT integration.

---

## Generated Outputs

Running the case pipeline generates:

```text
outputs/findings.json
outputs/timeline.json
outputs/claims.json
outputs/self_correction_trace.json
outputs/final_report.json
outputs/final_report.md
outputs/accuracy_report.json
outputs/accuracy_report.md
outputs/tool_runs.json
```

---

## Evidence Dataset Documentation

AstraGrid uses normalized cyber-physical evidence from public/safe datasets and curated case files.

### Evidence Layers

| Layer                    | Dataset / Source                | Purpose                                          |
| ------------------------ | ------------------------------- | ------------------------------------------------ |
| Power grid               | MSU / ORNL Power System Dataset | Power-side cyber-physical evidence               |
| Water treatment          | SWaT                            | Water treatment process behavior                 |
| Water distribution       | BATADAL                         | Water distribution anomaly context               |
| Large water distribution | WADI                            | Planned expansion for larger water scenarios     |
| Network / ICS            | CIC Modbus Dataset 2023         | Modbus / OT network evidence                     |
| Endpoint forensic        | Mordor Windows samples          | Endpoint compromise and defense-evasion evidence |
| Threat context           | MITRE ATT&CK ICS / Enterprise   | Technique mapping and enrichment                 |
| Dependency graph         | Curated infrastructure graph    | Power-to-water dependency reasoning              |

Full dataset documentation:

```text
docs/dataset_documentation.md
```

---

## Accuracy Report

The demo ground truth expected:

```text
Power grid cyber event occurred → CONFIRMED
Water operational anomaly occurred → CONFIRMED
Direct water cyberattack occurred → UNSUPPORTED
Power-to-water cascade is plausible → PARTIALLY_CONFIRMED
Endpoint defense-evasion evidence exists → CONFIRMED
```

AstraGrid result:

```text
Accuracy: 1.0
False-positive review: direct water cyberattack was not overclaimed
Hallucination review: no hallucinated claims detected
Evidence integrity: read-only case files and tool-run traceability maintained
```

Generated files:

```text
outputs/accuracy_report.json
outputs/accuracy_report.md
```

---

## Local Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/khushira2244/AstraGrid.git
cd AstraGrid
```

### 2. Create and activate a Python environment

Linux / SIFT VM:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run the investigation pipeline

```bash
python -m app.run_case
```

Expected output includes:

```text
Case: ASTRAGRID-001 - Power-to-Water Cascade Cyber-Physical Incident
Classification hint: POWER_TO_WATER_CASCADE
Findings: 5
Timeline events: 6
Claims: 6
Self-correction steps: 6
Accuracy: 1.0
```

### 5. Optional API run

```bash
python -m uvicorn api.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## API Routes

```text
GET  /
GET  /health
POST /case/run

GET  /case/summary
GET  /case/findings
GET  /case/timeline
GET  /case/claims
GET  /case/self-correction
GET  /case/tool-runs
GET  /case/threat-origin

GET  /case/reports/final
GET  /case/reports/accuracy
```

---

## SIFT VM Proof

AstraGrid was tested inside the SANS SIFT Workstation VM at:

```text
/cases/ASTRAGRID-001/AstraGrid
```

Successful VM run:

```bash
python -m app.run_case
```

The VM execution generated findings, timeline, claims, self-correction trace, final report, accuracy report, and tool-run logs.

Claude Code / Protocol SIFT reviewed those generated outputs and confirmed:

```text
Direct water cyberattack → UNSUPPORTED
Power-to-water cascade → PARTIALLY_CONFIRMED
Classification → POWER_TO_WATER_CASCADE
Accuracy → 1.0
No unsupported country attribution claimed
Evidence integrity maintained
```

---

## Key Finding

The most important forensic pivot:

```text
The water anomaly existed, but the water evidence did not prove a direct PLC or water command path.

The dependency graph confirmed:
POWER_SUBSTATION_01 → WATER_PUMP_STATION_03

Therefore, AstraGrid corrected the hypothesis from direct water cyberattack to power-to-water cascade.
```

---

## Guardrails

### Prompt-Based Guardrails

* Use generated outputs only
* Do not modify evidence files
* Do not infer attacker country from source IP
* Mark unsupported claims explicitly

### Architectural Guardrails

* Read-only normalized case files
* Safe path loading
* Structured tool wrappers
* Tool-run logging
* Evidence references attached to findings
* Claim statuses tied to tool outputs
* Accuracy report against ground truth

---

## Frontend

The deployed frontend is a judge-facing visualization layer:

[https://astragrid.netlify.app/](https://astragrid.netlify.app/)

It shows:

* Power and water incident context
* The investigation gap
* AstraGrid capabilities
* Architecture
* Future roadmap
* Demo case proof pages
* SIFT VM execution evidence

The frontend does not replace Protocol SIFT. It explains the outputs generated by the SIFT/agent run.

#Architecture
<img width="1672" height="941" alt="architecture" src="https://github.com/user-attachments/assets/3e3d9327-6ca4-44d7-b205-c1d5d28b62d8" />




---

## Future Capability

Planned upgrades:

* Full MCP server registration with Protocol SIFT
* Live SCADA and OT telemetry ingestion
* WADI-based large water-distribution scenarios
* Expanded infrastructure layers: telecom, transport, healthcare, energy
* Real-time alert ingestion from SIEM, EDR, and OT monitoring tools
* Deeper MITRE ATT&CK for ICS mapping
* Multi-case correlation across cascading incidents
* Human approval workflow for high-impact response actions

---

## Built With

```text
Python
FastAPI
Uvicorn
SANS SIFT Workstation
Protocol SIFT / Claude Code
JSON
MITRE ATT&CK
SWaT
BATADAL
WADI planned expansion
Mordor endpoint evidence
CIC Modbus evidence
Netlify
```

---

## Project Status

AstraGrid is a working hackathon prototype.

Completed:

```text
Core investigation tools
Case pipeline
Findings
Timeline
Claims validation
Self-correction trace
Final report
Accuracy report
Tool-run logs
FastAPI routes
Frontend deployment
SIFT VM execution proof
```

Next:

```text
Native MCP server registration
Live telemetry ingestion
Expanded cyber-physical datasets
```
