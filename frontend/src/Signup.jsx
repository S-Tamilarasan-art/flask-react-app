import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "./Signup.css";

function Signup() {
  async function submit(event) {
    event.preventDefault();

    const form = event.target.form || event.target.closest("form"); //  get the form element

    if (!form.checkValidity()) {
      //  check validity before sending
      form.reportValidity(); //  show browser validation messages
      return;
    }
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL;
      const response = await fetch(`${backendUrl}/signup/post`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          age: age,
          address: address,
          email: email,
          mobile: mobile,
          password: password,
        }),
      });
      const data = await response.json();
      if (data.signup) {
        alert("Signup sucessfully");
        navigate("/login");
      } else if (data.login) {
        alert("user already exists ");
        navigate("/dashboard");
      }
    } catch (err) {
      console.error(err);
    }
  }

  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [address, setAddress] = useState("");
  const [email, setEmail] = useState("");
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  return (
    <>
      <form>
        <h1>Sign Up</h1>
        <input
          type="text"
          placeholder="Name"
          pattern="^[A-Za-z\s]{3,}$"
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Age"
          min="10"
          max="99"
          onChange={(e) => setAge(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Address"
          onChange={(e) => setAddress(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="E-mail id"
          pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
          title="Please enter a valid email address (e.g., user@example.com)."
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="tel"
          placeholder="Mobile Number"
          pattern="\d{10}"
          title="Mobile number must be exactly 10 digits"
          onChange={(e) => setMobile(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Enter Password"
          minLength="6"
          pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
          title={`Password must have at least:
            - 1 uppercase letter
            - 1 lowercase letter
            - 1 number
            - 1 special character (@$!%*?&)
            - Minimum 6 characters`}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button className="SignUp" onClick={submit}>
          Sign Up
        </button>
        <div>
          <p>Already have an account ? </p>
          <Link to="/login">Login</Link>
        </div>
      </form>
    </>
  );
}

export default Signup;
