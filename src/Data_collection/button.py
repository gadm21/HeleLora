from more_itertools import last
import wiringpi
import time

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

program_state = 'idle' # Either 'idle' (not long pressed), 'listening' (counting short pressed after a long press), 'collecting' (started collecting data)
button_state = 'pressed' # Either 'not_pressed', 'pressed', 'long_pressed' 
long_pressed = False 
presses_counter = 0
last_long_press_at = 0 
last_short_press_at = 0 
long_press_threshold = 3
waiting_between_short_presses = 2

wiringpi.pinMode(led_pin, OUTPUT)  # LED
wiringpi.pinMode(button_pin, INPUT)  # push button
wiringpi.pullUpDnControl(button_pin, PULL_DOWN)  # pull down


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

def turn_on(pin): 
    wiringpi.digitalWrite(pin, False) 

def change_state(pin): 
    state = is_on(pin) 
    wiringpi.digitalWrite(pin, not state)  

# make all LEDs off
def clear_all():
    wiringpi.digitalWrite(led_pin, LOW)










def start() : 
    global last_long_press_at
    last_long_press_at = time.time()

def end() : 
    global last_long_press_at
    last_long_press_at = time.time()


def handle_states (prog_state, button_state) : 
    global last_long_press_at, presses_counter

    if prog_state == 'idle': 
        if button_state == 'long_press': 
            start() 
    elif prog_state == 'listening': 
        if button_state == 'long_pressed': 
            end()
        elif button_state == 'pressed': 
            pressed_counter += 1
        else : 
            if time.time() - last_long_press_at > waiting_between_short_presses :
                print("running script label:", pressed_counter)  
    
    elif prog_state == 'collecting': 
        if button_state == 'long_pressed': 
            end() 

    print("program_state: {}, button_state:{}".format(prog_state, button_state))





try:
    clear_all()
    while True : 
        button_state = 'not_pressed'
        if is_on(button_pin) :
            button_state = 'pressed'
            wiringpi.delay(30) 
            if is_long_pressed(button_pin, long_press_threshold) :
                button_state = 'long_pressed'
                wiringpi.delay(50) 

        handle_states(program_state, button_state) 
        wiringpi.delay(200)

except KeyboardInterrupt:
    clear_all()

print("done")
 