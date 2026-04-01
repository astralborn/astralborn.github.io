"""Tests — Hero section."""
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage


class TestHeroSection:
    """Verify the hero / landing section content and interactive links."""

    def test_tag_says_test_automation_engineer(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Tag line must identify the role as 'test automation engineer'."""
        portfolio_local_ready.hero.expect_tag_contains("test automation engineer")

    def test_subtitle_is_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Subtitle element must contain non-empty text."""
        text = portfolio_local_ready.hero.get_subtitle_text()
        assert text.strip() != ""

    def test_hero_photo_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """Profile photo (.hero-photo) must be visible."""
        portfolio_local_ready.hero.expect_photo_visible()

    def test_hero_terminal_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """Hero terminal window (.hero-terminal) must be visible."""
        portfolio_local_ready.hero.expect_terminal_visible()

    def test_hero_terminal_contains_projects_link(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Terminal must contain a visible link to #projects."""
        expect(portfolio_local_ready.hero.projects_link).to_be_visible()

    def test_hero_terminal_contains_contact_link(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Terminal must contain a visible link to #contact."""
        expect(portfolio_local_ready.hero.contact_link).to_be_visible()

    def test_hero_photo_has_no_alt_text(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """The decorative photo must have alt='' (empty) — it is purely presentational."""
        alt = portfolio_local_ready.hero.photo.get_attribute("alt")
        assert alt == "", f"Expected empty alt for decorative image, got: {alt!r}"

    def test_sr_only_h1_contains_name(self, portfolio_local_ready: PortfolioPage) -> None:
        """Screen-reader-only <h1> must include the author's first name for accessibility."""
        h1 = portfolio_local_ready._page.locator("#home h1.sr-only")
        assert "Stanislav" in h1.inner_text()

    def test_subtitle_exact_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """Subtitle must match the exact tagline copy."""
        expect(portfolio_local_ready.hero.subtitle).to_have_text(
            "Automation author. Manual work arsonist."
        )

    def test_terminal_has_three_dot_decorators(self, portfolio_local_ready: PortfolioPage) -> None:
        """Hero terminal header must have exactly 3 traffic-light dots."""
        dots = portfolio_local_ready.hero.terminal_window.locator(".terminal-dot")
        expect(dots).to_have_count(3)

    def test_terminal_dot_colours_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """All three traffic-light dot colours (red, yellow, green) must be present."""
        terminal = portfolio_local_ready.hero.terminal_window
        expect(terminal.locator(".dot-red")).to_be_attached()
        expect(terminal.locator(".dot-yellow")).to_be_attached()
        expect(terminal.locator(".dot-green")).to_be_attached()

    def test_terminal_shows_get_profile_command(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal body must show the './get-profile.sh' command line."""
        expect(portfolio_local_ready.hero.terminal_window).to_contain_text("./get-profile.sh")

    def test_terminal_shows_navigate_command(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal body must show the './navigate.sh' command line."""
        expect(portfolio_local_ready.hero.terminal_window).to_contain_text("./navigate.sh")

    def test_terminal_nav_link_1_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """First terminal nav link must read '[1] cd projects'."""
        expect(portfolio_local_ready.hero.projects_link).to_contain_text("cd projects")

    def test_terminal_nav_link_2_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """Second terminal nav link must read '[2] ./contact.sh'."""
        expect(portfolio_local_ready.hero.contact_link).to_contain_text("./contact.sh")

    def test_hero_section_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #home section element must be visible after the boot screen is dismissed."""
        expect(portfolio_local_ready.hero.section).to_be_visible()

    def test_hero_tag_text_exact(self, portfolio_local_ready: PortfolioPage) -> None:
        """Tag line must match the exact copy '// test automation engineer'."""
        expect(portfolio_local_ready.hero.tag).to_have_text("// test automation engineer")

    def test_terminal_output_mentions_python(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal output must mention Python as part of the tech stack."""
        expect(portfolio_local_ready.hero.terminal_window).to_contain_text("Python")

    def test_terminal_output_mentions_embedded(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal output must mention 'Embedded Systems' as a domain of expertise."""
        expect(portfolio_local_ready.hero.terminal_window).to_contain_text("Embedded Systems")

    def test_terminal_cursor_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Blinking cursor element (.cursor) must be present in the hero terminal."""
        expect(portfolio_local_ready.hero.terminal_window.locator(".cursor")).to_be_attached()

    def test_projects_link_href(self, portfolio_local_ready: PortfolioPage) -> None:
        """Projects link href must be exactly '#projects'."""
        href = portfolio_local_ready.hero.projects_link.get_attribute("href") or ""
        assert href == "#projects"

    def test_contact_link_href(self, portfolio_local_ready: PortfolioPage) -> None:
        """Contact link href must be exactly '#contact'."""
        href = portfolio_local_ready.hero.contact_link.get_attribute("href") or ""
        assert href == "#contact"

    def test_projects_link_click_scrolls_to_projects(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Clicking '[1] cd projects' must scroll #projects into the viewport."""
        portfolio_local_ready.hero.projects_link.click()
        portfolio_local_ready._page.wait_for_timeout(600)
        expect(portfolio_local_ready._page.locator("#projects")).to_be_in_viewport()

    def test_contact_link_click_scrolls_to_contact(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Clicking '[2] ./contact.sh' must scroll #contact into the viewport."""
        portfolio_local_ready.hero.contact_link.click()
        portfolio_local_ready._page.wait_for_timeout(600)
        expect(portfolio_local_ready._page.locator("#contact")).to_be_in_viewport()

