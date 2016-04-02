import pytest

from utils.page_model import BasePage


# dumb tests here for framework testing
def test_page_log_pass(browser):
    url = 'http://127.0.0.1:8000/base-uri?allow=true&'\
          'policy=base-uri%20http://example.com'
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Pass')


def test_page_log_fail(browser):
    url = 'http://127.0.0.1:8000/base-uri?allow=true&'\
          'policy=base-uri%20http://example.com'
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Fail')


@pytest.mark.xfail(reason='asdasdasd')
def test_page_log_xfail(browser):
    url = 'http://127.0.0.1:8000/base-uri?allow=true&'\
          'policy=base-uri%20http://example.com'
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Fail')


@pytest.mark.xfail(reason='xfail')
def test_page_log_xpass(browser):
    url = 'http://127.0.0.1:8000/base-uri?policy=base-uri%20http://example.com'
    page = BasePage(browser).open(url)
    res = page.get_test_results()
    assert (res == 'Fail')
