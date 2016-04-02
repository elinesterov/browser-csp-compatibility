from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class BasePage(object):

    def __init__(self, browser):
        self.browser = browser

    def open(self, url):
        self.browser.get(url)
        return self

    def get_test_results(self):
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )
        except TimeoutException as e:
            e.msg = "Can't locate element"
            raise e
        result = element.text
        return result


class TestResultPage(BasePage):

    def __init__(self, *args, **kwargs):
        super(TestResultPage, self).__init__(*args, **kwargs)
