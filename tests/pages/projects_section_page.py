"""Page Object — Projects section."""
from playwright.sync_api import Page, Locator, expect


class ProjectsSection:
    """Represents the Featured Projects section (#projects)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.section: Locator = page.locator("#projects")
        self.heading: Locator = page.locator("#projects h2")
        self.cards: Locator = page.locator(".project-card")

    # --- Queries ---

    def get_card_count(self) -> int:
        return self.cards.count()

    def card_by_index(self, index: int) -> Locator:
        return self.cards.nth(index)

    def card_by_title(self, title: str) -> Locator:
        return self.cards.filter(has_text=title)

    def get_github_link(self, card: Locator) -> str:
        return card.locator(".project-link").get_attribute("href") or ""

    def get_tags(self, card: Locator) -> list[str]:
        return card.locator(".blog-tag").all_inner_texts()

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.heading).to_be_visible()

    def expect_card_count(self, count: int) -> None:
        expect(self.cards).to_have_count(count)

    def expect_github_links_open_new_tab(self) -> None:
        """All project 'View on GitHub' links should open in a new tab."""
        for link in self.cards.locator(".project-link").all():
            expect(link).to_have_attribute("target", "_blank")
            expect(link).to_have_attribute("rel", "noopener noreferrer")

    def expect_card_visible(self, title: str) -> None:
        expect(self.card_by_title(title)).to_be_visible()

