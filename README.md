<div align="center">

# 🟣 Personal Portfolio

**Terminal-style website** · Vanilla HTML/CSS/JS · Playwright-tested

[![CI](https://github.com/astralborn/astralborn.github.io/actions/workflows/tests.yml/badge.svg)](https://github.com/astralborn/astralborn.github.io/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet?style=flat-square)](LICENSE)

### [🚀 astralborn.github.io](https://astralborn.github.io)

</div>

---

- **Frontend:** no frameworks, no bundler, no build step
- **Tests:** Playwright + Pytest, Page Object Model
- **CI/CD:** GitHub Actions → GitHub Pages

```bash
uv sync --group test
uv run playwright install --with-deps chromium
uv run pytest
```