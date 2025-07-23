import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Navbar.module.css';

function Navbar({ userName }) {
  const firstLetter = userName ? userName.charAt(0).toUpperCase() : '';

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        MindEase+
      </div>
      <ul className={styles.navLinks}>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/ChatBot">ChatBot</Link></li>
        <li><Link to="/about">About</Link></li>
        {userName ? (
          <li className={styles.profileCircle}>{firstLetter}</li>
        ) : (
          <li><Link to="/login">Login</Link></li>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
