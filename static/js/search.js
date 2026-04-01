document.addEventListener('DOMContentLoaded', function() {
  const searchModal = document.getElementById('search-modal');
  const searchToggles = document.querySelectorAll('[id="search-toggle"]');
  const searchInput = document.getElementById('search-input');
  const searchClose = document.getElementById('search-close');
  const searchOverlay = document.getElementById('search-overlay');
  const searchResults = document.getElementById('search-results');
  let searchIndex = null;
  let searchDocs = [];

  function initSearch() {
    searchIndex = lunr(function () {
      this.ref('id');
      this.field('title', {boost: 10});
      this.field('content');
      this.field('section', {boost: 5});
      this.field('summary');
    });

    fetch('/index.json')
      .then(function(response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function(data) {
        searchDocs = data;
        data.forEach(function(doc) { searchIndex.add(doc); });
        console.log('Search index loaded: ' + data.length + ' pages');
      })
      .catch(function(err) { console.error('Search index load failed:', err); });
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

  searchToggles.forEach(function(btn) {
    btn.addEventListener('click', function() {
      searchModal.style.display = 'flex';
      searchInput.focus();
    });
  });

  searchClose.addEventListener('click', () => {
    searchModal.style.display = 'none';
  });

  searchModal.addEventListener('click', function(e) {
    if (e.target === searchModal || e.target.id === 'search-overlay') {
      searchModal.style.display = 'none';
    }
  });

  searchInput.addEventListener('input', function() {
    var query = searchInput.value.trim();
    if (query.length < 2) {
      searchResults.innerHTML = '';
      return;
    }
    if (!searchIndex || searchDocs.length === 0) {
      searchResults.innerHTML = '<li style="padding:1rem 1.5rem;color:#888;">Loading search index...</li>';
      return;
    }
    try {
      var results = searchIndex.search(query);
      showResults(results);
    } catch(e) {
      searchResults.innerHTML = '<li style="padding:1rem 1.5rem;color:#c00;">Search error: ' + e.message + '</li>';
      console.error('Search error:', e);
    }
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