document.addEventListener('DOMContentLoaded', function() {
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

    // Responsive Navbar functionality (not needed here since the button always shows "☰")
    function updateNavbar() {
        dropdownButton.innerHTML = '☰'; // Keep showing the three-line icon regardless of the viewport width
    }

    // Initial Navbar Setup
    updateNavbar();
    window.addEventListener('resize', updateNavbar);
});
