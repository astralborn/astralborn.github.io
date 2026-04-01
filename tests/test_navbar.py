"""Tests — Navigation bar."""
import re
import pytest
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage


class TestNavBar:
    """Verify the sticky navigation bar, links, CV button, and active-scroll behaviour."""

    def test_logo_contains_astralborn(self, portfolio_local_ready: PortfolioPage) -> None:
        """Logo text must include 'astralborn' (case-insensitive)."""
        portfolio_local_ready.nav.expect_logo_contains("astralborn")

    def test_all_nav_links_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """All 5 section links (Home, About, Skills, Projects, Contact) must be visible."""
        portfolio_local_ready.nav.expect_all_nav_links_visible()

    def test_cv_link_is_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """'View CV' button must be visible in the nav bar."""
        portfolio_local_ready.nav.expect_cv_link_visible()

    def test_cv_link_opens_in_new_tab(self, portfolio_local_ready: PortfolioPage) -> None:
        """CV link must have target='_blank' so it opens in a new tab."""
        expect(portfolio_local_ready.nav.cv_link).to_have_attribute("target", "_blank")

    def test_cv_link_points_to_pdf(self, portfolio_local_ready: PortfolioPage) -> None:
        """CV link href must end in .pdf — not an HTML page or a broken path."""
        href = portfolio_local_ready.nav.cv_link.get_attribute("href") or ""
        assert href.endswith(".pdf"), f"Expected a PDF link, got: {href}"

    def test_hamburger_button_exists(self, portfolio_local_ready: PortfolioPage) -> None:
        """Hamburger toggle element (.hamburger) must be present in the DOM."""
        expect(portfolio_local_ready.nav.hamburger).to_be_attached()

    @pytest.mark.parametrize("label", ["Home", "About", "Skills", "Projects", "Contact"])
    def test_nav_link_has_correct_anchor(
        self, portfolio_local_ready: PortfolioPage, label: str
    ) -> None:
        """Each nav link must use an anchor href (#section) matching its label."""
        link = portfolio_local_ready.nav.nav_link(label)
        href = link.get_attribute("href") or ""
        assert href.startswith("#"), f"Expected anchor href, got: {href}"
        assert label.lower() in href.lower()

    def test_logo_contains_prompt_chars(self, portfolio_local_ready: PortfolioPage) -> None:
        """Logo text must contain '>>' to maintain the shell-prompt branding."""
        logo_text = portfolio_local_ready.nav.get_logo_text()
        assert ">>" in logo_text

    def test_cv_link_text_contains_view_cv(self, portfolio_local_ready: PortfolioPage) -> None:
        """CV button label must contain the text 'View CV'."""
        expect(portfolio_local_ready.nav.cv_link).to_contain_text("View CV")

    def test_nav_active_class_set_on_scroll(self, portfolio_local_ready: PortfolioPage) -> None:
        """Scrolling to #about must apply the .nav-active class to the About link."""
        portfolio_local_ready.scroll_to_section("about")
        about_link = portfolio_local_ready.nav.nav_link("About")
        expect(about_link).to_have_class(re.compile(r"nav-active"), timeout=3_000)

    def test_nav_is_present_in_dom(self, portfolio_local_ready: PortfolioPage) -> None:
        """The <nav> element must be attached to the DOM at all times."""
        expect(portfolio_local_ready.nav.nav).to_be_attached()

    def test_five_nav_links_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """#navLinks must contain at least 5 anchor elements (5 sections + 1 CV button)."""
        links = portfolio_local_ready.nav.nav_links_container.get_by_role("link")
        count = links.count()
        assert count >= 5, f"Expected at least 5 nav links, got {count}"

    def test_cv_link_has_noopener(self, portfolio_local_ready: PortfolioPage) -> None:
        """CV link must have rel=noopener (noreferrer) — required security practice for target=_blank."""
        expect(portfolio_local_ready.nav.cv_link).to_have_attribute(
            "rel", re.compile(r"noopener")
        )

    @pytest.mark.parametrize("section", ["about", "skills", "projects", "contact"])
    def test_nav_active_updates_per_section(
        self, portfolio_local_ready: PortfolioPage, section: str
    ) -> None:
        """Scrolling to each section must activate the matching nav link (.nav-active)."""
        portfolio_local_ready.scroll_to_section(section)
        link = portfolio_local_ready.nav.nav_link(section.capitalize())
        expect(link).to_have_class(re.compile(r"nav-active"), timeout=3_000)

    @pytest.mark.parametrize("label,section_id", [
        ("About",    "about"),
        ("Skills",   "skills"),
        ("Projects", "projects"),
        ("Contact",  "contact"),
    ])
    def test_nav_link_click_scrolls_to_section(
        self, portfolio_local_ready: PortfolioPage, label: str, section_id: str
    ) -> None:
        """Clicking each nav link must scroll the matching section into the viewport."""
        portfolio_local_ready.nav.click_nav_link_and_wait(label, section_id)

    def test_home_nav_link_click_scrolls_to_top(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Clicking 'Home' after scrolling down must bring #home back into the viewport."""
        portfolio_local_ready.scroll_to_section("contact")
        portfolio_local_ready.nav.click_nav_link_and_wait("Home", "home")

