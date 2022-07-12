import LoRa
from time import time


def prepare_data(raw_data, segment_size):
    num_packets = len(raw_data) // segment_size + 1
    return [(str(i+1) + '\r\n' + raw_data[i * segment_size:]) if i == num_packets - 1 else
            (str(i+1) + '\r\n' + raw_data[i * segment_size:(i + 1) * segment_size]) for i in range(num_packets)]


def rcv_ack(next_packet_num, senderSocket: LoRa, timeout, last_ack_num):
    ack_num = last_ack_num
    start_time = time()
    while True:
        if (time() - start_time >= timeout) or (next_packet_num - 1 == ack_num):
            break
        message = senderSocket.read_msg()
        ack_num = message
    return ack_num
