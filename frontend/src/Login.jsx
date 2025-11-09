import "./Login.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
function Login() {
  async function checkUser(e) {
    e.preventDefault();
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    const apiurl = `${backendUrl}/login/search`;
    const parms = new URLSearchParams({
      email,
      password,
    });
    const res = await fetch(`${apiurl}?${parms.toString()}`, {
      method: "GET",
    });
    const data = await res;

    if (data.status == 200) {
      alert("Login successful!");
      localStorage.setItem("userEmail", email);
      navigate("/Dashboard");
    } else if (data.status == 201) {
      alert("invalid email id or password");
    } else {
      alert("you are not already signup");
      navigate("/signup");
    }
  }
  const [email, setMail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  return (
    <>
      <form>
        <h1>Login</h1>
        <input
          type="email"
          placeholder="Enter your email id"
          onChange={(e) => setMail(e.target.value)}
          required
        />
        <input
          type="Password"
          placeholder="Enter your password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button id="submit" onClick={checkUser}>
          submit
        </button>
        <div>
          <p>If you don't have account </p>
          <Link to="/SignUp">Sign In</Link>
        </div>
      </form>
    </>
  );
}
export default Login;
