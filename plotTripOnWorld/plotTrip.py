#!/usr/bin/env python

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import csv
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
def plotDataOnMap(x,y):
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
                llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

    
    xx = [i+0.5 for i in range(180)]
    yy = [i for i in range(180)]

    """
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(np.arange(-90.,91.,30.))
    m.drawmeridians(np.arange(-180.,181.,60.))
    m.drawmapboundary(fill_color='aqua')
    scale=0.2
    """
    m.bluemarble(scale=0.2)
    m.drawcoastlines(color='white', linewidth=0.2)

    #m.contour(x,y,x,color='k',latlon=True)
    print(len(x))
    print(len(y))

    m.scatter(x, y, 10, marker='.',color='red',latlon=True)

    #m.shadedrelief()
    plt.title("Mercator Projection")
    plt.show()


def read_csv_data(file_path):
    timestamp = []
    lat_deg = []
    lat_min = []
    lat_sec = []
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


    #dLats = [lat_deg[i]+lat_min[i]/60+lat_sec[i]/3600 for i in range(len(lat_deg))]
    #dLongs = [long_deg[i]+long_min[i]/60+long_sec[i]/3600 for i in range(len(long_deg))]

    return equivalentDegree(lat_deg,lat_min,lat_sec),equivalentDegree(long_deg,long_min,long_sec)
    #return lat_deg,long_deg

def equivalentDegree(degs,mins,secs):
    eqLat = []
    for i in range(len(degs)):
        #if(degs[i]>0):
        eqLat.append(degs[i]+mins[i]/60+secs[i]/3600) #forse da modificare
        #else:
        #    eqLat.append(degs[i]-mins[i]/60-secs[i]/3600) #forse da modificare
    #return decimal degree

    return eqLat


def main():
    lats,longs = read_csv_data('../zz_astrolorenzini/zz_astrolorenzini_data.csv')
    plotDataOnMap(longs,lats)


main()