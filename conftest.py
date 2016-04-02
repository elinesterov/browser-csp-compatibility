import pytest

import utils.webdriver
import utils.config

from utils.server import Server
from utils.config import config


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     choices=['firefox', 'chrome', 'safari'],
                     help="Browser to run tests")


@pytest.fixture(scope='session', autouse=True)
def extra_json_environment(request):
    """
    Add additonal information into report
    """
    browser = request.config.getoption("--browser")
    request.config._json_environment.append(('browser', browser))


@pytest.fixture(scope="session", autouse=True)
def environment_setup(request):
    """
    Setup testing environment
    """
    # TODO:
    # start selenium remote server if needed
    # start test server if needed
    print('Starting webserver')
    server = Server(config['server_address'],
                    config['server_port'])
    # import pdb;pdb.set_trace()
    server.start()

    def tear_down_session():
        print('[Session tear down]')
        print('Closing session....')
        # shutdown selenim server
        # shutdown test server
        server.stop()
        print('Test run complete')

    request.addfinalizer(tear_down_session)


@pytest.fixture()
def browser(request):
    """
    Run selected browser
    """
    print('[Setup]')
    target_browser = request.config.getoption("--browser")
    print('Starting test using browser: {}'.format(target_browser))
    driver = utils.webdriver.start_webdriver(target_browser)

    def tear_down():
        print("\n[Tear down]\nClosing browser  ...")
        driver.quit()

    def reporter():
        print('Test result: ')

    request.addfinalizer(reporter)
    request.addfinalizer(tear_down)
    return driver
