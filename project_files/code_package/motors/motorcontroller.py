import RPi.GPIO as io
import time
from time import sleep


class Motorcontroller(object):
    # ENA, ENB, IN1, IN2, IN3, IN4
    def __init__(self, m_pins):
        self.m_pins = m_pins

        # GPIO Layout BCM / BOARD
        io.setmode(io.BCM)
        
        # Set all pins as OUTPUT and off
        for i in range(6):
            io.setup( self.m_pins[i], io.OUT )
            io.output( self.m_pins[i], 0 )

        # Setup enable pins as PWM pins
        self.motor_l = io.PWM(m_pins[0], 500)
        self.motor_r = io.PWM(m_pins[1], 500)
        self.motor_l.start(0)
        self.motor_r.start(0)


    def set_speed(self, left, right):
        self.left = left
        self.right = right
        if self.left >= 0:
            self.left = self.constrain(self.left, 0, 100)
            io.output(self.m_pins[2], 1)
            io.output(self.m_pins[3], 0)
            self.motor_l.ChangeDutyCycle(self.left)
        else:
            self.left = self.constrain(left, -100, 0)
            io.output(self.m_pins[2], 0)
            io.output(self.m_pins[3], 1)
            self.motor_l.ChangeDutyCycle(abs(self.left))
        if self.right >= 0:
            self.right = self.constrain(self.right, 0, 100)
            io.output(self.m_pins[4], 1)
            io.output(self.m_pins[5], 0)
            self.motor_r.ChangeDutyCycle(self.right)
        else:
            self.right = self.constrain(right, -100, 0)
            io.output(self.m_pins[4], 0)
            io.output(self.m_pins[5], 1)
            self.motor_r.ChangeDutyCycle(abs(self.right))


    def set_freq(self, freq):
        self.freq = freq
        self.motor_l.ChangeFrequency(self.freq)
        self.motor_r.ChangeFrequency(self.freq)


    def startup_sound(self):
        self.set_freq(500)
        self.set_speed(5,5)
        sleep(0.05)
        self.set_speed(0,0)
        sleep(0.1)
        self.set_speed(5,5)
        sleep(0.1)
        self.set_speed(0,0)
        sleep(0.1)
        self.set_freq(800)
        self.set_speed(5,5)
        sleep(0.5)
        self.set_speed(0,0)
        self.set_freq(500)


    def constrain(self, val, min_val, max_val):
        self.val = val
        self.min_val = min_val
        self.max_val = max_val
        return min(self.max_val, max(self.min_val, self.val) )


    def __exit__(self):
        io.cleanup()


    def close(self):
        io.cleanup()
