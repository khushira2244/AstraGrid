import { Link } from "react-router-dom";
import styles from "./AstraGridArchitecture.module.css";

function AstraGridArchitecture() {
  return (
    <main className={styles.page}>
      <section className={styles.topBar}>
        <Link to="/" className={styles.logo}>
          AstraGrid
        </Link>

        <div className={styles.rightText}>SANS &amp; SIFT Station</div>
      </section>

      <section className={styles.hero}>
        <p className={styles.eyebrow}>Architecture</p>

        <h1>Protocol SIFT Cyber-Physical Investigation Extension</h1>

        <p>
          AstraGrid extends SANS SIFT and Protocol SIFT with structured
          cyber-physical reasoning tools for power, water, endpoint, network,
          and dependency evidence.
        </p>

        <div className={styles.actions}>
          <Link to="/" className={styles.btnGhost}>
            Back Home
          </Link>

          <Link to="/demo" className={styles.btnSolid}>
            View Demo Case
          </Link>
        </div>
      </section>

      <section className={styles.imageWrap}>
        <img
          src="/architecture.png"
          alt="AstraGrid architecture diagram showing Protocol SIFT cyber-physical investigation extension"
          className={styles.archImage}
        />
      </section>
    </main>
  );
}

export default AstraGridArchitecture;