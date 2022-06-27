import wiringpi
import time 

# initialize
wiringpi.wiringPiSetup()

# define GPIO mode
button_pin = 4
led_pin = 5
LOW = 0
HIGH = 1
OUTPUT = 1
INPUT = 0
PULL_DOWN = 1
wiringpi.pinMode(button_pin, OUTPUT)  # LED
wiringpi.pinMode(led_pin, INPUT)  # push button
wiringpi.pullUpDnControl(led_pin, PULL_DOWN)  # pull down


# make all LEDs off
def clear_all():
    wiringpi.digitalWrite(button_pin, LOW)

def get_state(pin): 
    return wiringpi.digitalRead(pin) 

def long_pressed(pin, long_press_threshold = 3) : 
    t1 = time.time() 
    while get_state(pin) == True : 
        if time.time() - t1 > long_press_threshold : 
            return True 
    return False 

def turn_on(pin): 
    wiringpi.digitalWrite(pin, True) 

def turn_on(pin): 
    wiringpi.digitalWrite(pin, False) 

def change_state(pin): 
    state = get_state(pin) 
    wiringpi.digitalWrite(pin, not state)  


try:
    clear_all()
    while True : 
        if get_state(button_pin) == True: 
            if long_pressed(button_pin) : 
                change_state(led_pin) 

        wiringpi.delay(10)

except KeyboardInterrupt:
    clear_all()

print("done")
