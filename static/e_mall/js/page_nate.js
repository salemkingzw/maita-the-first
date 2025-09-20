document.addEventListener('DOMContentLoaded', function () {
    let page = 1;
    let loading = false;
    let moreposts = true;
    let responses='';   

    async function loadMorePosts() {
        if (loading || !moreposts) return;
        loading = true;
        document.getElementById('loading').style.display = 'block';
        page += 1;       
            
            try {
            const response = await fetch(responses, 
                { 
                    headers: { 
                    accept: 'application/json' 
                    } 
                });         
            
            if (!response.ok) throw new Error('Network response was not ok');   
              
            const data = await response.json();
            moreposts=data.has_more_pages;     
              
            if(data.has_more_pages){
            const postContainer = document.getElementById('post-container');    
            postContainer.insertAdjacentHTML('beforeend', data.html); 
            }
            paginationUrl=data.pagination_url;
            console.log(paginationUrl);
            responses=paginationUrl+page;
            console.log(responses)
            
            
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        } finally {
            loading = false;
            document.getElementById('loading').style.display = 'none';
        }
        }

    window.addEventListener('scroll', function () {
        if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 200) {
            loadMorePosts();
        }
    });
});