import RPi.GPIO as io
import time
from time import sleep

class SR04(object):


    def __init__(self, t_pin, e_pin):
        self.t_pin = t_pin
        self.e_pin = e_pin

        self.start_time = time.time()
        self.stop_time = time.time()
        
        # GPIO Layout BCM / BOARD
        io.setmode(io.BCM)

        #io.remove_event_detect(self.e_pin)
        
        io.setup( self.t_pin, io.OUT )
        io.output( self.t_pin, 0 )
        io.setup( self.e_pin, io.IN )
    

    def get_distance(self):
        io.output(self.t_pin, 1)
        sleep(0.00001)
        io.output(self.t_pin, 0)
        while io.input(self.e_pin) == 0:
            self.start_time = time.time()
        while io.input(self.e_pin):
            self.stop_time = time.time()
        self.dist = round((self.stop_time - self.start_time) * 17150)
        return self.dist

    def __exit__(self):
        io.cleanup()


    def close(self):
        io.cleanup()
