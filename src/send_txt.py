import LoRa
import time
import os
import argparse 
import random

lora = LoRa.LoRa() # Initialize serial instance
sender_address = 1
receiver_address = 2
lora.set_addr(sender_address)  # Sets the LoRa address

def get_args() : 
    parser = argparse.ArgumentParser()
    parser.add_argument('-SF', '--spreading factor', required=False, type = int, help='set the spreading factor of LoRa.', default = 12)
    parser.add_argument('-L', '--num_lines', required=False, type = int, help='Number of lines in the simulation file to be sent.', default = 20)
    parser.add_argument('-D', '--delay', required=False, type = int, help='Sending delay between line (in seconds).', default = 0)
    args = parser.parse_args()
    return args

data_dir = '/home/pi/Desktop/Data/'

if __name__ == "__main__" : 
    args = get_args
    file_id = str(random.randint(0, 999))
    print("File id:{}  msg length:{}  delay:{}"\
        .format(file_id, len(lora.sample_message(file_id = file_id, line_id = 0, SF = args.SF)), args.delay)) 
    
    for line in range(args.num_lines) : 
        msg = lora.sample_message(file_id = file_id, line_id = line, SF = args.SF)
        lora.send_msg(receiver_address, msg)
        time.sleep(args.delay) 
    print("Done sending file id:", file_id) 
    
    