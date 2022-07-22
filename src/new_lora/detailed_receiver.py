
import LoRa
import time

lora = LoRa.LoRa() # Initialize serial instance
lora.set_addr(2)  # Sets the LoRa address

data_dir = '/home/pi/Desktop/Data/'

all_data = {}
data_maxlen = 99 
idle_maxwait = 5 # seconds
last_received_at = 0


        
while 1:
        received = lora.read_msg()
        waiting_time = time.time() - last_received_at
        
        if bool(received):
            new_file = False
            
            last_received_at = time.time() 
            datum = received['data']
            filename = received['filename']
            
            if not filename in all_data.keys() :
                new_file = True
                all_data[filename] = []
            all_data[filename].append(datum)
            
            print(' received:{}\n file:{}\n line:{}'\
                  .format(datum, filename, len(all_data[filename])))
            if new_file :
                print(" New file created")
            else :
                print(" waited for:", waiting_time)
            print("___________________________")
 
        

