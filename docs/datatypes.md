| Layer                      | Dataset                             |            Status | Role                                                             |
| -------------------------- | ----------------------------------- | ----------------: | ---------------------------------------------------------------- |
| Power grid                 | **MSU/ORNL Power System Dataset**   |          Must use | PMU/synchrophasor + Snort + relay + control + labels             |
| Water treatment            | **SWaT**                            |          Must use | Sensors + actuators + pumps/valves + normal/attack labels        |
| Water distribution         | **BATADAL**                         |   Strong optional | Tank/pump/valve/pressure + attack labels                         |
| Large water distribution   | **WADI**                            |    Optional/heavy | Distribution-scale normal + attack-label data                    |
| Network/ICS                | **CIC Modbus Dataset 2023**         | Use if manageable | Modbus/PLC-style network intrusion layer                         |
| Endpoint forensic          | **Mordor selected Windows samples** | Use selected only | PowerShell / scheduled task / WMI / startup persistence evidence |
| Threat intelligence        | **MITRE ATT&CK ICS STIX**           |          Must use | ICS/SCADA technique mapping                                      |
| Endpoint technique mapping | **MITRE Enterprise STIX**           |   Optional/useful | Windows endpoint technique mapping                               |
