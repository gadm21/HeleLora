import LoRa
import time

lora = LoRa.LoRa() # Initialize serial instance
lora.set_addr(2)  # Sets the LoRa address

data_dir = '/home/pi/Desktop/Data/'
count = 0
all_data = {}
data_maxlen = 99 
idle_maxwait = 10 # seconds
last_received_at = time.time()

def save_data(filepath):
    global all_data
    data = all_data[filepath]
    with open(filepath, 'a') as f:
        num_lines = len(data) 
        for datum in data :
            f.write(datum+'\n')
        print("file {} has {} lines".format(filepath.split('/')[-1], num_lines))
        
        
while 1:
        received = lora.read_msg()
        if bool(received):
            waiting_time = time.time() - last_received_at
            last_received_at = time.time() 
            datum = received['data']
            filename = received['filename']
            print('received:', datum)
            if not filename in all_data.keys() :
                all_data[filename] = []
            all_data[filename].append(datum)
            if len(all_data[filename]) > data_maxlen or waiting_time > idle_maxwait:
                save_data(filename)
                all_data[filename] = [] 
