// ============================================
// PORTFOLIO WEBSITE - JAVASCRIPT
// ============================================

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Close mobile menu if open
            document.querySelector('.nav-menu')?.classList.remove('active');
        }
    });
});

// CTA Button functionality
const ctaButton = document.querySelector('.cta-button');
if (ctaButton) {
    ctaButton.addEventListener('click', function() {
        const contactSection = document.querySelector('#contact');
        contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
}

// Contact button functionality
const contactLink = document.querySelector('.contact-link');
if (contactLink) {
    contactLink.addEventListener('click', function(e) {
        // Email link will open mail client
    });
}

// Navbar background on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 8px 32px 0 rgba(0, 255, 136, 0.15)';
    } else {
        navbar.style.boxShadow = '0 8px 32px 0 rgba(0, 255, 136, 0.1)';
    }
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe achievement and course cards
document.querySelectorAll('.achievement-card, .course-card, .service-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease-out';
    observer.observe(card);
});

// Mobile menu toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });
}

// Handle mouse move for glow effect on hero
const hero = document.querySelector('.hero');
if (hero) {
    hero.addEventListener('mousemove', function(e) {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        const glowCircles = document.querySelectorAll('.glow-circle');
        glowCircles.forEach((circle, index) => {
            const moveX = (x - 0.5) * (index + 1) * 20;
            const moveY = (y - 0.5) * (index + 1) * 20;
            circle.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });
}

// Intersection Observer for fade-in animations
const fadeInElements = document.querySelectorAll('section');
fadeInElements.forEach((element, index) => {
    element.style.opacity = '1';
});

// Add ripple effect to buttons on click
document.querySelectorAll('.cta-button, .social-icon').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Page load animation
window.addEventListener('load', function() {
    document.body.style.opacity = '1';
});

// Performance optimization: Debounce scroll events
let scrollTimeout;
window.addEventListener('scroll', function() {
    if (scrollTimeout) {
        window.cancelAnimationFrame(scrollTimeout);
    }
    scrollTimeout = window.requestAnimationFrame(function() {
        // Scroll animations here
    });
}, { passive: true });

console.log('Portfolio website loaded successfully!');
