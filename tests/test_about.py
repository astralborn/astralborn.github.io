"""Tests — About section."""
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage


class TestAboutSection:
    """Verify the About Me section: intro text, stat counters, and code window."""

    def test_about_heading_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #about <h2> heading must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_heading_visible()

    def test_about_intro_mentions_astralborn(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Intro paragraph must contain the 'astralborn' handle."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_intro_contains("astralborn")

    def test_about_intro_mentions_prague(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Intro paragraph must state the location as Prague."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_intro_contains("Prague")

    def test_about_intro_has_two_paragraphs(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Intro separates the personal introduction from the work approach."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.intro_text.locator("p")).to_have_count(2)

    def test_about_has_three_stat_items(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Stat grid must contain years of experience and two durable areas of focus."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_stat_count(3)

    def test_code_window_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The faux code window (.code-window) must be visible."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_code_window_visible()

    def test_code_file_is_about_py(self, portfolio_local_ready: PortfolioPage) -> None:
        """Code window title tab must display 'about.py'."""
        portfolio_local_ready.scroll_to_section("about")
        title = portfolio_local_ready.about.get_code_title()
        assert "about.py" in title

    def test_code_window_contains_engineer_class(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code content must define the AQAEngineer class."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("AQAEngineer")

    def test_code_window_shows_quality_approach(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code profile must describe focus, mindset, and quality approach."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Embedded devices")
        expect(portfolio_local_ready.about.code_content).to_contain_text("AI-driven analysis")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Users first")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Evidence over assumptions")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Systems people can trust")

    def test_code_window_shows_quality_principle(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code profile must state that quality is built in."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text(
            "Quality is built in, not bolted on."
        )

    def test_code_window_has_three_dot_decorators(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code window header must have exactly 3 traffic-light dots (.code-dot)."""
        portfolio_local_ready.scroll_to_section("about")
        dots = portfolio_local_ready.about.code_window.locator(".code-dot")
        expect(dots).to_have_count(3)

    def test_stat_label_years_experience(self, portfolio_local_ready: PortfolioPage) -> None:
        """'Years Experience' stat item must display the '4+' value."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_stat_value("Years Experience", "4+")

    def test_stat_label_embedded_distributed_systems(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Embedded and distributed systems stat item must be visible."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_stat_visible("Embedded Systems")

    def test_stat_label_product_minded_quality(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Product-minded quality stat item must be visible."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_stat_visible("Product Mindset")

    def test_about_intro_mentions_embedded_and_distributed_systems(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Intro paragraph must mention embedded and distributed systems."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.intro_text).to_contain_text(
            "embedded and distributed systems"
        )

    def test_about_intro_mentions_early_team_collaboration(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Intro paragraph must describe collaboration and building quality in early."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.intro_text).to_contain_text(
            "I partner with teams to spot risks early and build quality in from the start."
        )

    def test_about_section_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #about section element must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.section).to_be_visible()

    def test_about_heading_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """The section heading must read exactly 'About Me'."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.heading).to_have_text("About Me")

    def test_about_intro_mentions_product_behavior(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Intro paragraph must express interest in how systems behave and fail."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.intro_text).to_contain_text(
            "work—and fail"
        )

    def test_code_window_heading_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """Code window title tab (.code-title) must be visible."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_title).to_be_visible()

    # --- Negative / edge-case tests ---

    def test_stat_nonexistent_label_not_present(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """A completely made-up stat label must not appear in the section."""
        portfolio_local_ready.scroll_to_section("about")
        portfolio_local_ready.about.expect_stat_not_visible("Nonexistent Stat")

    def test_stat_count_is_not_zero(self, portfolio_local_ready: PortfolioPage) -> None:
        """Stat grid must not be empty — at least one stat item must exist."""
        portfolio_local_ready.scroll_to_section("about")
        count = portfolio_local_ready.about.get_stat_count()
        assert count > 0, "Expected at least one .stat-item but found none"

    def test_about_heading_is_not_empty(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #about heading must not be an empty string."""
        portfolio_local_ready.scroll_to_section("about")
        heading_text = portfolio_local_ready.about.heading.inner_text()
        assert heading_text.strip() != "", "About heading must not be empty"

    def test_code_title_is_not_empty(self, portfolio_local_ready: PortfolioPage) -> None:
        """Code window title tab must not be an empty string."""
        portfolio_local_ready.scroll_to_section("about")
        title = portfolio_local_ready.about.get_code_title()
        assert title.strip() != "", "Code window title must not be empty"

    def test_intro_does_not_contain_placeholder_text(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Intro paragraph must not contain 'Lorem ipsum' placeholder text."""
        portfolio_local_ready.scroll_to_section("about")
        intro = portfolio_local_ready.about.get_intro_text()
        assert "Lorem ipsum" not in intro, "Intro must not contain placeholder text"
