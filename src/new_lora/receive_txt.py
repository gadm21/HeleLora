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
    with open(data_dir+filename+'.txt', 'a') as f:
        num_lines = len(data) 
        for datum in data :
            datum = '_'.join([str(d) for d in datum]) 
            f.write(datum+'\n')
        print("file {} has {} lines".format(filename, num_lines))
        
        
while 1:
        received = lora.read_msg()
        waiting_time = time.time() - last_received_at
        if bool(received):
            last_received_at = time.time() 
            data = received['data']
            rssi = received['rssi'] 
            snr = received['snr']
            print(type(data), ' ', len(received['rssi']))
            rssi = int(received['rssi'])
            snr= int(received['snr'])
            print("rssi:", rssi, " snr:", snr) 
            file_id = data[0]
            print('received:', data, ' rssi:{} snr:{}'.format(rssi, snr))

            if not file_id in all_data.keys() :
                all_data[file_id] = []
            all_data[file_id].append(data)

        elif waiting_time > idle_maxwait :
            for file_id, data in all_data.items() :
                if len(data) > 0 :
                    save_data(file_id)
                    all_data[file_id]= [] 
            
