import requests
import time
from os import urandom
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from abstract_page import AbstractPage

# products id: 19 ~ 3162
# https://health-diet.ru/api2/base_of_food/common/3162.json?10
# use unicode to represent names

def get_data(url:str):

    # INITIALIZING SELENIUM DRIVERS
    calorie_page = AbstractPage(url,['log-level=3', '--start-maximized'])
    wait = WebDriverWait(calorie_page.driver, 10)

    # initializing headers for a request:
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mzr-tree-node')))
    categories_list = calorie_page.driver.find_elements_by_class_name('mzr-tree-node') 

    # open each category
    for item in categories_list:
        item.click()

    # saving and creating soup instance 
    calorie_page.write_page_source('.\pages\source.html')
    with open('.\pages\source.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file,'lxml')

    # get all group names
    sibilings = soup.find(class_='mzr-tree-node').find_next_siblings(class_='mod-padding-element')
    products_list = []
    for i, item in enumerate(sibilings):
        temp_list = {
            'ID': i,
            'Group Name': item.text,
            'Products':[]
            }
        products_list.append(temp_list)
    
    # selenium objects of all products
    # products = calorie_page.find_elements_by_class('mod-padding-element')
    found = False
    for i in range(200):
        url = "https://health-diet.ru/api2/base_of_food/common/{0}.json?10".format(str(i))
        response = requests.get(url, headers=headers)
        if response:
            response_json = response.json()
            # print(response_json)
            product = {
                'id':response_json['id'],
                'name':str(response_json['name']),
                'name_group':str(response_json['name_group']),
                'calories':str(response_json['nutrients']['11']),
                #'protein':str(response_json['nutrients']['13']),
                #'fat':str(response_json['nutrients']['14']),
                #'carbohydrates':str(response_json['nutrients']['15']),
                #'SFAs':response.json()['nutrients']['24'],
            }

            found = False
            for group in products_list:
                if group['Group Name'] == product['name_group']:
                    group['Products'].append(product)
                    found = True
            if not found:
                temp_list = {
                'ID': 'NONE',
                'Group Name': item.text,
                'Products':[]
                }
                temp_list['Products'].append(product)
                products_list.append(temp_list)
        
        print(i, end=" ")
        if response:
            print(response.json()['name'])
        else:
            print('None')

    print(products_list)    

def save_to_json_file():
    pass

def main():
    get_data('https://health-diet.ru/calorie')

if __name__ == "__main__":
    main()