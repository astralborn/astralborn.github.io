<div align="center">

Personal portfolio — terminal-inspired, cyberpunk aesthetic, zero dependencies.

<br>

<a href="https://astralborn.github.io">
  <img src="https://img.shields.io/badge/Live_Site-00FF8C?style=for-the-badge&logoColor=black" alt="Live site" />
</a>
&nbsp;
<a href="https://astralborn.github.io/src/assets/CV_astralborn.pdf">
  <img src="https://img.shields.io/badge/Download_CV-00D9FF?style=for-the-badge&logoColor=black" alt="CV" />
</a>

</div>

---

[![Preview](src/assets/images/mockup.png)](https://astralborn.github.io)

---

## Features

- **Terminal boot screen** — animated startup sequence on first load, skippable on click or keypress
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
├── favicon.svg             # Terminal cursor favicon
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
            └── mockup.png
```

---

## Tech

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-FFD700?style=flat-square&logo=javascript&logoColor=black)

---

## Deployment

Hosted on **GitHub Pages** from the `main` branch root. Push to `main` and the site updates automatically. The custom 404 page is picked up by GitHub Pages without any extra config.

---

*Built with vanilla JS and the audacity to not use React.*