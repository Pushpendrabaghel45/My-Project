/* ================= SCROLL ANIMATION ================= */

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show');
      }
    });
  },
  { threshold: 0.15 }
);

document.querySelectorAll(
  '.hero-content, .hero-image-wrapper, .category-item, .living-box, .product-card'
).forEach(el => observer.observe(el));


/* ================= NAVBAR ACTIVE LINK ================= */
const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach(link => {
  link.addEventListener('click', () => {
    navLinks.forEach(l => l.classList.remove('active'));
    link.classList.add('active');
  });
});


// Counter Animation
const counters = document.querySelectorAll('.counter');

counters.forEach(counter => {
  const updateCount = () => {
    const target = +counter.getAttribute('data-target');
    const count = +counter.innerText;
    const increment = target / 200;

    if (count < target) {
      counter.innerText = Math.ceil(count + increment);
      setTimeout(updateCount, 10);
    } else {
      counter.innerText = target;
    }
  };
  updateCount();
});


// Countdown Timer
const endDate = new Date();
endDate.setDate(endDate.getDate() + 5);

function updateCountdown() {
  const now = new Date().getTime();
  const distance = endDate - now;

  document.getElementById("days").innerText = Math.floor(distance / (1000 * 60 * 60 * 24));
  document.getElementById("hours").innerText = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  document.getElementById("minutes").innerText = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  document.getElementById("seconds").innerText = Math.floor((distance % (1000 * 60)) / 1000);
}
setInterval(updateCountdown, 1000);
updateCountdown();



// Fade-up on Scroll
const fadeElements = document.querySelectorAll('.fade-up');

window.addEventListener('scroll', () => {
  fadeElements.forEach(el => {
    const position = el.getBoundingClientRect().top;
    const screenHeight = window.innerHeight;

    if (position < screenHeight - 100) {
      el.classList.add('show');
    }
  });
});
