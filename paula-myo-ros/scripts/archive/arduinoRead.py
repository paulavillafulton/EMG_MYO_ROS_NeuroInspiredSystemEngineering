import serial
import time

ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
time.sleep(1)

logfile = open('test.csv', 'a')

while 1:
	line = ser.readline()
	now = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
	a =  "%s, %s, %s" % (now, line, "\n")
	print a	
	logfile.write(a)
        logfile.flush()   
logfile.close()
ser.close()
