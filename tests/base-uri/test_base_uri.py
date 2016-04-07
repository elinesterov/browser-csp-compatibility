import pytest

from utils.page_model import BasePage

from tests.common import generate_test_url

# Test base-uri directive.
# When you visit "http://127.0.0.1:8000/base-uri?policy=base-uri 'self'" URL
# javascript on page will try to add base element with href attribute value
# http://example.com. Depends on CSP policy that will be allowed or not.
# if allow=true is specified, test assumes, that changes should be permitted
# and evaluate results based on this, so if:
# allow=True, but CSP doesn't allow changes, test result is Fail
# allow=False, but base element successfully added or changed, then test Fail


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_base_uri_change_allowed(browser, header, meta):
    """
    Test description
    """
    policy = 'base-uri http://example.com'
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='base-uri')
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_base_uri_change_blocked(browser, header, meta):
    """
    Test description
    """
    policy = "base-uri 'self'"
    url = generate_test_url(policy, header=header, meta=meta, allow=False,
                            fixture_url='base-uri')
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')