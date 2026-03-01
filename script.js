/* ── 0. JOB EXPAND / COLLAPSE ── */
function toggleJob(btn) {
  const details = btn.nextElementSibling;
  const isOpen  = details.classList.contains('open');
  btn.classList.toggle('open', !isOpen);
  details.classList.toggle('open', !isOpen);
  btn.querySelector('.toggle-arrow').textContent        = isOpen ? '+' : '×';
  btn.querySelector('span:first-child').textContent     = isOpen ? 'Show details' : 'Hide details';
}

/* ── 1. PARTICLE CANVAS ── */
(function () {
  const canvas = document.getElementById('bg-canvas');
  const ctx    = canvas.getContext('2d');
  let W, H, nodes = [];
  const COUNT = 80, DIST = 140, COLOR = '#00e5a0';

  function resize() { W = canvas.width = innerWidth; H = canvas.height = innerHeight; }

  function init() {
    nodes = Array.from({ length: COUNT }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 1.5 + 0.5,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (const n of nodes) {
      n.x += n.vx; n.y += n.vy;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
    }
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x, dy = nodes[i].y - nodes[j].y;
        const d  = Math.sqrt(dx * dx + dy * dy);
        if (d < DIST) {
          ctx.beginPath();
          ctx.strokeStyle = COLOR;
          ctx.globalAlpha = (1 - d / DIST) * 0.4;
          ctx.lineWidth = 0.5;
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }
    ctx.globalAlpha = 0.7;
    for (const n of nodes) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = COLOR;
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', () => { resize(); init(); });
  resize(); init(); draw();
})();

/* ── 2. TYPEWRITER ── */
(function () {
  const el      = document.getElementById('typed-text');
  const phrases = [
    'Test Automation · Python · Playwright',
    'CI/CD · Jenkins · Pytest',
    'Embedded Systems · VoIP · EtherNet/IP',
    'QA Engineer based in Prague 🇨🇿',
  ];
  let pi = 0, ci = 0, deleting = false;
  const TYPE = 55, DEL = 28, PAUSE = 1800;

  function tick() {
    const phrase = phrases[pi];
    if (!deleting) {
      el.textContent = phrase.slice(0, ++ci);
      if (ci === phrase.length) { deleting = true; setTimeout(tick, PAUSE); return; }
    } else {
      el.textContent = phrase.slice(0, --ci);
      if (ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; }
    }
    setTimeout(tick, deleting ? DEL : TYPE);
  }
  tick();
})();

/* ── 3. SCROLL REVEAL ── */
(function () {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const siblings = [...e.target.parentElement.querySelectorAll('.reveal')];
        setTimeout(() => e.target.classList.add('visible'), siblings.indexOf(e.target) * 80);
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
})();

/* ── 4. SKILL BARS ── */
(function () {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.skill-fill').forEach(f => f.style.width = f.dataset.pct + '%');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('#skills').forEach(s => obs.observe(s));
})();

/* ── 5. TAG ANIMATION ── */
(function () {
  const tags = [
    'Git', 'Gerrit', 'Jira', 'Confluence',
    'VirtualBox', 'PySide', 'Insomnia',
    'EtherNet/IP', 'TCP/IP', 'VoIP',
    'Agile', 'TDD', 'BDD', 'REST API',
  ];
  const container = document.getElementById('tags-container');
  tags.forEach((tag, i) => {
    const el = document.createElement('span');
    el.className = 'tag';
    el.textContent = tag;
    el.style.cssText = `opacity:0; transform:scale(0.85); transition: opacity .3s ease ${i * 60}ms, transform .3s ease ${i * 60}ms`;
    container.appendChild(el);
  });
  const obs = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      container.querySelectorAll('.tag').forEach(t => { t.style.opacity = '1'; t.style.transform = 'scale(1)'; });
      obs.disconnect();
    }
  }, { threshold: 0.2 });
  obs.observe(container);
})();

/* ── 6. ACTIVE NAV ── */
(function () {
  const links = document.querySelectorAll('.nav-links a');
  const obs   = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(l => l.style.color = '');
        const a = document.querySelector(`.nav-links a[href="#${e.target.id}"]`);
        if (a) a.style.color = 'var(--green)';
      }
    });
  }, { rootMargin: '-40% 0px -40% 0px' });
  document.querySelectorAll('section[id]').forEach(s => obs.observe(s));
})();

/* ── 7. KONAMI EASTER EGG ── */
(function () {
  const CODE = [38,38,40,40,37,39,37,39,66,65];
  let i = 0;
  document.addEventListener('keydown', e => {
    i = (e.keyCode === CODE[i]) ? i + 1 : 0;
    if (i === CODE.length) {
      document.body.style.filter = 'hue-rotate(180deg)';
      setTimeout(() => document.body.style.filter = '', 2000);
      i = 0;
    }
  });
})();
