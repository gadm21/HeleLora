import LoRa
import time
import os
import wiringpi

lora = LoRa.LoRa() # Initialize serial instance
#time.sleep(3)
lora.set_addr(1)  # Sets the LoRa address
receiver_addr = 2
file_path = '/home/pi/Desktop/Data/test.txt'
delays = [1, 2]
for delay in delays :
    fake_filename = str(delay) + '_' + str(int(time.time()))
    with open(file_path) as f:
        for line in f:
            lora.send_msg(receiver_addr, fake_filename+','+line.strip('\r\n'))
            time.sleep(delay)
        print("Done sending file with delay:", delay)

