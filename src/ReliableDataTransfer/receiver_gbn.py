import LoRa
from math import inf
from time import time

lora = LoRa.LoRa()  # Initialize serial instance
lora.set_addr(2)  # Sets the LoRa address
sender_address = 1
data_dir = '/home/pi/Desktop/Data/'

num_packets = inf
received_data = ''
num_received_packets = 0
next_packet_num = 0

start_time = time()
while num_received_packets < num_packets:
    message = lora.read_msg()
    packet_num, data = message.split("\r\n")
    packet_num = int(packet_num)
    if packet_num == next_packet_num:
        if packet_num == 0 and num_packets == inf:
            num_packets = int(data)
            next_packet_num = packet_num + 1
        else:
            received_data += data
            num_received_packets += 1
            next_packet_num = packet_num + 1
        ack = str(packet_num)
        lora.send_msg(sender_address, str(len(ack)) + ',' + ack)
    else:
        ack = str(next_packet_num)
        lora.send_msg(sender_address, str(len(ack)) + ',' + ack)

for i in range(5):
    ack = str(next_packet_num)
    lora.send_msg(sender_address, str(len(ack)) + ',' + ack)

end_time = time()
text_file = open(f"{end_time-start_time}_received.txt", "w")
text_file.write(received_data)
text_file.close()
