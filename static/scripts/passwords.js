document.getElementById("add-password-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent default form submission

    // Collect form data
    const passwordName = document.getElementById("password-name").value;
    const passwordValue = document.getElementById("password-value").value;
    const expirationValue = document.getElementById("Expiration").value;
    const passwordCategory = document.getElementById("password-category").value;

    // Retrieve the CSRF token from the hidden input
    const csrfToken = document.querySelector("[name=csrf_token]").value;

    // Construct the data to send
    const formData = {
        password_name: passwordName,
        password_value: passwordValue,
        expiration_value: expirationValue,
        password_category: passwordCategory,
        csrf_token: csrfToken,
    };

    try {
        // Make a POST request to the Flask route
        const response = await fetch("/add_password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message); // Notify the user of success
            document.getElementById("add-password-form").reset();
        } else {
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("An unexpected error occurred. Please try again.");
    }
});
