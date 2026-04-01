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

    def test_about_has_three_stat_items(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Stat grid must contain exactly 3 items (Years Experience, Primary Weapon, Tests Automated)."""
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
        assert "about.py" in title.lower()

    def test_code_window_contains_engineer_class(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code content must define the 'Engineer' class."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Engineer")

    def test_code_window_contains_self_diagnosis_method(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code content must include the 'self_diagnosis' static method."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("self_diagnosis")

    def test_code_window_contains_allergic_to_repetition(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Return value of self_diagnosis() must contain the 'Allergic to repetition' string."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Allergic to repetition")

    def test_code_window_stack_contains_pytest(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Tech stack list in the code window must include 'Pytest'."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Pytest")

    def test_code_window_stack_contains_playwright(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Tech stack list in the code window must include 'Playwright'."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Playwright")

    def test_code_window_has_three_dot_decorators(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code window header must have exactly 3 traffic-light dots (.code-dot)."""
        portfolio_local_ready.scroll_to_section("about")
        dots = portfolio_local_ready.about.code_window.locator(".code-dot")
        expect(dots).to_have_count(3)

    def test_stat_label_years_experience(self, portfolio_local_ready: PortfolioPage) -> None:
        """'Years Experience' stat item must display the '3+' value."""
        portfolio_local_ready.scroll_to_section("about")
        stat = portfolio_local_ready._page.locator(".stat-item", has_text="Years Experience")
        expect(stat).to_contain_text("3+")

    def test_stat_label_primary_weapon(self, portfolio_local_ready: PortfolioPage) -> None:
        """'Primary Weapon' stat item must be visible."""
        portfolio_local_ready.scroll_to_section("about")
        stat = portfolio_local_ready._page.locator(".stat-item", has_text="Primary Weapon")
        expect(stat).to_be_visible()

    def test_stat_label_tests_automated(self, portfolio_local_ready: PortfolioPage) -> None:
        """'Tests Automated' stat item must be visible."""
        portfolio_local_ready.scroll_to_section("about")
        stat = portfolio_local_ready._page.locator(".stat-item", has_text="Tests Automated")
        expect(stat).to_be_visible()

    def test_about_intro_mentions_ci_cd(self, portfolio_local_ready: PortfolioPage) -> None:
        """Intro paragraph must mention CI/CD as a domain of work."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.intro_text).to_contain_text("CI/CD")

    def test_about_section_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #about section element must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.section).to_be_visible()

    def test_about_heading_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """The section heading must read exactly 'About Me'."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.heading).to_have_text("About Me")

    def test_about_intro_mentions_python(self, portfolio_local_ready: PortfolioPage) -> None:
        """Intro paragraph must mention Python as the primary language."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.intro_text).to_contain_text("Python")

    def test_code_window_heading_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """Code window title tab (.code-title) must be visible."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_title).to_be_visible()

    def test_code_window_contains_location_prague(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code content must include 'Prague' as the location attribute value."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Prague")

    def test_code_window_contains_stanislav(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Code content must include the author's first name 'Stanislav'."""
        portfolio_local_ready.scroll_to_section("about")
        expect(portfolio_local_ready.about.code_content).to_contain_text("Stanislav")

