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

# ── constants ────────────────────────────────────────────────────────────────

# All page sections that receive .lazy-section + .visible via JS.
SECTIONS: list[str] = ["home", "about", "skills", "projects", "contact"]

# Key .fade-in elements — (section_to_scroll_to, CSS selector).
FADE_IN_ELEMENTS: list[tuple[str, str]] = [
    ("about", "#about .about-content"),
    ("skills", ".skills-terminal"),
    ("projects", ".project-card"),
    ("contact", ".contact-terminal"),
]

# Tolerance for asserting that opacity / translateY are "close enough" to the
# expected value after a CSS transition completes.
_OPACITY_TOLERANCE: float = 0.05
_TRANSLATE_Y_TOLERANCE: float = 0.5

# Sentinel used when a matrix() string cannot be parsed.
_TRANSLATE_Y_FALLBACK: float = 999.0

# Identity matrix values that mean "no transform applied".
_IDENTITY_TRANSFORMS = frozenset({"none", "matrix(1, 0, 0, 1, 0, 0)"})


# ── helpers ──────────────────────────────────────────────────────────────────


def _parse_translate_y(transform: str) -> float:
    """Extract the translateY component from a CSS ``matrix()`` string.

    Returns ``0.0`` for identity / ``none`` transforms and
    ``_TRANSLATE_Y_FALLBACK`` when the matrix cannot be parsed.
    """
    if transform in _IDENTITY_TRANSFORMS:
        return 0.0
    nums = re.findall(r"[-\d.]+", transform)
    if len(nums) >= 6:
        return float(nums[5])
    return _TRANSLATE_Y_FALLBACK


def _assert_translate_y_near_zero(transform: str, label: str) -> None:
    """Assert that *transform*'s translateY component is effectively zero."""
    translate_y = _parse_translate_y(transform)
    assert abs(translate_y) < _TRANSLATE_Y_TOLERANCE, (
        f"'{label}' still has transform '{transform}' after reveal — "
        "translateY was not reset to 0"
    )


class TestScrollReveal:
    """Verify that the IntersectionObserver correctly applies classes and
    inline styles to sections and ``.fade-in`` elements as they scroll
    into the viewport.
    """

    # ── lazy-section reveal ──────────────────────────────────────────────

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_section_gets_lazy_section_class_on_load(
        self, portfolio_local_ready: PortfolioPage, section_id: str,
    ) -> None:
        """JS must add .lazy-section to every <section> on
        DOMContentLoaded, before the IntersectionObserver fires."""
        section = portfolio_local_ready._page.locator(f"#{section_id}")
        expect(section).to_have_class(re.compile(r"lazy-section"), timeout=3_000)

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_section_gets_visible_class_after_scroll(
        self, portfolio_local_ready: PortfolioPage, section_id: str,
    ) -> None:
        """Scrolling a section into view must cause the
        IntersectionObserver to add .visible."""
        portfolio_local_ready.scroll_to_section(section_id)
        section = portfolio_local_ready._page.locator(f"#{section_id}")
        expect(section).to_have_class(re.compile(r"visible"), timeout=3_000)

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_visible_section_has_full_opacity(
        self, portfolio_local_ready: PortfolioPage, section_id: str,
    ) -> None:
        """After .visible is applied the section's computed opacity must
        be 1.0 (fully visible)."""
        portfolio_local_ready.scroll_to_section(section_id)
        portfolio_local_ready._page.wait_for_function(
            "id => parseFloat("
            "getComputedStyle(document.getElementById(id)).opacity) >= 0.99",
            arg=section_id,
            timeout=3_000,
        )
        opacity = portfolio_local_ready._page.evaluate(
            "id => parseFloat("
            "getComputedStyle(document.getElementById(id)).opacity)",
            arg=section_id,
        )
        assert opacity == pytest.approx(1.0, abs=_OPACITY_TOLERANCE), (
            f"#{section_id} opacity is {opacity} — expected 1.0 after reveal"
        )

    @pytest.mark.parametrize("section_id", SECTIONS)
    def test_visible_section_has_no_y_transform(
        self, portfolio_local_ready: PortfolioPage, section_id: str,
    ) -> None:
        """After .visible is applied the translateY offset must be 0 —
        the section must no longer be shifted downward."""
        portfolio_local_ready.scroll_to_section(section_id)
        portfolio_local_ready._page.wait_for_function(
            """id => {
                const el = document.getElementById(id);
                const s = getComputedStyle(el);
                const opOk = parseFloat(s.opacity) >= 0.99;
                const m = s.transform;
                const ty = (m === 'none') ? 0 : parseFloat(m.split(',')[5]);
                return opOk && Math.abs(ty) < 0.5;
            }""",
            arg=section_id,
            timeout=3_000,
        )
        transform = portfolio_local_ready._page.evaluate(
            "id => getComputedStyle(document.getElementById(id)).transform",
            arg=section_id,
        )
        _assert_translate_y_near_zero(transform, f"#{section_id}")

    # ── fade-in elements ─────────────────────────────────────────────────

    @pytest.mark.parametrize("section_id,selector", FADE_IN_ELEMENTS)
    def test_fade_in_element_reaches_full_opacity_on_scroll(
        self, portfolio_local_ready: PortfolioPage,
        section_id: str, selector: str,
    ) -> None:
        """After scrolling into view, the .fade-in element's opacity must
        reach 1.0.  The JS observer sets opacity inline — this confirms
        the callback fired."""
        portfolio_local_ready.scroll_to_section(section_id)
        portfolio_local_ready._page.wait_for_function(
            """sel => {
                const el = document.querySelector(sel);
                return el
                    && parseFloat(getComputedStyle(el).opacity) >= 0.99;
            }""",
            arg=selector,
            timeout=3_000,
        )
        opacity = portfolio_local_ready._page.evaluate(
            "sel => parseFloat("
            "getComputedStyle(document.querySelector(sel)).opacity)",
            arg=selector,
        )
        assert opacity == pytest.approx(1.0, abs=_OPACITY_TOLERANCE), (
            f"'{selector}' opacity is {opacity} after scroll — "
            "JS reveal observer may not have fired"
        )

    @pytest.mark.parametrize("section_id,selector", FADE_IN_ELEMENTS)
    def test_fade_in_element_has_no_y_transform_after_scroll(
        self, portfolio_local_ready: PortfolioPage,
        section_id: str, selector: str,
    ) -> None:
        """After the reveal observer fires, the .fade-in element's inline
        transform must be reset to translateY(0) — no remaining downward
        shift."""
        portfolio_local_ready.scroll_to_section(section_id)
        portfolio_local_ready._page.wait_for_function(
            """sel => {
                const el = document.querySelector(sel);
                if (!el) return false;
                const s = getComputedStyle(el);
                const opOk = parseFloat(s.opacity) >= 0.99;
                const m = s.transform;
                const ty = (m === 'none') ? 0 : parseFloat(m.split(',')[5]);
                return opOk && Math.abs(ty) < 0.5;
            }""",
            arg=selector,
            timeout=3_000,
        )
        transform = portfolio_local_ready._page.evaluate(
            "sel => getComputedStyle(document.querySelector(sel)).transform",
            arg=selector,
        )
        _assert_translate_y_near_zero(transform, selector)
