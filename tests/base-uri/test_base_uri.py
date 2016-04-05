import pytest

from utils.page_model import BasePage
from utils.config import config

# Test base-uri directive.
# When you visit "http://127.0.0.1:8000/base-uri?policy=base-uri 'self'" URL
# javascript on page will try to add base element with href attribute value
# http://example.com. Depends on CSP policy that will be allowed or not.
# if allow=true is specified, test assumes, that changes should be permitted
# and evaluate results based on this, so if:
# allow=True, but CSP doesn't allow changes, test result is Fail
# allow=False, but base element successfully added or changed, then test Fail


def generate_test_url(policy="default-src 'none'", meta=False, header=False,
                      allow=False, fixture_url=''):
    """
    Generates test URL

    policy: CSP policy. default CSP policy is 'default-src 'none'
    meta: CSP policy in meta element. default value is False
    header: CSP policy in CSP header. default is True
    allow: Do changes allowed by  CSP policy? Need for client side javascript
           to generate test result
    fixture_url: Test fixture base URL. Specific for each tests category
    """
    q_str = ''
    if allow is True:
        q_str += 'allow=True&'
    if meta is True:
        q_str += 'meta=True&'
    if header is True:
        q_str += 'header=True&'
    q_str += 'policy={}'.format(policy)

    return 'http://{}:{}/{}?{}'.format(config['server_address'],
                                       config['server_port'],
                                       fixture_url,
                                       q_str)


@pytest.mark.parametrize("header, meta", [(True, False), (False, True)])
def test_base_uri_change_allowed(browser, header, meta):
    """
    Test description
    """
    policy = 'base-uri http://example.com'
    url = generate_test_url(policy, header=header, meta=meta, allow=True,
                            fixture_url='base-uri')
    print(url)
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
    print(url)
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')