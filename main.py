
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap = cv.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)

def drawAll(img,buttonlist):

    for button in buttonlist:
        x, y = button.pos
        w, h = button.size
        cv.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv.FILLED)
        cv.putText(img, button.txt, (x + 25, y + 60), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    return img

class Button():
    def __init__(self,pos,txt,size=[85,85]):
        self.pos=pos
        self.size = size
        self.txt=txt


buttonlist=[]
keys = [['Q','W','E','R','T','Y','U','I','O','P'],
        ['A','S','D','F','G','H','J','K','L','Ñ'],
        ['Z','X','C','V','B','N','M',',','.','-']]

final=""

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonlist.append(Button([100 * j + 50, 100 * i + 50], key))
        print(keys[i])

while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmlist,bbox = detector.findPosition(img)

    img = drawAll(img,buttonlist)

    if lmlist:
        for button in buttonlist:
            x,y = button.pos
            w,h = button.size

            if x<lmlist[8][0]< x+w and y<lmlist[8][1]<y+h:
                cv.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv.FILLED)
                cv.putText(img, button.txt, (x + 25, y + 60), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                l,_,_ = detector.findDistance(8,12,img,draw=False)
                print(l)
                if l<30:
                    cv.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv.FILLED)
                    cv.putText(img, button.txt, (x + 25, y + 60), cv.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 5)
                    final +=button.txt
                    sleep(0.3)


    cv.rectangle(img, (50,350), (700,450), (175, 0, 175), cv.FILLED)
    cv.putText(img, final, (60,425), cv.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv.imshow('img',img)
    cv.waitKey(1)