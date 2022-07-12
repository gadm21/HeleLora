import LoRa
from HelperFunctions import *


lora = LoRa.LoRa()  # Initialize serial instance
lora.set_addr(1)  # Sets the LoRa address
receiver_address = 2
# data_dir = '/home/pi/Desktop/Data/'
data_dir = ''
filename = data_dir + 'test.txt'

# protocol parameters
window_size = 8
segment_size = 32  # 7-bit characters - 224 Bytes Segment
timeout = 0.1

# prepare the packets
f = open(data_dir + filename)
data = f.read()
data_packets = prepare_data(data, segment_size)
num_packets = len(data_packets) + 1
all_packets = [('0\r\n' + str(num_packets)), ]
all_packets.extend(data_packets)

# start sending
next_packet_num = 0
while next_packet_num < num_packets:
    packets_to_send = all_packets[next_packet_num:next_packet_num + window_size]
    for packet in packets_to_send:
        lora.send_msg(receiver_address, str(len(packet)) + ',' + packet)
        ack_num = rcv_ack(next_packet_num + window_size, lora, timeout, next_packet_num)
        next_packet_num = int(ack_num)
