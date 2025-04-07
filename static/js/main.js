// Слайдери для Популярне
const movieSlides = document.querySelectorAll('.movie-slide');
const movieNextBtn = document.getElementById('movie-next');
const moviePrevBtn = document.getElementById('movie-prev');

let movieIndex = 0;

function showMovieSlide(index) {
  movieSlides.forEach(slide => slide.classList.remove('active'));
  movieSlides[index].classList.add('active');
}

movieNextBtn.addEventListener('click', () => {
  movieIndex = (movieIndex + 1) % movieSlides.length;
  showMovieSlide(movieIndex);
});

moviePrevBtn.addEventListener('click', () => {
  movieIndex = (movieIndex - 1 + movieSlides.length) % movieSlides.length;
  showMovieSlide(movieIndex);
})
showMovieSlide(movieIndex);

// Слайдери для Рекомендації
  // const items = document.querySelectorAll('.item');
  // const nextBtn = document.getElementById('nextBtn');
  // const prevBtn = document.getElementById('prevBtn');

  // const itemsPerPage = 4;
  // let currentIndex = 0;

  // function updateVisibleItems() {
  //   items.forEach(item => item.classList.remove('show'));

  //   for (let i = currentIndex; i < currentIndex + itemsPerPage; i++) {
  //     if (items[i]) {
  //       items[i].classList.add('show');
  //     }
  //   }
  // }

  // nextBtn.addEventListener('click', () => {
  //   currentIndex += itemsPerPage;
  //   if (currentIndex >= items.length) {
  //     currentIndex = 0;
  //   }
  //   updateVisibleItems();
  // });

  // prevBtn.addEventListener('click', () => {
  //   currentIndex -= itemsPerPage;
  //   if (currentIndex < 0) {
  //     // Переходимо до останнього повного набору
  //     currentIndex = Math.max(0, items.length - itemsPerPage);
  //   }
  //   updateVisibleItems();
  // });

  // // Показати перші
  // updateVisibleItems();

  const container = document.getElementById('container');

let isDown = false;
let startX;
let scrollLeft;

container.addEventListener('mousedown', (e) => {
  isDown = true;
  container.classList.add('active'); // для стилів grab
  startX = e.pageX - container.offsetLeft;
  scrollLeft = container.scrollLeft;
});

container.addEventListener('mouseleave', () => {
  isDown = false;
  container.classList.remove('active');
});

container.addEventListener('mouseup', () => {
  isDown = false;
  container.classList.remove('active');
});

container.addEventListener('mousemove', (e) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - container.offsetLeft;
  const walk = (x - startX) * 1.5; // коефіцієнт швидкості
  container.scrollLeft = scrollLeft - walk;
});



  
