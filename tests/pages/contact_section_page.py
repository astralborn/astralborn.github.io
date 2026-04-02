"""Page Object — Contact section."""
from playwright.sync_api import Page, Locator, expect


class ContactSection:
    """Represents the Get In Touch / Contact section (#contact)."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.section: Locator = page.locator("#contact")
        self.heading: Locator = page.locator("#contact h2")
        self.terminal: Locator = page.locator(".contact-terminal")

        self.email_link: Locator = page.locator("a.contact-link[href^='mailto']")
        self.github_link: Locator = page.locator("a.contact-link[href*='github']")
        self.linkedin_link: Locator = page.locator("a.contact-link[href*='linkedin']")

        self.copy_buttons: Locator = page.locator(".copy-btn")

    # --- Queries ---

    def get_copy_button_count(self) -> int:
        return self.copy_buttons.count()

    def copy_button_for(self, value: str) -> Locator:
        return self.section.locator(f".copy-btn[data-copy='{value}']")

    # --- Actions ---

    def click_copy_email(self) -> None:
        self.copy_button_for("stas.nikolaevski@gmail.com").click()

    def click_copy_github(self) -> None:
        self.copy_button_for("github.com/astralborn").click()

    def click_copy_linkedin(self) -> None:
        self.copy_button_for("linkedin.com/in/stas-nikolaievskyi").click()

    # --- Assertions ---

    def expect_heading_visible(self) -> None:
        expect(self.heading).to_be_visible()

    def expect_terminal_visible(self) -> None:
        expect(self.terminal).to_be_visible()

    def expect_email_link_correct(self) -> None:
        expect(self.email_link).to_have_attribute("href", "mailto:stas.nikolaevski@gmail.com")

    def expect_github_link_correct(self) -> None:
        expect(self.github_link).to_have_attribute("href", "https://github.com/astralborn")

    def expect_linkedin_link_correct(self) -> None:
        expect(self.linkedin_link).to_have_attribute(
            "href", "https://linkedin.com/in/stas-nikolaievskyi"
        )

    def expect_external_links_open_new_tab(self) -> None:
        for link in [self.github_link, self.linkedin_link]:
            expect(link).to_have_attribute("target", "_blank")
            expect(link).to_have_attribute("rel", "noopener noreferrer")

    def expect_copy_button_changes_text_after_click(self, value: str) -> None:
        """Click a copy button and verify it changes to [✓] then reverts.

        Requires a real clipboard permission grant (headed mode / cdp).
        """
        btn = self.copy_button_for(value)
        btn.click()
        expect(btn).to_have_text("[✓]", timeout=2_000)
        expect(btn).to_have_text("[copy]", timeout=3_000)

