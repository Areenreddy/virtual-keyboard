import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Key, Controller

cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)

# def drawall(img,buttonlist):
#     for button in buttonlist:
#         x,y = button.pos
#         w,h = button.size
#         cv.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv.FILLED)
#         cv.putText(img,button.text,(x+20,y+65),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
#     return img


def drawall(img, buttonlist):
    for button in buttonlist:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),20, rt=0)
        cv.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv.FILLED)
        cv.putText(img, button.text, (x + 20, y + 65),cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

class button():
    def __init__(self,pos,text,size=(85,85)):
        self.pos =pos
        self.size = size
        self.text = text
        
buttonlist=[]
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", " "],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "bac"]]

finaltext = ""
keyboard = Controller()

for i,k in enumerate(keys):
        for j,key in enumerate(k):
            buttonlist.append(button((100*j+50,100*i+50),key))

xmin, ymin, boxW, boxH =0,0,0,0
while True:
    sucess,img = cap.read()
    img=cv.resize(img,(1280,720))
    img = cv.flip(img,1)
    lmlist,img = detector.findHands(img)
    if lmlist:
        lmlist=lmlist[0]
        xmin, ymin, boxW, boxH = lmlist['bbox']
        lmlist=lmlist["lmList"]
        

    img = drawall(img,buttonlist)

    if lmlist:
        for buttons in buttonlist:
            x,y =buttons.pos
            w,h = buttons.size
            if x<lmlist[8][0]<x+w and y<lmlist[8][1]<y+h :
                cv.rectangle(img,buttons.pos,(x+w,y+h),(175,0,175),cv.FILLED)
                cv.putText(img,buttons.text,(x+20,y+65),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                l,_= detector.findDistance((lmlist[8][0],lmlist[8][1]),(lmlist[12][0],lmlist[12][1]))

                if l<50:
                    if buttons.text == "bac":
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                    else:
                        keyboard.press(buttons.text)
                    cv.rectangle(img,buttons.pos,(x+w,y+h),(0,255,0),cv.FILLED)
                    cv.putText(img,buttons.text,(x+20,y+65),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    if buttons.text == "bac":
                        finaltext = finaltext[:-1]
                    else:
                        finaltext += buttons.text
                    
                    sleep(0.3)

    cv.rectangle(img,(50,350),(700,450),(175,0,175),cv.FILLED)
    cv.putText(img,finaltext,(60,425),cv.FONT_HERSHEY_COMPLEX,3,(255,255,255),2)



    cv.imshow('video',img)
    if cv.waitKey(1)& 0xFF==ord('d'):
        break

cv.destroyAllWindows()