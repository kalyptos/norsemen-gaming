// Simple lightweight search implementation (no dependencies)
(function() {
  'use strict';

  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  const searchOverlay = document.getElementById('search-overlay');
  let searchIndex = [];

  // Fetch search index
  fetch('/index.json')
    .then(response => response.json())
    .then(data => {
      searchIndex = data;
    })
    .catch(err => console.error('Error loading search index:', err));

  // Simple search function
  function search(query) {
    if (!query || query.length < 2) {
      return [];
    }

    query = query.toLowerCase();
    return searchIndex.filter(item => {
      const titleMatch = item.title.toLowerCase().includes(query);
      const summaryMatch = item.summary.toLowerCase().includes(query);
      const contentMatch = item.content.toLowerCase().includes(query);
      const tagsMatch = item.tags && item.tags.some(tag => tag.toLowerCase().includes(query));
      const categoriesMatch = item.categories && item.categories.some(cat => cat.toLowerCase().includes(query));

      return titleMatch || summaryMatch || contentMatch || tagsMatch || categoriesMatch;
    }).slice(0, 10); // Limit to 10 results
  }

  // Display results
  function displayResults(results) {
    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-no-results">Ingen resultater funnet</div>';
      return;
    }

    const html = results.map(result => `
      <a href="${result.permalink}" class="search-result">
        <h3>${result.title}</h3>
        <p>${result.summary}</p>
        <small>${result.date}</small>
      </a>
    `).join('');

    searchResults.innerHTML = html;
  }

  // Event listeners
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value;
      if (query.length < 2) {
        searchResults.innerHTML = '';
        searchOverlay.style.display = 'none';
        return;
      }

      const results = search(query);
      displayResults(results);
      searchOverlay.style.display = 'block';
    });

    // Close search on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        searchInput.value = '';
        searchResults.innerHTML = '';
        searchOverlay.style.display = 'none';
      }
    });

    // Close search when clicking overlay
    if (searchOverlay) {
      searchOverlay.addEventListener('click', () => {
        searchInput.value = '';
        searchResults.innerHTML = '';
        searchOverlay.style.display = 'none';
      });
    }
  }

  // Keyboard shortcut: Ctrl+K or Cmd+K to focus search
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchInput.focus();
    }
  });
})();
