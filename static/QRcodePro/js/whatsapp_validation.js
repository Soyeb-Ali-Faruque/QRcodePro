document.addEventListener('DOMContentLoaded', function () {
    // Initialize intl-tel-input for WhatsApp number input
    const input = document.querySelector("#whatsapp-number");
    const iti = window.intlTelInput(input, {
        initialCountry: "auto",
        separateDialCode: false, // Set this to false to show country code within the input
        nationalMode: false, // Allow international numbers
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.min.js" // Utils script for formatting
    });

    input.addEventListener('input', function () {
        const isValid = iti.isValidNumber();

        // Validate phone number based on intl-tel-input validation
        if (!isValid) {
            input.setCustomValidity('Please enter a valid phone number.');
        } else {
            input.setCustomValidity('');
        }
    });
});
