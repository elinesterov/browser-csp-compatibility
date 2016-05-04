import pytest

from utils.page_model import FormActionPage
from utils.server import Server
from utils.config import config
from tests.common import generate_test_url


@pytest.mark.parametrize("header, meta, method", [(True, False, 'post'),
                                                  (True, False, 'get'),
                                                  (False, True, 'post'),
                                                  (False, True, 'get')
                                                  ])
def test_form_action_allowed(browser, header, meta, method):
    """
    Test submitting a form is allowed if CSP is "form-action 'self'"
    """
    policy = "form-action 'self'"
    params = "method={0}".format(method)
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='form-action', params=params)
    form_page = FormActionPage(browser).open(url)
    echo_page = form_page.submit_form()
    assert echo_page.on_page(wait_for_page_to_load=True)
    assert server.is_request_received(method, '/echo', ignore_query=True)


@pytest.mark.parametrize("header, meta, method", [(True, False, 'post'),
                                                  (True, False, 'get'),
                                                  (False, True, 'post'),
                                                  (False, True, 'get')
                                                  ])
def test_form_action_blocked(browser, header, meta, method):
    """
    Test submitting a form is blocked if CSP is "form-action 'none'"
    """
    policy = "form-action 'none'"
    params = "method={0}".format(method)
    server = Server(config['server_address'], config['server_port'])
    server.update_log_pointer()
    url = generate_test_url(policy, header=header, meta=meta, allow=False,
                            fixture_url='form-action', params=params)
    form_page = FormActionPage(browser).open(url)
    echo_page = form_page.submit_form()

    assert not echo_page.on_page(wait_for_page_to_load=True)
    assert not server.is_request_received(method, '/echo', ignore_query=True)
