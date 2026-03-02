/* script.js */

/* ── 1. SCROLL REVEAL ── */
(function () {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const siblings = [...e.target.parentElement.querySelectorAll('.reveal')];
        setTimeout(() => e.target.classList.add('visible'), siblings.indexOf(e.target) * 90);
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
})();

/* ── 2. ACTIVE NAV ── */
(function () {
  const links = document.querySelectorAll('.nav-links a');
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const a = document.querySelector(`.nav-links a[href="#${e.target.id}"]`);
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '-40% 0px -40% 0px' });
  document.querySelectorAll('section[id]').forEach(s => obs.observe(s));
})();

/* ── 3. STAT COUNTERS ── */
(function () {
  function animateCount(el, target, suffix) {
    const dur = 1400, start = performance.now();
    function step(now) {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.floor(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCount(e.target, parseFloat(e.target.dataset.target), e.target.dataset.suffix || '');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-target]').forEach(el => obs.observe(el));
})();

/* ── 4. MARQUEE ── */
(function () {
  const el = document.getElementById('marquee-inner');
  if (!el) return;
  let x = 0;
  const speed = 0.5;
  function step() {
    x -= speed;
    const half = el.scrollWidth / 2;
    if (Math.abs(x) >= half) x = 0;
    el.style.transform = `translateX(${x}px)`;
    requestAnimationFrame(step);
  }
  step();
})();

/* ── 5. KONAMI ── */
(function () {
  const CODE = [38,38,40,40,37,39,37,39,66,65]; let i = 0;
  document.addEventListener('keydown', e => {
    i = e.keyCode === CODE[i] ? i + 1 : 0;
    if (i === CODE.length) {
      document.body.style.filter = 'sepia(0.8) hue-rotate(320deg)';
      setTimeout(() => document.body.style.filter = '', 2500);
      i = 0;
    }
  });
})();
