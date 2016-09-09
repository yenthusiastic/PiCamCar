from srf02 import SRF02
from time import sleep

s = SRF02(0x70)
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
