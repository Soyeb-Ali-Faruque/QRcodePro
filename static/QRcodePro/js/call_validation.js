document.addEventListener('DOMContentLoaded', function () {
    const callInput = document.querySelector("#phone-number");

    const callIti = window.intlTelInput(callInput, {
        initialCountry: "auto",
        separateDialCode: false,
        nationalMode: false,
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.min.js"
    });

    callInput.addEventListener('input', function () {
        const isValid = callIti.isValidNumber();
        if (!isValid) {
            callInput.setCustomValidity('Please enter a valid phone number.');
        } else {
            callInput.setCustomValidity('');
        }
    });
});
