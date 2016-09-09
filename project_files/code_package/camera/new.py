from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from random import randint
import time
import cv2
from motorcontroller import Motorcontroller
from sr04 import SR04


m = Motorcontroller([17, 18, 27, 22, 23, 24])

s = SR04(5, 6)

face_detected = False
run_cam = True
data = ()

run = True
resolution = (320,240)
framerate = 5
target_ratio = 0.05

cam = PiCamera()
cam.resolution = resolution
cam.framerate = framerate

sleep(0.1)

"""
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
                print("x: {}, ratio: {}".format(x_position, ratio))
                return (x_position, ratio)
 
 
    else:
        num_face = 0
        print("number of faces: {}". format(num_face))
        return num_face
"""

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
                print("x: {}, ratio: {}".format(x_position, ratio))
                return (x_position, ratio)


    else:
        num_face = None
        return num_face
    

def camera():
    global run_cam
    global face_detected
    global data
    global cam
    global resolution
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
            cv2.imshow('Video', gray)
            #print(biggest_face)
            key = cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)
            if key == ord("q"):
                run_cam = False
                cam.close()
                cv2.destroyAllWindows()
                break
    cv2.destroyAllWindows()
    


t = Thread(target=camera, args=())
t.start()


m.startup_sound()

while run:
    if face_detected:
        print (data)
    else:
        ("no face")
        """
        dist = s.get_distance()
        if dist > 30:           # no obstruction
            m.set_speed(30, 30)
        else:                   # obstruction
            while s.get_distance() < 30:
                rand = randint(0,20)  
                m.set_speed(-rand, rand)
                sleep(0.2)
        """ 
            
    """
    for fr in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = fr.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        get_biggest_faces(gray)
        # Display the resulting frame
        cv2.imshow('Video', gray)
        #print(biggest_face)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            run = False
            cam.close()
            break
    """
    
m.close()
s.close()

