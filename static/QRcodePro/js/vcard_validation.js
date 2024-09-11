document.addEventListener('DOMContentLoaded', function () {
    // Initialize intl-tel-input for VCard phone number input
    const phoneInput = document.querySelector("#vcard-phone");
    const iti = window.intlTelInput(phoneInput, {
        initialCountry: "auto",
        separateDialCode: false, // Show country code separate from input
        nationalMode: false, // Allow international numbers
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.min.js" // Utils script for formatting
    });

    phoneInput.addEventListener('input', function () {
        const isValid = iti.isValidNumber();

        // Validate phone number based on intl-tel-input validation
        if (!isValid) {
            phoneInput.setCustomValidity('Please enter a valid phone number.');
        } else {
            phoneInput.setCustomValidity('');
        }
    });
});
