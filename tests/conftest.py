"""
Shared fixtures for the portfolio test suite.

Running locally against the live site (default)
------------------------------------------------
pytest tests/

Running against a local file server
-------------------------------------
pytest tests/ --base-url ""  (override BASE_URL in portfolio_page.py)

Playwright CLI options used below:
  --headed        show the browser
  --slowmo 500    slow down by 500 ms
"""
import pathlib

import pytest
from playwright.sync_api import Page

from tests.pages.portfolio_page import PortfolioPage

# Absolute path to index.html — used for offline tests.
_INDEX = pathlib.Path(__file__).parent.parent / "index.html"
LOCAL_FILE_URL = _INDEX.as_uri()


@pytest.fixture()
def portfolio(page: Page) -> PortfolioPage:
    """
    Navigates to the live portfolio page, returns a ready-to-use PortfolioPage.
    The boot screen is NOT dismissed — individual tests decide when/how to do that.
    """
    po = PortfolioPage(page)
    po.open()
    return po


@pytest.fixture()
def portfolio_local(page: Page) -> PortfolioPage:
    """
    Opens index.html from the local filesystem — no network required.
    Boot screen is not dismissed.
    """
    po = PortfolioPage(page)
    po.open_local(str(_INDEX))
    return po


@pytest.fixture()
def portfolio_ready(page: Page) -> PortfolioPage:
    """
    Navigates to the live site AND dismisses the boot screen so tests
    can interact with the main content immediately.
    """
    po = PortfolioPage(page)
    po.open()
    po.dismiss_boot_screen()
    return po


@pytest.fixture()
def portfolio_local_ready(page: Page) -> PortfolioPage:
    """Local variant with boot screen already dismissed."""
    po = PortfolioPage(page)
    po.open_local(str(_INDEX))
    po.dismiss_boot_screen()
    return po

