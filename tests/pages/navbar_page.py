"""Page Object — Navigation bar."""
from playwright.sync_api import Page, Locator, expect


class NavBar:
    """Represents the sticky navigation bar."""

    NAV_ITEMS = ("Home", "About", "Skills", "Projects", "Contact")

    def __init__(self, page: Page) -> None:
        self._page = page
        self.nav: Locator = page.locator("nav")
        self.logo: Locator = page.locator(".logo")
        self.hamburger: Locator = page.locator(".hamburger")
        self.nav_links_container: Locator = page.locator("#navLinks")
        self.cv_link: Locator = page.locator("a.btn-cv")

    # --- Queries ---

    def get_logo_text(self) -> str:
        return self.logo.inner_text()

    def nav_link(self, label: str) -> Locator:
        return self.nav_links_container.get_by_role("link", name=label, exact=True)

    # --- Actions ---

    def click_nav_link(self, label: str) -> None:
        self.nav_link(label).click()

    def click_cv(self) -> None:
        self.cv_link.click()

    # --- Assertions ---

    def expect_logo_contains(self, text: str) -> None:
        expect(self.logo).to_contain_text(text)

    def expect_all_nav_links_visible(self) -> None:
        for label in self.NAV_ITEMS:
            expect(self.nav_link(label)).to_be_visible()

    def expect_cv_link_visible(self) -> None:
        expect(self.cv_link).to_be_visible()
