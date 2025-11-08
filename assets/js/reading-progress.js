// Reading progress bar
(function() {
  'use strict';

  const progressBar = document.getElementById('reading-progress');
  if (!progressBar) return;

  const updateProgress = () => {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const progress = (scrollTop / documentHeight) * 100;

    progressBar.style.width = Math.min(progress, 100) + '%';
  };

  // Update on scroll
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        updateProgress();
        ticking = false;
      });
      ticking = true;
    }
  });

  // Initial update
  updateProgress();
})();
