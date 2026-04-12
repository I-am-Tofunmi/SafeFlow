document.addEventListener("DOMContentLoaded", () => {
  const API_BASE_URL = window.location.origin;

  // --- SIGN UP LOGIC ---
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      const phone = document.getElementById("phone").value;
      const fullName = document.getElementById("full_name").value;
      const password = document.getElementById("password").value;
      const terms = document.getElementById("terms").checked;

      if (!terms) {
        alert("You must agree to the Terms of Service.");
        return;
      }

      try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            phone_number: phone,
            full_name: fullName,
            password: password
          }),
        });

        const data = await response.json();

        if (response.ok) {
          alert("Account created successfully! Please sign in.");
          window.location.href = "main.html"; // Redirect to login
        } else {
          alert(`Error: ${data.detail || "Failed to create account"}`);
        }
      } catch (error) {
        console.error("Signup error:", error);
        alert("A network error occurred. Please try again.");
      }
    });
  }

  // --- LOG IN LOGIC ---
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const phone = document.getElementById("phone_number").value;
      const password = document.getElementById("password").value;

      try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            phone_number: phone,
            password: password
          }),
        });

        const data = await response.json();

        if (response.ok) {
          // Save session state
          localStorage.setItem("safeflow_token", data.token);
          localStorage.setItem("safeflow_user_id", data.user_id);
          localStorage.setItem("safeflow_full_name", data.full_name);
          localStorage.setItem("safeflow_trust_score", data.current_trust_score);

          // Head to dashboard
          window.location.href = "homepage.html";
        } else {
          alert(`Error: ${data.detail || "Invalid credentials"}`);
        }
      } catch (error) {
        console.error("Login error:", error);
        alert("A network error occurred. Please try again.");
      }
    });
  }

});
