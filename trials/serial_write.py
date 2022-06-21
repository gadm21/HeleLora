#!/usr/bin/env python
import time
import serial

serial_conn = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
#serial_conn.write(str.encode("AT+ADDRESS=" + str(1) + "\r\n"))
#serial_payload = (serial_conn.readline())[:-2]
#print("Address set?", serial_payload.decode(encoding="utf-8"))

counter=0
ser_command=b'AT\r\n'
serial_conn.write(ser_command)
time.sleep(1)
counter += 1
