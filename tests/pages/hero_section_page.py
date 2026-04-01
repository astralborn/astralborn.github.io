"""Page Object — Hero section."""
from playwright.sync_api import Page, Locator, expect


class HeroSection:
    """Represents the hero / landing section (#home)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.section: Locator = page.locator("#home")
        self.tag: Locator = page.locator(".tag")
        self.subtitle: Locator = page.locator(".subtitle")
        self.photo: Locator = page.locator(".hero-photo")
        self.terminal_window: Locator = page.locator(".hero-terminal")
        self.projects_link: Locator = page.locator(".hero-terminal a[href='#projects']")
        self.contact_link: Locator = page.locator(".hero-terminal a[href='#contact']")

    # --- Queries ---

    def get_tag_text(self) -> str:
        return self.tag.inner_text()

    def get_subtitle_text(self) -> str:
        return self.subtitle.inner_text()

    # --- Actions ---

    def click_projects_link(self) -> None:
        self.projects_link.click()

    def click_contact_link(self) -> None:
        self.contact_link.click()

    # --- Assertions ---

    def expect_photo_visible(self) -> None:
        expect(self.photo).to_be_visible()

    def expect_terminal_visible(self) -> None:
        expect(self.terminal_window).to_be_visible()

    def expect_tag_contains(self, text: str) -> None:
        expect(self.tag).to_contain_text(text)

