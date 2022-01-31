import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.mark.skip("sample test using selenium")
def test_eight_components():

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    driver.get("https://google.com")

    assert driver.title == "Google"

    driver.implicitly_wait(0.5)

    search_box = driver.find_element(by=By.NAME, value="q")
    search_button = driver.find_element(by=By.NAME, value="btnK")

    search_box.send_keys("Selenium")
    search_button.click()

    search_box = driver.find_element(by=By.NAME, value="q")
    assert search_box.get_attribute("value") == "Selenium"

    driver.quit()