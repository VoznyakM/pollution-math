import requests
import numpy as np
import sys
from datetime import datetime, timedelta

DAYS_OF_SIMULATION = 366
POLLUTION_API_URL = 'http://localhost:3000/stats/'
START_DATE = datetime(2021, 1, 1, 1, 1, 1, 1)
np.random.seed(0)

if __name__ == "__main__":
    days = np.arange(1, DAYS_OF_SIMULATION)
    date = START_DATE

    for day in days:

        date = date + timedelta(days=1)
        stats = {
           "date":  datetime.strftime(date, "%Y-%m-%d"), 
           "cases": np.random.randint(1, 100), 
           "deaths": np.random.randint(1, 100), 
           "recovered": np.random.randint(1, 100)
        }
        print (stats)

        try:
          resp = requests.post(POLLUTION_API_URL, json=stats)
          print(resp)
          if resp.status_code != 201:
            raise ApiError('POST ' + POLLUTION_API_URL + ' {}'.format(resp.status_code))
          print('Created stats. ID: {}'.format(resp.json()["id"]))
        except:
          print( resp.status_code )
#          print ('Cant connect to API server')
          sys.exit()
