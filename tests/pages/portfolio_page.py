"""Top-level Page Object — full portfolio page."""
from playwright.sync_api import Page, Locator, expect

from tests.pages.boot_screen_page import BootScreen
from tests.pages.navbar_page import NavBar
from tests.pages.hero_section_page import HeroSection
from tests.pages.about_section_page import AboutSection
from tests.pages.skills_section_page import SkillsSection
from tests.pages.projects_section_page import ProjectsSection
from tests.pages.contact_section_page import ContactSection

BASE_URL = "https://astralborn.github.io"


class PortfolioPage:
    """
    Facade that composes all section page objects.

    Usage
    -----
    portfolio = PortfolioPage(page)
    portfolio.open()
    portfolio.dismiss_boot_screen()
    portfolio.nav.click_nav_link("About")
    """

    def __init__(self, page: Page) -> None:
        self._page = page
        self.boot_screen = BootScreen(page)
        self.nav = NavBar(page)
        self.hero = HeroSection(page)
        self.about = AboutSection(page)
        self.skills = SkillsSection(page)
        self.projects = ProjectsSection(page)
        self.contact = ContactSection(page)
        self.footer: Locator = page.locator("footer")

    # --- Navigation ---

    def open(self, base_url: str = BASE_URL) -> None:
        self._page.goto(base_url)

    def open_local(self, path: str) -> None:
        """Open a local HTML file, e.g. for offline testing."""
        self._page.goto(f"file:///{path}")

    def dismiss_boot_screen(self) -> None:
        """Click to skip the boot animation and wait for it to disappear."""
        self.boot_screen.dismiss_by_click()
        self.boot_screen.wait_until_gone()

    def scroll_to_section(self, section_id: str) -> None:
        self._page.evaluate(
            "id => document.getElementById(id).scrollIntoView({behavior:'instant'})",
            section_id,
        )

    # --- Meta / Footer ---

    def get_title(self) -> str:
        return self._page.title()

    def get_meta_description(self) -> str:
        return (
            self._page.locator("meta[name='description']").get_attribute("content") or ""
        )

    def get_footer_year(self) -> str:
        return self._page.locator("#year").inner_text()

    def expect_title_contains(self, text: str) -> None:
        expect(self._page).to_have_title(f".*{text}.*")

    def expect_footer_visible(self) -> None:
        expect(self.footer).to_be_visible()

