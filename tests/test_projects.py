"""Tests — Projects section."""
import pytest
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage

EXPECTED_PROJECTS = [
    {
        "title": "WSL Port Bridge",
        "tags": ["Python", "Networking", "WSL"],
        "github": "WindowsWslPortBridge",
    },
    {
        "title": "API Tester",
        "tags": ["Python", "API Testing", "PySide6"],
        "github": "API-tester",
    },
    {
        "title": "This Portfolio",
        "tags": ["JavaScript", "CSS", "HTML"],
        "github": "astralborn.github.io",
    },
]


class TestProjectsSection:
    """Verify the featured projects grid: card presence, GitHub links, tags, and descriptions."""

    def test_projects_heading_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #projects <h2> heading must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("projects")
        portfolio_local_ready.projects.expect_heading_visible()

    def test_three_project_cards_present(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """The projects grid must contain exactly 3 project cards."""
        portfolio_local_ready.scroll_to_section("projects")
        portfolio_local_ready.projects.expect_card_count(3)

    @pytest.mark.parametrize("project", EXPECTED_PROJECTS, ids=[p["title"] for p in EXPECTED_PROJECTS])
    def test_project_card_visible(
        self, portfolio_local_ready: PortfolioPage, project: dict
    ) -> None:
        """Each project card must be visible and identifiable by its title."""
        portfolio_local_ready.scroll_to_section("projects")
        portfolio_local_ready.projects.expect_card_visible(project["title"])

    @pytest.mark.parametrize("project", EXPECTED_PROJECTS, ids=[p["title"] for p in EXPECTED_PROJECTS])
    def test_project_github_link_points_to_correct_repo(
        self, portfolio_local_ready: PortfolioPage, project: dict
    ) -> None:
        """Each project's GitHub link href must contain the expected repository slug."""
        portfolio_local_ready.scroll_to_section("projects")
        card = portfolio_local_ready.projects.card_by_title(project["title"])
        href = portfolio_local_ready.projects.get_github_link(card)
        assert project["github"].lower() in href.lower(), (
            f"Expected '{project['github']}' in href, got: {href}"
        )

    @pytest.mark.parametrize("project", EXPECTED_PROJECTS, ids=[p["title"] for p in EXPECTED_PROJECTS])
    def test_project_tags_correct(
        self, portfolio_local_ready: PortfolioPage, project: dict
    ) -> None:
        """Each project card's technology tags must exactly match the expected list in order."""
        portfolio_local_ready.scroll_to_section("projects")
        card = portfolio_local_ready.projects.card_by_title(project["title"])
        tags = portfolio_local_ready.projects.get_tags(card)
        assert tags == project["tags"], f"Tag mismatch for {project['title']}: {tags}"

    def test_all_github_links_open_new_tab(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """All 'View on GitHub' links must have target=_blank and rel=noopener noreferrer."""
        portfolio_local_ready.scroll_to_section("projects")
        portfolio_local_ready.projects.expect_github_links_open_new_tab()

    @pytest.mark.parametrize("project", EXPECTED_PROJECTS, ids=[p["title"] for p in EXPECTED_PROJECTS])
    def test_project_card_has_description(
        self, portfolio_local_ready: PortfolioPage, project: dict
    ) -> None:
        """Each project card must include a non-empty description paragraph."""
        portfolio_local_ready.scroll_to_section("projects")
        card = portfolio_local_ready.projects.card_by_title(project["title"])
        desc = card.locator("p").first.inner_text()
        assert desc.strip() != "", f"Card '{project['title']}' has empty description"

    @pytest.mark.parametrize("project", EXPECTED_PROJECTS, ids=[p["title"] for p in EXPECTED_PROJECTS])
    def test_project_link_text_says_view_on_github(
        self, portfolio_local_ready: PortfolioPage, project: dict
    ) -> None:
        """Each project link (.project-link) must contain the text 'View on GitHub'."""
        portfolio_local_ready.scroll_to_section("projects")
        card = portfolio_local_ready.projects.card_by_title(project["title"])
        expect(card.locator(".project-link")).to_contain_text("View on GitHub")

    def test_projects_heading_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """The section heading must read exactly 'Featured Projects'."""
        portfolio_local_ready.scroll_to_section("projects")
        expect(portfolio_local_ready.projects.heading).to_have_text("Featured Projects")

    def test_projects_section_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #projects section element must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("projects")
        expect(portfolio_local_ready.projects.section).to_be_visible()

    def test_all_github_links_point_to_github_com(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Every project link href must contain 'github.com' — no broken or misrouted URLs."""
        portfolio_local_ready.scroll_to_section("projects")
        for card in portfolio_local_ready.projects.cards.all():
            href = portfolio_local_ready.projects.get_github_link(card)
            assert "github.com" in href.lower(), f"Expected github.com in href, got: {href}"
