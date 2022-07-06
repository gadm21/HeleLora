#!/usr/bin/env python3

import time, re, threading, os, sys 
import argparse 
from bluepy.btle import BTLEDisconnectError
import pathlib

from miband import miband


def get_args() : 
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--label', required=True, type = int, help='Set the label to be associated with the data that will be collection.')
    parser.add_argument('-d', '--duration', required=True, type = int, help='Set the duration (in minutes) for the script to run and collect data.')
    args = parser.parse_args()
    return args


auth_key_filename = 'auth_key.txt'
mac_filename = 'mac.txt'
dataset_path = None 
band = None

# list of lists. Each element is a list of 6 measurements at some time t. The measurements are (ordered):
# [gyro_x_delta, gryo_y_delta, gyro_z_delta, abs_delta_sum, current_HR, HR_change_rate]
timeseries_data = [] 
timeseries_maxlen = 30
start_time = 0
stop_flag = False
#-------------------------------------------------------------------------#


class regex_patterns():
    mac_regex_pattern = re.compile(r'([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})')
    authkey_regex_pattern = re.compile(r'([0-9a-fA-F]){32}')


def get_mac_address(filename):
    try:
        with open(filename, "r") as f:
            hwaddr_search = re.search(regex_patterns.mac_regex_pattern, f.read().strip())
            if hwaddr_search:
                MAC_ADDR = hwaddr_search[0]
            else:
                print ("No valid MAC address found in {}".format(filename))
                exit(1)
    except FileNotFoundError:
            print ("MAC file not found: {}".format(filename))
            exit(1)
    return MAC_ADDR


def get_auth_key(filename):
    try:
        with open(filename, "r") as f:
            key_search = re.search(regex_patterns.authkey_regex_pattern, f.read().strip())
            if key_search:
                AUTH_KEY = bytes.fromhex(key_search[0])
            else:
                print ("No valid auth key found in {}".format(filename))
                exit(1)
    except FileNotFoundError:
            print ("Auth key file not found: {}".format(filename))
            exit(1)
    return AUTH_KEY



def save_dataset(is_last = False, label = None): 
    ''' 
    saves a txt file containing the data in the following format: 
    - The first line contains the label, which can be either 1 (exercise), 2 (sleeping), or 3 (studying). 
    - Each of the following line will either contain 4 or 2 comma separated values: 
        * IF it contains 4 values, the values are for the variables ['gyro_x', 'gryo_y', 'gyro_z', 'timestamp']
        * If it contains 2 values, the values are for the variables ['heart rate', 'timestamp']
    '''
    global timeseries_data, dataset_path
    
    first_attempt = False
    dir_path = '/home/pi/Desktop/Data'
    if not os.path.exists(dir_path) :
        os.makedirs(dir_path)
    
    if dataset_path is None : 
        dataset_path = os.path.join(dir_path, '{}_{}_.txt'.format(label, int(time.time())) )
        first_attempt = True
        
    with open(dataset_path, 'a') as f :
        if first_attempt : 
            f.write('start')
            f.write('\n')
        elif is_last :
            f.write('end')
            f.write('\n') 
        for datum in timeseries_data : 
            f.write(','.join(str(d) for d in datum))
            f.write('\n') 
    timeseries_data = [] 


   

def sensors_callback(data):
    global stop_flag
    tick_time = time.time() 

    data_type = data[0] 
    data = data[1] 

    if data_type == 'GYRO_RAW': 
        for datum in data : 
            current_data = [datum['gyro_raw_x'], datum['gyro_raw_y'], datum['gyro_raw_z'], tick_time]
            timeseries_data.append(current_data)
    elif data_type == 'HR' : 
        current_data = [data, tick_time]
        timeseries_data.append(current_data)
        
    if len(timeseries_data) > timeseries_maxlen :
        save_dataset()
    
    if stop_flag :
        print("stop flag:", stop_flag) 
    return stop_flag



def connect():
    global band
    success = False
    timeout = 3
    msg = 'Connection to the band failed. Trying again in {} seconds'
    
    current_directory = pathlib.Path(__file__).parent.resolve()
    MAC_ADDR = get_mac_address(os.path.join(current_directory, mac_filename))
    AUTH_KEY = get_auth_key(os.path.join(current_directory, auth_key_filename))

    while not success:
        try:
            band = miband(MAC_ADDR, AUTH_KEY, debug=True)
            success = band.initialize()
        except BTLEDisconnectError:
            print(msg.format(timeout))
            time.sleep(timeout)
        except KeyboardInterrupt:
            print("\nExit.")
            exit()


def start_data_pull(duration, label):
    global start_time
    start_time = time.time() 
    while True:
        try:
            save_dataset(label = label) # just to create the file and name it with label.
            band.start_heart_and_gyro(sensitivity=1, callback=sensors_callback, start_time = start_time, duration = duration)
            if int(time.time() - start_time) > duration * 60 : 
                save_dataset(is_last = True) 
                return  
             
        except BTLEDisconnectError:
            band.gyro_started_flag = False
            connect()



if __name__ == "__main__":
    args = get_args() 
    connect()
    t1 = threading.Thread(target=start_data_pull, args = (args.duration, args.label,))
    t1.start()
    t1.join()
