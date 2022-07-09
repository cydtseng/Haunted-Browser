import cv2
import numpy as np
from numpy import size
from face_rec import FaceRec
import cvzone

#load camera
capture = cv2.VideoCapture(1)
#Encode faces from folder
sfr = FaceRec()

class Video(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1)
        sfr.load_img_for_encoding('img/')
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()
        face_locations, face_names = sfr.detect_known_faces(frame)
        hb, wb, cb = frame.shape
        
        scare_img = cv2.imread('./ghost.webp')
        scare_img_size = (wb, hb)
        scare_img = cv2.resize(scare_img, scare_img_size)
        scare_grey =cv2.cvtColor(scare_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(scare_grey, 1 ,255, cv2.THRESH_BINARY)

        for face_location, name in zip(face_locations, face_names):
            y1,x2,y2,x1 = face_location[0], face_location[1], face_location[2], face_location[3]

            if name == 'Unknown':
                roi = frame[0:hb, 0:wb]
                roi[np.where(mask)] = 0
                roi += scare_img
                
            else :
                cv2.putText(frame, name, (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0,200,0),1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,200,0),2)
        

        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()

