"""Tests — Boot screen."""
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage


class TestBootScreen:
    """Verify the terminal boot screen that greets users on first load."""

    def test_boot_screen_is_visible_on_load(self, portfolio_local: PortfolioPage) -> None:
        """Boot screen overlay (#bootScreen) must be visible immediately after page load."""
        expect(portfolio_local.boot_screen.container).to_be_visible()

    def test_boot_screen_contains_ascii_art(self, portfolio_local: PortfolioPage) -> None:
        """ASCII art <pre> block must be visible and non-empty.

        The art renders 'astralborn' as box-drawing characters, not plain text,
        so we only assert the element is present and contains some content.
        """
        expect(portfolio_local.boot_screen.ascii_art).to_be_visible()
        ascii_text = portfolio_local.boot_screen.ascii_art.inner_text()
        assert ascii_text.strip() != "", "ASCII art block should not be empty"

    def test_boot_screen_shows_seven_status_lines(self, portfolio_local: PortfolioPage) -> None:
        """Boot terminal must display exactly 7 status lines (6 × [OK] + 1 × [READY])."""
        lines = portfolio_local.boot_screen.get_status_labels()
        assert len(lines) == 7

    def test_boot_screen_all_lines_contain_ok_or_ready(
        self, portfolio_local: PortfolioPage
    ) -> None:
        """Every status line must end with either [OK] or [READY] — no unknown states."""
        lines = portfolio_local.boot_screen.get_status_labels()
        for line in lines:
            assert "[OK]" in line or "[READY]" in line, f"Unexpected line: {line!r}"

    def test_boot_screen_dismisses_on_click(self, portfolio_local: PortfolioPage) -> None:
        """Clicking the boot screen must dismiss it within 2 seconds."""
        portfolio_local.boot_screen.dismiss_by_click()
        portfolio_local.boot_screen.wait_until_gone(timeout=2_000)

    def test_boot_screen_dismisses_on_keypress(self, portfolio_local: PortfolioPage) -> None:
        """Pressing Escape must dismiss the boot screen within 2 seconds."""
        portfolio_local.boot_screen.dismiss_by_key()
        portfolio_local.boot_screen.wait_until_gone(timeout=2_000)

    def test_boot_screen_auto_dismisses(self, portfolio_local: PortfolioPage) -> None:
        """Boot screen must auto-dismiss after ~6 seconds without any interaction."""
        portfolio_local.boot_screen.wait_for_auto_dismiss(timeout=8_000)

    def test_boot_screen_progress_bar_present(self, portfolio_local: PortfolioPage) -> None:
        """Progress bar element (.boot-progress-bar) must be present in the DOM."""
        expect(portfolio_local.boot_screen.progress_bar).to_be_attached()

    def test_boot_screen_footer_text_present(self, portfolio_local: PortfolioPage) -> None:
        """Footer hint must tell the user how to dismiss ('Press any key to continue')."""
        expect(portfolio_local.boot_screen.footer).to_contain_text("Press any key to continue")

    def test_boot_screen_footer_has_signature(self, portfolio_local: PortfolioPage) -> None:
        """Footer must include the 'astralborn' author signature."""
        expect(portfolio_local.boot_screen.footer).to_contain_text("astralborn")

    def test_boot_screen_last_line_is_ready(self, portfolio_local: PortfolioPage) -> None:
        """The 7th (last) status line must contain [READY], signalling boot completion."""
        lines = portfolio_local.boot_screen.get_status_labels()
        assert "[READY]" in lines[-1], f"Expected last line to contain [READY], got: {lines[-1]!r}"

    def test_boot_screen_first_six_lines_are_ok(self, portfolio_local: PortfolioPage) -> None:
        """The first 6 status lines must all contain [OK] (system checks passing)."""
        lines = portfolio_local.boot_screen.get_status_labels()
        for line in lines[:6]:
            assert "[OK]" in line, f"Expected [OK] in line: {line!r}"

    def test_main_content_accessible_after_dismiss(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """After dismissing the boot screen, the nav and hero section must be visible."""
        expect(portfolio_local_ready.nav.nav).to_be_visible()
        expect(portfolio_local_ready.hero.section).to_be_visible()

    def test_click_dismiss_reveals_hero_links(
        self, portfolio_local: PortfolioPage
    ) -> None:
        """After clicking to dismiss the boot screen, both hero terminal links must be clickable."""
        portfolio_local.boot_screen.dismiss_by_click()
        portfolio_local.boot_screen.wait_until_gone(timeout=2_000)
        expect(portfolio_local._page.locator(".hero-terminal a[href='#projects']")).to_be_visible()
        expect(portfolio_local._page.locator(".hero-terminal a[href='#contact']")).to_be_visible()

