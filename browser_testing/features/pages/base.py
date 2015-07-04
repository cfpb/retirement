from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import Utils

import sys
import time

# DEFAULT VALUES
default_driver_wait = 10

# ELEMENT ID'S FOR SELECTORS
ret_age_selector = "retirement-age-selector"
search = "query"

# XPATH LOCATORS
button = "//button[text()='Sign up']"
get_estimates_button = "//*[@id='get-your-estimates']"
age_selector = "//*[@id='age-selector-response']/div[1]/h3/span"
option_70 = "//*[@id='retirement-age-selector']/option[10]"
age_selection_div = "//*[@id='age-selector-response']"
fra_result_text = "//*[@id='graph-container']/div[1]/div[1]/p[1]/span[1]"


class Base(object):
    def __init__(self, logger, results_folder, base_url=r'http://localhost/',
                 driver=None, driver_wait=default_driver_wait, delay_secs=0):
        if driver is None:
            assert 'Driver is invalid or was not provided.'

        self.driver_wait = driver_wait
        self.base_url = base_url
        self.driver = driver
        self.chain = ActionChains(self.driver)
        self.logger = logger
        self.utils = Utils(delay_secs)
        self.results_folder = results_folder

    def go(self, relative_url=''):
        full_url = self.utils.build_url(self.base_url, relative_url)
        try:
            self.logger.info("Getting %s" % full_url)
            self.driver.get(full_url)
        except Exception:
            self.logger.info("Unexpected error running: %s" % full_url)
            self.logger.info("Exception type: %s" % sys.exc_info()[0])
            self.logger.info("Currently at: %s" % (self.driver.current_url))
            raise

    def wait(self, driver_wait=default_driver_wait):
        return WebDriverWait(self.driver, driver_wait)

    # Switch to the tab specified by relative_url
    # And return the page title
    def switch_to_new_tab(self, relative_url):
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)
            # Wait for the URL to display in the address bar
            WebDriverWait(self.driver, 5)\
                .until(lambda s: len(s.current_url) > 1)

            self.logger.info("Current url: %s" % self.driver.current_url)
            if relative_url in (self.driver.current_url):
                return self.driver.title
                self.driver.close()
                break

        return relative_url + " tab not found!"

    def close_browser(self):
        self.utils.zzz(1)
        self.driver.quit()

    def sleep(self, time):
        self.utils.zzz(float(time))

    def get_screenshot(self, filename=None):
        if filename is None:
            filename = self.driver.current_url

        filename = "%s" % (filename.replace('/', '_'))
        full_path = '%s/%s.%s' % (self.results_folder, filename, 'png')
        self.logger.info("Saving screenshot to %s" % full_path)
        self.driver.save_screenshot(full_path)

    def get_page_title(self):
        print "handles: %s" % self.driver.window_handles
        print "current handle: %s" % self.driver.current_window_handle
        print "current title: %s" % self.driver.title
        return self.driver.title

    def get_current_url(self):
        print "handles: %s" % self.driver.window_handles
        print "current handle: %s" % self.driver.current_window_handle
        print "current url: %s" % self.driver.current_url
        return self.driver.current_url

    def enter_month(self, month):
        month_input = self.driver.find_element_by_id('bd-month')
        month_input.send_keys(month)

    def enter_day(self, day):
        day_input = self.driver.find_element_by_id('bd-day')
        day_input.send_keys(day)

    def enter_year(self, year):
        year_input = self.driver.find_element_by_id('bd-year')
        year_input.send_keys(year)

    def enter_income(self, income):
        income_input = self.driver.find_element_by_id('salary-input')
        income_input.send_keys(income)

    def get_estimate(self):
        estimate_button = self.driver.find_element_by_xpath(get_estimates_button)
        estimate_button.click()
        Utils().zzz(1)

    def get_fra_result(self):
        select = self.driver.find_element_by_xpath(fra_result_text)
        return select.text

    def choose_retirement_age(self, retirement_age):
        age_selector = Select(self.driver.find_element_by_id("retirement-age-selector"))
        age_selector.select_by_value(retirement_age)
        # Utils().zzz(1)

    def click_link(self, link_text):
        element = self.driver.find_element_by_link_text(link_text)
        script = "arguments[0].scrollIntoView(true);"
        self.driver.execute_script(script, element)
        element.click()

    def get_blank_handle_title(self):
        blank_handle = self.driver.window_handles[1]
        self.driver.switch_to.window(blank_handle)
        # print "handles: %s" % self.driver.window_handles
        # print "current handle: %s" % self.driver.current_window_handle
        # print "current title: %s" % self.driver.title
        return self.driver.title

    def get_blank_handle_url(self):
        blank_handle = self.driver.window_handles[1]
        self.driver.switch_to.window(blank_handle)
        # print "handles: %s" % self.driver.window_handles
        # print "current handle: %s" % self.driver.current_window_handle
        # print "current url: %s" % self.driver.current_url
        return self.driver.current_url

    def get_age_choice_result(self):
        age_div = self.driver.find_element_by_xpath(age_selection_div)
        for div in age_div.find_elements_by_tag_name('div'):
            if div.is_displayed():
                return div.find_element_by_class_name("age-response-value").text
