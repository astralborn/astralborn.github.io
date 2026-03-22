document.addEventListener('DOMContentLoaded', () => {
    // --- Footer year ---
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // --- Boot screen ---
    const bootScreen = document.getElementById('bootScreen');

    const skipBoot = () => {
        bootScreen.classList.add('fade-out');
        setTimeout(() => {
            bootScreen.style.display = 'none';
        }, 500);
    };

    setTimeout(skipBoot, 6000);
    document.addEventListener('keydown', skipBoot, { once: true });
    bootScreen.addEventListener('click', skipBoot, { once: true });

    // --- Active nav highlight on scroll ---
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

    const navObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => link.classList.remove('nav-active'));
                const active = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
                if (active) active.classList.add('nav-active');
            }
        });
    }, { threshold: 0.4 });

    sections.forEach(section => navObserver.observe(section));

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
                    window.scrollTo({ top: targetPosition, behavior: 'smooth' });
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

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.classList.add('visible');
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
                revealObserver.unobserve(el);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -100px 0px' });

    document.querySelectorAll('section').forEach(section => {
        section.classList.add('lazy-section');
        revealObserver.observe(section);
    });

    document.querySelectorAll('.fade-in').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
        revealObserver.observe(el);
    });

    // --- FIX: skillObserver moved inside DOMContentLoaded so .skill-category
    //     elements are guaranteed to exist when querySelectorAll runs ---
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
});


// --- Nav menu toggle ---
window.toggleMenu = function () {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
};

window.closeMenu = function () {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.remove('active');
};