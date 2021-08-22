
"""
@author: zil.ink/anvaari
"""
# Import reqired packages
import time 
from datetime import datetime as dt
from selenium import webdriver
import os
from os.path import join
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# Specify path where this code exist
script_path=os.path.dirname(os.path.abspath(__file__))

while not os.path.isfile(join(script_path,'geckodriver')) :
    print('\nPlease download lastest version of Firefox webdrive (geckodriver) from: https://www.selenium.dev/documentation/en/webdriver/driver_requirements/ and do following:\n\t* Extract it and fin geckodriver\n\t* Copy it where this code exist\n')
    temp_=input("Please copy the file and press Enter")

print('\nHi! Please wait, Program loading...\n')


# Use webdrive option in order to set browser headless
fx_option=webdriver.firefox.options.Options()
fx_option.headless=True

# initiate webdrive
driver=webdriver.Firefox(executable_path=join(script_path,'geckodriver'),options=fx_option)
main_url='https://patents.google.com'

driver.get(main_url)

# Get search items from user
title=input('\nPlease Enter the title of your search\nGuide:\n\tYou can use "AND","OR" logic. But if you want to use them, you must insert them in parentheses and write them in uppercase. For example --> ((3D AND Printing) OR (3D AND "Print"))"\n\t* If you want search phrase (i.e 3D Print) you must use AND between them. For Example --> 3D Printing : (3D AND Printing) So google will search for title include both 3D and printing\n\t* You can use "" for exact search. For example:\n\t\t("3D" and "Printing") only search for 3D not 3d and search for Printing not print, printer and ...\n\t\t"3D Printig" only search for title include 3D Printing\n\t* If dont use "" google will search for relevent words for example if type school, google also show you  college in title\nFor more information see https://support.google.com/faqs/answer/7049475?hl=en\n')

date_interval=[input('Please enter start of time interval of search in this format: YYYY/MM/DD --> 2020/05/08\n'),
               input('Please enter end of time interval of search in this format: YYYY/MM/DD --> 2021/05/08\n')]
date_type=input('\nPlease enter type of date. Only "publication", "priority" and "filing" allowed. Default is priority\n')
# Change time format into valid format for google patent
start_date=dt.strptime(date_interval[0], '%Y/%m/%d').strftime('%Y%m%d')
end_date=dt.strptime(date_interval[1], '%Y/%m/%d').strftime('%Y%m%d')

language='english'

patent_office=input('\nPlease enter Patent office you want search between their patents.\nThis is optional, if you want search among all just Enter\n')

type_='patent'

status=input('\nPlease enter status of patent.\nOnly 2 status allowed : grant and application\nThis is optional, if you want search among all just Enter\n')

# Construct phrase search in order to feed into the search bar
search_filters={'TI':f'={title}',
                'country':f':{patent_office}',
                'before':f':{date_type}:"{end_date}" ',
                'after':f':{date_type}:"{start_date}" ',
                'status':f':{status}',
                'language':f':{language}',
                'type':f':{type_}'}
search_phrase=''
for key,value in search_filters.items():
    if len(value)>2:
        search_phrase+=key+value+' '

# Feed search phrase to search bar
search_elem=driver.find_element_by_id('searchInput').send_keys(search_phrase)
search_butt=driver.find_element_by_id('searchButton').click()
# Set result page to show 100 result per page
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#count > div:nth-child(2) > span:nth-child(1) > span:nth-child(4) > dropdown-menu:nth-child(1) > span:nth-child(1) > span:nth-child(1)')))
resutl_per_peage_num=driver.find_element_by_css_selector('#count > div:nth-child(2) > span:nth-child(1) > span:nth-child(4) > dropdown-menu:nth-child(1) > span:nth-child(1) > span:nth-child(1)').click()
result_100=driver.find_element_by_css_selector('#count > div:nth-child(2) > span:nth-child(1) > span:nth-child(4) > dropdown-menu:nth-child(1) > iron-dropdown:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4)').click()

time.sleep(2)
# Google don't recognize date type in search bar so i change in address 
# search_url is final url and we can use it for download csv file
search_url=driver.current_url.replace('priority',date_type)

driver.close()

print(f'Please enter following URL in your browser and click on "download" icon places on top of page:\n{search_url}')

