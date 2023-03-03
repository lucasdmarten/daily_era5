import os, sys, requests
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By

import logging as log


def make_url(variable, level, year, month):
    url = "https://cds.climate.copernicus.eu/apps/user-apps/"\
            "app-c3s-daily-era5-statistics?dataset=reanalysis-era5-pressure-levels"\
            "&product_type=reanalysis"\
            f"&variable_e5pl={variable}"\
            f"&pressure_level_e5pl={level}"\
            f"&statistic=daily_mean"\
            f"&year_e5pl={year}"\
            f"&month={month}"\
            "&frequency=1-hourly"\
            "&time_zone=UTC%2B00:00"\
            "&grid_e5=0.25/0.25"\
            "&area.lat:record:list:float=-90"\
            "&area.lat:record:list:float=90"\
            "&area.lon:record:list:float=-180"\
            "&area.lon:record:list:float=180"
    return url

def select_input(driver, _id, content):
    text_area = driver.find_element(By.ID, _id)
    text_area.send_keys(content)
    return 

def login(driver, user='', pasw=''):
    url = "https://cds.climate.copernicus.eu/user/login?"
    driver.get(url)
    select_input(driver, 'edit-name', user)
    select_input(driver, 'edit-pass', pasw)
    #sleep(3)
    driver.find_element(By.ID, 'edit-submit').click()


def get_href(time, driver, url, _id="p-button-text p-c"):
    n_retrys = 100000
    driver.get(url)
    is_button = None
    count = 0
    while is_button == None:
        sleep(1.5)
        btns = driver.find_elements(By.TAG_NAME, 'button')
        for i, button in enumerate(btns):
            #print(f"{i}.{button.text}")
            if button.text == 'Run':
                is_button = True
                button.click()
            count += 1
        log.info(f'[{datetime.now()}] - app.helpers.is_download() @ waiting for button of download, retry number: {count}')
        if count >= n_retrys:
            raise Exception('try many times rule is_button and does not work')
        
    
    is_download = None
    count = 0
    while is_download == None:
        sleep(3)
        tags = driver.find_elements(By.TAG_NAME, 'a')
        for i, tag in enumerate(tags):
            #print(f"{i}.{tag.text}")
            if 'Download' in tag.text:
                is_download = True
                href = tag.get_attribute('href')
                log.info(f'[{time}] - app.helpers.get_href() @ href: {href}')
                return href
            count += 1
        button.click()
        log.info(f'[{datetime.now()}] - app.helpers.is_download() @ waiting for button2 of download, retry number: {count}')
        if count >= n_retrys:
            raise Exception('try many times rule is_download and does not work')


def get_request(time, url, file_out):
    log.info(f'[{time}] - app.helpers.get_request() @ starting request')
    response = requests.get(url)
    log.info(f'[{time}] - app.helpers.get_request() @ getting data')
    with open(file_out, 'wb') as file:
        file.write(response.content)
        log.info(f'[{time}] - app.helpers.get_request() @ saving data')

def check_file_status(filepath, filesize):
    sys.stdout.write("\r")
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size / filesize) * 100
    sys.stdout.write("%.3f %s" % (percent_complete, "% Completed"))
    sys.stdout.flush()