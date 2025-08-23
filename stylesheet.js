// Auto-tag paragraphs + list items
document.querySelectorAll('.about-info p, .about-info li, .about-info img, .data-circle').forEach(el => {
  el.classList.add('fade-on-scroll');
});

// Observer to toggle class
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
    } else {
      entry.target.classList.remove('is-visible'); // fade-out when leaving
    }
  });
}, {
  threshold: 0.15
});

document.querySelectorAll('.fade-on-scroll').forEach(el => io.observe(el));