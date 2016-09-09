from sr04 import SR04
from time import sleep

s = SR04(5, 6)
try:
   while True:
      dist = 0
      for i in range(4):
         dist += s.get_distance()
      dist /= 4
      print("Distance: {}cm".format(dist))
      #sleep(0.1)
        
except KeyboardInterrupt:
    s.close()
