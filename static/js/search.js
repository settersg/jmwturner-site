document.addEventListener('DOMContentLoaded', function() {
  const searchModal = document.getElementById('search-modal');
  const searchToggle = document.getElementById('search-toggle');
  const searchInput = document.getElementById('search-input');
  const searchClose = document.getElementById('search-close');
  const searchOverlay = document.getElementById('search-overlay');
  const searchResults = document.getElementById('search-results');
  let searchIndex = null;
  let searchDocs = [];

  function initSearch() {
    lunr.tokenizer.separator = /[\\s\\-]+/;
    searchIndex = lunr(function () {
      this.ref('id');
      this.field('title', {boost: 10});
      this.field('content');
      this.field('section', {boost: 5});
      this.field('summary');
    });

    fetch('/index.json')
      .then(response => response.json())
      .then(data => {
        searchDocs = data;
        data.forEach(doc => searchIndex.add(doc));
      })
      .catch(err => console.error('Search index load failed', err));
  }

  function showResults(results) {
    searchResults.innerHTML = '';
    if (results.length === 0) {
      searchResults.innerHTML = '<li>No results found.</li>';
      return;
    }
    results.forEach(result => {
      const doc = searchDocs.find(d => d.id === result.ref);
      if (doc) {
        const li = document.createElement('li');
        li.innerHTML = `
          <a href="${doc.url}">
            <strong>${doc.title}</strong>
            <p>${doc.summary || doc.content.substring(0, 200)}...</p>
          </a>
        `;
        searchResults.appendChild(li);
      }
    });
  }

  searchToggle.addEventListener('click', () => {
    searchModal.style.display = 'flex';
    searchInput.focus();
  });

  searchClose.addEventListener('click', () => {
    searchModal.style.display = 'none';
  });

  searchOverlay.addEventListener('click', () => {
    searchModal.style.display = 'none';
  });

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim();
    if (query.length < 2) {
      showResults([]);
      return;
    }
    const results = searchIndex.search(query);
    showResults(results);
  });

  document.addEventListener('keydown', (e) => {
    if (searchModal.style.display === 'flex') {
      if (e.key === 'Escape') {
        searchModal.style.display = 'none';
      }
    }
  });

  initSearch();
});