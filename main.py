import cv2
import sys
import logging as log
import datetime as dt


log.basicConfig(filename='webcam.log', level=log.INFO)
video_capture = cv2.VideoCapture(0)

anterior = 0

def get_faces(frame):
    faceCascPath = 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(faceCascPath)
    frame_width = video_capture.get(3)
    frame_height = video_capture.get(4)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(0.03 * frame_width), int(0.03 * frame_height)))
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

while True:
    ret, frame = video_capture.read()
    faces = get_faces(frame)
    biggest_face = get_biggest_face(faces)
    draw_faces(biggest_face, faces, frame)
    print(biggest_face)
    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))

    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()