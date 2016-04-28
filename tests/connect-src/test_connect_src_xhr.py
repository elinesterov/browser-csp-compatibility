import pytest

from utils.page_model import BasePage
from utils.server import Server
from utils.config import config
from tests.common import generate_test_url


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_connect_src_xhr_allowed(browser, header, meta):
    """
    Test sending xhr is allowed if CSP is "connect-src 'self'"
    """
    policy = "connect-src 'self'"
    params = "xhr=true"
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='connect-src', params=params)
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
    assert server.is_request_reseived('get', '/ping')


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_connect_src_xhr_blocked(browser, header, meta):
    """
    Test sending xhr is blocked if CSP is "connect-src 'none'"
    """
    policy = "connect-src 'none'"
    params = "xhr=true"
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=False,
                            fixture_url='connect-src', params=params)
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
    assert not server.is_request_reseived('get', '/ping')
