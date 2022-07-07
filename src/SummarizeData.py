import os
import collections
import json

data_dir = '/home/pi/desktop/data'
measurements_dir = '/home/pi/desktop/measurements/'

try:
    f = open(data_dir + 'measurements_dict.json', 'r')
    measurements_dict = json.load(f)
    f.close()
except FileNotFoundError:
    measurements_dict = collections.defaultdict(dict)

for filename in os.listdir(data_dir):
    f = open(data_dir + filename, 'r')
    lines = f.readlines()
    f.close()
    delay, timestamp = filename.split('_')
    timestamp = timestamp.split('.')[0]
    measurements_dict[delay][timestamp] = len(lines)

with open(measurements_dir + 'measurements_dict.json', 'w') as f:
    json.dump(measurements_dict, f)
