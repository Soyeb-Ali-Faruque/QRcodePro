document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('url');
    const urlForm = document.querySelector('form');

    // Function to validate URL
    function isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (_) {
            return false;
        }
    }

    // Event listener for form submission
    urlForm.addEventListener('submit', (event) => {
        const urlValue = urlInput.value;
        if (!isValidUrl(urlValue)) {
            alert('Please enter a valid URL. Example: https://example.com');
            event.preventDefault(); // Prevent form submission
        }
    });
});
