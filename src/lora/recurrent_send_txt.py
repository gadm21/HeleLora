import LoRa
import time
import os

lora = LoRa.LoRa() # Initialize serial instance
#time.sleep(3)
lora.set_addr(1)  # Sets the LoRa address
receiver_addr = 2
file_path = '/home/pi/Desktop/Data/test.txt'
delays = [1, 3, 5]
for delay in delays :

    with open(file_path) as f:
        for line in f:
            lora.send_msg(receiver_addr, filename+','+line)
            time.sleep(delay)
        print("Done sending file with delay:", delay)

