document.addEventListener('DOMContentLoaded', function () {
    const encryptionSelect = document.getElementById('encryption');
    const passwordContainer = document.getElementById('wifi-password-container');

    function updatePasswordField() {
        const selectedEncryption = encryptionSelect.value;
        if (selectedEncryption === 'nopass') {
            passwordContainer.style.display = 'none';
        } else {
            passwordContainer.style.display = 'block';
        }
    }

    // Initialize the form visibility based on the current selection
    updatePasswordField();

    // Update the form visibility when the encryption type changes
    encryptionSelect.addEventListener('change', updatePasswordField);
});
