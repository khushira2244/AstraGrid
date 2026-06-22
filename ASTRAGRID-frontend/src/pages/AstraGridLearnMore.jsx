import styles from './AstraGridLearnMore.module.css';
import { Link } from 'react-router-dom';

const VERDICTS = [
  { cls: 'lvC', label: 'Confirmed' },
  { cls: 'lvP', label: 'Partially Confirmed' },
  { cls: 'lvI', label: 'Inferred' },
  { cls: 'lvU', label: 'Unsupported' },
  { cls: 'lvX', label: 'Contradicted' },
];

const SIFT_ROWS = [
  { type: 'sift', label: 'Evidence handling & DFIR workflows' },
  { type: 'sift', label: 'Logs, artifacts, forensic execution' },
  { type: 'sift', label: 'Trusted investigation environment' },
];

const AG_ROWS = [
  { type: 'ag', label: 'Cross-infrastructure evidence reasoning' },
  { type: 'ag', label: 'Context integrity validation' },
  { type: 'ag', label: 'Claim verdicts & self-correction' },
  { type: 'ag', label: 'Safe response planning' },
];

const ADDS = [
  { num: '01 · Evidence', title: 'Cross-Infrastructure Evidence', body: 'Power, water, network, endpoint, dependency, and WADI water-distribution context are checked together — not in isolation.', tag: '6 Layers', wide: false },
  { num: '02 · Validation', title: 'Context Integrity', body: 'Sensor context, actuator context, timestamp context, dependency context, and command-path support are validated before any claim is promoted.', tag: '5 Context Types', wide: false },
  { num: '03 · Verdicts', title: 'Claim Validation', body: 'Every claim is classified as CONFIRMED, PARTIALLY_CONFIRMED, INFERRED, UNSUPPORTED, or CONTRADICTED — tied to real tool outputs.', tag: '5 Verdict Types', wide: false },
  { num: '04 · Reasoning', title: 'Self-Correction', body: 'When the first hypothesis fails, AstraGrid records the reasoning pivot and revises the conclusion — the correction trace is part of the final report.', tag: 'Traceable', wide: false },
  { num: '05 · Response', title: 'Safe Response Planning', body: 'AstraGrid recommends response actions with evidence preservation, operations triage, monitoring, and human approval gates for high-risk changes. No action is autonomous without human gate sign-off.', tag: 'Human-Gated', wide: true },
];

const STACK = [
  { icon: '🔍', name: 'SANS SIFT', desc: 'Trusted forensic workstation. Evidence handling, artifact analysis, DFIR execution. Unchanged — still the foundation.' },
  { icon: '⚡', name: 'AstraGrid Layer', desc: 'Cyber-physical reasoning. Cross-infrastructure evidence, context integrity, claim verdicts, self-correction, response planning.' },
  { icon: '🛡️', name: 'Together', desc: 'Infrastructure incidents investigated where cybersecurity, operations, physical systems, and business continuity collide — with a full audit trail.' },
];

