

import RPi.GPIO as GPIO
import threading
import ctypes
import time 


url = 'http://nightlight/' # I map this to my internal DNS hosting the node app
gpio_pin_button=8 # The GPIO pin the button is attached to
gpio_pin_led=20 # the GPIO pin the led is attached to
longpress_threshold=4 # If button is held this length of time, tells system to leave light on
waiting_time_thershold = 7 # wait for this time (seconds) between starting the service and triggering the script

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 

GPIO.setup(gpio_pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pin_led, GPIO.OUT) 

service_started = False 
service_started_at = None # timestamp of when the service started, if its working. None otherwise
label = -1 

botton_state = 'rest' # can be 'rest', 'pressed', 'longpressed'

def start_service(): 
    global service_started, service_started_at, label
    service_started = True 
    service_started_at = time.time() 
    label = 0

def stop_service() : 
    global service_started, service_started_at, label
    service_started = False 
    service_started_at = None 
    label -1 


def respond_to_button(button_state):
    global service_started, service_started_at, label
    
    if button_state == 'rest' and service_started:
        waiting_time = time.time() - service_started_at 
        if waiting_time > waiting_time_thershold : 
            print("label: ", label) 
    if button_state == 'pressed' and service_started : 
        label += 1
    if button_state == 'longpressed' : 
        if service_started : 
            stop_service() 
        else : 
            start_service()




class MyThread(threading.Thread):
    """this thread inherets Threads and adds the functionality that it can be terminated
    """
    def __init__(self, name, target_func):
        threading.Thread.__init__(self)
        self.name = name
        self.target = target_func
        self.daemon = True
             
    def run(self):
 
        # target function of the thread class
        try:
            self.target()
        finally:
            print('ended')
          
    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def terminate(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


