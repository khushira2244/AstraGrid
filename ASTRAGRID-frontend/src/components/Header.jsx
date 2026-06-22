import { Link } from "react-router-dom";
import styles from "./Header.module.css";

function Header() {
  return (
    <header className={styles.header}>
      <Link to="/" className={styles.logo}>
        AstraGrid
      </Link>

      <div className={styles.rightLogoWrap}>
        <img
          src="/logo.png"
          alt="SANS & SIFT"
          className={styles.rightLogo}
        />
      </div>
    </header>
  );
}

export default Header;