export default function AstraGridLearnMore() {
  return (
    <div className={styles.page}>

      {/* NAV */}
      <nav className={styles.nav}>
        <div className={styles.navInner}>
          <Link to="/" className={styles.navLogo}>ASTRA<span>GRID</span></Link>
          <Link to="/" className={styles.navBack}>Back to Home</Link>
        </div>
      </nav>

      {/* HERO */}
      <div className={styles.hero}>
        <div className={styles.wrap}>
          <div className={styles.heroEyebrow}>Protocol SIFT Extension · Learn More</div>
          <h1 className={styles.heroH1}>
            Extending SANS SIFT into<br />
            <em>Cyber-Physical Response</em>
          </h1>
          <p className={styles.heroSub}>
            AstraGrid uses the SANS SIFT workstation as the trusted forensic base, then adds cyber-physical reasoning across power, water, network, endpoint, dependency, and context-integrity layers.
          </p>
          <span className={styles.heroRule}>No direct attack claim is promoted without validated infrastructure context</span>
        </div>
      </div>

      {/* S1: WHY EXISTS */}
      <section className={styles.section}>
        <div className={styles.wrap}>
          <div className={styles.whyGrid}>
            <div className={styles.whyText}>
              <div className={styles.sectionEyebrow}>01 · Why AstraGrid Exists</div>
              <h2 className={styles.sectionTitle}>
                Critical infrastructure incidents<br />
                <em>rarely stay inside one system.</em>
              </h2>
              <p>A water anomaly may look like a direct water cyberattack. A pump disruption may actually come from upstream power failure. A Modbus signal may support investigation, but not prove causality. Endpoint activity may show compromise, but not explain the physical impact.</p>
              <p><strong>AstraGrid was built to stop AI responders from jumping to the first visible symptom.</strong></p>
              <p>Instead of treating alerts as conclusions, AstraGrid checks evidence layer by layer and asks: is this claim actually supported?</p>
            </div>
            <div>
              <div className={styles.whyCallout}>
                <div className={styles.wcLabel}>The core problem</div>
                <div className={styles.wcRule}>The first visible symptom is not always the root cause.</div>
                <div className={styles.wcSub}>Power → Network → Endpoint → Water. Each layer can mask the real attack origin. Without cross-infrastructure reasoning, responders blame the wrong system.</div>
              </div>
              <div className={styles.legendWrap}>
                <div className={styles.legend}>
                  {VERDICTS.map(v => (
                    <span key={v.label} className={`${styles.lv} ${styles[v.cls]}`}>{v.label}</span>
                  ))}
                </div>
                <p className={styles.legendNote}>Every claim in AstraGrid gets one of these verdicts — nothing is assumed.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* S2: HOW SIFT HELPS */}
      <section className={`${styles.section} ${styles.sectionAlt}`}>
        <div className={styles.wrap}>
          <div className={styles.siftGrid}>
            <div className={styles.siftText}>
              <div className={styles.sectionEyebrow}>02 · How SANS SIFT Helps</div>
              <h2 className={styles.sectionTitle}>
                The Trusted<br />
                <em>Forensic Foundation</em>
              </h2>
              <p>SANS SIFT provides the forensic workstation foundation for investigation. It gives responders a trusted environment for evidence handling, DFIR workflows, logs, artifacts, and investigation execution.</p>
              <p><strong>AstraGrid does not replace SANS SIFT.</strong></p>
              <p>AstraGrid extends the SIFT environment by adding structured cyber-physical reasoning tools. It helps the responder connect forensic evidence with infrastructure behavior, dependency paths, claim validation, and safe response planning.</p>
            </div>
            <div className={styles.siftDiagram}>
              <div className={styles.sdBar}>
                <span className={`${styles.sdDot} ${styles.sdDotR}`} />
                <span className={`${styles.sdDot} ${styles.sdDotY}`} />
                <span className={`${styles.sdDot} ${styles.sdDotG}`} />
                <span className={styles.sdLabel}>System Relationship</span>
              </div>
              <div className={styles.sdBody}>
                {SIFT_ROWS.map(r => (
                  <div key={r.label} className={`${styles.sdRow} ${styles.sdRowSift}`}>
                    <span className={`${styles.sdBadge} ${styles.sdBadgeSift}`}>SIFT</span>
                    <span className={styles.sdRowLabel}>{r.label}</span>
                  </div>
                ))}
                <div className={styles.sdDivider}>AstraGrid adds on top</div>
                {AG_ROWS.map(r => (
                  <div key={r.label} className={`${styles.sdRow} ${styles.sdRowAg}`}>
                    <span className={`${styles.sdBadge} ${styles.sdBadgeAg}`}>AG</span>
                    <span className={styles.sdRowLabel}>{r.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* S3: WHAT IT ADDS */}
      <section className={styles.section}>
        <div className={styles.wrap}>
          <div className={styles.sectionEyebrow}>03 · What AstraGrid Adds</div>
          <h2 className={styles.sectionTitle}>
            Five Capabilities<br />
            <em>SIFT Doesn&apos;t Have</em>
          </h2>
          <div className={styles.addsGrid}>
            {ADDS.map(a => (
              <div
                key={a.num}
                className={`${styles.addsCard} ${a.wide ? styles.addsCardWide : ''}`}
              >
                <div className={styles.acNum}>{a.num}</div>
                <div className={styles.acTitle}>{a.title}</div>
                <p className={styles.acBody}>{a.body}</p>
                <span className={styles.acTag}>{a.tag}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CALLOUT BANNER */}
      <div className={styles.calloutBanner}>
        <div className={styles.cbInner}>
          <div className={styles.cbLabel}>Core Rule</div>
          <div className={styles.cbText}>
            AstraGrid&apos;s rule is simple: <em>no direct attack or cascade claim</em> is promoted without validated infrastructure context.
          </div>
        </div>
      </div>

      {/* S4: BIGGER PICTURE */}
      <section className={`${styles.section} ${styles.sectionAlt}`}>
        <div className={styles.wrap}>
          <div className={styles.biggerGrid}>
            <div className={styles.biggerText}>
              <div className={styles.sectionEyebrow}>04 · The Bigger Picture</div>
              <h2 className={styles.sectionTitle}>
                SIFT as a<br />
                <em>Response Cockpit</em>
              </h2>
              <p>The bigger vision is to turn SANS SIFT from a forensic workstation into a <strong>cyber-physical response cockpit.</strong></p>
              <p>SIFT remains the trusted investigation environment. AstraGrid becomes the reasoning layer on top.</p>
              <p>Together, they can help responders investigate infrastructure incidents where cybersecurity, operations, physical systems, and business continuity collide.</p>
            </div>
            <div className={styles.biggerStack}>
              {STACK.map(s => (
                <div key={s.name} className={styles.bsItem}>
                  <div className={styles.bsIcon}>{s.icon}</div>
                  <div>
                    <div className={styles.bsName}>{s.name}</div>
                    <div className={styles.bsDesc}>{s.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* POWER + WATER CONTEXT */}
      <section className={`${styles.section} ${styles.contextSection}`}>
        <div className={styles.wrap}>
          <div className={styles.sectionEyebrow}>Infrastructure Context</div>
          <h2 className={styles.sectionTitle}>
            How AstraGrid Treats<br />
            <em>Power &amp; Water Evidence</em>
          </h2>
          <div className={styles.contextGrid}>
            <div className={`${styles.ctxCard} ${styles.ctxPower}`}>
              <div className={`${styles.ctxTag} ${styles.ctxTagPower}`}>⚡ Power Grid Layer</div>
              <div className={styles.ctxTitle}>Power Evidence Checked First</div>
              <p className={styles.ctxBody}>Power-grid evidence is checked first because upstream power disruption can silently affect downstream infrastructure. AstraGrid reviews power telemetry and confirms whether a power-side event exists before blaming the water system.</p>
            </div>
            <div className={`${styles.ctxCard} ${styles.ctxWater}`}>
              <div className={`${styles.ctxTag} ${styles.ctxTagWater}`}>💧 Water Utility Layer</div>
              <div className={styles.ctxTitle}>Water as Symptom, Not Always Cause</div>
              <p className={styles.ctxBody}>Water utility evidence is the visible symptom, but not always the root cause. AstraGrid checks SWaT, BATADAL, and WADI water-distribution context to separate water evidence from unsupported direct water cyberattack claims.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className={`${styles.section} ${styles.ctaSection}`}>
        <div className={styles.wrap}>
          <div className={styles.ctaLabel}>Ready to explore</div>
          <div className={styles.ctaTitle}>
            See AstraGrid<br /><em>In Action</em>
          </div>
          <div className={styles.ctaBtns}>
            <Link to="/demo" className={`${styles.btn} ${styles.btnSolid}`}>View Demo Case</Link>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <div className={styles.footerLogo}>ASTRA<span>GRID</span></div>
          <div className={styles.footerNote}>Protocol SIFT Extension · Cyber-Physical Response</div>
        </div>
      </footer>

    </div>
  );
}
