import cv2
import math
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
from time import sleep
import time
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
detector = HandDetector(detectionCon=0.5)
Capkeys = [
    ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "~", "_", "+"],
    ["Q", "2", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":", '"', "Cl"],
    ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "Up", "Sc"],
]
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "`", "-", "="],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Cl"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Up", "Sc"],
]
finalText = ""
keyboard = Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 42), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 3)
    return img

class Button():
    def __init__(self, pos, text, size=[65, 65]):
        self.pos = pos
        self.size = size
        self.text = text    

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([80 * j + 150, 80 * i + 100], key))
lmList = []
bboxInfo = []
b = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    # hands = detector.findHands(img, draw=False)
    # lmList, bboxInfo = detector.findDistance(img)
    if hands:
        #hand1
        hand1 = hands[0]
        lmList = hand1["lmList"]
        bboxInfo = hand1["bbox"]
    img = drawAll(img, buttonList)
    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 200), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 42), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                x1, y1 = (lmList[8][0], lmList[8][1])
                x2, y2 = (lmList[12][0], lmList[12][1])
                l = math.hypot(x2 - x1, y2 - y1)
                cv2.circle(img, (lmList[8][0], lmList[8][1]), 10, (255, 255, 0), cv2.FILLED)
                if l < 40:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10, y + 42), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                    if len(button.text) == 1:
                        keyboard.press(button.text)
                        finalText += button.text
                    elif button.text == "Sc":
                        finalText = finalText + " "
                    elif button.text == "Cl":
                        finalText = finalText[:-1] 
                    elif button.text == "Up":
                        b = not b
                        if b:
                            buttonList = []
                            for i in range(len(Capkeys)):
                                for j, key in enumerate(Capkeys[i]):
                                    buttonList.append(Button([80 * j + 150, 80 * i + 100], key))
                        else :
                            buttonList = []
                            for i in range(len(keys)):
                                for j, key in enumerate(keys[i]):
                                    buttonList.append(Button([80 * j + 150, 80 * i + 100], key))     
                    sleep(0.3)

    cv2.rectangle(img, (150, 500), (1135, 600), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, finalText, (170, 580), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    cv2.imshow('Image', img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()