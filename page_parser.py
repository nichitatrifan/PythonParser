from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from abstract_page import AbstractPage


calorie_page = AbstractPage('https://health-diet.ru/calorie',['log-level=3', '--start-maximized'])
wait = WebDriverWait(calorie_page.driver, 10)

wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mzr-tree-node')))

categories_list = calorie_page.driver.find_elements_by_class_name('mzr-tree-node') 

for item in categories_list:
    item.click()

calorie_page.write_page_source('.\pages\source.html')

with open('.\pages\source.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file,'lxml')

sibilings = soup.find(class_='mzr-tree-node').find_next_siblings(class_='mod-padding-element')

products_list_ans = []

for item in sibilings:
    # print(item.text)
    product_description = {'product':item.text, 'calories':'','protein':'',
    'fat':'', 'carbs':'', 'water':'', 'cellulose':''}
    products_list_ans.append(product_description)

products_list = calorie_page.driver.find_elements_by_class_name('mod-padding-element')

for i, item in enumerate(products_list):
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'mzr-tree-node')))
    
    calorie_page.driver.execute_script("arguments[0].click();", item)
    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.uk-overflow-container')))
    content = calorie_page.find_element_by_css('.uk-overflow-container') # mzr-block-content
    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mzr-macronutrients-item-header-value')))
    content_list = content.find_elements_by_css_selector('.mzr-macronutrients-item-header-value')
    
    products_list_ans[i]['calories'] = content_list[0].text
    products_list_ans[i]['protein'] = content_list[1].text
    products_list_ans[i]['fat'] = content_list[2].text
    products_list_ans[i]['carbs'] = content_list[3].text
    products_list_ans[i]['water'] = content_list[4].text
    products_list_ans[i]['cellulose'] = content_list[5].text

    if i == 20:
        break

    calorie_page.find_element_by_css('svg[name="close"]').click()
    

for i, item in enumerate(products_list_ans):
    print(item)
    if i == 20:
        break

#calorie_page.stop_driver()
