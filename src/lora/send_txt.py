import LoRa
import time
import os

lora = LoRa.LoRa() # Initialize serial instance
#time.sleep(3)
lora.set_addr(1)  # Sets the LoRa address
receiver_addr = 2
data_dir = '/home/pi/Desktop/Data/'

for filename in os.listdir(data_dir):
    if os.path.isfile(os.path.join(data_dir, filename)):
        with open(data_dir+filename) as f:
            for line in f:
                print("sending data", line.strip('\r\n'))
                lora.send_msg(receiver_addr, filename+','+line)
                time.sleep(5)
            print("Done sending file")
        os.system('mv '+data_dir+filename+' '+data_dir+'Sent/'+filename)
