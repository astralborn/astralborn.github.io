"""Tests that the retired Skills section is absent from the portfolio."""
from playwright.sync_api import expect

from tests.pages.portfolio_page import PortfolioPage


def test_skills_section_is_removed(portfolio_local_ready: PortfolioPage) -> None:
    expect(portfolio_local_ready._page.locator("#skills")).to_have_count(0)
    expect(portfolio_local_ready._page.locator('a[href="#skills"]')).to_have_count(0)
    expect(portfolio_local_ready._page.locator(".skills-terminal")).to_have_count(0)
