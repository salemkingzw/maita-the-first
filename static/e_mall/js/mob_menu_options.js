document.addEventListener('DOMContentLoaded', function () {
    // Function to toggle the display of the options menu
    function toggleMenu(button) {
        var menu = button.parentNode.querySelector('.mob-options-menu');
        var isMenuVisible = menu.style.display == 'grid';
       
        // Hide all menus
        var allMenus = document.querySelectorAll('.mob-options-menu');
        allMenus.forEach(function (menu) {
            menu.style.display = 'none';
        });

        // Toggle the clicked menu
        menu.style.display = isMenuVisible ? 'none' : 'grid';
    }
    // Attach event listeners to each options button
    var buttons = document.querySelectorAll('.mob-options-button');
    buttons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent the click from propagating to the document
            toggleMenu(button);
        });
    });

    // Event listener to close the menu when clicking outside of it
    document.addEventListener('click', function (event) {
        var allMenus = document.querySelectorAll('.mob-options-menu');
        allMenus.forEach(function (menu) {
            menu.style.display = 'none';
        });
    });

    // Prevent closing the menu when clicking inside the menu
    var menus = document.querySelectorAll('.mob-options-menu');
    menus.forEach(function (menu) {
        menu.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent the click from propagating to the document
        });
    });
});