"""Tests — Scroll-reveal animations and IntersectionObserver behaviour.

Two mechanisms are tested:
  1. Sections (.lazy-section) — JS adds .lazy-section on DOMContentLoaded, then
     the IntersectionObserver adds .visible when the section enters the viewport.
  2. Fade-in elements (.fade-in) — JS sets opacity/transform to hidden on load,
     then the same observer resets them to visible values when scrolled into view.
"""
import re
import pytest
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage


# All page sections that receive .lazy-section + .visible via JS
SECTIONS = ["home", "about", "skills", "projects", "contact"]

# Key .fade-in elements — (section_to_scroll_to, CSS selector)
FADE_IN_ELEMENTS = [
    ("about",    "#about .about-content"),
    ("skills",   ".skills-terminal"),
    ("projects", ".project-card"),
    ("contact",  ".contact-terminal"),
]


class TestScrollReveal:
    """Verify that the IntersectionObserver correctly applies classes and inline styles
    to sections and .fade-in elements as they scroll into the viewport."""

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_section_gets_lazy_section_class_on_load(
        self, portfolio_local_ready: PortfolioPage, section_id: str
    ) -> None:
        """JS must add .lazy-section to every <section> on DOMContentLoaded,
        before the IntersectionObserver fires."""
        section = portfolio_local_ready._page.locator(f"#{section_id}")
        expect(section).to_have_class(re.compile(r"lazy-section"), timeout=3_000)

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_section_gets_visible_class_after_scroll(
        self, portfolio_local_ready: PortfolioPage, section_id: str
    ) -> None:
        """Scrolling a section into view must cause the IntersectionObserver to add .visible."""
        portfolio_local_ready.scroll_to_section(section_id)
        section = portfolio_local_ready._page.locator(f"#{section_id}")
        expect(section).to_have_class(re.compile(r"visible"), timeout=3_000)

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_visible_section_has_full_opacity(
        self, portfolio_local_ready: PortfolioPage, section_id: str
    ) -> None:
        """After .visible is applied the section's computed opacity must be 1.0 (fully visible)."""
        portfolio_local_ready.scroll_to_section(section_id)
        # Wait until the CSS transition completes and opacity reaches 1
        portfolio_local_ready._page.wait_for_function(
            "id => parseFloat(getComputedStyle(document.getElementById(id)).opacity) >= 0.99",
            section_id,
            timeout=3_000,
        )
        opacity = portfolio_local_ready._page.evaluate(
            "id => parseFloat(getComputedStyle(document.getElementById(id)).opacity)",
            section_id,
        )
        assert opacity == pytest.approx(1.0, abs=0.05), (
            f"#{section_id} opacity is {opacity} — expected 1.0 after reveal"
        )

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_visible_section_has_no_y_transform(
        self, portfolio_local_ready: PortfolioPage, section_id: str
    ) -> None:
        """After .visible is applied the translateY offset must be 0 —
        the section must no longer be shifted downward."""
        portfolio_local_ready.scroll_to_section(section_id)
        portfolio_local_ready._page.wait_for_function(
            "id => parseFloat(getComputedStyle(document.getElementById(id)).opacity) >= 0.99",
            section_id,
            timeout=3_000,
        )
        transform = portfolio_local_ready._page.evaluate(
            "id => getComputedStyle(document.getElementById(id)).transform",
            section_id,
        )
        assert transform in ("none", "matrix(1, 0, 0, 1, 0, 0)"), (
            f"#{section_id} still has transform '{transform}' after reveal — "
            "translateY was not reset to 0"
        )

    @pytest.mark.parametrize("section_id,selector", FADE_IN_ELEMENTS)
    def test_fade_in_element_reaches_full_opacity_on_scroll(
        self, portfolio_local_ready: PortfolioPage, section_id: str, selector: str
    ) -> None:
        """After scrolling into view, the .fade-in element's opacity must reach 1.0.
        The JS observer sets opacity inline — this confirms the callback fired."""
        portfolio_local_ready.scroll_to_section(section_id)
        portfolio_local_ready._page.wait_for_function(
            "sel => { const el = document.querySelector(sel); return el && parseFloat(getComputedStyle(el).opacity) >= 0.99; }",
            selector,
            timeout=3_000,
        )
        opacity = portfolio_local_ready._page.evaluate(
            "sel => parseFloat(getComputedStyle(document.querySelector(sel)).opacity)",
            selector,
        )
        assert opacity == pytest.approx(1.0, abs=0.05), (
            f"'{selector}' opacity is {opacity} after scroll — "
            "JS reveal observer may not have fired"
        )

    @pytest.mark.parametrize("section_id,selector", FADE_IN_ELEMENTS)
    def test_fade_in_element_has_no_y_transform_after_scroll(
        self, portfolio_local_ready: PortfolioPage, section_id: str, selector: str
    ) -> None:
        """After the reveal observer fires, the .fade-in element's inline transform
        must be reset to translateY(0) — no remaining downward shift."""
        portfolio_local_ready.scroll_to_section(section_id)
        portfolio_local_ready._page.wait_for_function(
            "sel => { const el = document.querySelector(sel); return el && parseFloat(getComputedStyle(el).opacity) >= 0.99; }",
            selector,
            timeout=3_000,
        )
        transform = portfolio_local_ready._page.evaluate(
            "sel => getComputedStyle(document.querySelector(sel)).transform",
            selector,
        )
        assert transform in ("none", "matrix(1, 0, 0, 1, 0, 0)"), (
            f"'{selector}' still has transform '{transform}' after reveal"
        )
