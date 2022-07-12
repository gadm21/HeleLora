#!/usr/bin/python
import wiringpi
import time
import subprocess
import threading

from connect_and_collect import connect, start_data_pull

# initialize
wiringpi.wiringPiSetup()

# define GPIO mode
led_pin = 4
button_pin = 5
LOW = 0
HIGH = 1
OUTPUT = 1
INPUT = 0
PULL_DOWN = 1



wiringpi.pinMode(led_pin, OUTPUT)  # LED
wiringpi.pinMode(button_pin, INPUT)  # push button
wiringpi.pullUpDnControl(button_pin, PULL_DOWN)  # pull down


program_state = 'idle' # Either 'idle' (not long pressed), 'listening' (counting short pressed after a long press), 'collecting' (started collecting data)
button_state = 'pressed' # Either 'not_pressed', 'pressed', 'long_pressed'
long_pressed = False 
presses_counter = 0
last_long_press_at = 0 
last_short_press_at = 0 
long_press_threshold = 3
waiting_between_short_presses = 5

file_path = '/home/pi/Desktop/Data/test.txt'



def is_on(pin): 
    return wiringpi.digitalRead(pin) 

def is_long_pressed(pin, long_press_threshold) : 
    t1 = time.time() 
    while is_on(pin): 
        if time.time() - t1 > long_press_threshold :
            return True 
    return False 

def turn_on(pin): 
    wiringpi.digitalWrite(pin, True) 

def turn_off(pin): 
    wiringpi.digitalWrite(pin, False) 

def change_state(pin): 
    state = is_on(pin) 
    wiringpi.digitalWrite(pin, not state)  

# make all LEDs off
def clear_all():
    print("clear all") 
    wiringpi.digitalWrite(led_pin, LOW)







def blnk(pin, in_between_delay = 1000, iterations = 10):
    for _ in range(iterations):
        turn_off(pin)
        wiringpi.delay(in_between_delay)
        turn_on(pin)
        wiringpi.delay(in_between_delay)
    turn_off(pin)

def turn_on_for(pin, milliseconds) :
    turn_on(pin)
    wiringpi.delay(milliseconds)
    turn_off(pin) 


def start() :
    print("START")
    global last_long_press_at, program_state, last_short_press_at, presses_counter, stop_flag
    stop_flag = False
    last_long_press_at = time.time()
    last_short_press_at = 0
    presses_counter = 0
    program_state = 'listening'
    turn_on_for(led_pin, 4000) 

def end() :
    print("END")
    global last_long_press_at, program_state, last_short_press_at, presses_counter
    presses_counter = 0
    last_long_press_at = time.time()
    program_state = 'idle'
    last_short_press_at = 0
    turn_on_for(led_pin, 4000) 


def collect_data() :
    global program_state, presses_counter, stop_flag
    program_state = 'collecting' 
    print("collecting data")
    blnk(led_pin, in_between_delay = 500, iterations = presses_counter)
    wiringpi.delay(3000)
    while not is_long_pressed(button_pin, long_press_threshold) :
        blnk(led_pin, in_between_delay = 300, iterations = 3)
    stop_flag = True
    end()
    

def handle_states (prog_state, button_state) : 
    global last_long_press_at, last_short_press_at, presses_counter
    
    if prog_state == 'idle': 
        if button_state == 'long_pressed': 
            start()
            
    elif prog_state == 'listening': 
        if button_state == 'long_pressed' and presses_counter > 0: 
            end()
        elif button_state == 'pressed':
            print("pressed") 
            turn_on_for(led_pin, 1000) 
            presses_counter += 1
            last_short_press_at = time.time()
        else :
            
	    if presses_counter > 0 and last_short_press_at > 0 and time.time() - last_short_press_at > waiting_between_short_presses :
	    	delay = presses_counter - 1
       	    	fake_filename = 'z'+str(delay)+'z'+str(time.time())+'z'
	    	with open(file_path) as f : 
	    		for line in f : 
				lora.send_msg(receiver_addr, fake_filename+','line.strip('\r\n'))
				turn_on(led_pin)
				time.sleep(delay)
				turn_off(led_pin)
	    	end() 

    
    elif prog_state == 'collecting': 
        if button_state == 'long_pressed': 
            end()

    # print("program_state: {}, button_state:{}".format(prog_state, button_state))
    





try:
    clear_all()
    while True : 
        button_state = 'not_pressed'
        if is_on(button_pin) :
            button_state = 'pressed'
            if is_long_pressed(button_pin, long_press_threshold) :
                button_state = 'long_pressed'

        handle_states(program_state, button_state)
        wiringpi.delay(250)

except KeyboardInterrupt:
    clear_all()

print("done")



