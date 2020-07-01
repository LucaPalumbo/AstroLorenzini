#!/usr/bin/env python
import csv
import time

def read_csv_data(file_path):
    timestamp = []
    yaw = []
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
            yaw.append(row[9])
            line_count+=1
    yaw = [float(_) for _ in yaw]

    return timestamp,yaw


def timestamp_to_time(t):
    time_values = []
    for _ in t:
        tempTimeObject = time.strptime(_,"%d/%m/%Y-%H:%M:%S:%f")
        time_values.append(tempTimeObject.tm_hour*3600+tempTimeObject.tm_min*60+tempTimeObject.tm_sec)
    time0 = time_values[0]
    time_values = [t-time0 for t in time_values]
    return time_values


def computeOrbitTime(time,yaw):
    i=0
    startTime = -1
    endTime = -1
    ib = 0
    ie = 0
    while i < len(yaw):
        if yaw[i] > 357:
            if startTime == -1:
                ib = i
                startTime = time[i]
                i+=20
                continue
            else:
                ie = i
                endTime = time[i]
                break
        i+=1
    return endTime-startTime, ib, ie


def main():
    timestamp,yaw = read_csv_data('../zz_astrolorenzini/zz_astrolorenzini_data.csv')
    time_values = timestamp_to_time(timestamp)
    orbitTime,ib,ie = computeOrbitTime(time_values,yaw)
    print("Il tempo di orbita è di {} secondi. {},{}".format(orbitTime,ib,ie))



main()