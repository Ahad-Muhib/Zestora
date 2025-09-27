// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Featured Recipes Carousel
    const carousel = document.getElementById('featuredCarousel');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (carousel && prevBtn && nextBtn) {
        let currentIndex = 0;
        const totalCards = carousel.children.length;
        
        function getCardWidth() {
            return window.innerWidth <= 768 ? 300 : 330; // Responsive card width
        }
        
        function getVisibleCards() {
            return window.innerWidth <= 768 ? 1 : 2; // Show 1 card on mobile, 2 on desktop
        }
        
        function updateCarousel() {
            const cardWidth = getCardWidth();
            const visibleCards = getVisibleCards();
            const maxIndex = Math.max(0, totalCards - visibleCards);
            
            // Adjust currentIndex if it's out of bounds
            if (currentIndex > maxIndex) {
                currentIndex = maxIndex;
            }
            
            const translateX = -currentIndex * cardWidth;
            carousel.style.transform = `translateX(${translateX}px)`;
            
            // Update button states
            prevBtn.disabled = currentIndex === 0;
            nextBtn.disabled = currentIndex >= maxIndex;
            
            // Update button styles
            prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            nextBtn.style.opacity = currentIndex >= maxIndex ? '0.5' : '1';
        }
        
        prevBtn.addEventListener('click', function() {
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        });
        
        nextBtn.addEventListener('click', function() {
            const visibleCards = getVisibleCards();
            const maxIndex = Math.max(0, totalCards - visibleCards);
            if (currentIndex < maxIndex) {
                currentIndex++;
                updateCarousel();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', updateCarousel);
        
        // Initialize carousel
        updateCarousel();
        
        // Auto-play carousel (optional)
        let autoPlayInterval = setInterval(function() {
            const visibleCards = getVisibleCards();
            const maxIndex = Math.max(0, totalCards - visibleCards);
            if (currentIndex >= maxIndex) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }
            updateCarousel();
        }, 5000); // Change slide every 5 seconds
        
        // Pause auto-play on hover
        carousel.addEventListener('mouseenter', function() {
            clearInterval(autoPlayInterval);
        });
        
        carousel.addEventListener('mouseleave', function() {
            autoPlayInterval = setInterval(function() {
                const visibleCards = getVisibleCards();
                const maxIndex = Math.max(0, totalCards - visibleCards);
                if (currentIndex >= maxIndex) {
                    currentIndex = 0;
                } else {
                    currentIndex++;
                }
                updateCarousel();
            }, 5000);
        });
    }

    // Search form enhancement
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            searchForm.classList.add('focused');
        });
        
        searchInput.addEventListener('blur', function() {
            searchForm.classList.remove('focused');
        });
    }

    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            if (email) {
                alert('Thank you for subscribing! We will send you weekly recipes and cooking tips.');
                this.reset();
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Category filtering for Journey section
    const categoryTabs = document.querySelectorAll('.category-tab');
    const recipeCards = document.querySelectorAll('.recipes-journey-grid .recipe-card');
    
    if (categoryTabs.length > 0 && recipeCards.length > 0) {
        categoryTabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                categoryTabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Get selected category
                const selectedCategory = this.getAttribute('data-category');
                
                // Filter recipe cards
                recipeCards.forEach(card => {
                    const cardCategory = card.getAttribute('data-category');
                    
                    if (selectedCategory === 'all' || cardCategory === selectedCategory) {
                        card.style.display = 'block';
                        card.style.opacity = '0';
                        setTimeout(() => {
                            card.style.opacity = '1';
                        }, 100);
                    } else {
                        card.style.opacity = '0';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }
});

// Profile Functions
function goToAdminProfile() {
    alert('Admin Profile Page\n\n(Feature coming soon!)');
}

function goToUserProfile() {
    alert('User Profile Page\n\n(Feature coming soon!)');
}

function showStats() {
    alert('Admin Statistics:\n\n' +
          'Total Users: 1,234\n' +
          'Total Recipes: 567\n' +
          'Total Categories: 12\n' +
          'Active Users Today: 89\n' +
          'New Registrations: 23');
}

function manageUsers() {
    alert('User Management:\n\nThis would redirect to user management page.\n(Feature coming soon!)');
}

function systemTools() {
    alert('System Tools:\n\n' +
          '• Clear Cache\n' +
          '• Database Backup\n' +
          '• System Health Check\n' +
          '• Error Logs\n\n' +
          '(Features coming soon!)');
}

function showStats() {
    alert('Admin Statistics:\n\n' +
          'Total Users: 1,234\n' +
          'Total Recipes: 567\n' +
          'Total Categories: 12\n' +
          'Active Users Today: 89\n' +
          'New Registrations: 23');
}

function manageUsers() {
    alert('User Management:\n\nThis would redirect to user management page.\n(Feature coming soon!)');
}

function systemTools() {
    alert('System Tools:\n\n' +
          '• Clear Cache\n' +
          '• Database Backup\n' +
          '• System Health Check\n' +
          '• Error Logs\n\n' +
          '(Features coming soon!)');
}

function goToAdminProfile() {
    // Redirect to admin profile page (implement later)
    alert('Admin Profile Page\n\n(Feature coming soon!)');
}

function goToUserProfile() {
    // Redirect to user profile page (implement later) 
    alert('User Profile Page\n\n(Feature coming soon!)');
}