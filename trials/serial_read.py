
#!/usr/bin/env python
import time
import serial

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

#out = ''
while 1:
	out = ser.readline()
#	if len(out) != 0:
#		out = ord(out)
	print(out)
#while 1:
#	x=ser.read(10) & 0x7F
#	print(x)
