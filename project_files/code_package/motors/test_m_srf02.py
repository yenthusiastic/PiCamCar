import sys
sys.path.append('sensors')
sys.path.append('motors')
sys.path.append('sound')
sys.path.append('camera')
from srf02 import SRF02
from motorcontroller import Motorcontroller
from time import sleep
import time
from random import randint
from os import system
from threading import Thread


m = Motorcontroller([17, 18, 27, 22, 23, 24])
s = SRF02(0x70)

play_file = ""
play = False
run_cam = True


def play_sound(volume=80):
    global play_file
    global play
    global run_cam
    while run_cam:
        if play:
            #print("Playing: {}".format(play_file))
            system('aplay sound/sound-files/' + str(play_file))
            play = False
        else:
            sleep(0.1)
    print("Thread  play-sound  terminated.")


try:
    m.startup_sound()
    print("{} {}".format(play_file, play))
    pt = Thread(target=play_sound, args=() )
    pt.start()
    s_time = time.time()
    t = time.time() - s_time
    c_obstr = 0
    c_freeway = 0
    clear_way = True
    while True:
        dist = 0
        for i in range(4):
            dist += s.get_distance()
        dist = round(dist / 4)
        print("Distance: {}cm  {}{}".format(dist, play_file,play))
        if dist > 60 or dist == 1:           # no obstruction
            print("Drive  {}".format(c_freeway))
            if not clear_way:
                play_file = 'clear.wav'
                play = True
                clear_way = True
            m.set_speed(25, 25)
        else:                   # obstruction
            print("Obstruction  {}".format(c_obstr))
            if clear_way:
                play_file = 'stand_out.wav'
                play = True
                clear_way = False
            rand = randint(40,60)  
            m.set_speed(- rand, rand)
        #sleep(0.1)
        t = time.time() - s_time
    s.close()
    m.close()
    run_cam = False
    pt.join()
        
except KeyboardInterrupt:
    run_cam = False
    pt.join()
    s.close()
    m.close()




