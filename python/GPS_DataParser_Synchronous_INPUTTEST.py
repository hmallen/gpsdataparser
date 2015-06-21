""" GPS Log Parser """
import serial
import time
from time import strftime, localtime

def parseLog():
    gpsDataType = gpsDataSelect()
    if gpsDataType == 1:
        gpsNameTag = '-GPGGA'
    elif gpsDataType == 2:
        gpsNameTag = '-GPRMC'
    
    addr  = '/dev/ttyACM0'
    baud  = 57600
    fname = 'logs/GPSLogParsed_' + timeStamp() + gpsNameTag + '.csv'
    fmode = 'ab'

    with serial.Serial(addr,baud) as ser, open(fname,fmode) as outf:
        ser.flushOutput()
        time.sleep(1)
        ser.flushInput()
        
        print "Beginning log acquisition and assembly."
        time.sleep(1)
        
        ser.write('p')
        time.sleep(0.5)
        
        if gpsDataType == 1:
            ser.write('G')
        elif gpsDataType == 2:
            ser.write('R')
        else:
            print "Program failure do to mishandling of user input."
            while True:
                print "Please restart program..."
                time.sleep(30)
        time.sleep(0.5)
        
        ser.write('l')
        time.sleep(0.5)
        
        if ser.inWaiting() == 0:
            print "Waiting for serial data at program start."
            while ser.inWaiting == 0:
                time.sleep(0.01)
                
        while ser.inWaiting() > 0:
            logLine = ser.readline().strip('\r\n')
            if logLine is not '':
                print logLine
                outf.write(logLine)
                outf.flush()
                ser.write('l')
                time.sleep(0.01)
                if ser.inWaiting() == 0:
                    time.sleep(0.01)
                    print "Waiting for serial data."
            else:
                print "Empty line -- Excluded from parsed log."

def timeStamp():
    month = strftime('%m', localtime())
    day = strftime('%d', localtime())
    year = strftime('%y', localtime())
    hour = strftime('%H', localtime())
    minute = strftime('%M', localtime())
    second = strftime('%S', localtime())
    currentDateTime = month + day + year + '-' + hour + minute + second
    return currentDateTime

def gpsDataSelect():
    while True:
        print "Options: 1 - GPGGA / 2 - GPRMC"
        gpsDataType = input("Which GPS data type would you like parsed? ")
        if gpsDataType == 1 or gpsDataType == 2:
            return gpsDataType
        else:
            print "Invalid selection."
    
try:
    parseLog()
    print "Parsing of GPS log file completed successfully."
except KeyboardInterrupt:
    #CMD TO EXEC ON INTERRUPT
    print "Program interrupted before completion of log file parsing."
