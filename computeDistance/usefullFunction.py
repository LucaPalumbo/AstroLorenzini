from astropy.constants import M_earth, G
from z3 import *
from math import pi
import time
import csv

#costanti
raggioTerra = 6371000
omega_terra = 360/(23*3600+56*60+4)
mu = M_earth.value*G.value
a = 6774373.659567392

#funzioni
def rad(deg):
    return deg*pi/180

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
    yaw = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count==0 :
                #print('Reading name of columns')
                for i in range(len(row)):
                    pass
                    #print(row[i],i)
                line_count+=1
                continue
            timestamp.append(row[0])
            yaw.append(row[9])
            line_count+=1
    yaw = [float(_) for _ in yaw]

    return timestamp, yaw

def thirdKeplerLaw(t):
    return (t**2*(G.value*M_earth.value)/(4*pi**2))**(1./3)

def computeRadius2(v):
    return ((v**2)/(2*mu)+1/(2*a))**-1

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

def read_csv_longitude(file_path):
    timestamp = []
    long_deg = []
    long_min = []
    long_sec = []
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
            long_deg.append(row[4])
            long_min.append(row[5])
            long_sec.append(row[6])
            line_count+=1
    long_deg = [int(_) for _ in long_deg]
    long_min = [int(_) for _ in long_min]
    long_sec = [float(_) for _ in long_sec]
    return timestamp,equivalentDegree(long_deg,long_min,long_sec)

def fixOmegas(omegas):
    orbitTime_gyro = 5549
    orbitTime_longitude = 5913
    alpha = (2*pi/orbitTime_gyro)*orbitTime_longitude
    earth_omega = (alpha-2*pi)/orbitTime_longitude
    omegas = [omega-earth_omega for omega in omegas]
    return omegas