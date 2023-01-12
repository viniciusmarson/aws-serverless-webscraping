"""Module for setup scrap"""
import os
from tempfile import mkdtemp
from selenium import webdriver

ENVIRONMENT = os.getenv('ENVIRONMENT')

def create_options():
    """Create chrome options based on environment variables"""
    options = webdriver.ChromeOptions()

    if ENVIRONMENT != 'local':
        options.binary_location = '/opt/chrome/chrome'
        # Bypass OS security model
        options.add_argument('--no-sandbox')
        # applicable to windows os only
        options.add_argument("--disable-gpu")
        options.add_argument('--headless')
        options.add_argument("--single-process")
        options.add_argument("disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        # overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
    return options


def scrape(url):
    """"Scrap data form page url"""
    driver = webdriver.Chrome("/opt/chromedriver", options=create_options())
    driver.get(url)
    return driver
