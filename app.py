import os
from pandas import date_range
from datetime import datetime

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from helpers import login, make_url, get_href, get_request

import logging as log

log.basicConfig(format='%(message)s', level=log.INFO)
TIMES = date_range('1979-01-01T00:00:00', '2022-01-01T00:00:00', freq='1M')

cfg = {
    "specific_humidity": {
        'levels': ['850','1000'],
        'years': [time.strftime('%Y') for time in TIMES],
        'months': [time.strftime('%m') for time in TIMES]
        
    },
    "u_component_of_wind": {
        'levels': ['700'],
        'years': [time.strftime('%Y') for time in TIMES],
        'months': [time.strftime('%m') for time in TIMES]
    },
    "v_component_of_wind": {
        'levels': ['700'],
        'years': [time.strftime('%Y') for time in TIMES],
        'months': [time.strftime('%m') for time in TIMES]
    },
}

if __name__ == "__main__":
    log.info(f'[ START SCRIPT ] - app.py')
    user=''
    pasw=''

    for variable, infos in cfg.items():
        for level in infos['levels']:
            for year in infos['years']:
                for month in infos['months']:
                    t1 = datetime.now()
                    time = datetime.strptime(f"{year}{month}", "%Y%m")
                    file_out = f"/home/marten/Desktop/download_era5_daily/src/{variable}/{time.strftime('%Y/%m')}/{level}_{variable}_{time.strftime('%Y%j')}.nc"
                    if not os.path.isfile(file_out):
                        options = Options()
                        options.add_argument('-headless')

                        driver = webdriver.Firefox(options=options)
                        os.makedirs(os.path.dirname(file_out), exist_ok=True)
                        try:
                            login(driver, user, pasw)
                        except:
                            log.info(f'[{time}] - app.helpers.login() @ already logged, skip to download')

                        url = make_url(variable, level, year, month)
                        href = get_href(time, driver, url, _id="p-button-text p-c")
                        t2 = datetime.now()
                        get_request(time, href, file_out)
                        log.info(f"[{time}] - app.main() @ FILE DOWNLOADED in {datetime.now()-t2} seconds: {file_out}")
                        driver.close()
                    else:
                        log.info(f'[{time}] - app.main() @ FILE ALREADY DOWNLOADED: {file_out}')
                    log.info(f'[{time}] - app.main() @ DONE {level}.{variable}.{year}.{month} in {datetime.now()-t1} seconds.')
