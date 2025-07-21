import styles from "./LoginPage.module.css";
import axios from "axios"


function LoginButton() {
  const email = document.getElementById("emailInput").value;
  const password = document.getElementById("passwordInput").value;

  axios.get("http://localhost:8080/users")
    .then(response => {
      const users = response.data;
      const found = users.find(u => u.email === email && u.password === password);

      if (found) {
        alert("Login successful!");
        // TODO: Redirect to dashboard
      } else {
        alert("Invalid email or password.");
      }
    })
    .catch(error => {
      console.error(error);
      alert("Error checking login.");
    });
}


function LoginPage() {
  return (
    <div className={styles.container}>
      {/* Left: form */}

      <div className={styles.left}>
        <div className={styles.title}>
          <img src="YOUR_LOGO_URL_HERE" alt="Logo" />
          <h2>MindEase+</h2>
        </div>
        <div className={styles.formContent}>
          <h2>Welcome Back</h2>
          <h5>Please enter your details</h5>

          <div className={styles.emailContainer}>
            <h3>Email Address</h3>
            <input type="text" name="email" required id="emailInput"/>
          </div>

          <div className={styles.passwordContainer}>
            <h3>Password</h3>
            <input type="password" name="password" required id="passwordInput"/>
          </div>

          <div className={styles.forgotPassword}>
            <p>Forgot Password?</p>
          </div>

          <div className={styles.signButton}>
            <button onClick={LoginButton}>Login</button>
          </div>
        </div>
      </div>

      {/* Right: image */}
      <div className={styles.right}>
        <img
          src="YOUR_IMAGE_URL_HERE"
          alt="Illustration"
          className={styles.illustration}
        />
      </div>
    </div>
  );
}

export default LoginPage;
