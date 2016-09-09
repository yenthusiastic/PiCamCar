import smbus
import time
from time import sleep

class SRF02(object):

    def __init__(self, i2c_address = 0x70):
        self.i2c = smbus.SMBus(1)
        self.addr = i2c_address

    def get_distance(self):
        self.i2c.write_byte_data(self.addr, 0, 81)
        time.sleep(0.08)    # sleep for 80ms
        self.dist = round(self.i2c.read_word_data(self.addr, 2) / 255)
        return self.dist

    def __exit__(self):
        pass


    def close(self):
        pass
