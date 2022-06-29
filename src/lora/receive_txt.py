import LoRa
import time

lora = LoRa.LoRa() # Initialize serial instance
lora.set_addr(2)  # Sets the LoRa address
data_dir = '/home/pi/Desktop/Data/'
count = 0
while 1:
        received = lora.read_msg()
        if bool(received):
            data = received['data']
            filename = received['filename']
            print(received['data'])
            with open(data_dir+filename, 'a') as f:
                f.write(data+'\n')
                count = count+1
                print(count)
