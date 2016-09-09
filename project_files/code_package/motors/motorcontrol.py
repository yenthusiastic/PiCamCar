import RPi.GPIO as io
import time
from time import sleep as sleep

# GPIO Layout BCM / BOARD
io.setmode(io.BCM)
#io.pwmSetMode(PWM_MODE_MS)

# motor_pins  ENA ENB IN1 IN2 IN3 IN4 
motor_pins = [17, 18, 27, 22, 23, 24] 


#Set all pins as OUTPUT
for i in range(6):
    io.setup( motor_pins[i], io.OUT )
    io.output( motor_pins[i], 0 )


speed_left = io.PWM(motor_pins[0], 500)
speed_right = io.PWM(motor_pins[1], 500)
speed_left.start(0)
speed_right.start(0)


def set_speed(left, right):
    io.output(motor_pins[2], 1)
    io.output(motor_pins[4], 1)
    speed_left.ChangeDutyCycle(left)
    speed_right.ChangeDutyCycle(right)


def set_freq(freq):
    speed_left.ChangeFrequency(freq)
    speed_right.ChangeFrequency(freq)


def startup_sound():
    set_freq(500)
    set_speed(5,5)
    time.sleep(0.1)
    set_speed(0,0)
    time.sleep(0.1)
    set_speed(5,5)
    time.sleep(0.1)
    set_speed(0,0)
    set_freq(800)
    set_speed(5,5)
    time.sleep(0.5)
    set_speed(0,0)
    set_freq(500)


try:
    while True:
        startup_sound()
        sleep(1)
        set_speed(20,20)
        time.sleep(2)
        set_speed(0,0)
        time.sleep(1)
        set_speed(50,50)
        time.sleep(2)
        set_speed(0,0)
        time.sleep(2)
        
except KeyboardInterrupt:
    io.cleanup()


io.cleanup()
