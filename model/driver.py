from selenium import webdriver
from selenium.webdriver.edge.service import Service
from model.soup import SeleniumHandler

class Driver:

    def __init__(self, path_driver) -> None:
        self.path_driver = path_driver
        self.driver = None
    
    def start(self):
        ser = Service(self.path_driver)
        op = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=ser, options=op)
        self.driver = driver
        self.selenium_handler = SeleniumHandler(self.driver)

        return driver
    
    def enter_page(self, url_page):
        self.driver.get(url_page)

    def get_elements(self, tag, attr = '', attr_value = ''):
        return self.selenium_handler.find_element(element=self.driver, tag=tag, attr=attr, attr_value=attr_value)
    
    def find_text_in_element(self, element, tag, attr = '', attr_value = '', all_elements=False):
        return self.selenium_handler.find_element(element=element, tag=tag, attr=attr, attr_value=attr_value, all_elements=all_elements).text

    def click_element(self, element):
        element.click()