document.addEventListener('DOMContentLoaded', function () {
    const countrySelect = document.getElementById('id_country');
    const locationSelect = document.getElementById('id_location');
    
    countrySelect.addEventListener('change', function () {
        const countryId = this.value;

        // Clear existing locations
        locationSelect.innerHTML = '';
        async function loadMorePosts() {
        if (countryId) {
            try {
                const response = await fetch(`/get-locations/?country_id=${countryId}`, 
                    { 
                        headers: { 
                        accept: 'application/json' 
                        } 
                    });         
                
                if (!response.ok) throw new Error('Network response was not ok');   
                  
                const data = await response.json();
                  
                
                locationSelect.innerHTML = data.html;
                locationSelect.style.backgroundColor='#5d997d';
                locationSelect.style.borderRadius='10px';
                  
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
        
    };
    
};
loadMorePosts();
});

});