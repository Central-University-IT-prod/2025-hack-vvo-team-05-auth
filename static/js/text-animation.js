document.addEventListener("DOMContentLoaded", () => {
  const elements = document.querySelectorAll('.animated-line span, .side-text span');

  function isInViewport(el) {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight * 0.9 && rect.bottom > 0;
  }

  function triggerAnimations() {
    elements.forEach(el => {
      if (!el.classList.contains('visible') && isInViewport(el)) {
        el.classList.add('visible');
      }
    });
  }

  window.addEventListener('scroll', triggerAnimations);
  window.addEventListener('resize', triggerAnimations);
  triggerAnimations(); // Initial call
});