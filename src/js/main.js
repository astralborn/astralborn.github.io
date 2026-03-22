// Boot Screen Animation
document.addEventListener('DOMContentLoaded', () => {
    // --- Boot screen ---
    const bootScreen = document.getElementById('bootScreen');

    const skipBoot = () => {
        bootScreen.classList.add('fade-out');
        setTimeout(() => {
            bootScreen.style.display = 'none';
        }, 500);
    };

    setTimeout(skipBoot, 6000); // 6 seconds total boot time
    document.addEventListener('keydown', skipBoot, { once: true });
    bootScreen.addEventListener('click', skipBoot, { once: true });

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offset = 20;
                    const targetPosition = target.offsetTop - offset;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // --- Clipboard copy buttons ---
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const text = btn.getAttribute('data-copy');
            const confirm = btn.nextElementSibling;
            try {
                await navigator.clipboard.writeText(text);
                btn.textContent = '[✓]';
                setTimeout(() => btn.textContent = '[copy]', 1500);
            } catch {
                // Fallback: show manual copy hint
                if (confirm) {
                    confirm.textContent = '[SELECT & COPY]';
                    confirm.style.opacity = '1';
                    setTimeout(() => {
                        confirm.style.opacity = '0';
                        confirm.textContent = '[COPIED]';
                    }, 2000);
                }
            }
        });
    });

    // --- Lazy section reveal ---
    const lazyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                lazyObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('section').forEach(section => {
        section.classList.add('lazy-section');
        lazyObserver.observe(section);
    });
});

// --- Fade-in observer ---
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});

// --- Skill bar observer ---
const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const progressBars = entry.target.querySelectorAll('.skill-progress');
            progressBars.forEach(bar => {
                const width = bar.getAttribute('data-width');
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
            skillObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.skill-category').forEach(category => {
    skillObserver.observe(category);
});

// --- Nav menu toggle (explicit globals so onclick="" attrs work even with type="module") ---
window.toggleMenu = function () {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
};

window.closeMenu = function () {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.remove('active');
};