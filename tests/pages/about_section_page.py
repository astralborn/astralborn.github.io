"""Page Object — About section."""
from playwright.sync_api import Page, Locator, expect


class AboutSection:
    """Represents the About Me section (#about)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.section: Locator = page.locator("#about")
        self.heading: Locator = page.locator("#about h2")
        self.intro_text: Locator = page.locator(".about-intro")
        self.stats: Locator = page.locator(".stat-item")
        self.code_window: Locator = page.locator(".code-window")
        self.code_title: Locator = page.locator(".code-title")
        self.code_content: Locator = page.locator(".code-content")

    # --- Queries ---

    def get_stat_count(self) -> int:
        return self.stats.count()

    def get_code_title(self) -> str:
        return self.code_title.inner_text()

    def get_intro_text(self) -> str:
        return self.intro_text.inner_text()

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.heading).to_be_visible()

    def expect_code_window_visible(self) -> None:
        expect(self.code_window).to_be_visible()

    def expect_intro_contains(self, text: str) -> None:
        expect(self.intro_text).to_contain_text(text)

    def expect_stat_count(self, count: int) -> None:
        expect(self.stats).to_have_count(count)

