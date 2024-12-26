document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();
        const csrfToken = document.getElementById("csrf_token").value; // CSRF token

        if (!username || !password) {
            alert("Please fill out both fields.");
            return;
        }

        try {
            const response = await fetch("/get_otp", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Response Data:", data); // Debugging output

                if (data.success) {
                    // Redirect to the provided URL
                    window.location.href = data.redirect_url;
                } else {
                    // Show error message
                    alert(data.message || "An error occurred.");
                }
            } else {
                const errorData = await response.json();
                alert(errorData.message || "An error occurred.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Unable to connect to the server.");
        }
    });
});
