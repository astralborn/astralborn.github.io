"""Tests — Skills section."""
import pytest
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage

EXPECTED_SKILLS = ["Python", "Pytest", "Playwright", "JavaScript",
                   "Packet analysis", "Jenkins", "Git", "Linux"]

EXPECTED_CATEGORIES = ["# Automation", "# Domain & Tools"]

EXPECTED_LABELS = {"proficient", "solid", "basic"}

# Expected proficiency label per skill, directly from the HTML
SKILL_PROFICIENCY = {
    "Python":           "proficient",
    "Pytest":           "proficient",
    "Playwright":       "solid",
    "JavaScript":       "basic",
    "Packet analysis":  "proficient",
    "Jenkins":          "solid",
    "Git":              "solid",
    "Linux":            "solid",
}


class TestSkillsSection:
    """Verify the skills terminal: rows, categories, proficiency labels, and bar content."""

    def test_skills_heading_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #skills <h2> heading must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("skills")
        portfolio_local_ready.skills.expect_heading_visible()

    def test_skills_terminal_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The skills terminal window (.skills-terminal) must be visible."""
        portfolio_local_ready.scroll_to_section("skills")
        portfolio_local_ready.skills.expect_terminal_visible()

    def test_eight_skill_rows_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """There must be exactly 8 skill rows — 4 Automation + 4 Domain & Tools."""
        portfolio_local_ready.scroll_to_section("skills")
        portfolio_local_ready.skills.expect_skill_row_count(8)

    def test_two_category_headings(self, portfolio_local_ready: PortfolioPage) -> None:
        """Skills must be grouped under exactly 2 category headings: '# Automation' and '# Domain & Tools'."""
        portfolio_local_ready.scroll_to_section("skills")
        headings = portfolio_local_ready.skills.get_category_headings()
        assert headings == EXPECTED_CATEGORIES

    @pytest.mark.parametrize("skill", EXPECTED_SKILLS)
    def test_skill_is_present(
        self, portfolio_local_ready: PortfolioPage, skill: str
    ) -> None:
        """Each expected skill name must appear in the skills terminal."""
        portfolio_local_ready.scroll_to_section("skills")
        portfolio_local_ready.skills.expect_skill_present(skill)

    def test_all_skill_labels_are_known(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Every proficiency label must be one of: 'proficient', 'solid', or 'basic'."""
        portfolio_local_ready.scroll_to_section("skills")
        labels = portfolio_local_ready.skills.get_skill_labels()
        for label in labels:
            assert label in EXPECTED_LABELS, f"Unknown skill label: {label!r}"

    @pytest.mark.parametrize("skill,expected_label", SKILL_PROFICIENCY.items())
    def test_skill_proficiency_label_correct(
        self, portfolio_local_ready: PortfolioPage, skill: str, expected_label: str
    ) -> None:
        """Each skill's proficiency label must exactly match the value defined in SKILL_PROFICIENCY."""
        portfolio_local_ready.scroll_to_section("skills")
        row = portfolio_local_ready._page.locator(
            ".skill-row", has=portfolio_local_ready._page.locator(".skill-name-col", has_text=skill)
        )
        label_el = row.locator("[class*='skill-label']")
        expect(label_el).to_have_text(expected_label)

    def test_terminal_has_three_dot_decorators(self, portfolio_local_ready: PortfolioPage) -> None:
        """Skills terminal header must have exactly 3 traffic-light dots."""
        portfolio_local_ready.scroll_to_section("skills")
        dots = portfolio_local_ready.skills.terminal.locator(".terminal-dot")
        expect(dots).to_have_count(3)

    def test_skills_command_line_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal must display the 'skills --list --verbose' command line."""
        portfolio_local_ready.scroll_to_section("skills")
        expect(portfolio_local_ready.skills.terminal).to_contain_text("skills --list --verbose")

    def test_skill_bars_contain_filled_blocks(self, portfolio_local_ready: PortfolioPage) -> None:
        """Every skill row bar must contain at least one filled '█' block character."""
        portfolio_local_ready.scroll_to_section("skills")
        for row in portfolio_local_ready.skills.skill_rows.all():
            bar_el = row.locator("[class*='skill-bar']")
            bar_text = bar_el.inner_text()
            assert "█" in bar_text, f"No filled block in bar: {bar_text!r}"

    def test_skills_section_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #skills section element must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("skills")
        expect(portfolio_local_ready.skills.section).to_be_visible()

    def test_skills_heading_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """The section heading must read exactly 'Skills'."""
        portfolio_local_ready.scroll_to_section("skills")
        expect(portfolio_local_ready.skills.heading).to_have_text("Skills")

    def test_terminal_dot_colours_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """All three traffic-light dot colours (red, yellow, green) must be present in the terminal."""
        portfolio_local_ready.scroll_to_section("skills")
        terminal = portfolio_local_ready.skills.terminal
        expect(terminal.locator(".dot-red")).to_be_attached()
        expect(terminal.locator(".dot-yellow")).to_be_attached()
        expect(terminal.locator(".dot-green")).to_be_attached()
