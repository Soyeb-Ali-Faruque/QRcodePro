document.querySelectorAll('.customize-link').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        const customizationContainer = this.nextElementSibling;
        if (customizationContainer.classList.contains('hidden')) {
            customizationContainer.classList.remove('hidden');
            this.textContent = 'Hide customization options';
        } else {
            customizationContainer.classList.add('hidden');
            this.textContent = 'Tap here to customize your QR code';
        }
    });
});

document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const preview = event.target.closest('form').querySelector('.logo-preview');

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        } else {
            preview.src = '#';
            preview.style.display = 'none';
        }
    });
});

document.querySelector('#logo-upload').addEventListener('change', function(event) {
const file = event.target.files[0];
const logoShapeContainer = document.getElementById('logo-shape-container');

if (file) {
    logoShapeContainer.classList.remove('hidden'); // Show logo shape selection
    const preview = event.target.closest('form').querySelector('.logo-preview');

    const reader = new FileReader();
    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
    }
    reader.readAsDataURL(file);
} else {
    logoShapeContainer.classList.add('hidden'); // Hide if no file is selected
}
});
document.querySelector('#logo-shape').addEventListener('change', function(event) {
const selectedShape = event.target.value;
const logoCornerContainer = document.getElementById('logo-corner-container');

if (selectedShape === 'square' || selectedShape === 'rectangular') {
    logoCornerContainer.style.display = 'block'; // Show the logo corner container
} else {
    logoCornerContainer.style.display = 'none'; // Hide the logo corner container
}
});

document.querySelector('#logo-upload').addEventListener('change', function(event) {
const file = event.target.files[0];
const logoShapeContainer = document.getElementById('logo-shape-container');

if (file) {
    logoShapeContainer.classList.remove('hidden'); // Show logo shape selection
    const preview = event.target.closest('form').querySelector('.logo-preview');

    const reader = new FileReader();
    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
    }
    reader.readAsDataURL(file);
} else {
    logoShapeContainer.classList.add('hidden'); // Hide if no file is selected
    document.getElementById('logo-corner-container').style.display = 'none'; // Ensure the logo corner container is also hidden
}
});
document.querySelector('#logo-upload').addEventListener('change', function(event) {
const file = event.target.files[0];
const logoShapeContainer = document.getElementById('logo-shape-container');

if (file) {
    logoShapeContainer.style.display = 'block'; // Show the logo shape container when a file is uploaded
    const preview = event.target.closest('form').querySelector('.logo-preview');

    const reader = new FileReader();
    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
    }
    reader.readAsDataURL(file);
} else {
    logoShapeContainer.style.display = 'none'; // Hide the logo shape container if no file is selected
}
});

document.querySelector('.qrform').addEventListener('submit', function(event) {
    const fillColor = document.getElementById('fill-color').value;
    const bgColor = document.getElementById('background-color').value;

    if (fillColor.toLowerCase() === bgColor.toLowerCase()) {
        event.preventDefault(); // Prevent form submission
        alert('Fill color and background color cannot be the same. Please choose different colors.');
    }
});

