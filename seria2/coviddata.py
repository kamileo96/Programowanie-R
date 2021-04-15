import requests, csv, numpy as np
url = 'https://covid.ourworldindata.org/data/jhu/full_data.csv'

#os.path.realpath(__file__)


response = requests.get(url)

with open("full_data.csv", "wb") as f:
    f.write(response.content) 
    lines = open("full_data.csv").readlines()
    datarr = np.array([[1,1,1,1,1,1,1,1,1,1]])

    for x in lines:
        short_arr = np.array([x.split(',')])
        datarr = np.append(datarr, short_arr, 0)
    print(datarr[:4])
