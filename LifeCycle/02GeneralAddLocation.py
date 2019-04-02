# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os
from Helper.ConfigFile import ConfigFile

class GeneralAddLocation(unittest.TestCase):
    def setUp(self):
        self.config = ConfigFile()
        pic_file_name = os.path.basename(__file__) + ".png"
        pic_dir = self.config.dict['test.pics.dir']
        self.pic_save_loc = pic_dir + pic_file_name
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_general_add_location(self, driver):
        #driver = self.driver
        # TODO: Add text verification...
        driver.find_element_by_name("btAddNewLocation").click()
        driver.find_element_by_name("taDetails").clear()
        driver.find_element_by_name("taDetails").send_keys("This is a room where interns go to thrive.")
        driver.find_element_by_name("btSave").click()
        # Save a picture of the add-location page
        driver.save_screenshot(self.pic_save_loc)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
