
# Selenium controls a web browser through a "webdriver"
from selenium import webdriver

# Webdrivers need to be installed separately
# The webdriver_manager package will handle this for us
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Here we are using Firefox but drivers exist for Chrome, Edge, Safari, and IE as well
service = FirefoxService(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

# we can configure where and how large the browser window should be
driver.set_window_position(-2166, -1187)
driver.set_window_size(1452, 1262)
# or all at once as
driver.set_window_rect(-2166, -1187, 1452, 1262)

# open a web page
ocean_navigator_url = "https://oceansdata.net/public/"
driver.get(ocean_navigator_url)

print(driver.title)

print(driver.get_window_position())
print(driver.get_window_size())
print(driver.get_window_rect())

# elements on a page can be located by CSS_SELECTOR
from selenium.webdriver.common.by import By

dataset_selector = driver.find_element(By.CSS_SELECTOR, "div.form-group:nth-child(1) > select:nth-child(3)")
# Select lists have special behaviour compared to other elemnts
from selenium.webdriver.support.select import Select
select_object = Select(dataset_selector)   

for dataset_option in select_object.options:
    value = dataset_option.get_attribute('value')
    text = dataset_option.text
    print(value, text)

# Select an <option> based upon the <select> element's internal index
#select_object.select_by_index(1)
# Select an <option> based upon its text
#select_object.select_by_visible_text('02. GIOPS 10 day Forecast Surface - LatLon')
# Select an <option> based upon its value attribute
select_object.select_by_value('giops_fc_10d_2dll')

# we want to wait until the new dataset has been loaded before proceeding

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-group:nth-child(1) > select:nth-child(3)")))

dataset_locator = (By.CSS_SELECTOR, "div.form-group:nth-child(1) > select:nth-child(3)")

# after select a dataset, the dataselection element is destroyed and needs to be refound again
def select_dataset(value):
    dataset_selector = driver.find_element(*dataset_locator)
    select_object = Select(dataset_selector)   
    select_object.select_by_value(value)

    WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located(dataset_locator))

def get_dataset_values():

    dataset_selector = driver.find_element(*dataset_locator)
    select_object = Select(dataset_selector)   

    values = [o.get_attribute('value') for o in select_object.options]
    return values


dataset_values = get_dataset_values()

select_dataset(dataset_values[4])
 
# shutdown the web browser
driver.quit()