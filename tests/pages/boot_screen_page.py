"""Page Object — Boot Screen overlay."""
from playwright.sync_api import Page, Locator, expect


class BootScreen:
    """Represents the terminal boot screen that appears on first load."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self.container: Locator = page.locator("#bootScreen")
        self.ascii_art: Locator = page.locator(".ascii-art")
        self.progress_bar: Locator = page.locator(".boot-progress-bar")
        self.footer: Locator = page.locator(".boot-footer")
        self.boot_lines: Locator = page.locator(".boot-terminal p")

    # --- Queries ---

    def is_visible(self) -> bool:
        return self.container.is_visible()

    def get_status_labels(self) -> list[str]:
        return self.boot_lines.all_inner_texts()

    # --- Actions ---

    def dismiss_by_click(self) -> None:
        self.container.click()

    def dismiss_by_key(self, key: str = "Escape") -> None:
        """Press any key to trigger the keydown dismiss handler. Defaults to Escape."""
        self._page.keyboard.press(key)

    def wait_for_auto_dismiss(self, timeout: float = 8_000) -> None:
        """Wait for the boot screen to auto-dismiss (default timeout ≥ 6 s)."""
        expect(self.container).to_be_hidden(timeout=timeout)

    def wait_until_gone(self, timeout: float = 3_000) -> None:
        expect(self.container).to_be_hidden(timeout=timeout)

