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
maximize_graph = False

vibration_settings = {
    'interval_minutes': 20,
    'duration_seconds': 10,
    'type': 'random',
    'heartrate_alarm_pct': 17
    }

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
    x_feature_names = ['gyro_x_delta', 'gryo_y_delta', 'gyro_z_delta', 'abs_delta_sum', 'current_HR', 'HR_change_rate']
    df = pd.DataFrame(timeseries_data, columns = x_feature_names) 
    df['activity'] = [args.label] * len(df)
    file_path = os.path.join('Data', '{}_{}_{}.csv'.format(args.label, args.duration, int(time.time())) )
    df.to_csv(file_path)  


def get_HR_change_rate(current_HR):
    min_HR = timeseries_data[0][4]
    for data in timeseries_data : 
        if data[4] < min_HR : 
            min_HR  = data[4] 
    if min_HR == 0 : min_HR += 0.1
    return int((current_HR - min_HR) / min_HR * 100 )
   

def sleep_monitor_callback(data):
    tick_time = time.time()

    current_data = [0]*6
    if data[0] == 'GYRO_RAW': 
        gyro_movement = sleepdata.process_gyro_data(data[1], tick_time)  
        current_data[:-1] = gyro_movement
        print("Gyro movement: {}".format(gyro_movement))

    elif data[0] == 'HR' : 
        current_data[4] = data[1]
        print("Heart rate: {}".format(data[1]), end = '\t') 
        current_data[5] = get_HR_change_rate(data[1]) 
        
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
            band.start_heart_and_gyro(sensitivity=1, callback=sleep_monitor_callback, start_time = start_time, duration = args.duration)
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
