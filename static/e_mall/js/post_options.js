document.addEventListener('DOMContentLoaded', function () {
    // Function to toggle the display of the options menu
    function toggleMenu(button) {
        var menu = button.parentNode.querySelector('.options-menu');
        var isMenuVisible = menu.style.display == 'grid';
       
        // Hide all menus
        var allMenus = document.querySelectorAll('.options-menu');
        allMenus.forEach(function (menu) {
            menu.style.display = 'none';
        });

        // Toggle the clicked menu
        menu.style.display = isMenuVisible ? 'none' : 'grid';
    }
    // Attach event listeners to each options button
    var buttons = document.querySelectorAll('.options-button');
    buttons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent the click from propagating to the document
            toggleMenu(button);
        });
    });

    // Event listener to close the menu when clicking outside of it
    document.addEventListener('click', function (event) {
        var allMenus = document.querySelectorAll('.options-menu');
        allMenus.forEach(function (menu) {
            menu.style.display = 'none';
        });
    });

    // Prevent closing the menu when clicking inside the menu
    var menus = document.querySelectorAll('.options-menu');
    menus.forEach(function (menu) {
        menu.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent the click from propagating to the document
        });
    });
    
//this one, not so much because ChatGPT is legit   
document.querySelectorAll('.delete-button').forEach(function(button) {
    button.addEventListener('click', function() {
        var postId = button.getAttribute('data-post-id');
        if (confirm('Are you sure you want to delete this post?')) {
            deletePost(postId);
        }
    });
});


});

function deletePost(postId) {
    fetch(`/delete-post/${postId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    }).then(response => {
        if (response.ok) {
            document.querySelector(`.delete-button[data-post-id="${postId}"]`).closest('.image-container').remove();
         
        } else {
            alert('Failed to delete post.');
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}