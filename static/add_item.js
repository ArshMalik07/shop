document.addEventListener('DOMContentLoaded', function() {
    // Form Validation
    const form = document.querySelector('form[action=""]');
    form.addEventListener('submit', function(event) {
        const itemName = document.getElementById('item_name').value.trim();
        const quantity = document.getElementById('quantity').value.trim();
        const uniqueCode = document.getElementById('unique_code').value.trim();
        
        if (itemName === '' || quantity === '' || uniqueCode === '') {
            event.preventDefault();
            alert('All fields must be filled out.');
        } else if (isNaN(quantity) || parseInt(quantity) <= 0) {
            event.preventDefault();
            alert('Quantity must be a positive number.');
        }
    });

    // Dropdown Menu
    const dropdownButton = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownButton.innerHTML = '☰'; // Always show three lines

    dropdownButton.addEventListener('click', function(event) {
        dropdownContent.classList.toggle('show');
        event.stopPropagation();
    });

    // Close the dropdown if the user clicks outside of it
    window.addEventListener('click', function(event) {
        if (!event.target.matches('.dropbtn')) {
            if (dropdownContent.classList.contains('show')) {
                dropdownContent.classList.remove('show');
            }
        }
    });

    // Hide the success message after 5 seconds
    const messageElement = document.querySelector('p');
    if (messageElement) {
        setTimeout(() => {
            messageElement.style.display = 'none';
        }, 3000);
    }
});
