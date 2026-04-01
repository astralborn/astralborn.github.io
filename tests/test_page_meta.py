"""Tests — Page-level metadata, title, footer, and 404 page."""
import pathlib
import re
from datetime import date

from playwright.sync_api import Page, expect

from tests.pages.portfolio_page import PortfolioPage


class TestPageMeta:
    """Verify <head> metadata: title, description, Open Graph, Twitter card, and document attributes."""

    def test_page_title_contains_astralborn(self, portfolio_local_ready: PortfolioPage) -> None:
        """Browser tab title must contain 'astralborn'."""
        assert "astralborn" in portfolio_local_ready.get_title().lower()

    def test_meta_description_mentions_prague(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Meta description must mention Prague as the engineer's location."""
        desc = portfolio_local_ready.get_meta_description()
        assert "Prague" in desc

    def test_meta_description_mentions_playwright(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Meta description must include 'Playwright' as part of the tech stack."""
        desc = portfolio_local_ready.get_meta_description()
        assert "Playwright" in desc

    def test_meta_author_is_astralborn(self, portfolio_local_ready: PortfolioPage) -> None:
        """meta[name='author'] must be set to 'astralborn'."""
        author = (
            portfolio_local_ready._page
            .locator("meta[name='author']")
            .get_attribute("content")
        )
        assert author == "astralborn"

    def test_favicon_linked(self, portfolio_local_ready: PortfolioPage) -> None:
        """A favicon link element must be present and point to an SVG file."""
        favicon = portfolio_local_ready._page.locator("link[rel='icon']")
        href = favicon.get_attribute("href") or ""
        assert href.endswith(".svg")

    def test_og_title_set(self, portfolio_local_ready: PortfolioPage) -> None:
        """og:title meta property must be set to a non-empty value."""
        og_title = (
            portfolio_local_ready._page
            .locator("meta[property='og:title']")
            .get_attribute("content") or ""
        )
        assert og_title.strip() != ""

    def test_og_image_is_mockup(self, portfolio_local_ready: PortfolioPage) -> None:
        """og:image must point to the mockup.png screenshot."""
        og_image = (
            portfolio_local_ready._page
            .locator("meta[property='og:image']")
            .get_attribute("content") or ""
        )
        assert "mockup.png" in og_image

    def test_og_url_is_set(self, portfolio_local_ready: PortfolioPage) -> None:
        """og:url must be set to a non-empty canonical URL."""
        og_url = (
            portfolio_local_ready._page
            .locator("meta[property='og:url']")
            .get_attribute("content") or ""
        )
        assert og_url.strip() != ""

    def test_twitter_card_is_set(self, portfolio_local_ready: PortfolioPage) -> None:
        """twitter:card meta tag must be present and non-empty (e.g. 'summary_large_image')."""
        card = (
            portfolio_local_ready._page
            .locator("meta[name='twitter:card']")
            .get_attribute("content") or ""
        )
        assert card.strip() != ""

    def test_twitter_title_is_set(self, portfolio_local_ready: PortfolioPage) -> None:
        """twitter:title meta tag must be present and non-empty."""
        title = (
            portfolio_local_ready._page
            .locator("meta[name='twitter:title']")
            .get_attribute("content") or ""
        )
        assert title.strip() != ""

    def test_twitter_image_is_mockup(self, portfolio_local_ready: PortfolioPage) -> None:
        """twitter:image must point to the mockup.png screenshot."""
        image = (
            portfolio_local_ready._page
            .locator("meta[name='twitter:image']")
            .get_attribute("content") or ""
        )
        assert "mockup.png" in image

    def test_lang_attribute_is_en(self, portfolio_local_ready: PortfolioPage) -> None:
        """The <html> element must have lang='en' for accessibility and SEO."""
        lang = portfolio_local_ready._page.locator("html").get_attribute("lang") or ""
        assert lang == "en"

    def test_charset_is_utf8(self, portfolio_local_ready: PortfolioPage) -> None:
        """The <meta charset> declaration must be 'utf-8'."""
        charset = (
            portfolio_local_ready._page
            .locator("meta[charset]")
            .get_attribute("charset") or ""
        )
        assert charset.lower() == "utf-8"


class TestFooter:
    """Verify the footer: visibility, dynamic year, signature, and sub-text."""

    def test_footer_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The <footer> element must be visible at the bottom of the page."""
        portfolio_local_ready.expect_footer_visible()

    def test_footer_contains_current_year(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #year span must display the current calendar year (set dynamically by JS)."""
        year = portfolio_local_ready.get_footer_year()
        assert year == str(date.today().year)

    def test_footer_contains_astralborn_signature(
        self, portfolio_local_ready: PortfolioPage
    ) -> None:
        """Footer must include the 'astralborn' author signature."""
        expect(portfolio_local_ready.footer).to_contain_text("astralborn")

    def test_footer_contains_react_joke(self, portfolio_local_ready: PortfolioPage) -> None:
        """Footer sub-text must mention 'React' as part of the 'no React' joke."""
        expect(portfolio_local_ready.footer).to_contain_text("React")

    def test_footer_sub_contains_vanilla_js(self, portfolio_local_ready: PortfolioPage) -> None:
        """Footer .footer-sub line must state the site is built with 'vanilla JS'."""
        sub = portfolio_local_ready._page.locator(".footer-sub")
        expect(sub).to_contain_text("vanilla JS")

    def test_footer_contains_copyright_symbol(self, portfolio_local_ready: PortfolioPage) -> None:
        """Footer must contain the © copyright symbol."""
        footer_text = portfolio_local_ready.footer.inner_text()
        assert "©" in footer_text, "Footer should contain the © copyright symbol"


class Test404Page:
    """Verify the custom 404 page is served correctly for unknown routes."""

    # ── helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _goto_404(page: Page) -> None:
        index_404 = pathlib.Path(__file__).parent.parent / "404.html"
        page.goto(index_404.as_uri())

    # ── meta / structure ─────────────────────────────────────────────────────

    def test_404_page_loads(self, page: Page) -> None:
        """404.html must load and have a title containing '404'."""
        self._goto_404(page)
        expect(page).to_have_title(re.compile(r"404", re.IGNORECASE))

    def test_404_page_has_go_home_link(self, page: Page) -> None:
        """404 page must contain a visible 'return to base' home link (.home-link)."""
        self._goto_404(page)
        home_link = page.locator("a.home-link")
        expect(home_link).to_be_visible(timeout=5_000)
        expect(home_link).to_contain_text("return to base")

    def test_404_error_code_displayed(self, page: Page) -> None:
        """The large .error-code element must display the text '404'."""
        self._goto_404(page)
        error_code = page.locator(".error-code")
        expect(error_code).to_be_visible()
        expect(error_code).to_contain_text("404")

    def test_404_terminal_block_is_visible(self, page: Page) -> None:
        """The themed terminal block (.terminal) must be rendered on the page."""
        self._goto_404(page)
        expect(page.locator(".terminal")).to_be_visible()

    def test_404_error_label_shown(self, page: Page) -> None:
        """The .error-label must contain the exception hint text."""
        self._goto_404(page)
        expect(page.locator(".error-label")).to_contain_text("PathNotFoundException")

    def test_404_lang_attribute_is_en(self, page: Page) -> None:
        """The <html> element on the 404 page must carry lang='en'."""
        self._goto_404(page)
        lang = page.locator("html").get_attribute("lang") or ""
        assert lang == "en"

    # ── interactions ─────────────────────────────────────────────────────────

    def test_404_home_link_href_points_to_root(self, page: Page) -> None:
        """The home link href must target the site root ('/')."""
        self._goto_404(page)
        href = page.locator("a.home-link").get_attribute("href") or ""
        assert href == "/", f"Expected href='/', got '{href}'"

    def test_404_home_link_click_navigates_away(self, page: Page) -> None:
        """Clicking the home link must navigate the browser away from the 404 page."""
        self._goto_404(page)
        url_before = page.url
        with page.expect_navigation():
            page.locator("a.home-link").click()
        assert page.url != url_before, "URL should change after clicking the home link"

    def test_404_home_link_is_keyboard_focusable(self, page: Page) -> None:
        """The home link must be reachable via keyboard Tab."""
        self._goto_404(page)
        page.keyboard.press("Tab")
        focused_tag = page.evaluate("document.activeElement.tagName").lower()
        focused_class = page.evaluate("document.activeElement.className")
        assert focused_tag == "a" and "home-link" in focused_class, (
            f"Expected <a class='home-link'> to be focused, "
            f"got <{focused_tag} class='{focused_class}'>"
        )

    def test_404_home_link_hover_changes_style(self, page: Page) -> None:
        """Hovering the home link must apply a background (CSS hover transition)."""
        self._goto_404(page)
        link = page.locator("a.home-link")
        link.hover()
        bg_color = link.evaluate("el => getComputedStyle(el).backgroundColor")
        # The hover rule sets background: #00FF8C — must be non-transparent
        assert bg_color != "rgba(0, 0, 0, 0)", (
            f"Expected a coloured background on hover, got '{bg_color}'"
        )

    def test_404_bad_path_script_runs(self, page: Page) -> None:
        """The inline JS must inject the current pathname into #badpath."""
        self._goto_404(page)
        bad_path_text = page.locator("#badpath").inner_text()
        # When opened as a file:// URI the pathname will not be empty
        assert bad_path_text.strip() != "", "#badpath should be populated by the inline script"

