from sr04 import SR04
from time import sleep

s = SR04(5, 6)
try:
   while True:
        print("Distance: {}cm".format(s.get_distance()))
        sleep(0.1)
        
except KeyboardInterrupt:
    s.close()
