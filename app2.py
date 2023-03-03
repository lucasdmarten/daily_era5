__author__      = "Lucas Marten"
__copyright__   = "Copyright 2023, myhome"
__email__       = "lucasdmarten@gmail.com"

import cdsapi
import os
from pandas import date_range
from datetime import datetime
from multiprocessing import Pool
import requests

c = cdsapi.Client()

TIMES = date_range('1979-01-01T00:00:00', '2022-01-01T00:00:00', freq='1M')
YEARS = [time.strftime('%Y') for time in TIMES],
MONTHS = [time.strftime('%m') for time in TIMES]
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

def main_download(variable, level, year, month, file_out):
    result = c.service(
            "tool.toolbox.orchestrator.workflow",
            params={
                "realm": "c3s",
                "project": "app-c3s-daily-era5-statistics",
                "version": "master",
                "kwargs": {
                "dataset": "reanalysis-era5-pressure-levels",
                "product_type": "reanalysis",
                "variable": variable,
                "statistic": "daily_mean",
                "pressure_level": level,
                "year": year,
                "month": month,
                "time_zone": "UTC+00:0",
                "frequency": "1-hourly",
                "grid": "0.25/0.25",
                "area": {"lat": [-90, 90], "lon": [-180, 180]}
                },
            "workflow_name": "application"
        })
    os.makedirs(os.path.dirname(file_out), exist_ok=True)
    location=result[0]['location']
    res = requests.get(location, stream = True)
    print("Writing data to " + file_out)
    with open(file_out,'wb') as fh:
        for r in res.iter_content(chunk_size = 1024):
            fh.write(r)
    fh.close()
    #c.download(result)


def main(variable, infos):
    for level in infos['levels']:
        for year in infos['years']:
            for month in infos['months']:
                t1 = datetime.now()
                itime = datetime.strptime(f"{year}{month}", "%Y%m")
                file_out = f"{BASE_DIR}/{variable}/{itime.strftime('%Y/%m')}/{level}_{variable}_{itime.strftime('%Y%j')}.nc"
                if not os.path.isfile(file_out):
                    main_download(variable, level, year, month, file_out)
                else:
                    print(f'[{datetime.now()}] - app.main() @ FILE ALREADY DOWNLOADED: {file_out}')
                print(f'[{datetime.now()}] - app.main() @ DONE {level}.{variable}.{year}.{month} in {datetime.now()-t1} seconds.')




if __name__ == "__main__":
    list_args = [(variable, infos) for variable, infos in cfg.items()]

    with Pool(processes=3) as pool:
        results = pool.starmap(main, list_args)