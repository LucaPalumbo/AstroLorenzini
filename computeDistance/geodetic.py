from astropy.constants import M_earth, G
from z3 import *
from math import pi,sin,acos,cos,radians,atan2,sqrt
import time
import csv


"""
#include <math.h>
/* Questa funzione calcola la distanza tra due punti 
sulla superficie terrestre, date le coordinate in
latitudine e longitudine espresse in
gradi decimali */
double disgeod (double latA, double lonA,
                double latB, double lonB)
{
      /* Definisce le costanti e le variabili */
      const double R = 6371;
      const double pigreco = 3.1415927;
      double lat_alfa, lat_beta;
      double lon_alfa, lon_beta;
      double fi;
      double p, d;
      /* Converte i gradi in radianti */
      lat_alfa = pigreco * latA / 180;
      lat_beta = pigreco * latB / 180;
      lon_alfa = pigreco * lonA / 180;
      lon_beta = pigreco * lonB / 180;
      /* Calcola l'angolo compreso fi */
      fi = fabs(lon_alfa - lon_beta);
      /* Calcola il terzo lato del triangolo sferico */
	  p = acos(sin(lat_beta) * sin(lat_alfa) + 
        cos(lat_beta) * cos(lat_alfa) * cos(fi));
      /* Calcola la distanza sulla superficie 
      terrestre R = ~6371 km */
      d = p * R;
      return(d);
}
"""
def disgeod(latA,lonA,latB,lonB):
    lat_alfa = pi * latA / 180
    lat_beta = pi * latB / 180
    lon_alfa = pi * lonA / 180
    lon_beta = pi * lonB / 180
    fi = abs(lon_alfa - lon_beta)
    p = acos(sin(lat_beta) * sin(lat_alfa) +cos(lat_beta) * cos(lat_alfa) * cos(fi))
    return p

def distanza(lat1,lon1,lat2,lon2):
    la1 = radians(lat1)
    la2 = radians(lat2)
    lo1 = radians(lon1)
    lo2 = radians(lon2)
    dLat = la1-la2
    dLon = lo1-lo2
    a = sin(dLat/2)*sin(dLat/2)+sin(dLon/2)*sin(dLon/2)* cos(la1) * cos(la2)
    c = 2*atan2(math.sqrt(a),sqrt(1-a))
    return c

