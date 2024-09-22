document.addEventListener('DOMContentLoaded', function() {
    // Form Validation for Search Form
    const searchForm = document.querySelector('.search-form');
    const searchInput = searchForm.querySelector('input[name="search"]');

    searchForm.addEventListener('submit', function(event) {
        const query = searchInput.value.trim();
        if (query === '') {
            alert('Please enter a search query.');
            event.preventDefault();
        }
    });

    // Dropdown Menu Functionality
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

    // Responsive Navbar Toggle
    function updateNavbar() {
        dropdownButton.innerHTML = '☰'; // Keep showing the three-line icon regardless of the viewport width
    }

    // Initial Navbar Setup
    updateNavbar();
    window.addEventListener('resize', updateNavbar);

    // Function to Reset Search Form
    function resetSearch() {
        searchInput.value = '';
    }

    // Add Reset Button to Search Form
    const resetButton = document.createElement('button');
    resetButton.type = 'button';
    resetButton.textContent = 'Reset';
    resetButton.classList.add('reset-button');
    resetButton.addEventListener('click', resetSearch);
    searchForm.appendChild(resetButton);

    // Additional Styling for Reset Button
    const resetButtonStyles = `
        .reset-button {
            padding: 10px 20px;
            margin-left: 10px;
            border: none;
            border-radius: 5px;
            background-color: #dc3545;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
        }
        .reset-button:hover {
            background-color: #c82333;
            transform: translateY(-2px);
        }
    `;
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = resetButtonStyles;
    document.head.appendChild(styleSheet);

    // Function to Highlight Table Rows on Hover
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            row.style.backgroundColor = '#f1f1f1';
        });
        row.addEventListener('mouseleave', function() {
            row.style.backgroundColor = '';
        });
    });

    // Handle Table Sorting (Optional)
    const tableHeaders = document.querySelectorAll('table thead th');
    tableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            sortTable(header.cellIndex);
        });
    });

    function sortTable(columnIndex) {
        const table = document.querySelector('table tbody');
        const rows = Array.from(table.rows);
        const ascending = table.getAttribute('data-sort-asc') === 'true';
        rows.sort((a, b) => {
            const aText = a.cells[columnIndex].textContent;
            const bText = b.cells[columnIndex].textContent;
            return ascending ? aText.localeCompare(bText) : bText.localeCompare(aText);
        });
        rows.forEach(row => table.appendChild(row));
        table.setAttribute('data-sort-asc', !ascending);
    }
});
