# AstraGrid


<img width="1408" height="768" alt="Gemini_Generated_Image_78fgd578fgd578fg" src="https://github.com/user-attachments/assets/7bd518bb-3396-4fdf-91e3-8d5f96371d2e" />

**AstraGrid** is an autonomous critical-infrastructure incident reasoning agent for cyber-physical attacks, cascade analysis, and evidence-backed incident response.

The project focuses on analyzing multi-sector infrastructure incidents across power-grid, water-treatment, water-distribution, network/ICS, and endpoint-forensic layers.

## Core Idea

AstraGrid is not a normal log summarizer.

It is designed to behave like an incident-response analyst:

1. Load multi-source critical-infrastructure data
2. Detect cyber-physical anomalies
3. Correlate events across infrastructure sectors
4. Check whether the incident is isolated, cascading, coordinated, or unsupported
5. Validate every finding with evidence
6. Self-correct when analysis is incomplete
7. Generate an audit-ready investigation report

## First Demo Scenario

The first demo will focus on a **power-to-water cascade incident**.

Example investigation question:

> Did a power-grid cyber event cause downstream water-utility disruption, or was the water anomaly a separate direct attack?

The agent will analyze:

- power-grid telemetry
- water-treatment or water-distribution data
- network/ICS logs
- endpoint forensic evidence
- infrastructure dependency graph
- MITRE ATT&CK mapping

## Data Layers

| Layer | Dataset | Status | Role |
| --- | --- | ---: | --- |
| Power grid | **MSU/ORNL Power System Dataset** | Must use | PMU/synchrophasor + Snort + relay + control + labels |
| Water treatment | **SWaT** | Must use | Sensors + actuators + pumps/valves + normal/attack labels |
| Water distribution | **BATADAL** | Strong optional | Tank/pump/valve/pressure + attack labels |
| Large water distribution | **WADI** | Optional/heavy | Distribution-scale normal + attack-label data |
| Network/ICS | **CIC Modbus Dataset 2023** | Use if manageable | Modbus/PLC-style network intrusion layer |
| Endpoint forensic | **Mordor selected Windows samples** | Use selected only | PowerShell / scheduled task / WMI / startup persistence evidence |
| Threat intelligence | **MITRE ATT&CK ICS STIX** | Must use | ICS/SCADA technique mapping |
| Endpoint technique mapping | **MITRE Enterprise STIX** | Optional/useful | Windows endpoint technique mapping |

## Planned Architecture

```text
Raw Data
   ↓
Safe Tool Wrappers
   ↓
Normalized Events
   ↓
Sector Agents
   ↓
Correlation Agent
   ↓
Cascade Reasoning Agent
   ↓
Evidence Validation Agent
   ↓
Self-Correction Agent
   ↓
Audit-Ready Report
