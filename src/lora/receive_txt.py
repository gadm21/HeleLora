import LoRa
import time

lora = LoRa.LoRa() # Initialize serial instance
lora.set_addr(2)  # Sets the LoRa address

data_dir = '/home/pi/Desktop/Data/'
count = 0
all_data = {}
data_maxlen = 99 
idle_maxwait = 5 # seconds
last_received_at = time.time()

def save_data(filename):
    global all_data
    data = all_data[filename]
    with open(data_dir+filename, 'a') as f:
        num_lines = len(data) 
        for datum in data :
            f.write(datum+'\n')
        print("file {} has {} lines".format(filename, num_lines))
        
        
while 1:
        received = lora.read_msg()
        waiting_time = time.time() - last_received_at
        if bool(received):
            last_received_at = time.time() 
            datum = received['data']
            filename = received['filename']
            print('received:', datum)
            if not filename in all_data.keys() :
                all_data[filename] = []
            all_data[filename].append(datum)
            if len(all_data[filename]) > data_maxlen:
                save_data(filename)
                all_data[filename] = []
        elif waiting_time > idle_maxwait :
            for filename, data in all_data.items() :
                if len(data) > 0 :
                    save_data(data_dir+filename)
                    all_data[filename]= [] 
            
