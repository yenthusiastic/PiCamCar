import RPi.GPIO as io
from test_class import *
import time
from time import sleep as sleep


init_motors(17, 18, 27, 22, 23, 24) 


startup_sound()
set_speed(15,15)
sleep(2)
set_speed(0,0)
