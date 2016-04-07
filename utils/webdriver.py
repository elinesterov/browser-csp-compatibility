from selenium import webdriver
from config import config


driver_url = 'http://{}:{}{}'.format(config['wd_host'],
                                     config['wd_port'],
                                     config['wd_uri'])


def fixed_update_preferences(self):
    """
    monkey patching of webdriver.FirefoxProfile.update_preferences method
    to workaround 'frozen' preferences update like 'security.csp.enable'
    otherwise it always get re-written to 'false', so CSP is actually disabled
    See https://github.com/seleniumhq/selenium/issues/918 for more details,
    but I actually don't understand why they do it, especially adding
    CSP control option to 'frozen' preference [I KNOW WHAT I DO IF I CHANGE IT]
    """
    for key, value in self.DEFAULT_PREFERENCES['frozen'].items():
        if key != 'security.csp.enable':
            self.default_preferences[key] = value
    self._write_user_prefs(self.default_preferences)


def start_webdriver(browser='firefox'):

    profile = None

    if browser == 'firefox':
        webdriver.FirefoxProfile.update_preferences = fixed_update_preferences
        profile = webdriver.FirefoxProfile()
        profile.set_preference('security.csp.enable', True)
        capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    elif browser == 'chrome':
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    elif browser == 'safari':
        capabilities = webdriver.DesiredCapabilities.SAFARI.copy()

    driver = webdriver.Remote(driver_url, capabilities, browser_profile=profile)

    return driver
