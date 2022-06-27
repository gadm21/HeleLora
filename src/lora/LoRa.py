import serial
import time
class LoRa:
    def __init__(self):
        self.serial = serial.Serial(
            port = '/dev/ttyS0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )            
    
    def cmd(self, lora_cmd):
        self.serial.write(('{}\r\n'.format(lora_cmd)).encode())
        time.sleep(1)
        reply = self.serial.read(self.serial.in_waiting)
        print(reply)
    def test(self):
        self.cmd('AT')

    def set_addr(self, addr):
        self.cmd('AT+ADDRESS={}'.format(addr))
        self.cmd('AT+ADDRESS?')


    def send_msg(self, addr, msg):
        self.cmd('AT+SEND={},{},{}'.format(addr,len(msg),msg))

    def read_msg(self):
        msg = self.serial.read(self.serial.in_waiting)
        if msg!=b'':
            print(msg)
