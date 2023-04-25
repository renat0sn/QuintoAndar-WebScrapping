from selenium.webdriver.common.by import By

class SeleniumHandler:

    def __init__(self, driver) -> None:
        self.driver = driver
        
    def find_element(self, element, tag, attr='', attr_value='', all_elements=True):
        xpath_str = '//' + tag

        if attr != '':
            xpath_str += f'[@{attr}'

            if attr_value != '':
                xpath_str += f'="{attr_value}"'
            
            xpath_str += ']'
        
        if all_elements:
            return element.find_elements(By.XPATH, xpath_str)
        else:
            return element.find_element(By.XPATH, xpath_str)