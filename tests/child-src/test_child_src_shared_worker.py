import pytest

from utils.page_model import TestResultPage

from tests.common import generate_test_url


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_child_src_shared_worker_allowed(browser, header, meta):
    """
    Test shared worker is allowed if CSP is "child-src 'self'"
    """
    policy = "child-src 'self'"
    params = "shared=true"
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='child-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_child_src_shared_worker_blocked(browser, header, meta):
    """
    Test shared worker is blocked if CSP is "child-src 'none'"
    """

    policy = "child-src 'none'"
    params = "shared=true"
    url = generate_test_url(policy, header=header, meta=meta, allow=False,
                            fixture_url='child-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')
