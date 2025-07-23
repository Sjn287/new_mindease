import React from "react";
import { useParams } from "react-router-dom";
import NavBar from "../NavBar/NavBar";
import styles from './HomePage.module.css'

const HomePage = () => {
  let { user } = useParams();
  return (
    <>
      <NavBar userName={user} />
      <section className={styles.hero}>
        <h1>Welcome back, {user.charAt(0).toUpperCase()+user.slice(1)}!</h1>
        <p>Your personal mental wellness companion.</p>
        <button>Start Session</button>
      </section>

      <section className={styles.features}>
        <div className={styles.featurecard}>
          <h2>Mood Tracker</h2>
          <p>Track your mood and progress daily.</p>
        </div>
        <div className={styles.featurecard}>
          <h2>Mindful Exercises</h2>
          <p>Guided exercises to ease your mind.</p>
        </div>
        <div className={styles.featurecard}>
          <h2>Expert Guidance</h2>
          <p>Connect with wellness experts anytime.</p>
        </div>
      </section>

      <footer>
        <p>MindEase+ © 2025</p>
      </footer>
    </>
  );
};

export default HomePage;
