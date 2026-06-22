import Header from '../components/Header';
import styles from './AstraGridDemo.module.css';

const POWER_GRID_PROOF_LINK =
  'https://vimeo.com/1201600468?share=copy&fl=sv&fe=ci';

const WATER_UTILITY_PROOF_LINK = 'https://vimeo.com/1202363127';
const NETWORK_ENDPOINT_PROOF_LINK = 'https://vimeo.com/1202363466';
const INFRASTRUCTURE_DEPENDENCY_PROOF_LINK = 'https://vimeo.com/1202363797';
const WADI_CONTEXT_PROOF_LINK = 'https://vimeo.com/1203321133';

const WATER_UTILITY_DOC_LINK =
  '/doc_of_proof/Water%20Utility%20Evidence%20Proof.docx';

const NETWORK_ENDPOINT_DOC_LINK =
  '/doc_of_proof/Network_evidence.docx';

const INFRASTRUCTURE_DEPENDENCY_DOC_LINK =
  '/doc_of_proof/Infrastructure%20Dependency%20Graph%20Proof.docx';

const WADI_CONTEXT_DOC_LINK =
  '/doc_of_proof/vm_context_integrity_proof.md';

/* ── DATA ── */
const VB_ROWS = [
  { name: 'Direct Water Cyberattack', pill: 'UNSUPPORTED', cls: 'vu' },
  { name: 'Power-to-Water Cascade', pill: 'PARTIALLY CONFIRMED', cls: 'vp2' },
  { name: 'Power-Grid Evidence', pill: 'CONFIRMED', cls: 'vc' },
  { name: 'Endpoint Defense Evasion', pill: 'CONFIRMED', cls: 'vc' },
  { name: 'Country Attribution', pill: 'NOT CLAIMED', cls: 'vi' },
];

