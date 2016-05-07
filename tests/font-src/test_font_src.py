import pytest

from utils.page_model import TestResultPage
from utils.server import Server
from utils.config import config
from tests.common import generate_test_url


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_font_src_allowed(browser, header, meta):
    """
    Test loading fonts allowed if CSP is "font-src 'self'"
    """
    policy = "connect-src 'self'"
    params = "xhr=true"
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='connect-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
    assert server.is_request_received('get', '/ping')


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_font_src_blocked(browser, header, meta):
    """
    Test loading fonts is blocked if CSP is "font-src 'none'"
    """
    policy = "connect-src 'none'"
    params = "xhr=true"
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=False,
                            fixture_url='connect-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
    assert not server.is_request_received('get', '/ping')
