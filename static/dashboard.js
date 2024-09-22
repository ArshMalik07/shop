document.addEventListener('DOMContentLoaded', function() {
    // Functionality for logging out
    const logoutButton = document.getElementById('logout');
    logoutButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        // Send a request to logout route
        fetch('/logout', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Redirect to the login page after successful logout
                window.location.href = '/login';
            } else {
                console.error('Logout failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Functionality for dynamically adjusting button styles
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            button.style.backgroundColor = '#0056b3';
            button.style.transform = 'translateY(-2px)';
        });
        button.addEventListener('mouseleave', function() {
            button.style.backgroundColor = '#007bff';
            button.style.transform = 'none';
        });
    });

});
