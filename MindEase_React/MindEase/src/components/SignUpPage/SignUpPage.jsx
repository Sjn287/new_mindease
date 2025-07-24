import axios from "axios";
import styles from "./SignUpPage.module.css";
import { useNavigate,Link } from "react-router-dom";


function SignUpPage() {
  let navigate = useNavigate();
  

  function handleSignup() {
  const name = document.getElementById("signupName").value.trim();
  const age = document.getElementById("signupAge").value.trim();
  const phonenumber = document.getElementById("signupNumber").value.trim();
  const email = document.getElementById("signupEmail").value.trim();
  const password = document.getElementById("signupPassword").value.trim();
  const gender = document.getElementById("signupGender").value;

  // Check for empty fields
  if (!name || !age || !phonenumber || !email || !password || !gender) {
    alert("Please fill in all fields.");
    return;
  }

  // Validate age is positive number
  if (isNaN(age) || Number(age) <= 0) {
    alert("Please enter a valid age.");
    return;
  }

  // Validate phone number is numeric and reasonable length
  if (!/^\d{7,15}$/.test(phonenumber)) {
    alert("Please enter a valid phone number.");
    return;
  }

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  // Validate password minimum length
  if (password.length < 6) {
    alert("Password must be at least 6 characters.");
    return;
  }

  // Validate gender
  if (gender === "") {
    alert("Please select a gender.");
    return;
  }

  // If all valid, send request
  axios.post("http://localhost:8080/users", {
    name,
    age: Number(age),
    phonenumber,
    email,
    password,
    gender
  })
    .then(() => {
      alert("User signed up successfully!");
      navigate("/");
    })
    .catch((error) => {
      console.error(error);
      alert("Error signing up.");
    });
}


  return (
    <div className={styles.container}>
      {/* Left: Sign Up Form */}
      <div className={styles.left}>
        <div className={styles.title}>
          <img src="YOUR_LOGO_URL_HERE" alt="Logo" />
          <h2>MindEase+</h2>
        </div>
        <div className={styles.formContent}>
          <h2>Sign Up</h2>
          <h5>Please enter your details</h5>

          <div className={styles.formGroup}>
            <label>Name</label>
            <input type="text" id="signupName" placeholder="Enter your name" />
          </div>

          <div className={styles.formGroup}>
            <label>Age</label>
            <input type="number" id="signupAge" placeholder="Enter your age" />
          </div>

          <div className={styles.formGroup}>
            <label>Phone Number</label>
            <input type="number" id="signupNumber" placeholder="Enter your phone number" />
          </div>

          <div className={styles.formGroup}>
            <label>Email</label>
            <input type="email" id="signupEmail" placeholder="Enter your email" />
          </div>

          <div className={styles.formGroup}>
            <label>Password</label>
            <input type="password" id="signupPassword" placeholder="Enter your password" />
          </div>

          <div className={styles.formGroup}>
            <label>Gender</label>
            <select id="signupGender">
              <option value="" disabled selected>Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          <button onClick={handleSignup} className={styles.signupButton}>Sign Up</button>

          <p className={styles.loginLink}>
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </div>
      </div>

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

export default SignUpPage;