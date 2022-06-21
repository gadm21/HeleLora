import LoRa

lora = LoRa.LoRa() # Initialize serial instance
#time.sleep(3)
lora.set_addr(1)  # Sets the LoRa address
while 1:
	lora.read_msg()
