import serial
import time
class LoRa:
    def __init__(self):
        self.serial = serial.Serial(
            port = '/dev/ttyAMA0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )            
        self.parameters = {'SF': 12, 'BW': 7, 'CR': 1, 'PP': 4}
        
    def cmd(self, lora_cmd):
        self.serial.write(('{}\r\n'.format(lora_cmd)).encode())
        return self.serial.readline().decode()
        
    
    def test(self):
        self.cmd('AT')

    def set_addr(self, addr):
        self.cmd('AT+ADDRESS={}'.format(addr))
        return self.cmd('AT+ADDRESS?')

    def set_param(self, parameter, value): 
        assert parameter in self.parameters.keys() # Spreading Factor, Bandwidth, Coding Rate, Programmed Preamble
        if self.parameters[parameter] == value : 
            return 
        self.parameters[parameter] = value
        command = 'AT+PARAMETER=' + ','.join(self.parameters.values())
        self.cmd(command) 
    
    def send_msg(self, addr, msg):
        return self.cmd('AT+SEND={},{},{}'.format(addr,len(msg),msg))

    def read_msg(self):
        msg = self.serial.readline().decode() 
        read_timestamp = int(time.time()) 
        if msg.startswith("+RCV="):
            rcv = msg.removeprefix("+RCV=").strip('\r\n').split(",")
            received_dict = {'sender': rcv[0], 'length': rcv[1], 'data': self._decode_data(rcv[2], read_timestamp),  'rssi': rcv[-2], 'snr': rcv[-1]}
            return received_dict
        else : 
            print("received strange msg:{}".format(msg))

    def _decode_data(self, msg, read_timestamp): 
        data = msg.split('_') 
        return [data[0], int(data[1]), int(data[2]), int(data[3]), read_timestamp - int(data[4]), int(data[5])] # file_id, line_id (int), total number of lines (int), SF (int), time to read (int), delay (int)



    def sample_message(self, file_id, line_id, num_lines, delay, SF):

        self.set_param('SF', SF)  
        return '{}_{}_{}_{}_{}_{}'\
            .format(file_id.zfill(4), line_id.zfill(3), num_lines.zfill(3), self.parameters['SF'].zfill(2), str(int(time.time())), delay.zfill(2))
    
    def sample_file(self, num_lines, SF = None): 
        return [self.sample_message(i, SF) for i in range(num_lines)]