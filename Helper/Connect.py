
# Input: URL
# Output:

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from Helper.ConfigFile import ConfigFile

class Connect:
    def __init__(self, url):
        self.url = url
        self.options = Options()
        self.config = ConfigFile()
        if self.config.dict['test.headless']:
            self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options, executable_path='./Helper/WebDriver/chromedriver.exe')
        self.driver.get(self.url)
        print("Chrome Web Driver Initialized")

    def close(self):
        self.driver.quit()
