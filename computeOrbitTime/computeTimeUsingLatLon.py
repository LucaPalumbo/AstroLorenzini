#!/usr/bin/env python
import csv
import time

def read_csv_data(file_path):
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

    return timestamp,long_deg,long_min,long_sec

def timestamp_to_time(t):
    time_values = []
    for _ in t:
        tempTimeObject = time.strptime(_,"%d/%m/%Y-%H:%M:%S:%f")
        time_values.append(tempTimeObject.tm_hour*3600+tempTimeObject.tm_min*60+tempTimeObject.tm_sec)
    time0 = time_values[0]
    time_values = [t-time0 for t in time_values]
    return time_values

def equivalentLongitude(degs,mins,secs):
    eqLat = []
    for i in range(len(degs)):
        eqLat.append(degs[i]+mins[i]/60+secs[i]/60) #forse da modificare
    return eqLat

def computeOrbitTime(time,longitude):
    i=0
    startTime = -1
    ib = 0
    endTime = -1
    ie = 0
    #for i in range(len(longitude)):
    while i < len(longitude):
        if longitude[i] < -170:
            print(longitude[i])

            if startTime < 0:
                startTime = time[i]
                ib = i
                i+=20
            else:
                endTime = time[i]
                ie = i
                i+=20
        i+=1
    return endTime - startTime, ib,ie
        

def main():
    timestamp,latDeg,latMin,latSec = read_csv_data('../zz_astrolorenzini/zz_astrolorenzini_data.csv')    #print(latDeg,latMin,latSec)
    time_values = timestamp_to_time(timestamp)
    eqLongitude = equivalentLongitude(latDeg,latMin,latSec)
    orbitTime,ib,ie = computeOrbitTime(time_values, eqLongitude)
    print("Il tempo di orbita è di {} secondi. {},{}".format(orbitTime,ib,ie))


main()