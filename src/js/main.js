document.addEventListener('DOMContentLoaded', () => {
    // --- Footer year ---
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();


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
            try {
                await navigator.clipboard.writeText(text);
                btn.textContent = '[✓]';
                setTimeout(() => btn.textContent = '[copy]', 1500);
            } catch {
                btn.textContent = '[✗]';
                setTimeout(() => btn.textContent = '[copy]', 1500);
            }
        });
    });

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.classList.add('visible');
                // Let the CSS .lazy-section.visible / .fade-in transition handle
                // opacity and transform — avoid inline styles that skip the transition
                // and leave sub-pixel residuals when read mid-flight by tests.
                if (el.classList.contains('fade-in')) {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }
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

    // --- Nav menu toggle ---
    const hamburger = document.getElementById('hamburger');
    const navLinksEl = document.getElementById('navLinks');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
            hamburger.setAttribute('aria-expanded', String(!isExpanded));
            navLinksEl.classList.toggle('active', !isExpanded);
        });
    }

    navLinksEl.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', () => {
            navLinksEl.classList.remove('active');
            if (hamburger) hamburger.setAttribute('aria-expanded', 'false');
        });
    });
});
