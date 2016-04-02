from selenium import webdriver
from config import config


driver_url = 'http://{}:{}{}'.format(config['wd_host'],
                                     config['wd_port'],
                                     config['wd_uri'])


def start_webdriver(browser='firefox'):

    if browser == 'firefox':
        capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    elif browser == 'chrome':
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    elif browser == 'safari':
        capabilities = webdriver.DesiredCapabilities.SAFARI.copy()

    driver = webdriver.Remote(driver_url, capabilities)
    return driver
