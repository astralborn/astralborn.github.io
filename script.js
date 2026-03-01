/* ═══════════════════════════════════════
   script.js
═══════════════════════════════════════ */

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
  const obs   = new IntersectionObserver((entries) => {
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

/* ── 3. ANIMATED STAT COUNTERS ── */
(function () {
  function animateCount(el, target, suffix) {
    const dur = 1400, start = performance.now();
    const isFloat = target % 1 !== 0;
    function step(now) {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      const val = isFloat ? (target * eased).toFixed(1) : Math.floor(target * eased);
      el.textContent = val + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const el = e.target;
        animateCount(el, parseFloat(el.dataset.target), el.dataset.suffix || '');
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-target]').forEach(el => obs.observe(el));
})();

/* ── 4. TYPEWRITER on hero role line ── */
(function () {
  const el = document.getElementById('typed-role');
  if (!el) return;
  const phrases = [
    'QA Automation Engineer',
    'Embedded Systems Tester',
    'Python Tooling Builder',
    'CI/CD Pipeline Engineer',
  ];
  let pi = 0, ci = 0, del = false;
  const cursor = document.getElementById('typed-cursor');

  function tick() {
    const p = phrases[pi];
    el.textContent = del ? p.slice(0, --ci) : p.slice(0, ++ci);
    if (!del && ci === p.length) { del = true; setTimeout(tick, 2000); return; }
    if (del && ci === 0) { del = false; pi = (pi + 1) % phrases.length; }
    setTimeout(tick, del ? 30 : 65);
  }
  tick();
})();

/* ── 5. HORIZONTAL MARQUEE on hero (subtle) ── */
(function () {
  const el = document.getElementById('marquee-inner');
  if (!el) return;
  let x = 0;
  const speed = 0.4;
  const width = el.scrollWidth / 2;
  function step() {
    x -= speed;
    if (Math.abs(x) >= width) x = 0;
    el.style.transform = `translateX(${x}px)`;
    requestAnimationFrame(step);
  }
  step();
})();

/* ── 6. KONAMI ── */
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