const EV_SECTIONS = [
  {
    id: 0,
    flip: false,
    eyebrow: 'Step 00 · Context Integrity + WADI',
    h2: ['Context Integrity', 'WADI Adapter'],
    situation:
      'A cyber-physical conclusion can collapse if sensor mapping, actuator mapping, timestamp context, dependency context, or command-path context is missing. AstraGrid checks this context before promoting high-risk claims.',
    checks: [
      'Water treatment context present',
      'Water distribution context present',
      'WADI optional adapter accepted',
      'Sensor, actuator, timestamp, and dependency context validated',
      'Direct command path remains unsupported',
    ],
    result:
      'Context integrity is STRONG. WADI strengthens the water-distribution context, but it does not prove a direct water cyberattack.',
    tool: 'Context Integrity: context_integrity_report.json',
    run: 'WADI Config: configs/column_maps/wadi_optional.json',
    buttons: [
      {
        label: 'Watch WADI Context Proof →',
        ghost: false,
        href: WADI_CONTEXT_PROOF_LINK,
      },
      {
        label: 'Open Context Proof Doc →',
        ghost: true,
        href: WADI_CONTEXT_DOC_LINK,
      },
    ],
    cards: [
      {
        icon: '🧭',
        label: 'Context Integrity',
        val: null,
        valPill: { text: 'STRONG', cls: 'vc' },
        sub: 'Sensor, actuator, timestamp, dependency, and water context validated',
        subStyle: { marginTop: 8 },
      },
      {
        icon: '💧',
        label: 'WADI Optional Adapter',
        val: null,
        valPill: { text: 'ACCEPTED', cls: 'vc' },
        sub: 'Large-scale water-distribution context added as optional adapter',
        subStyle: { marginTop: 8 },
      },
      {
        icon: '🎯',
        label: 'Direct Command Path',
        val: null,
        valPill: { text: 'UNSUPPORTED', cls: 'vu' },
        sub: 'WADI does not prove direct PLC or SCADA command causality',
        subStyle: { marginTop: 8 },
      },
    ],
    extras: [
      {
        red: false,
        amber: true,
        label: 'Claim Boundary',
        val: 'WADI strengthens context · does not prove direct attack',
      },
      {
        red: false,
        label: 'Safety Boundary',
        val: 'Country attribution not claimed · destructive response requires human approval',
      },
    ],
  },
  {
    id: 1,
    flip: false,
    eyebrow: 'Step 01 · Power Layer',
    h2: ['Power Grid', 'Evidence'],
    situation:
      'A power-side event was detected in the case. AstraGrid checks the power layer before blaming the downstream water system.',
    checks: [
      'Power-grid telemetry',
      'Event classification',
      'Power anomaly evidence',
      'Evidence refs PWR-000322 to PWR-000331',
    ],
    result:
      'A confirmed power-side event means the water anomaly may be downstream impact, not a direct water cyberattack.',
    tool: 'Tool: get_power_event_summary',
    run: 'Tool run: TOOL-000002',
    btn: {
      label: 'Watch SIFT Proof →',
      ghost: false,
      href: POWER_GRID_PROOF_LINK,
    },
    cards: [
      {
        icon: '⚡',
        label: 'Status',
        val: null,
        valPill: { text: 'CONFIRMED', cls: 'vc' },
        sub: 'Power-grid event confirmed in ASTRAGRID-001 case',
        subStyle: { marginTop: 8 },
      },
      {
        icon: '📋',
        label: 'Sector',
        val: 'Power',
        valPill: null,
        sub: 'Evidence refs: PWR-000322 – PWR-000331',
      },
      {
        icon: '🔖',
        label: 'Tool Run',
        val: 'TOOL-000002',
        valPill: null,
        sub: 'get_power_event_summary · read-only',
      },
    ],
    extras: [],
  },
  {
    id: 2,
    flip: true,
    eyebrow: 'Step 02 · Water Layer',
    h2: ['Water Utility', 'Evidence'],
    situation:
      'The visible symptom was a water utility anomaly. At first, this looked like a direct water cyberattack. AstraGrid checks before concluding.',
    checks: [
      'SWaT water-treatment evidence',
      'BATADAL water-distribution evidence',
      'Water anomaly records',
      'Whether sample proves direct water attack',
    ],
    result:
      'Water evidence exists but direct water cyberattack is UNSUPPORTED. AstraGrid avoids overclaiming.',
    tool: 'Tool: get_water_event_summary',
    run: 'Tool run: TOOL-000003',
    buttons: [
      {
        label: 'Watch Self-Correction →',
        ghost: false,
        href: WATER_UTILITY_PROOF_LINK,
      },
      {
        label: 'Open Proof Doc →',
        ghost: true,
        href: WATER_UTILITY_DOC_LINK,
      },
    ],
    cards: [
      {
        icon: '💧',
        label: 'Water Evidence',
        val: null,
        valPill: { text: 'CONFIRMED', cls: 'vc' },
        sub: 'Evidence refs: SWAT-000000 – SWAT-000004',
        subStyle: { marginTop: 8 },
      },
      {
        icon: '🎯',
        label: 'Direct Water Attack',
        val: null,
        valPill: { text: 'UNSUPPORTED', cls: 'vu' },
        sub: 'No direct PLC or SCADA command path proven',
        subStyle: { marginTop: 8 },
      },
      {
        icon: '🔖',
        label: 'Tool Run',
        val: 'TOOL-000003',
        valPill: null,
        sub: 'get_water_event_summary · read-only',
      },
    ],
    extras: [
      {
        red: true,
        label: 'Important Finding',
        val: 'no_water_attack_in_loaded_sample',
      },
    ],
  },
  {
    id: 3,
    flip: false,
    eyebrow: 'Step 03 · Network Layer',
    h2: ['Network &', 'Endpoint'],
    situation:
      'Network indicators were present on Modbus/TCP traffic. Endpoint activity may indicate operator workstation compromise or defense evasion.',
    checks: [
      'NET-000295, NET-000428, NET-000562',
      'NET-000687, NET-000788, NET-000917',
      'END-000000 — endpoint forensics',
      'Audit log clearing detected',
    ],
    result:
      'Network indicators support investigation, but do not prove direct attribution to a water command path.',
    tool: 'Network: get_network_attack_evidence · TOOL-000004',
    run: 'Endpoint: get_endpoint_evidence · TOOL-000005',
    buttons: [
      {
        label: 'Watch Network / Endpoint Proof →',
        ghost: false,
        href: NETWORK_ENDPOINT_PROOF_LINK,
      },
      {
        label: 'Open Proof Doc →',
        ghost: true,
        href: NETWORK_ENDPOINT_DOC_LINK,
      },
    ],
    cards: [
      {
        icon: '🌐',
        label: 'Network Attack Evidence',
        val: 'Present',
        valPill: null,
        sub: 'Modbus/TCP indicators — 6 evidence refs',
      },
      {
        icon: '💻',
        label: 'Endpoint Defense Evasion',
        val: null,
        valPill: { text: 'CONFIRMED', cls: 'vc' },
        sub: 'Audit log clearing detected · END-000000',
        subStyle: { marginTop: 6 },
      },
    ],
    extras: [
      {
        red: false,
        amber: true,
        label: 'Network Conclusion',
        val: 'Supports investigation · not direct attribution',
      },
    ],
  },
];

