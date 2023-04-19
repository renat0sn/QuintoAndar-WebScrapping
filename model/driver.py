from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

class Driver:

    def __init__(self, path_driver) -> None:
        self.path_driver = path_driver
        self.driver = None
    
    def start(self):
        ser = Service(self.path_driver)
        op = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=ser, options=op)
        self.driver = driver

        return driver
    
    def enter_page(self, url_page):
        self.driver.get(url_page)

    def get_elements(self, element, attr = '', value = ''):
        xpath_str = '//' + element


        if attr != '':
            xpath_str += f'[@{attr}'

            if value != '':
                xpath_str += f'="{value}"'
            
            xpath_str += ']'
        
        
        return self.driver.find_elements(By.XPATH, xpath_str)