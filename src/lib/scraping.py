"""Module for setup scrap"""
from tempfile import mkdtemp
from selenium import webdriver


def scrap(url):
    """"Scrap data form page url"""
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--single-process")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    driver = webdriver.Chrome("/opt/chromedriver", options=options)
    driver.get(url)
    return driver
