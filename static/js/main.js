// Main JavaScript file for the design demo

console.log('Static JavaScript file loaded successfully!');

// Utility function to show static files are working
function showStaticFilesStatus() {
    const statusElement = document.createElement('div');
    statusElement.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <strong>Success!</strong> Static files are working correctly.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Insert at the top of the body
    document.body.insertBefore(statusElement, document.body.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// Add smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Show status message
    showStaticFilesStatus();
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add animation to feature cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Export for potential use in other scripts
window.StaticFilesDemo = {
    showStatus: showStaticFilesStatus
}; 