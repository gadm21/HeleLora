#!/usr/bin/env python3

import time, re, threading, os
import argparse 
from bluepy.btle import BTLEDisconnectError
from miband import miband
import sleepdata
import pandas as pd 


parser = argparse.ArgumentParser()
parser.add_argument('-l', '--label', required=True, type = int, help='Set the label to be associated with the data that will be collection.')
parser.add_argument('-d', '--duration', required=True, type = int, help='Set the duration (in minutes) for the script to run and collect data.')
args = parser.parse_args()


auth_key_filename = 'auth_key.txt'
mac_filename = 'mac.txt'

band = None

# list of lists. Each element is a list of 6 measurements at some time t. The measurements are (ordered):
# [gyro_x_delta, gryo_y_delta, gyro_z_delta, abs_delta_sum, current_HR, HR_change_rate]
timeseries_data = [] 
timeseries_maxlen = 30
start_time = 0

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


def average_data(tick_time):
    if (tick_time - sleepdata.last_tick_time) >= sleepdata.tick_seconds:
        sleepdata.average_raw_data(tick_time)
        sleepdata.last_tick_time = time.time()


def save_dataset(): 
    ''' 
    saves a txt file containing the data in the following format: 
    - The first line contains the label 
    - Each of the following line will either contain 4 or 2 comma separated values: 
        * IF it contains 4 values, the values are for the variables ['gyro_x', 'gryo_y', 'gyro_z', 'timestamp']
        * If it contains 2 values, the values are for the variables ['heart rate', 'timestamp']
    '''
    file_path = os.path.join('Data', '{}_{}.txt'.format(args.label, int(time.time())) )
    with open(file_path, 'w') as f : 
        f.write(args.label) 
        for datum in timeseries_data : 
            f.write(','.join(datum)) 
      


   

def sensors_callback(data):
    tick_time = int(time.time())

    data_type = data[0] 
    data = data[1] 

    if data_type == 'GYRO_RAW': 
        current_data = [data['gyro_raw_x'], data['gyro_raw_y'], data['gyro_raw_z'], tick_time]
    elif data_type == 'HR' : 
        current_data = [data, tick_time]
        
    timeseries_data.append(current_data)


def connect():
    global band
    success = False
    timeout = 3
    msg = 'Connection to the band failed. Trying again in {} seconds'

    MAC_ADDR = get_mac_address(mac_filename)
    AUTH_KEY = get_auth_key(auth_key_filename)

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


def start_data_pull():
    while True:
        try:
            band.start_heart_and_gyro(sensitivity=1, callback=sensors_callback, start_time = start_time, duration = args.duration)
            if int(time.time() - start_time) > args.duration * 60 : 
                save_dataset() 
                return  
             
        except BTLEDisconnectError:
            band.gyro_started_flag = False
            connect()



if __name__ == "__main__":
    connect()
    start_time = time.time() 
    threading.Thread(target=start_data_pull).start()
