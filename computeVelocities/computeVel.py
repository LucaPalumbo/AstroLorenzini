#!/usr/bin/env python
from astropy.constants import M_earth, G
from z3 import *
from math import pi, cos,sin,acos
import time
from statistics import mean
import csv
#from computeRadius import *
#from computeRadius import raggioTerra,omega_terra
import matplotlib.pyplot as plt
#from geodetic import *


#Constants
EarthRadius = 6371000
EarthAngularVel = 360/(23*3600+56*60+4)
mu = M_earth.value*G.value
a = 6774373.659567392



#functions
def disgeod(latA,lonA,latB,lonB):
    lat_alfa = pi * latA / 180
    lat_beta = pi * latB / 180
    lon_alfa = pi * lonA / 180
    lon_beta = pi * lonB / 180
    fi = abs(lon_alfa - lon_beta)
    p = acos(sin(lat_beta) * sin(lat_alfa) +cos(lat_beta) * cos(lat_alfa) * cos(fi))
    return p

def equivalentDegree(degs,mins,secs):
    eqLat = []
    for i in range(len(degs)):
        #if(degs[i]>0):
        eqLat.append(degs[i]+mins[i]/60+secs[i]/3600) #forse da modificare
        #else:
        #    eqLat.append(degs[i]-mins[i]/60-secs[i]/3600) #forse da modificare

    return eqLat
    
def timestamp_to_time(t):
    time_values = []
    for _ in t:
        tempTimeObject = time.strptime(_,"%d/%m/%Y-%H:%M:%S:%f")
        time_values.append(tempTimeObject.tm_hour*3600+tempTimeObject.tm_min*60+tempTimeObject.tm_sec)
    time0 = time_values[0]
    time_values = [t-time0 for t in time_values]
    return time_values

def computeRadius(omega):
    s = Solver()
    
    r = Real('r')
    
    s.add((omega**2)*(r**3)+mu*r/a-2*mu == 0)
    s.check()
    m = s.model()
    if is_algebraic_value(m[r]):
        #print( m[r].approx(20))
        r = m[r].approx(20)
        return ( float(r.numerator_as_long())/float(r.denominator_as_long()))

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
    alfa_correttivo = EarthAngularVel*intervallo*12

    while i < len(lons)-(intervallo+1):
        thetas.append(disgeod(lats[i],lons[i]-alfa_correttivo,lats[i+intervallo],lons[i+intervallo]))
        times.append(timestamp[i])
        i+=intervallo

    

    omegas = [theta/(12*intervallo) for theta in thetas]


    radius = [computeRadius(omega) for omega in omegas]

    i=0
    while i<len(radius):
        if ((radius[i]-EarthRadius > 411490) or (radius[i]-EarthRadius < 395700)):
            radius.pop(i)
            omegas.pop(i)
            times.pop(i)
        else:
            i+=1
    
    vels = [radius[i]*omegas[i] for i in range(len(radius))]
    for i in range(len(radius)):
        print(times[i],omegas[i],radius[i],vels[i])
        

    omegas.sort()
    radius.sort()
    print(omegas)
    print(radius)
    print("Velocita' Media:",mean(vels))
    print("Velocita' massima:",max(vels))
    print("Velocita' minima:",min(vels))


    plt.grid(True)
    plt.scatter(times,vels,color = 'green')
    plt.plot(times,vels)
    plt.title("Tangential Velocity over time", 
          fontdict={'family': 'serif', 
                    'color' : 'darkblue',
                    'weight': 'bold',
                    'size': 18})
    plt.xlabel("Time [s]",size = 14)
    plt.ylabel("Velocity [m/s]",size = 14)
    plt.show()
    vels.sort()
    print(vels)

main()