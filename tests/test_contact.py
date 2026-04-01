"""Tests — Contact section."""
import pathlib
import pytest
from playwright.sync_api import Page, expect

from tests.pages.portfolio_page import PortfolioPage


class TestContactSection:
    """Verify the Get In Touch section: terminal content, links, copy buttons, and schemes."""

    def test_contact_heading_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #contact <h2> heading must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("contact")
        portfolio_local_ready.contact.expect_heading_visible()

    def test_contact_terminal_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The contact terminal window (.contact-terminal) must be visible."""
        portfolio_local_ready.scroll_to_section("contact")
        portfolio_local_ready.contact.expect_terminal_visible()

    def test_email_link_correct(self, portfolio_local_ready: PortfolioPage) -> None:
        """Email link href must be 'mailto:stas.nikolaevski@gmail.com'."""
        portfolio_local_ready.scroll_to_section("contact")
        portfolio_local_ready.contact.expect_email_link_correct()

    def test_github_link_correct(self, portfolio_local_ready: PortfolioPage) -> None:
        """GitHub link href must be 'https://github.com/astralborn'."""
        portfolio_local_ready.scroll_to_section("contact")
        portfolio_local_ready.contact.expect_github_link_correct()

    def test_linkedin_link_correct(self, portfolio_local_ready: PortfolioPage) -> None:
        """LinkedIn link href must be 'https://linkedin.com/in/stas-nikolaievskyi'."""
        portfolio_local_ready.scroll_to_section("contact")
        portfolio_local_ready.contact.expect_linkedin_link_correct()

    def test_external_links_open_new_tab(self, portfolio_local_ready: PortfolioPage) -> None:
        """GitHub and LinkedIn links must have target=_blank and rel=noopener noreferrer."""
        portfolio_local_ready.scroll_to_section("contact")
        portfolio_local_ready.contact.expect_external_links_open_new_tab()

    def test_three_copy_buttons_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """There must be exactly 3 copy buttons — one per contact channel."""
        portfolio_local_ready.scroll_to_section("contact")
        assert portfolio_local_ready.contact.get_copy_button_count() == 3

    @pytest.mark.parametrize("value", [
        "stas.nikolaevski@gmail.com",
        "github.com/astralborn",
        "linkedin.com/in/stas-nikolaievskyi",
    ])
    def test_copy_button_exists_for_value(
        self, portfolio_local_ready: PortfolioPage, value: str
    ) -> None:
        """Each copy button must be visible and display the default '[copy]' label."""
        portfolio_local_ready.scroll_to_section("contact")
        btn = portfolio_local_ready.contact.copy_button_for(value)
        expect(btn).to_be_visible()
        expect(btn).to_have_text("[copy]")

    def test_copy_button_text_changes_after_click(self, page: Page) -> None:
        """Clicking a copy button must change its text to '[✓]' then revert to '[copy]'.

        Clipboard-write permission is granted explicitly so the JS success path fires
        even in headless mode.
        """
        page.context.grant_permissions(["clipboard-read", "clipboard-write"])

        index = pathlib.Path(__file__).parent.parent / "index.html"
        po = PortfolioPage(page)
        po.open_local(str(index))
        po.dismiss_boot_screen()
        po.scroll_to_section("contact")

        btn = po.contact.copy_button_for("stas.nikolaevski@gmail.com")
        btn.click()
        expect(btn).to_have_text("[✓]", timeout=2_000)
        expect(btn).to_have_text("[copy]", timeout=3_000)

    def test_response_time_line_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal must contain a line mentioning 'response time'."""
        portfolio_local_ready.scroll_to_section("contact")
        terminal = portfolio_local_ready.contact.terminal
        expect(terminal).to_contain_text("response time")

    def test_contact_heading_text(self, portfolio_local_ready: PortfolioPage) -> None:
        """The section heading must read exactly 'Get In Touch'."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.heading).to_have_text("Get In Touch")

    def test_whoami_output_line_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal must include the 'whoami' output stating availability ('open to work')."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.terminal).to_contain_text("open to work")

    def test_email_command_line_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal must display the 'reach-out --method=email' command line."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.terminal).to_contain_text("reach-out --method=email")

    def test_github_command_line_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal must display the 'view-code --platform=github' command line."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.terminal).to_contain_text("view-code --platform=github")

    def test_linkedin_command_line_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal must display the 'connect --platform=linkedin' command line."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.terminal).to_contain_text("connect --platform=linkedin")

    def test_email_data_copy_matches_link_href(self, portfolio_local_ready: PortfolioPage) -> None:
        """The email copy button's data-copy value must appear inside the email link href."""
        portfolio_local_ready.scroll_to_section("contact")
        copy_value = portfolio_local_ready.contact.copy_button_for(
            "stas.nikolaevski@gmail.com"
        ).get_attribute("data-copy")
        email_href = portfolio_local_ready.contact.email_link.get_attribute("href") or ""
        assert copy_value and copy_value in email_href

    def test_terminal_cursor_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Blinking cursor element (.cursor) must be present in the contact terminal."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.terminal.locator(".cursor")).to_be_attached()

    def test_terminal_has_three_dot_decorators(self, portfolio_local_ready: PortfolioPage) -> None:
        """Contact terminal header must have exactly 3 traffic-light dots."""
        portfolio_local_ready.scroll_to_section("contact")
        dots = portfolio_local_ready.contact.terminal.locator(".terminal-dot")
        expect(dots).to_have_count(3)

    def test_all_channels_open_line_present(self, portfolio_local_ready: PortfolioPage) -> None:
        """Terminal footer line must confirm 'all channels open'."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.terminal).to_contain_text("all channels open")

    def test_contact_section_is_visible(self, portfolio_local_ready: PortfolioPage) -> None:
        """The #contact section element must be visible after scrolling into view."""
        portfolio_local_ready.scroll_to_section("contact")
        expect(portfolio_local_ready.contact.section).to_be_visible()

    def test_email_link_has_mailto_scheme(self, portfolio_local_ready: PortfolioPage) -> None:
        """Email link href must use the 'mailto:' scheme."""
        portfolio_local_ready.scroll_to_section("contact")
        href = portfolio_local_ready.contact.email_link.get_attribute("href") or ""
        assert href.startswith("mailto:"), f"Expected mailto: scheme, got: {href}"

    def test_github_link_has_https_scheme(self, portfolio_local_ready: PortfolioPage) -> None:
        """GitHub link href must use the 'https://' scheme."""
        portfolio_local_ready.scroll_to_section("contact")
        href = portfolio_local_ready.contact.github_link.get_attribute("href") or ""
        assert href.startswith("https://"), f"Expected https:// scheme, got: {href}"

    def test_linkedin_link_has_https_scheme(self, portfolio_local_ready: PortfolioPage) -> None:
        """LinkedIn link href must use the 'https://' scheme."""
        portfolio_local_ready.scroll_to_section("contact")
        href = portfolio_local_ready.contact.linkedin_link.get_attribute("href") or ""
        assert href.startswith("https://"), f"Expected https:// scheme, got: {href}"

    @pytest.mark.parametrize("value", [
        "stas.nikolaevski@gmail.com",
        "github.com/astralborn",
        "linkedin.com/in/stas-nikolaievskyi",
    ])
    def test_copy_button_has_correct_data_copy_attribute(
        self, portfolio_local_ready: PortfolioPage, value: str
    ) -> None:
        """Each copy button's data-copy attribute must exactly match the contact value it copies."""
        portfolio_local_ready.scroll_to_section("contact")
        btn = portfolio_local_ready.contact.copy_button_for(value)
        assert btn.get_attribute("data-copy") == value

