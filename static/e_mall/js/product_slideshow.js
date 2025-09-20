const slideshow = document.querySelector('.slideshow');
const images = slideshow.querySelectorAll('img');
const prevButton = slideshow.querySelector('.prev');
const nextButton = slideshow.querySelector('.next');

let currentIndex = 0;
let startX = 0;
let endX = 0;
const SWIPE_THRESHOLD = 50; // Adjust this value for swipe sensitivity

function startSlideshow() {
  images[currentIndex].classList.add('active');
  if (images.length === 1) return;

  prevButton.addEventListener('click', () => {
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    images[currentIndex].classList.add('active');
  });

  nextButton.addEventListener('click', () => {
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].classList.add('active');
  });

  // Swipe on mobile
  slideshow.addEventListener(
    'touchstart',
    (e) => {
      startX = e.touches[0].clientX;
    },
    { passive: true }
  );

  slideshow.addEventListener(
    'touchend',
    (e) => {
      endX = e.changedTouches[0].clientX;
      handleSwipe();
    },
    { passive: true }
  );
}

function handleSwipe() {
  const distance = endX - startX;
  if (distance > SWIPE_THRESHOLD) {
    // Swipe right
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    images[currentIndex].classList.add('active');
  } else if (distance < -SWIPE_THRESHOLD) {
    // Swipe left
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % images.length;
    images[currentIndex].classList.add('active');
  }
}

startSlideshow();