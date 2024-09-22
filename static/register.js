document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (!username) {
            showError(usernameInput, 'Username is required');
        } else if (username.length < 3) {
            showError(usernameInput, 'Username must be at least 3 characters long');
        } else if (!password) {
            showError(passwordInput, 'Password is required');
        } else if (password.length < 6) {
            showError(passwordInput, 'Password must be at least 6 characters long');
        } else {
            // Submit the form if validation passes
            form.submit();
        }
    });

    function showError(input, message) {
        const formControl = input.parentElement;
        const errorMessage = formControl.querySelector('span');

        // Add error message
        if (!errorMessage) {
            const span = document.createElement('span');
            span.innerText = message;
            span.classList.add('error-message');
            formControl.appendChild(span);
        }

        // Add error styling
        formControl.classList.add('error');
    }

    // Remove error styling when input is focused
    usernameInput.addEventListener('focus', clearError);
    passwordInput.addEventListener('focus', clearError);

    function clearError() {
        const formControl = this.parentElement;
        formControl.classList.remove('error');
        const errorMessage = formControl.querySelector('span');
        if (errorMessage) {
            formControl.removeChild(errorMessage);
        }
    }
});
