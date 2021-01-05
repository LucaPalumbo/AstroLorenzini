import logging
import logzero
from logzero import logger, logfile
from sense_hat import SenseHat
import os
import time
import csv
import ephem
from datetime import datetime, timedelta
from picamera import PiCamera

dir_path =  os.path.dirname(os.path.realpath(__file__))

#connect to sense hat
sense = SenseHat()

#set a log file
logfile(dir_path+"/astrolorenzini.log")



#latest TLE data for ISS
name = "ISS (ZARYA)"
line1= "1 25544U 98067A   20006.55702477  .00001059  00000-0  26955-4 0  9991"
line2= "2 25544  51.6453  73.1830 0005159 105.4393  49.5527 15.49542542206802"
iss = ephem.readtle(name, line1, line2)

#set up camera
cam = PiCamera()
cam.resolution = (1296,972)

def create_csv_file(datafile):
    "Create a new CSV file and add the header row"
    with open(datafile, 'w') as f:
        writer = csv.writer(f)
        header = ('time_stamp','lat_deg','lat_min','lat_sec','long_deg','long_min','long_sec','gyro_pitch','gyro_roll','gyro_yaw','acc_x','acc_y','acc_z','mag_x','mag_y','mag_z','compass','humidity','temperature','pressure','gyro_vel_x','gyro_vel_y','gyro_vel_z')
        writer.writerow(header)
def add_csv_data(datafile,data):
    "Add a row of data to the datafile CSV"
    with open(datafile, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def setMetadata():
    iss.compute() # Get the lat/long values from ephem

    long_value = [float(i) for i in str(iss.sublong).split(":")]

    if long_value[0] < 0:

        long_value[0] = abs(long_value[0])
        cam.exif_tags['GPS.GPSLongitudeRef'] = "W"
    else:
        cam.exif_tags['GPS.GPSLongitudeRef'] = "E"
    cam.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (long_value[0], long_value[1], long_value[2]*10)

    lat_value = [float(i) for i in str(iss.sublat).split(":")]

    if lat_value[0] < 0:

        lat_value[0] = abs(lat_value[0])
        cam.exif_tags['GPS.GPSLatitudeRef'] = "S"
    else:
        cam.exif_tags['GPS.GPSLatitudeRef'] = "N"

    cam.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (lat_value[0], lat_value[1], lat_value[2]*10)

#initialise csv file
datafile = dir_path+"/data.csv"
create_csv_file(datafile)

#store start time
start_time = datetime.now()
#store the current time
last_catch = datetime.now()
photoCounter = 1

while(datetime.now() < start_time + timedelta(minutes=179)):
    try:
        logger.info("{} iteration {}".format(datetime.now,photoCounter))

        #get timestamp
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S:%f")

        #calculate position of iss
        iss.compute()
        lat = str(iss.sublat).split(':')
        long = str(iss.sublong).split(':')

        #get pitch, roll and yaw orientation from gyro
        o = sense.get_orientation()
        gyro_pitch = o['pitch']
        gyro_roll = o['roll']
        gyro_yaw = o['yaw']

        #get acceleration
        acc_x,acc_y,acc_z = sense.get_accelerometer_raw().values()
        acc_roll, acc_pitch, acc_yaw = sense.get_accelerometer().values()

        #get magnetometer values
        mag_x,mag_y,mag_z = sense.get_compass_raw().values()
        compass = sense.get_compass()

        #get gyro velocity
        gyro_vel = sense.get_gyroscope_raw()
        gyro_vel_x = gyro_vel['x']
        gyro_vel_y = gyro_vel['y']
        gyro_vel_z = gyro_vel['z']

        #get humidity
        humidity = sense.get_humidity()

        #get temperature
        temperature = sense.get_temperature()

        #get pressure
        pressure = sense.get_pressure()

        if(datetime.now()>last_catch+timedelta(seconds=12)):
            add_csv_data(datafile,(timestamp,lat[0],lat[1],lat[2],long[0],long[1],long[2],gyro_pitch,gyro_roll,gyro_yaw,acc_x,acc_y,acc_z,mag_x,mag_y,mag_z,compass,humidity,temperature,pressure,gyro_vel_x,gyro_vel_y,gyro_vel_z))
            last_catch = datetime.now()
            setMetadata()
            cam.capture(dir_path+"/{0:0=4d}.jpg".format(photoCounter))
            photoCounter+=1

    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__,e))