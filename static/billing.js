document.addEventListener('DOMContentLoaded', function() {
    // Function to add a new item entry
    function addItem() {
        const container = document.getElementById('items-container');
        const itemEntry = document.createElement('div');
        itemEntry.classList.add('item-entry');
        itemEntry.innerHTML = `
            <label for="item_code">Item Code:</label>
            <input type="text" name="item" required>
            <br>
            <label for="quantity">Quantity:</label>
            <input type="number" name="quantity" required>
            <br>
            <label for="amount">Amount:</label>
            <input type="number" step="0.01" name="amount" required>
            <br>
        `;
        container.appendChild(itemEntry);
    }

    // Event listener for adding items
    document.querySelector('button#add-item-btn').addEventListener('click', addItem);

    // Function to hide success message after 5 seconds
    function hideMessage() {
        const messageElement = document.querySelector('p');
        if (messageElement) {
            setTimeout(() => {
                messageElement.style.display = 'none';
            }, 5000);  // Hide message after 5 seconds
        }
    }

    // Initial call to hide message
    hideMessage();

    // Form validation before submission
    const form = document.getElementById('billing-form');
    form.addEventListener('submit', function(event) {
        const customerName = document.getElementById('customer_name').value.trim();
        const itemEntries = document.querySelectorAll('.item-entry');

        if (!customerName) {
            alert("Please enter a customer name.");
            event.preventDefault();
            return;
        }

        let valid = true;
        itemEntries.forEach(entry => {
            const itemCode = entry.querySelector('input[name="item"]').value.trim();
            const quantity = entry.querySelector('input[name="quantity"]').value.trim();
            const amount = entry.querySelector('input[name="amount"]').value.trim();

            if (!itemCode || isNaN(quantity) || parseInt(quantity) <= 0 || isNaN(amount) || parseFloat(amount) <= 0) {
                valid = false;
            }
        });

        if (!valid) {
            alert("Please fill in all fields with valid values for each item.");
            event.preventDefault();
        }
    });

    // Dropdown Menu functionality
    const dropdownButton = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    // Always show three lines ("☰") for the dropdown button
    dropdownButton.innerHTML = '☰';

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

    // Responsive Navbar functionality
    window.addEventListener('resize', function() {
        dropdownButton.innerHTML = '☰'; // Keep showing the three-line icon regardless of the viewport width
    });

    // Initial Responsive Navbar Check
    dropdownButton.innerHTML = '☰'; // Initially set to three-line icon

    // Reset form fields and items
    function resetForm() {
        // Reset form fields
        form.reset();

        // Clear dynamically added items
        const container = document.getElementById('items-container');
        container.innerHTML = '';
    }

    // Add event listener to reset button
    const resetButton = document.getElementById('reset-button');
    resetButton.addEventListener('click', resetForm);
});
