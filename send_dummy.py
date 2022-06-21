import LoRa
import time
lora = LoRa.LoRa() # Initialize serial instance
#time.sleep(3)
lora.set_addr(1)  # Sets the LoRa address
receiver_addr = 2
for i in range(5):
	print("Sending Hello{} to receiver with address {}".format(i, receiver_addr))
	lora.send_msg(receiver_addr,'Hello{} from device 1'.format(i))
	time.sleep(1)
