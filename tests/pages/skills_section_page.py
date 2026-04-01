"""Page Object — Skills section."""
from playwright.sync_api import Page, Locator, expect


class SkillsSection:
    """Represents the Skills section (#skills)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.section: Locator = page.locator("#skills")
        self.heading: Locator = page.locator("#skills h2")
        self.terminal: Locator = page.locator(".skills-terminal")
        self.skill_rows: Locator = page.locator(".skill-row")
        self.skill_headings: Locator = page.locator(".skill-cat-heading")

    # --- Queries ---

    def get_skill_row_count(self) -> int:
        return self.skill_rows.count()

    def get_category_headings(self) -> list[str]:
        return self.skill_headings.all_inner_texts()

    def get_skill_names(self) -> list[str]:
        return [
            row.locator(".skill-name-col").first.inner_text()
            for row in self.skill_rows.all()
        ]

    def get_skill_labels(self) -> list[str]:
        label_els = self.section.locator("[class*='skill-label']")
        return label_els.all_inner_texts()

    # --- Assertions ---

    def expect_terminal_visible(self) -> None:
        expect(self.terminal).to_be_visible()

    def expect_heading_visible(self) -> None:
        expect(self.heading).to_be_visible()

    def expect_skill_row_count(self, count: int) -> None:
        expect(self.skill_rows).to_have_count(count)

    def expect_skill_present(self, name: str) -> None:
        """Assert that a skill with the given name exists in the list."""
        matching = self.section.locator(".skill-name-col", has_text=name)
        expect(matching.first).to_be_visible()

