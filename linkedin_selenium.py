from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


class LinkedLn_Scrapper():
    def __init__(self):
        input_params = {

            'driver_path': 'C:\chromedriver.exe',
            'firefox_path': 'C:\geckodriver.exe',
            'phantom_path': 'C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',
            'url': 'https://www.linkedin.com/',

        }

        Firefox = True
        Phantom = False
        Chrome = False

        if Firefox:
            options = Options()
            profile = webdriver.FirefoxProfile()
            options.add_argument("--headless")
            options.add_argument("--disable-notifications")
            self.driver = webdriver.Firefox(executable_path=input_params['firefox_path'])
        if Chrome:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("user-agent=Hi")
            options.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(executable_path=input_params['driver_path'])

        if Phantom:
            self.driver = webdriver.PhantomJS(executable_path=input_params['phantom_path'])
        self.driver.get(input_params['url'])
        time.sleep(1)

    def login(self, email1, password):
        base_email = "//input[@id='session_key']"
        base_pass = "//input[@id='session_password']"
        base_submit = "//button[@class='sign-in-form__submit-button']"
        email = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, base_email)))
        time.sleep(2)
        email.send_keys(email1)
        pass_ = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, base_pass)))
        time.sleep(2)
        pass_.send_keys(password)
        submit = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, base_submit)))
        time.sleep(2)
        submit.click()

        cookies = self.driver.get_cookies()
        linkedin_cookies = {
            'li_at': '',
            'JSESSIONID': ''
        }
        for cook in cookies:
            if cook['name'] == 'li_at':
                linkedin_cookies['li_at'] = cook['value']

            if cook['name'] == 'JSESSIONID':
                linkedin_cookies['JSESSIONID'] = cook['value']

        return linkedin_cookies



