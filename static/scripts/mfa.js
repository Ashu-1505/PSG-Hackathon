document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("otp-form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const otp = document.getElementById("otp").value.trim();
        const csrfToken = document.getElementById("csrf_token").value; // CSRF token


        if (!otp) {
            alert("Please enter the OTP.");
            return;
        }

        try {
            const response = await fetch("/verify_otp", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ otp }),
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    alert("OTP verified successfully!");
                    window.location.href = data.redirect_url; // Redirect to the next page
                } else {
                    alert(data.message || "Invalid OTP.");
                }
            } else {
                alert("An error occurred while verifying the OTP.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Unable to connect to the server.");
        }
    });
});

function ResendOTP() {
    fetch("/resend_otp", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("OTP has been resent to your registered email.");
            } else {
                alert("Failed to resend OTP. Please try again later.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Unable to connect to the server.");
        });
}
