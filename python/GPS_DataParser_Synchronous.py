""" GPS Log Parser """
import serial
import time
from time import strftime, localtime

def parseLog():
    addr  = '/dev/ttyACM0'
    baud  = 57600
    fname = 'logs/GPSLogParsed_' + timeStamp() + '.csv'
    fmode = 'ab'

    with serial.Serial(addr,baud) as ser, open(fname,fmode) as outf:
        ser.flushOutput()
        time.sleep(1)
        ser.flushInput()
        
        print "Beginning log acquisition and assembly."
        time.sleep(1)
        
        ser.write('p')
        time.sleep(0.5)
        ser.write('l')
        time.sleep(0.5)
        
        if ser.inWaiting() == 0:
            print "Waiting for serial data at program start."
            while ser.inWaiting == 0:
                time.sleep(0.01)
                
        while ser.inWaiting() > 0:
            logLine = ser.readline().strip('\r\n')
            print logLine
            outf.write(logLine)
            outf.flush()
            ser.write('l')
            time.sleep(0.01)
            if ser.inWaiting() == 0:
                time.sleep(0.01)
                print "Waiting for serial data."

def timeStamp():
    month = strftime('%m', localtime())
    day = strftime('%d', localtime())
    year = strftime('%y', localtime())
    hour = strftime('%H', localtime())
    minute = strftime('%M', localtime())
    second = strftime('%S', localtime())
    currentDateTime = month + day + year + '-' + hour + minute + second
    return currentDateTime

try:
    parseLog()
    print "Parsing of GPS log file completed successfully."
except KeyboardInterrupt:
    #CMD TO EXEC ON INTERRUPT
    print "Program interrupted before completion of log file parsing."
