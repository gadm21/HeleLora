
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
long_press_threshold = 2
waiting_between_short_presses = 5

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

def turn_off(pin): 
    wiringpi.digitalWrite(pin, False) 

def change_state(pin): 
    state = is_on(pin) 
    wiringpi.digitalWrite(pin, not state)  

# make all LEDs off
def clear_all():
    wiringpi.digitalWrite(led_pin, LOW)







def blnk():
    turn_off(led_pin) 
    for i in range(4):
        turn_on(led_pin)
        wiringpi.delay(200)
        turn_off(led_pin)
        wiringpi.delay(200)

def start() : 
    global last_long_press_at, program_state
    last_long_press_at = time.time()
    program_state = 'listening'
    blnk() 

def end() : 
    global last_long_press_at, program_state
    last_long_press_at = time.time()
    program_state = 'idle'
    blnk()


def handle_states (prog_state, button_state) : 
    global last_long_press_at, last_short_press_at, presses_counter

    if prog_state == 'idle': 
        if button_state == 'long_pressed': 
            start()
            wiringpi.delay(500)
            
    elif prog_state == 'listening': 
        if button_state == 'long_pressed': 
            end()
        elif button_state == 'pressed':
            change_state(led_pin) 
            presses_counter += 1
            last_short_press_at = time.time()
        else :
            
            if last_short_press_at > 0 and time.time() - last_short_press_at > waiting_between_short_presses :
                print("running script label:", presses_counter)  
    
    elif prog_state == 'collecting': 
        if button_state == 'long_pressed': 
            end()
            wiringpi.delay(500)

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
        print("program state:{} button state:{} presses:{}".format(program_state, button_state, presses_counter) ) 
        wiringpi.delay(200)

except KeyboardInterrupt:
    clear_all()

print("done")

