#!/usr/bin/env python
from astropy.constants import M_earth, G
from z3 import *
from math import pi, cos,sin,acos
import time
from statistics import mean
import csv
from usefullFunction import *
from usefullFunction import raggioTerra,omega_terra
import matplotlib.pyplot as plt
from geodetic import *


def read_csv_data(file_path):
    timestamp = []
    long_deg = []
    long_min = []
    long_sec = []
    lat_deg = []
    lat_min = []
    lat_sec = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count==0 :
                #print('Reading name of columns')
                for i in range(len(row)):
                    #print(row[i],i)
                    pass
                line_count+=1
                continue
            timestamp.append(row[0])
            lat_deg.append(row[1])
            lat_min.append(row[2])
            lat_sec.append(row[3])
            long_deg.append(row[4])
            long_min.append(row[5])
            long_sec.append(row[6])
            line_count+=1
    for i in range(len(lat_deg)):
        if '-' in lat_deg[i]:
            lat_min[i] = '-'+lat_min[i]
            lat_sec[i] = '-'+lat_sec[i]
        if '-' in long_deg[i]:
            long_min[i] = '-'+long_min[i]
            long_sec[i] = '-'+long_sec[i]


    lat_deg = [int(_) for _ in lat_deg]
    lat_min = [int(_) for _ in lat_min]
    lat_sec = [float(_) for _ in lat_sec]
    long_deg = [int(_) for _ in long_deg]
    long_min = [int(_) for _ in long_min]
    long_sec = [float(_) for _ in long_sec]
    return timestamp_to_time(timestamp),equivalentDegree(long_deg,long_min,long_sec),equivalentDegree(lat_deg,lat_min,lat_sec)





def main():
    timestamp,lons,lats = read_csv_data('../zz_astrolorenzini/zz_astrolorenzini_data.csv')    #print(latDeg,latMin,latSec)
    omegas = []
    thetas = []
    times = []
    i = 0
    intervallo = 15
    alfa_correttivo = omega_terra*intervallo*12

    while i < len(lons)-(intervallo+1):
        thetas.append(disgeod(lats[i],lons[i]-alfa_correttivo,lats[i+intervallo],lons[i+intervallo]))
        times.append(timestamp[i])
        i+=intervallo

    #print(thetas)
    #plt.plot(times,thetas)
    #plt.show()

    omegas = [theta/(12*intervallo) for theta in thetas]

    for i in range(len(omegas)):
        print(times[i], omegas[i])

    velocities = [omega*a for omega in omegas]
    radius = [computeRadius(omega) for omega in omegas]

    i=0
    while i<len(radius):
        if ((radius[i]-raggioTerra > 411490) or (radius[i]-raggioTerra < 395700)):
            radius.pop(i)
            times.pop(i)
        else:
            i+=1
    



    #plot graph
    fig, ax1 = plt.subplots()
    plt.title("Distance from Earth over time", 
          fontdict={'family': 'serif', 
                    'color' : 'darkblue',
                    'weight': 'bold',
                    'size': 18})
    
    ax1.set_xlabel("Time [s]",size = 14)
    ax1.set_ylabel("Distance from Earth's centre [m]",size = 14)
    
    ax1.grid(True)
    ax1.scatter(times,radius)
    ax2 = ax1.twinx()

    radius = [r-raggioTerra for r in radius ]
    ax2.plot(times,radius,'g')
    

    ax2.set_ylabel('Distance from Earth\'s surface [m]',size = 14) 
    
    fig.tight_layout()
    plt.show()

    omegas.sort()
    print(omegas)

    print("Dati disponibili:",len(radius))

main()