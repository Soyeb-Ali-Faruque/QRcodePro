document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.qrform');
    const emailInput = document.getElementById('email-address');

    form.addEventListener('submit', function (event) {
        const emailValue = emailInput.value;
        if (!isValidEmail(emailValue)) {
            event.preventDefault(); // Prevent form submission
            alert('Please enter a valid email address.');
            emailInput.focus();
        }
    });

    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }
});
