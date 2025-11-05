// Theme toggle with localStorage persistence
(function() {
  'use strict';

  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = themeToggle?.querySelector('.theme-icon');
  const html = document.documentElement;

  // Get initial theme
  const getInitialTheme = () => {
    const stored = localStorage.getItem('theme');
    if (stored) return stored;

    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
      return 'light';
    }
    return 'dark';
  };

  // Apply theme
  const applyTheme = (theme) => {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);

    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
  };

  // Initialize theme
  const currentTheme = getInitialTheme();
  applyTheme(currentTheme);

  // Toggle theme
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const newTheme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
    });
  }

  // Listen for system theme changes
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
})();
