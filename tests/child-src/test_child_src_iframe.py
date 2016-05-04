import pytest

from utils.page_model import TestResultPage

from tests.common import generate_test_url


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_child_src_iframe_allowed(browser, header, meta):
    """
    Test iframe load allowed if CSP is "child-src 'self'"
    """
    policy = "child-src 'self'"
    params = "frame=true"
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='child-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_child_src_iframe_blocked(browser, header, meta):
    """
    Test iframe load blocked if CSP is "child-src 'self'"
    """

    policy = "child-src 'none'"
    params = "frame=true"
    url = generate_test_url(policy, header=header, meta=meta, allow=False,
                            fixture_url='child-src', params=params)
    page = TestResultPage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')

# TODO: - add test for redirect
#       - add test for different ways of adding iFrame element:
#           - appendChild
#           - replaceChild
#           - insertBefore
#           - innerHTML
#           - insertAdjacentHTML
