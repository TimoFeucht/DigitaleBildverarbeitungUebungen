# example from OpenCV: https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
import cv2 as cv
import numpy as np
import argparse
def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        #frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        pt1 = (x + w//2, y - 100)
        pt2 = (x, y)
        pt3 = (x + w, y)
        hat_cnt = np.array([pt1,pt2,pt3])

        pt1 = (x + w//2, y + h + 50)
        pt2 = (x + 15, y + h - 30)
        pt3 = (x + w - 15, y + h - 30)
        beard_cnt = np.array([pt1,pt2,pt3])

        cv.drawContours(frame, [hat_cnt], 0, (0,0,255),-1)
        cv.drawContours(frame, [beard_cnt], 0, (255,255,255),-1)
        #frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
    cv.imshow('Capture - Face detection', frame)

parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

#-- 1. Load the cascades
#if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
#if not face_cascade.load('./Bildverarbeitung_2021/09_Objekterkennung/data/haarcascades/haarcascade_frontalface_alt.xml'):
if not face_cascade.load('./09_Objekterkennung/data/haarcascades/haarcascade_frontalface_alt.xml'):
    print('--(!)Error loading face cascade')
    exit(0)
#if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
#if not eyes_cascade.load('./Bildverarbeitung_2021/09_Objekterkennung/data/haarcascades/haarcascade_smile.xml'):
#if not eyes_cascade.load('./Bildverarbeitung_2021/09_Objekterkennung/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml'):
if not eyes_cascade.load('./09_Objekterkennung/data/haarcascades/haarcascade_eye.xml'):
    print('--(!)Error loading eyes cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break