// Enhanced Navbar Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    const navbarSearchInput = document.getElementById('navbar-search-input');
    const navbarSuggestionsContainer = document.getElementById('navbar-search-suggestions');
    const navbarSearchHistory = document.getElementById('navbar-search-history');
    const navbarHistoryItems = document.getElementById('navbar-history-items');
    let navbarDebounceTimer;

    if (!navbarSearchInput) return; // Exit if navbar search not found

    // Load and display search history
    function loadSearchHistory() {
        const history = getSearchHistory();
        if (history.length > 0) {
            navbarHistoryItems.innerHTML = '';
            history.slice(0, 5).forEach(term => { // Show only top 5 in navbar
                const item = document.createElement('div');
                item.className = 'navbar-history-item';
                item.textContent = term;
                item.addEventListener('click', function() {
                    navbarSearchInput.value = term;
                    hideNavbarSuggestions();
                    hideNavbarHistory();
                    document.querySelector('.navbar-search-container .search-form').submit();
                });
                navbarHistoryItems.appendChild(item);
            });
        }
    }

    // Get search history from localStorage
    function getSearchHistory() {
        try {
            return JSON.parse(localStorage.getItem('zestora_search_history') || '[]');
        } catch {
            return [];
        }
    }

    // Save search history to localStorage
    function saveSearchHistory(term) {
        try {
            let history = getSearchHistory();
            
            // Remove if already exists
            history = history.filter(item => item !== term);
            
            // Add to beginning
            history.unshift(term);
            
            // Keep only last 10
            history = history.slice(0, 10);
            
            localStorage.setItem('zestora_search_history', JSON.stringify(history));
            loadSearchHistory();
        } catch (error) {
            console.error('Error saving search history:', error);
        }
    }

    // Navbar search suggestions
    navbarSearchInput.addEventListener('input', function() {
        clearTimeout(navbarDebounceTimer);
        const query = this.value.trim();
        
        if (query.length >= 2) {
            navbarDebounceTimer = setTimeout(() => {
                fetchNavbarSuggestions(query);
            }, 300);
            hideNavbarHistory();
        } else {
            hideNavbarSuggestions();
            if (query.length === 0) {
                showNavbarHistory();
            }
        }
    });

    // Show history when focusing empty input
    navbarSearchInput.addEventListener('focus', function() {
        if (this.value.trim().length === 0) {
            showNavbarHistory();
        }
    });

    // Handle form submission to save search history
    document.querySelector('.navbar-search-container .search-form').addEventListener('submit', function(e) {
        const query = navbarSearchInput.value.trim();
        if (query) {
            saveSearchHistory(query);
        }
    });

    // Hide suggestions and history when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.navbar-search-container')) {
            hideNavbarSuggestions();
            hideNavbarHistory();
        }
    });

    function fetchNavbarSuggestions(query) {
        fetch(`/api/search-suggestions/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                showNavbarSuggestions(data.suggestions);
            })
            .catch(error => {
                console.error('Error fetching navbar suggestions:', error);
            });
    }

    function showNavbarSuggestions(suggestions) {
        hideNavbarHistory();
        
        if (suggestions.length === 0) {
            hideNavbarSuggestions();
            return;
        }

        navbarSuggestionsContainer.innerHTML = '';
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'navbar-suggestion-item';
            item.innerHTML = `
                <i class="fas fa-search navbar-suggestion-icon"></i>
                <span>${suggestion}</span>
            `;
            item.addEventListener('click', function() {
                navbarSearchInput.value = suggestion;
                hideNavbarSuggestions();
                saveSearchHistory(suggestion);
                document.querySelector('.navbar-search-container .search-form').submit();
            });
            navbarSuggestionsContainer.appendChild(item);
        });
        
        navbarSuggestionsContainer.style.display = 'block';
    }

    function hideNavbarSuggestions() {
        navbarSuggestionsContainer.style.display = 'none';
    }

    function showNavbarHistory() {
        hideNavbarSuggestions();
        loadSearchHistory();
        if (navbarHistoryItems.children.length > 0) {
            navbarSearchHistory.style.display = 'block';
        }
    }

    function hideNavbarHistory() {
        navbarSearchHistory.style.display = 'none';
    }

    // Initialize
    loadSearchHistory();
});