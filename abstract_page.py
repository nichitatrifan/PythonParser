from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import wait

# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# options.add_argument('--ignore-certificate-errors-spki-list')
# options.add_argument('test-type')
# options.add_argument('-incognito')
# options.add_argument('no-sandbox')
# options.add_argument('--start-maximized')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# options.add_argument("--disable-logging")
# options.add_argument('log-level=3')


class AbstractPage():

    def __init__(self, url:str, options:list) -> None:
        self.url = url
        
        self.options = webdriver.ChromeOptions()

        for option in options:
            self.options.add_argument(option)

        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=".\chromedriver.exe")
        self.driver.get(url)
    
    def stop_driver(self):
        self.driver.quit()
    
    def write_page_source(self, file_path):
        page = self.driver.page_source
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page)
    
    def find_element_by_css(self, css_selector:str) -> WebElement:
        return self.driver.find_element_by_css_selector(css_selector=css_selector)

    def find_element_by_class(self, class_name:str) -> WebElement:
        return self.driver.find_element_by_class_name(class_name)
    
    def find_element_by_ID(self, ID:str) -> WebElement:
        return self.driver.find_element_by_id(ID)
    
    def find_elements_by_class(self, class_name:str) -> list[WebElement]:
        return self.driver.find_elements_by_class_name(class_name)