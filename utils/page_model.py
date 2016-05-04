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


class TestResultPage(BasePage):

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
