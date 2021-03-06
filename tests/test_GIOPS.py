import logging
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support.ui import Select


class element_has_css_class(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if self.css_class in element.get_attribute("class"):
        return element
    else:
        return False


class element_does_not_have_css_class(object):
  """An expectation for checking that an element does not have a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if self.css_class in element.get_attribute("class"):
        return False
    else:
        return element

class TestGIOPS10d():
  def setup_method(self, method):
    #service = ChromeService(executable_path=ChromeDriverManager().install())
    #self.driver = webdriver.Chrome(service=service)

    #service = EdgeService(executable_path=EdgeChromiumDriverManager(log_level=logging.NOTSET).install())
    #self.driver = webdriver.Edge(service=service)

    service = FirefoxService(executable_path=GeckoDriverManager().install())
    self.driver = webdriver.Firefox(service=service)

    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()

  def test_area(self):
    self.driver.get("https://oceansdata.net/public/")
    #self.driver.set_window_size(1099, 696)
    self.driver.find_element(By.ID, "area").click()
    self.driver.find_element(By.LINK_TEXT, "Enter Coordinate(s)").click()
    self.driver.find_element(By.CSS_SELECTOR, ".coordInputPanel:nth-child(2) .form-control:nth-child(2)").send_keys("45.3181")
    self.driver.find_element(By.CSS_SELECTOR, ".coordInputPanel:nth-child(2) .form-control:nth-child(5)").send_keys("-59.3802")
    self.driver.find_element(By.CSS_SELECTOR, ".coordInputPanel:nth-child(3) .form-control:nth-child(2)").send_keys("45.559")
    self.driver.find_element(By.CSS_SELECTOR, ".coordInputPanel:nth-child(3) .form-control:nth-child(5)").send_keys("-56.9418")
    self.driver.find_element(By.CSS_SELECTOR, ".coordInputPanel:nth-child(4) .form-control:nth-child(2)").send_keys("45.9945")
    self.driver.find_element(By.CSS_SELECTOR, ".coordInputPanel:nth-child(4) .form-control:nth-child(5)").send_keys("-57.6699")
    self.driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()

    # Wait until disabled button goes away
    wait = WebDriverWait(self.driver, 60000)
    wait.until(element_does_not_have_css_class((By.CSS_SELECTOR, '.btn-toolbar > .btn-group'), "disabled"))
    
    element = self.driver.find_element(By.CSS_SELECTOR, ".RenderedImage > img")
    image1 = element.screenshot_as_base64

    element.screenshot('area.png')
    
    # add the water velocity vectors
    dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, ".QuiverSelector > .ComboBox > .form-control"))
    dropdown.select_by_visible_text('Water Velocity')

     # Wait until disabled state
    #wait = WebDriverWait(self.driver, 60000)
    #wait.until(element_has_css_class((By.CSS_SELECTOR, '.btn-toolbar > .btn-group'), "disabled"))

    # Wait until disabled button goes away
    while True:
      wait = WebDriverWait(self.driver, 60000)
      wait.until(element_does_not_have_css_class((By.CSS_SELECTOR, '.btn-toolbar > .btn-group'), "disabled"))

      element = self.driver.find_element(By.CSS_SELECTOR, ".RenderedImage > img")
      image2 = element.screenshot_as_base64

      if image1 != image2:
        break 

    element.screenshot('area_with_velocity.png')

 
  def test_profile(self):
    # Test name: Profile
    # Step # | name | target | value
    # 1 | open | https://oceansdata.net/public/ | 
    self.driver.get("https://oceansdata.net/public/")
    # 2 | click | css=#point > span:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, "#point > span:nth-child(1)").click()
    # 3 | click | linkText=Enter Coordinate(s) | 
    self.driver.find_element(By.LINK_TEXT, "Enter Coordinate(s)").click()
    # 4 | type | css=.form-inline > .form-control:nth-child(2) | 44.9855
    self.driver.find_element(By.CSS_SELECTOR, ".form-inline > .form-control:nth-child(2)").send_keys("44.9855")
    # 5 | type | css=.form-control:nth-child(5) | -50.9582
    self.driver.find_element(By.CSS_SELECTOR, ".form-control:nth-child(5)").send_keys("-50.9582")
    # 6 | click | css=.modal-footer > .btn-primary | 
    self.driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()
    # 7 | waitForElementVisible | css=.RenderedImage > img | 2000

    # Wait until disabled button goes away
    wait = WebDriverWait(self.driver, 2000)
    wait.until(element_does_not_have_css_class((By.CSS_SELECTOR, '.btn-toolbar > .btn-group'), "disabled"))

    element = self.driver.find_element(By.CSS_SELECTOR, ".RenderedImage > img")

    src = element.get_attribute("src")

    element.screenshot('profile.png')

