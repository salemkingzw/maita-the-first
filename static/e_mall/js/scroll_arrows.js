document.addEventListener('DOMContentLoaded', function(){
const container = document.querySelector('.int-products-bar');
const scrollLeft = document.querySelector('.scroll-left');
const scrollRight = document.querySelector('.scroll-right');

scrollLeft.addEventListener('click', () => {
    container.scrollBy({ left: -100, behavior: 'smooth' });
});

scrollRight.addEventListener('click', () => {
    container.scrollBy({ left: 100, behavior: 'smooth' });
});
});