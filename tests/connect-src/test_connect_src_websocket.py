import pytest

from utils.page_model import TestResultPage
from utils.server import Server
from utils.config import config
from tests.common import generate_test_url


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_connect_src_websocket_allowed(browser, header, meta):
    """
    Test websocket connection is allowed if
    CSP is "connect-src ws://127.0.0.1:8000"
    """
    policy = "connect-src ws://127.0.0.1:8000"
    params = "websocket=true"
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='connect-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
    assert server.is_request_reseived('get', '/echo')


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_connect_src_websocket_blocked(browser, header, meta):
    """
    Test websocket connection is blocked if
    CSP is "connect-src ws://localhost:8000"
    """
    policy = "connect-src ws://localhost:8000"
    params = "websocket=true"
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=False,
                            fixture_url='connect-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
    assert not server.is_request_reseived('get', '/echo')
