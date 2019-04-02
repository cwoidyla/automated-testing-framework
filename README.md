# automated-testing-framework
Python-based automated testing framework that manages tests exported from Katalon (Selenium)

How to Run:

python3 run.py test.cfg

Directory Overview

- run.py
- test.cfg
- WebDriver
- LifeCycle
- Features
- Bugs
- Helper
- ScreenShots

* run.py: orchestrates automated tests
* test.cfg: configure tests to be run
* WebDriver: contains chrome webdriver and sample code for how to utilize
* LifeCycle: contains all lifecycle regression tests
* Features: contains tests that are independent of lifecycle tests
* Bugs: contains tests for previously identified bugs
* Helper: helper functions for test management
* ScreenShots:

FAQ:
How do I modify auto-generated Selenium files to integrate with this test suite?
1. use Katalon to prerecord and export to "python2 webdriver + unittest"
2. If you're going to take pictures then perform the following steps:
    - In each test file, add to setUp definition:
        - import Helper.ConfigFile
        - [CODE]
    - In each test file, add to test_* definition:
        - driver.save_screenshot(self.pic_save_loc)
3. If you need multiple tests to run in sequence, then perform the following steps:
    - In each test file, comment out references to self.driver
        - setUp
        - test_*
        - tearDown
    - In each test file, add to test_* definition:
        - driver (E.g. test_me(self) => test_me(self,driver)

How do I add new properties to the configuration file?
1. In Helper Directory, modify ConfigFile.py to find new property.
