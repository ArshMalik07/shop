// document.addEventListener('DOMContentLoaded', function() {
//     const searchForm = document.querySelector('.search-form');
//     const searchInput = document.getElementById('search');
//     const itemsTable = document.querySelector('tbody');

//     searchForm.addEventListener('submit', function(event) {
//         event.preventDefault();  // Prevent the default form submission

//         const searchTerm = searchInput.value.trim();
//         if (searchTerm) {
//             // Make a GET request to the /stock endpoint with the search term
//             fetch(`/stock?itemname=${encodeURIComponent(searchTerm)}`, {
//                 method: 'GET',
//                 headers: {
//                     'X-Requested-With': 'XMLHttpRequest'  // Indicate that this is an AJAX request
//                 }
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();  // Parse the JSON response
//             })
//             .then(data => {
//                 // Clear the table before adding new rows
//                 itemsTable.innerHTML = '';

//                 if (data.items && data.items.length > 0) {
//                     // Iterate over each item and create a row in the table
//                     data.items.forEach(item => {
//                         const row = document.createElement('tr');
//                         row.innerHTML = `
//                             <td>${item.name}</td>
//                             <td>${item.quantity}</td>
//                             <td>${item.unique_code}</td>
//                             <td>
//                                 <form action="/delete_item" method="post">
//                                     <input type="hidden" name="unique_code" value="${item.unique_code}">
//                                     <button type="submit" class="delete-button">Delete</button>
//                                 </form>
//                             </td>
//                         `;
//                         itemsTable.appendChild(row);
//                     });
//                 } else {
//                     // If no items are found, display a message in the table
//                     const row = document.createElement('tr');
//                     row.innerHTML = '<td colspan="4">No items found.</td>';
//                     itemsTable.appendChild(row);
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 alert('An error occurred while fetching the items. Please try again later.');
//             });
//         } else {
//             alert('Please enter an item name to search.');
//         }
//     });
    
// });

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.getElementById('search');
    const itemsTable = document.querySelector('tbody');

    // Define the confirmDelete function
    function confirmDelete() {
        return confirm("Are you sure you want to delete this item?");
    }

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        const searchTerm = searchInput.value.trim();
        if (searchTerm) {
            // Make a GET request to the /stock endpoint with the search term
            fetch(`/stock?itemname=${encodeURIComponent(searchTerm)}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'  // Indicate that this is an AJAX request
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();  // Parse the JSON response
            })
            .then(data => {
                // Clear the table before adding new rows
                itemsTable.innerHTML = '';

                if (data.items && data.items.length > 0) {
                    // Iterate over each item and create a row in the table
                    data.items.forEach(item => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${item.name}</td>
                            <td>${item.quantity}</td>
                            <td>${item.unique_code}</td>
                            <td>
                                <form action="/delete_item" method="post" class="delete-form">
                                    <input type="hidden" name="unique_code" value="${item.unique_code}">
                                    <button type="submit" class="delete-button">Delete</button>
                                </form>
                            </td>
                        `;
                        itemsTable.appendChild(row);
                    });

                    // Add event listeners to the delete forms
                    const deleteForms = document.querySelectorAll('.delete-form');
                    deleteForms.forEach(form => {
                        form.addEventListener('submit', function(event) {
                            event.preventDefault(); // Prevent default form submission
                            if (confirmDelete()) {
                                form.submit(); // Submit the form if confirmed
                            }
                        });
                    });
                } else {
                    // If no items are found, display a message in the table
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="4">No items found.</td>';
                    itemsTable.appendChild(row);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while fetching the items. Please try again later.');
            });
        } else {
            alert('Please enter an item name to search.');
        }
    });
});
