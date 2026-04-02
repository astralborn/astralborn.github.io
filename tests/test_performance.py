"""Tests — Page load performance baseline.

Uses the browser's Navigation Timing Level 2 API
(window.performance.timing) which is supported by Chromium, Firefox,
and WebKit via Playwright.

Threshold
---------
The full page load (navigationStart → loadEventEnd) must complete in
under 3 000 ms.  The local-file variant tests the HTML/CSS/JS parse and
execution cost in isolation; the live-site variant adds real network
latency but is skipped when the site is unreachable.
"""
import pathlib
import socket

import pytest
from playwright.sync_api import Page, BrowserContext

# ── constants ────────────────────────────────────────────────────────────────

LOAD_THRESHOLD_MS: int = 3_000
LIVE_HOST = "astralborn.github.io"

_INDEX = pathlib.Path(__file__).parent.parent / "index.html"
LOCAL_FILE_URL = _INDEX.as_uri()


# ── helpers ──────────────────────────────────────────────────────────────────

def _measure_load_ms(page: Page) -> float:
    """Return the total page-load duration in milliseconds using Navigation Timing."""
    return page.evaluate("""() => {
        const t = performance.getEntriesByType('navigation')[0]
                  || performance.timing;
        // Level 2 PerformanceNavigationTiming (preferred)
        if (t.loadEventEnd && t.startTime !== undefined) {
            return t.loadEventEnd - t.startTime;
        }
        // Legacy PerformanceTiming fallback
        return t.loadEventEnd - t.navigationStart;
    }""")


def _site_reachable() -> bool:
    """Quick TCP check — avoids a long timeout when running offline."""
    try:
        socket.setdefaulttimeout(3)
        with socket.create_connection((LIVE_HOST, 443)):
            return True
    except OSError:
        return False


# ── fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture()
def timed_local_page(page: Page) -> Page:
    """Navigate to the local index.html and wait for the load event."""
    page.goto(LOCAL_FILE_URL, wait_until="load")
    return page


@pytest.fixture()
def timed_live_page(page: Page) -> Page:
    """Navigate to the live site and wait for the load event."""
    page.goto(f"https://{LIVE_HOST}", wait_until="load", timeout=15_000)
    return page


# ── tests ────────────────────────────────────────────────────────────────────

class TestPerformanceBaseline:
    """Verify that the page loads within the 3-second threshold."""

    def test_local_page_loads_under_threshold(self, timed_local_page: Page) -> None:
        """The local file (no network) must parse, execute JS, and fire
        the load event in under 3 000 ms across all browser engines."""
        duration_ms = _measure_load_ms(timed_local_page)
        assert duration_ms < LOAD_THRESHOLD_MS, (
            f"Local page load took {duration_ms:.0f} ms — "
            f"threshold is {LOAD_THRESHOLD_MS} ms"
        )

    def test_local_dom_content_loaded_under_threshold(self, timed_local_page: Page) -> None:
        """DOMContentLoaded (HTML parsed + deferred scripts run) must also be
        under 3 000 ms — this isolates JS boot cost from image/asset loading."""
        dcl_ms = timed_local_page.evaluate("""() => {
            const t = performance.getEntriesByType('navigation')[0]
                      || performance.timing;
            if (t.domContentLoadedEventEnd && t.startTime !== undefined) {
                return t.domContentLoadedEventEnd - t.startTime;
            }
            return t.domContentLoadedEventEnd - t.navigationStart;
        }""")
        assert dcl_ms < LOAD_THRESHOLD_MS, (
            f"DOMContentLoaded took {dcl_ms:.0f} ms — "
            f"threshold is {LOAD_THRESHOLD_MS} ms"
        )

    def test_local_first_paint_under_one_second(self, timed_local_page: Page) -> None:
        """First Paint must occur within 1 000 ms on a local file load.
        Skipped automatically on browsers/engines that don't expose paint timing."""
        fp_ms = timed_local_page.evaluate("""() => {
            const entries = performance.getEntriesByType('paint');
            const fp = entries.find(e => e.name === 'first-paint');
            return fp ? fp.startTime : null;
        }""")
        if fp_ms is None:
            pytest.skip("paint timing not available in this browser engine")
        assert fp_ms < 1_000, (
            f"First Paint occurred at {fp_ms:.0f} ms — expected under 1 000 ms"
        )

    @pytest.mark.skipif(not _site_reachable(), reason="Live site not reachable — skipping network test")
    def test_live_page_loads_under_threshold(self, timed_live_page: Page) -> None:
        """End-to-end load of the live GitHub Pages site must be under 3 000 ms.
        Skipped automatically when the host is unreachable (e.g. CI with no egress)."""
        duration_ms = _measure_load_ms(timed_live_page)
        assert duration_ms < LOAD_THRESHOLD_MS, (
            f"Live page load took {duration_ms:.0f} ms — "
            f"threshold is {LOAD_THRESHOLD_MS} ms"
        )

