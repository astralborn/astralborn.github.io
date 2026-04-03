<div align="center">

Personal portfolio — terminal-inspired, cyberpunk aesthetic, zero dependencies.

<br>

<a href="https://astralborn.github.io">
  <img src="https://img.shields.io/badge/Live_Site-00FF8C?style=for-the-badge&logoColor=black" alt="Live site" />
</a>

<br><br>

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-FFD700?style=flat-square&logo=javascript&logoColor=black)
&nbsp;
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)

</div>

---

[![Preview](src/assets/images/mockup.png)](https://astralborn.github.io)

---

## Features

- **Terminal boot screen** — animated startup sequence on first load, skippable by click, Esc, Enter, or Space
- **Scroll reveal animations** — sections and cards fade in as they enter the viewport via `IntersectionObserver`
- **Active nav highlight** — current section tracked on scroll, underline indicator transitions smoothly
- **Clipboard copy buttons** — one-click copy for email, GitHub, and LinkedIn in the contact section
- **Responsive layout** — mobile hamburger nav, stacked grids, touch-friendly
- **SVG favicon** — terminal cursor icon, no `.ico` toolchain needed
- **Branded 404 page** — fake pytest failure screen, links back home, GitHub Pages auto-serves it
- **Open Graph / Twitter card meta** — rich link preview when shared on LinkedIn, Slack, iMessage
- **Dynamic copyright year** — never manually update it again
- **Zero runtime dependencies** — no React, no Vue, no framework

---

## Structure

```
.
├── index.html              # Single page
├── 404.html                # Custom GitHub Pages error page
├── pytest.ini              # Pytest config — sets pythonpath and testpaths
├── requirements-test.txt   # Test dependencies (playwright, pytest, pytest-playwright)
└── src/
    ├── css/
    │   ├── main.css        # Base styles, layout, boot screen, components
    │   ├── components.css  # Nav, hero grid, skills terminal, project cards
    │   └── animations.css  # Keyframe definitions
    ├── js/
    │   └── main.js         # Boot screen, scroll observers, copy buttons, nav
    └── assets/
        ├── CV_astralborn.pdf
        └── images/
            ├── photo.png
            ├── mockup.png
            └── favicon.svg
└── tests/
    ├── conftest.py                  # Shared fixtures (portfolio, portfolio_local, portfolio_local_ready)
    ├── test_boot_screen.py          # Boot screen overlay
    ├── test_navbar.py               # Navigation bar & active-scroll
    ├── test_hero.py                 # Hero section content & links
    ├── test_about.py                # About section & code window
    ├── test_skills.py               # Skills terminal & proficiency labels
    ├── test_projects.py             # Projects grid & GitHub links
    ├── test_contact.py              # Contact terminal, links & copy buttons
    ├── test_page_meta.py            # <head> meta, footer & 404 page
    ├── test_animations.py           # Scroll-reveal & IntersectionObserver
    ├── test_performance.py          # Navigation Timing API — load & DCL thresholds
    └── pages/                       # Page Object Model
        ├── portfolio_page.py        # Top-level facade
        ├── boot_screen_page.py
        ├── navbar_page.py
        ├── hero_section_page.py
        ├── about_section_page.py
        ├── skills_section_page.py
        ├── projects_section_page.py
        └── contact_section_page.py
```

---

## Tests

End-to-end Playwright suite written in Python, running against the local `index.html` — no live network required.

### Setup

```bash
pip install -r requirements-test.txt
playwright install chromium
```

### Run

```bash
# All tests (headless, local file)
pytest

# Headed mode — watch the browser
pytest --headed

# Specific file
pytest tests/test_navbar.py

# Verbose output
pytest -v
```


---

## Deployment

Hosted on **GitHub Pages** from the `main` branch root. The custom 404 page is picked up automatically — no extra config needed.

---

*Built with vanilla JS and the audacity to not use React.*

---