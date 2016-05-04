import time

from urlparse import urlparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

WAIT_ELEMENT_TIMEOUT = 10


class BasePage(object):

    def __init__(self, browser):
        self.browser = browser

    def open(self, url):
        self.browser.get(url)
        return self

    def find_element_by_id(self, id, wait=False):
        """
        Method to find element on page by it's ID
        """
        element = None
        timeout = 0

        if wait:
            timeout = WAIT_ELEMENT_TIMEOUT

        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.ID, id))
            )
        except TimeoutException as e:
            e.msg = "Can't locate element"
            raise e

        return element

    def get_relative_path(self):
        """
        Method to get relative path of loaded page
        """
        return urlparse(self.browser.current_url).path

    def on_page(self, wait_for_page_to_load=False):
        """
        Method to check if page is loaded
        """
        # TODO: fix this
        # that is really dumb, but seems Safari driver has some issues
        # with current_url method, which stuck sometimes
        # adding this simple 0,1 delay helped to solve that
        # but I would better fix this later
        if wait_for_page_to_load:
            pass
            time.sleep(0.1)
        if self.get_relative_path() == self.url:
            return True
        else:
            return False


class TestResultPage(BasePage):
    """
    Test result page object model for js tests
    """

    def __init__(self, *args, **kwargs):
        super(TestResultPage, self).__init__(*args, **kwargs)
        self.results_id = 'result'

    def get_test_results(self):
        """
        Method to get test results for pages which displays test
        results in div element with id=result
        """
        element = self.find_element_by_id(self.results_id, wait=True)

        if element:
            return element.text
        else:
            return False


class FormActionPage(BasePage):
    """
    From action page object model for url /form-action
    """

    def __init__(self, *args, **kwargs):
        super(FormActionPage, self).__init__(*args, **kwargs)
        self.url = '/from-action'

    def submit_form(self):
        submit = self.find_element_by_id('submit')
        submit.click()
        return EchoPage(self.browser)


class EchoPage(BasePage):
    """
    Echo page object model for url /echo
    """

    def __init__(self, *args, **kwargs):
        super(EchoPage, self).__init__(*args, **kwargs)
        self.url = '/echo'
