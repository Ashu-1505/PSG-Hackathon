    document.addEventListener("DOMContentLoaded", function () {
        const profileIcon = document.getElementById("profileDropdownToggle");
        const dropdownMenu = document.getElementById("profileDropdownMenu");

        // Toggle dropdown menu visibility
        profileIcon.addEventListener("click", function () {
            dropdownMenu.style.display = 
                dropdownMenu.style.display === "block" ? "none" : "block";
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", function (event) {
            if (!profileIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.style.display = "none";
            }
        });
    });
