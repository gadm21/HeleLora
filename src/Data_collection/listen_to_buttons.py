
from helpers import * 



while True:
    time.sleep(0.1)
    button_state = 'rest' 

    if GPIO.input(gpio_pin_button) == False: # Listen for the press, the loop until it steps
        pressed_time=time.time()
        while GPIO.input(gpio_pin_button) == False:
            time.sleep(0.1)
        pressed_time=time.time()-pressed_time

        if pressed_time < longpress_threshold:
            button_state = 'pressed' 
        else:
            button_state = 'longpressed'
    
    print("button_state:", button_state) 
    respond_to_button(button_state)

