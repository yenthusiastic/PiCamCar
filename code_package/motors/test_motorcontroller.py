from motorcontroller import Motorcontroller
from time import sleep

m = Motorcontroller([17, 18, 27, 22, 23, 24])
m.startup_sound()
sleep(1)
m.set_speed(50,50)
sleep(2)
m.set_speed(-50,-50)
sleep(2)
m.close()