const TL_STEPS = [
  {
    num: '01',
    title: 'Initial Hypothesis',
    body: 'Direct water cyberattack — based on the first visible symptom being a water utility anomaly.',
    badge: 'HYPOTHESIS SET',
    badgeCls: 'tbRed',
  },
  {
    num: '02',
    title: 'Water Evidence Check',
    body: 'Water treatment and distribution evidence existed, but the loaded sample did not prove a direct water attack.',
    badge: 'WATER CHECKED',
    badgeCls: 'tbGreen',
  },
  {
    num: '03',
    title: 'Gap Detection',
    body: 'Network evidence did not prove a direct PLC or SCADA command path into the water system.',
    badge: 'GAP DETECTED',
    badgeCls: 'tbAmber',
  },
  {
    num: '04',
    title: 'Context Integrity Check',
    body: 'AstraGrid validated water, WADI, sensor, actuator, timestamp, and dependency context before promoting claims.',
    badge: 'CONTEXT STRONG',
    badgeCls: 'tbGreen',
  },
  {
    num: '05',
    title: 'Context Expansion',
    body: 'Power evidence checked — power-grid event confirmed upstream from the water anomaly.',
    badge: 'POWER CONFIRMED',
    badgeCls: 'tbGreen',
  },
  {
    num: '06',
    title: 'Dependency Check',
    body: 'Power Substation 01 confirmed to supply power to Water Pump Station 03 — dependency path present.',
    badge: 'CASCADE PATH FOUND',
    badgeCls: 'tbGreen',
  },
  {
    num: '07',
    title: 'Corrected Conclusion',
    body: 'Direct water attack UNSUPPORTED. Power-to-water cascade PARTIALLY CONFIRMED. Destructive response requires human approval.',
    badge: 'SELF-CORRECTED ↻',
    badgeCls: 'tbGreen',
  },
];

const VS_INFO_CARDS = [
  {
    icon: '↻',
    title: 'Self-Corrected\nHypothesis',
    body: 'AstraGrid revised the initial wrong conclusion after evidence checks — without human intervention.',
  },
  {
    icon: '✓',
    title: 'Evidence-Backed\nVerdicts',
    body: 'Every claim is traceable to tool run IDs, evidence references, and execution logs — nothing assumed.',
  },
  {
    icon: '⚠',
    title: 'No Country\nAttribution',
    body: 'AstraGrid reports observed network origin indicators only. No nationality attribution is claimed from IP evidence.',
  },
];

const VM_CLAIMS = [
  { name: 'Direct water cyberattack', cls: 'vu', pill: 'UNSUPPORTED' },
  { name: 'Power-to-water cascade', cls: 'vp2', pill: 'PARTIALLY CONFIRMED' },
  { name: 'Context integrity', cls: 'vc', pill: 'STRONG' },
  { name: 'Power-grid evidence', cls: 'vc', pill: 'CONFIRMED' },
  { name: 'Water utility evidence', cls: 'vc', pill: 'CONFIRMED' },
  { name: 'Endpoint defense evasion', cls: 'vc', pill: 'CONFIRMED' },
];

