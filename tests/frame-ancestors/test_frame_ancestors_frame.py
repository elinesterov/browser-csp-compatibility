import pytest

from utils.page_model import TestResultPage
from utils.config import config
from tests.common import generate_test_url

UNALLOWED_PORT = config['server_port'] + 1
SAME_ORIGIN = 'http://' + config['server_address'] + ':' + str(config['server_port'])
DIFFERENT_ORIGIN = 'http://' + config['server_address'] + str(UNALLOWED_PORT)


def test_frame_ancestors_origin_allowed(browser):
    """
    Test frame is loaded if CSP dirctive frame-ancestors allows to load
    on the origin which is trying to load it
    e.g. if base page is http://127.0.0.1:8000 and it loads frame
    which has CSP directive frame-ancestors http://127.0.0.1:8000
    """
    policy = "frame-ancestors {0}".format(SAME_ORIGIN)
    params = "iframe=true"
    url = generate_test_url(policy, header=True, meta=False, allow=True,
                            fixture_url='frame-ancestors', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')


def test_frame_ancestors_origin_unallowed(browser):
    """
    Test frame is blocked if CSP dirctive frame-ancestors does not allow
    to load on the origin which is trying to load it
    e.g. if base page is http://127.0.0.1:8000 and it loads frame
    which has CSP directive frame-ancestors http://127.0.0.1:8001
    then since frame-ancestor directive has different origin (port)
    iFrame shoudln't be allowed load
    """

    policy = "frame-ancestors {0}".format(DIFFERENT_ORIGIN)
    params = "iframe=true"
    url = generate_test_url(policy, header=True, meta=False, allow=False,
                            fixture_url='frame-ancestors', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
