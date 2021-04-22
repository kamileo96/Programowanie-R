import requests, csv, numpy as np, pandas as pd, matplotlib.pyplot as plt, datetime
url = 'https://covid.ourworldindata.org/data/jhu/full_data.csv'

#os.path.realpath(__file__)


response = requests.get(url)

with open("full_data.csv", "wb") as f:
    f.write(response.content)
    """ 
    lines = open("full_data.csv").readlines()
    datarr = np.array([[1,1,1,1,1,1,1,1,1,1]])

    for x in lines:
        short_arr = np.array([x.split(',')])
        datarr = np.append(datarr, short_arr, 0)
    print(datarr[:4])
    """
with open('full_data.csv') as f:
    df = pd.read_csv(f)
    countries = df.location
    dates = np.array(df.date)
    newcases = df.new_cases
    current = "_delete_"
    start = 0
    stop = 0
    legend = []
    for cnt in countries:
        if cnt != current:
            lg = [current, start, stop]
            legend.append(lg)
            current = cnt
            start = stop
        
        stop += 1
    legend = legend[1:]
    print("Wybierz kraj:")

    slownik = {}
    for l in legend:
        print(l[0])
        slownik[l[0]] = l[1:]
    name = input("Podaj nazwę wybranego kraju: ")
    
    begin = slownik[name][0]
    end = slownik[name][1]
    ds = dates[begin:end]
    xs = []
    for dt in ds:
        dtime = datetime.datetime(int(dt[:4]),int(dt[5:7]),int(dt[8:]))
        xs.append(dtime.timestamp())
    xs = (np.array(xs)-xs[0])/86400
    ys = newcases[begin:end]
    plt.plot(xs,ys)
    plt.title(f'New cases in {name}')
    plt.xlabel(f'Number of days from {ds[0]}')
    plt.ylabel('New cases')
    plt.show()