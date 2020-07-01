#!/usr/bin/env python
from astropy.constants import M_earth, G
from math import pi

def thirdKeplerLow(t):
    return (t**2*(G.value*M_earth.value)/(4*pi**2))**(1./3)

def main():
    orbitTime = 5549 #seconds
    a = thirdKeplerLow(orbitTime)
    print(a)

main()