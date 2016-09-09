from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import time
import cv2

run = True
resolution = (320,240)
framerate = 5


cam = PiCamera()
cam.resolution = resolution
cam.framerate = framerate
rawCapture = PiRGBArray(cam, size=resolution)

sleep(0.1)


def get_faces(gray):
    faceCascPath = 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(faceCascPath)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(0.03 * resolution[0]), int(0.03 * resolution[1])))
    return faces

def get_biggest_face(faces):
    biggest_face = [0, 0]
    if len(faces) is not 0:
        for i in [0, len(faces) - 1]:
            face_size = faces[i][2] * faces[i][3]
            if face_size > biggest_face[1]:
                biggest_face = [i, face_size]
    return biggest_face

def draw_faces(biggest_face, faces, frame):
    for index, (x, y, w, h) in enumerate(faces):
        if index == biggest_face[0]:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


while run:
    for fr in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = fr.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = get_faces(gray)
        biggest_face = get_biggest_face(faces)
        draw_faces(biggest_face, faces, gray)
        # Display the resulting frame
        cv2.imshow('Video', gray)
        #print(biggest_face)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            run = False
            cam.close()
            break

cv2.destroyAllWindows()
