#/usr/bin/env python
import matplotlib.pyplot as plt
import scipy.optimize as opt
import math
import numpy as np
import csv
import time


def latitude(x,a,f,c):
    return a*np.sin(2*math.pi*f*x+c)


def read_csv_data(file_path):
    timestamp = []
    lat_deg = []
    lat_min = []
    lat_sec = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count==0 :
                print('Reading name of columns')
                for i in range(len(row)):
                    print(row[i],i)
                line_count+=1
                continue
            timestamp.append(row[0])
            lat_deg.append(row[1])
            lat_min.append(row[2])
            lat_sec.append(row[3])
            line_count+=1

    for i in range(len(lat_deg)):
        if '-' in lat_deg[i]:
            lat_min[i] = '-'+lat_min[i]
            lat_sec[i] = '-'+lat_sec[i]

    lat_deg = [int(_) for _ in lat_deg]
    lat_min = [int(_) for _ in lat_min]
    lat_sec = [float(_) for _ in lat_sec]

    return timestamp,lat_deg,lat_min,lat_sec


def timestamp_to_time(t):
    time_values = []
    for _ in t:
        tempTimeObject = time.strptime(_,"%d/%m/%Y-%H:%M:%S:%f")
        time_values.append(tempTimeObject.tm_hour*3600+tempTimeObject.tm_min*60+tempTimeObject.tm_sec)
    time0 = time_values[0]
    time_values = [t-time0 for t in time_values]
    return time_values


def equivalentDegrees(degs,mins,secs):
    eqLat = []
    for i in range(len(degs)):
        #if(degs[i]>0):
        eqLat.append(degs[i]+mins[i]/60+secs[i]/3600) #forse da modificare
        #else:
        #    eqLat.append(degs[i]-mins[i]/60-secs[i]/3600) #forse da modificare

    return eqLat


def plotGraph(x,y):
    #pass
    plt.plot(x,y)

def showGraph():
    plt.show()

def findCurveFit(func, x, y):
    optimizedParameters, pcov = opt.curve_fit(func, x, y, bounds = ((50.9,1/6000,0),(51,1/4000,2000)))
    return optimizedParameters
        
def main():
    #read csv file
    timestamp,latDeg,latMin,latSec = read_csv_data('../zz_astrolorenzini/zz_astrolorenzini_data.csv')    #print(latDeg,latMin,latSec)
    time_values = timestamp_to_time(timestamp)
    eqLatitude = equivalentDegrees(latDeg,latMin,latSec)
    params = findCurveFit(latitude,time_values,eqLatitude)

    print(params)
    plotGraph(time_values,eqLatitude)
    plotGraph(np.linspace(1,10000,10000),latitude(np.linspace(1,10000,10000),*params))
    showGraph()


main()