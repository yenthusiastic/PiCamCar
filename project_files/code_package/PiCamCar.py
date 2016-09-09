import sys
sys.path.append('sensors')
sys.path.append('motors')
sys.path.append('sound')
sys.path.append('camera')

from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from random import randint
from threading import Thread
from os import system
import time
from time import sleep
import cv2
from motorcontroller import Motorcontroller
from srf02 import SRF02
 


m = Motorcontroller([17, 18, 27, 22, 23, 24])

s = SRF02(0x70)

face_detected = False
run_cam = True
data = ()

play_file = ""
play = False

run = True
resolution = (320,240)
framerate = 5
target_ratio = 0.05

sleep(0.1)



def get_biggest_faces(gray, draw=False):
    faceCascPath = 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(faceCascPath)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(0.03 * resolution[0]), int(0.03 * resolution[1])))
    biggest_face = [0, 0]
    if len(faces) is not 0:
        for i in [0, len(faces) - 1]:
            face_size = faces[i][2] * faces[i][3]
            if face_size > biggest_face[1]:
                biggest_face = [i, face_size]
        for index, (x, y, w, h) in enumerate(faces):
            if index == biggest_face[0]:
                if draw is True:
                    cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
                ratio = float(h/resolution[0])
                x_position = x
                #print("x: {}, ratio: {}".format(x_position, ratio))
                return (x_position, ratio)


    else:
        num_face = None
        return num_face
    

def camera(show=False):
    global run_cam
    global face_detected
    global data
    global framerate
    global resolution
    cam = PiCamera()
    cam.resolution = resolution
    cam.framerate = framerate
    rawCapture = PiRGBArray(cam, size=resolution)
    
    while run_cam:
        for fr in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame = fr.array
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            response = get_biggest_faces(gray)
            if response is not None:
                if response[1] > target_ratio:
                    face_detected = True
                    data = response
            else:
                face_detected = False
            
            # Display the resulting frame
            if show:
                cv2.imshow('Video', gray)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cam.close()
                    cv2.destroyAllWindows()
                    run_cam = False
                    break
            rawCapture.truncate(0)


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
    t = Thread(target=camera, args=())
    t.start()
    c_obstr = 0
    c_freeway = 0
    clear_way = True
    while run:

        # check for face in camera picture
        if face_detected:
            if data[1] < 0.15:
                print('face detected: far')
                m.set_speed(30,30)
                play_file='i_see_u_me.wav'
                play = True 
            else:
                print('face detected: near')
                m.set_speed(0,0)
                play_file = 'welcome_google.wav'
                play = True
            # stop at ratio x
            #print (data)
        else:
            print("no face")

        # no face, therefore drive by sensor
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

    s.close()
    m.close()
    run_cam = False
    pt.join()
    t.join()
        
except KeyboardInterrupt:
    run_cam = False
    run = False
    pt.join()
    t.join()
    s.close()
    m.close()
    print('Programm completed, bye!')