/* ── COMPONENT ── */
export default function AstraGridDemo() {
  return (
    <div>
      <Header />

      {/* ══ HERO ══ */}
      <section className={styles.demoHero}>
        <div className={`${styles.wrap} ${styles.dhInner}`}>
          <div className={styles.dhLeft}>
            <div className={styles.dhTag}>Demo Case · ASTRAGRID-001</div>

            <h1>
              Power-to-Water
              <br />
              <em>Cascade</em>
              <br />
              Investigation
            </h1>

            <div className={styles.dhSub}>Protocol SIFT Evidence Sequencing</div>

            <p>
              A water anomaly looked like a direct cyberattack. AstraGrid used Protocol SIFT
              evidence sequencing to test that hypothesis and corrected the conclusion to a
              power-to-water cascade.
            </p>
          </div>

          <div>
            <div className={styles.verdictBoard}>
              <div className={styles.vbHeader}>
                <span className={styles.vbDot} style={{ background: 'var(--crimson)' }} />
                <span className={styles.vbDot} style={{ background: 'rgba(255,176,32,.7)' }} />
                <span className={styles.vbDot} style={{ background: 'rgba(0,214,143,.5)' }} />
                <span className={styles.vbTitle}>Final Investigation Output</span>
              </div>

              <div className={styles.vbBody}>
                <div className={styles.vbCase}>
                  Case: <span>ASTRAGRID-001</span>
                </div>

                {VB_ROWS.map((r) => (
                  <div key={r.name} className={styles.vbRow}>
                    <span className={styles.vbName}>{r.name}</span>
                    <span className={`${styles.vp} ${styles[r.cls]}`}>{r.pill}</span>
                  </div>
                ))}

                <div className={styles.vbCorrection}>
                  <span className={styles.vbcIcon}>↻</span>
                  <span className={styles.vbcLabel}>Self-correction steps</span>
                  <span className={styles.vbcVal}>6 corrections</span>
                </div>

                <div className={styles.vbScore}>
                  <span className={styles.vbsLabel}>Claim Accuracy</span>
                  <span className={styles.vbsVal}>1.0</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══ EVIDENCE SECTIONS ══ */}
      {EV_SECTIONS.map((sec, idx) => (
        <section
          key={sec.id}
          className={`${styles.evidenceSection} ${idx % 2 === 0 ? styles.evidenceSectionOdd : styles.evidenceSectionEven
            }`}
        >
          <div className={styles.wrap}>
            <div className={`${styles.evGrid} ${sec.flip ? styles.evGridFlip : ''}`}>
              <div className={styles.evLeft}>
                <div className={styles.eyebrow}>{sec.eyebrow}</div>

                <h2>
                  {sec.h2[0]}
                  <br />
                  <em>{sec.h2[1]}</em>
                </h2>

                <p className={styles.evSituation}>{sec.situation}</p>

                <div className={styles.evChecked}>
                  {sec.checks.map((c) => (
                    <div key={c} className={styles.evCheck}>
                      {c}
                    </div>
                  ))}
                </div>

                <div className={styles.evResult}>{sec.result}</div>

                <div className={styles.evTool}>
                  <span>{sec.tool}</span>
                  <span>{sec.run}</span>
                </div>

                {sec.btn && (
                  <a
                    href={sec.btn.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`${styles.evBtn} ${sec.btn.ghost ? styles.evBtnGhost : ''}`}
                  >
                    {sec.btn.label}
                  </a>
                )}

                {sec.buttons?.length > 0 && (
                  <div className={styles.evBtnRow}>
                    {sec.buttons.map((button) => (
                      <a
                        key={button.label}
                        href={button.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`${styles.evBtn} ${button.ghost ? styles.evBtnGhost : ''}`}
                      >
                        {button.label}
                      </a>
                    ))}
                  </div>
                )}
              </div>

              <div className={styles.evRight}>
                {sec.cards.map((card) => (
                  <div key={card.label} className={styles.evCard}>
                    <div className={styles.evCardIcon}>{card.icon}</div>
                    <div className={styles.evCardLabel}>{card.label}</div>

                    <div className={styles.evCardVal}>
                      {card.valPill ? (
                        <span className={`${styles.vp} ${styles[card.valPill.cls]}`}>
                          {card.valPill.text}
                        </span>
                      ) : (
                        card.val
                      )}
                    </div>

                    <div className={styles.evCardSub} style={card.subStyle || {}}>
                      {card.sub}
                    </div>
                  </div>
                ))}

                {sec.extras.map((ex) => (
                  <div
                    key={ex.label}
                    className={`${styles.findingCard} ${ex.red === false && !ex.amber ? styles.findingCardGreen : ''
                      }`}
                    style={
                      ex.amber
                        ? {
                          background: 'rgba(255,176,32,.06)',
                          borderColor: 'rgba(255,176,32,.2)',
                        }
                        : {}
                    }
                  >
                    <div className={styles.fcLabel}>{ex.label}</div>

                    <div
                      className={styles.fcVal}
                      style={
                        ex.amber
                          ? { color: 'var(--partial)' }
                          : ex.red === false
                            ? { color: 'var(--confirmed)' }
                            : {}
                      }
                    >
                      {ex.val}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      ))}

      {/* ══ DEPENDENCY ══ */}
      <section className={styles.dependencySection}>
        <div className={`${styles.wrap} ${styles.depGrid}`}>
          <div>
            <div className={styles.eyebrow}>Step 04 · Dependency Layer</div>

            <h2
              style={{
                fontFamily: 'var(--condensed)',
                fontSize: 'clamp(32px,4vw,52px)',
                fontWeight: 900,
                textTransform: 'uppercase',
                letterSpacing: '-.01em',
                marginBottom: 18,
                lineHeight: 0.95,
                color: '#fff',
              }}
            >
              Infrastructure
              <br />
              <span style={{ color: 'var(--crimson)' }}>Dependency</span> Graph
            </h2>

            <p
              style={{
                fontSize: 15,
                color: 'var(--pale)',
                maxWidth: 440,
                lineHeight: 1.7,
                marginBottom: 20,
              }}
            >
              If a power asset supplies a water asset, a power-side event can cascade into water
              impact. AstraGrid checks the dependency path explicitly.
            </p>

            <div className={styles.evChecked} style={{ marginBottom: 24 }}>
              <div className={styles.evCheck}>
                POWER_SUBSTATION_01 supplies power to WATER_PUMP_STATION_03
              </div>
              <div className={styles.evCheck}>Relationship: supplies_power_to</div>
              <div className={styles.evCheck}>Finding: power_to_water_dependency_present</div>
            </div>

            <div className={styles.evResult}>
              The dependency path makes the cascade hypothesis more evidence-supported than the
              direct-water-attack hypothesis.
            </div>

            <div className={styles.evTool} style={{ marginTop: 16 }}>
              <span>
                Tool: <b>get_dependency_summary</b>
              </span>
              <span>
                Tool run: <b>TOOL-000006</b>
              </span>
            </div>

            <div className={styles.evBtnRow}>
              <a
                href={INFRASTRUCTURE_DEPENDENCY_PROOF_LINK}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.evBtn}
              >
                Watch Dependency Proof →
              </a>

              <a
                href={INFRASTRUCTURE_DEPENDENCY_DOC_LINK}
                target="_blank"
                rel="noopener noreferrer"
                className={`${styles.evBtn} ${styles.evBtnGhost}`}
              >
                Open Proof Doc →
              </a>
            </div>
          </div>

          <div className={styles.depPath}>
            <div className={styles.dpLabel}>// Infrastructure Dependency Path</div>

            <div className={`${styles.dpNode} ${styles.dpNodePower}`}>
              <div className={styles.dpNodeIcon}>⚡</div>
              <div className={styles.dpNodeLabel}>Power Asset</div>
              <div className={styles.dpNodeName}>Power Substation 01</div>
            </div>

            <div className={styles.dpConnector}>
              <div className={styles.dpConnectorLine} />
              supplies_power_to
              <div className={styles.dpConnectorLine} />
            </div>

            <div className={`${styles.dpNode} ${styles.dpNodeWater}`}>
              <div className={styles.dpNodeIcon}>💧</div>
              <div className={styles.dpNodeLabel}>Water Asset</div>
              <div className={styles.dpNodeName}>Water Pump Station 03</div>
            </div>

            <div className={styles.dpResult}>
              <span className={styles.dpResultLabel}>Dependency Status</span>
              <span className={styles.dpResultVal}>CONFIRMED</span>
            </div>

            <div className={`${styles.findingCard} ${styles.findingCardGreen}`} style={{ marginTop: 12 }}>
              <div className={styles.fcLabel}>Finding</div>
              <div className={styles.fcVal}>power_to_water_dependency_present</div>
            </div>
          </div>
        </div>
      </section>

      {/* ══ TIMELINE ══ */}
      <section className={styles.timelineSection}>
        <div className={styles.wrap}>
          <div className={styles.tlHeading}>
            <div className={`${styles.eyebrow} ${styles.eyebrowCenter}`}>
              How the Hypothesis Changed
            </div>

            <h2>
              Self-Correction <em>Timeline</em>
            </h2>

            <p>7 reasoning steps from initial wrong hypothesis to context-validated conclusion.</p>
          </div>

          <div className={styles.timeline}>
            {TL_STEPS.map((step) => (
              <div key={step.num} className={styles.tlStep}>
                <div className={styles.tlNum}>{step.num}</div>

                <div className={styles.tlContent}>
                  <div className={styles.tlTitle}>{step.title}</div>
                  <div className={styles.tlBody}>{step.body}</div>
                  <span className={`${styles.tlBadge} ${styles[step.badgeCls]}`}>
                    {step.badge}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══ FINAL VERDICT ══ */}
      <section className={styles.verdictSection}>
        <div className={`${styles.wrap} ${styles.vsInner}`}>
          <div className={styles.vsHeading}>
            <div className={`${styles.eyebrow} ${styles.eyebrowCenter}`}>
              Investigation Complete
            </div>

            <h2>
              Final <em>Verdict</em>
            </h2>

            <p>AstraGrid separated confirmed facts from unsupported hypotheses across five evidence layers.</p>
          </div>

          <div className={styles.vsTopCards}>
            {VS_INFO_CARDS.map((c) => (
              <div key={c.title} className={styles.vsInfoCard}>
                <span className={styles.vsCardIcon}>{c.icon}</span>

                <div className={styles.vsCardTitle}>
                  {c.title.split('\n').map((line) => (
                    <span key={line}>
                      {line}
                      <br />
                    </span>
                  ))}
                </div>

                <div className={styles.vsCardBody}>{c.body}</div>
              </div>
            ))}
          </div>

          <div className={styles.verdictMain}>
            <div className={styles.vmTop}>
              <div>
                <div className={styles.vmClassLabel}>Classification</div>
                <div className={styles.vmClassVal}>Power-to-Water Cascade</div>
              </div>

              <div className={styles.vmStats}>
                <div>
                  <div className={styles.vmStatLabel}>Claim Accuracy</div>
                  <div className={`${styles.vmStatVal} ${styles.vmStatValGreen}`}>1.0</div>
                </div>

                <div>
                  <div className={styles.vmStatLabel}>Self-Corrections</div>
                  <div className={`${styles.vmStatVal} ${styles.vmStatValRed}`}>6</div>
                </div>

                <div>
                  <div className={styles.vmStatLabel}>Evidence Integrity</div>
                  <div
                    className={`${styles.vmStatVal} ${styles.vmStatValGreen}`}
                    style={{ fontSize: 22, paddingTop: 8 }}
                  >
                    Maintained
                  </div>
                </div>
              </div>
            </div>

            <div className={styles.vmClaims}>
              {VM_CLAIMS.map((c) => (
                <div key={c.name} className={styles.vmClaim}>
                  <span className={styles.vmClaimName}>{c.name}</span>
                  <span className={`${styles.vp} ${styles[c.cls]}`}>{c.pill}</span>
                </div>
              ))}
            </div>

            <div className={styles.vmAttribution}>
              Country attribution is not claimed. Observed origin: 192.168.56.113 →
              192.168.56.112. Infrastructure path: POWER_SUBSTATION_01 →
              WATER_PUMP_STATION_03.
            </div>

            <div className={styles.vmBtnRow}>
              <a href={WADI_CONTEXT_DOC_LINK} className={`${styles.evBtn} ${styles.evBtnGhost}`}>
                View Full Report
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}