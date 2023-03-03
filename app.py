import os
from time import sleep
from pandas import date_range
from datetime import datetime
from tqdm import tqdm
import logging as log

from selenium import webdriver

from helpers import login, make_url, get_href, get_request



log.basicConfig(format='%(message)s', level=log.INFO)
TIMES = date_range('1979-01-01T00:00:00', '2022-01-01T00:00:00', freq='1M')
BASE_DIR = os.path.dirname(__file__)

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


def main(variable, infos):

    for level in infos['levels']:
        for year in tqdm(infos['years']):
            for month in infos['months']:
                t1 = datetime.now()
                itime = datetime.strptime(f"{year}{month}", "%Y%m")
                file_out = f"{BASE_DIR}/{variable}/{itime.strftime('%Y/%m')}/{level}_{variable}_{itime.strftime('%Y%j')}.nc"
                if not os.path.isfile(file_out):
                    #options = Options()
                    #options.add_argument('-headless')

                    driver = webdriver.Firefox()#options=options)
                    os.makedirs(os.path.dirname(file_out), exist_ok=True)
                    try:
                        login(driver, user, pasw)
                    except:
                        log.info(f'[{datetime.now()}] - app.helpers.login() @ already logged, skip to download')

                    url = make_url(variable, level, year, month)
                    href = get_href(itime, driver, url, _id="p-button-text p-c")
                    driver.close()
                    
                    t2 = datetime.now()
                    get_request(itime, href, file_out)
                    log.info(f"[{datetime.now()}] - app.main() @ FILE DOWNLOADED in {datetime.now()-t2} seconds: {file_out}")
                else:
                    log.info(f'[{datetime.now()}] - app.main() @ FILE ALREADY DOWNLOADED: {file_out}')
                log.info(f'[{datetime.now()}] - app.main() @ DONE {level}.{variable}.{year}.{month} in {datetime.now()-t1} seconds.')



if __name__ == "__main__":
    log.info(f'[ START SCRIPT ] - app.py')
    user=''
    pasw=''
    
    #list_args = [(variable, infos) for variable, infos in cfg.items()]
    #with multiprocessing.Pool(processes=3) as pool:
    #    results = pool.starmap(main, list_args)

    for variable, infos in cfg.items():
        main(variable, infos)