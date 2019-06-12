import cv2

import PIL

import pytesseract

import RPi.GPIO as GPIO

import time

import os

 

 

LED = 23

Button = 18

 

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)   

GPIO.setup(Button, GPIO.IN)

 

GPIO.setup(10,GPIO.OUT)

GPIO.setup(9,GPIO.OUT)

GPIO.setup(11,GPIO.OUT)

GPIO.setup(5,GPIO.OUT)

GPIO.setup(6,GPIO.OUT)

GPIO.setup(13,GPIO.OUT)

 

GPIO.output(10,0)

GPIO.output(9,0)

GPIO.output(11,0)

GPIO.output(5,0)

GPIO.output(6,0)

GPIO.output(13,0)

 

def PORT(pin)

    GPIO.output(pin,1)

 

def removeAllFile(filePath)

    if os.path.exists(filePath)

        for file in os.scandir(filePath)

            os.remove(file.path)

 

 

try

        while True

                if GPIO.input(Button)==0

                        GPIO.output(LED, True)                        

                        img_path = r'mediapiSD_VOLDCIM100MEDIAIMAG0001.JPG'

                        img = cv2.imread(img_path,cv2.IMREAD_COLOR)

                        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                        img2 = PIL.Image.fromarray(img2)

                        txt = pytesseract.image_to_string(img2)

                        print(txt)

                        

                        from gtts import gTTS

 

                        tts = gTTS(text = txt , lang = 'en')

                        tts.save(speech.mp3)

 

                        from pygame import mixer

 

                        mixer.init()

                        mixer.music.load(r'homepispeech.mp3')

                        mixer.music.play()

                        

                        

                        txtlower = txt.lower()

                        TXT = ','.join(txtlower)

                        arr = TXT.split(',')

 

 

 

                        i=0

                        count = len(txt)

 

                        

 

                        for i in range(0,count)   

                           seg=arr[i]

                           if seg == 'a'

                              PORT(9)

                              PORT(11)

                              PORT(5)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'b'

                              PORT(9)

                              PORT(5)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'c'

                              PORT(11)

                              PORT(5)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'd'

                              PORT(11)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'e'

                              PORT(9)

                              PORT(11)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'f'

                              PORT(5)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'g'

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'h'

                              PORT(9)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'i'

                              PORT(10)

                              PORT(5)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'j'

                              PORT(10)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'k'

                              PORT(9)

                              PORT(11)

                              PORT(5)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'l'

                              PORT(9)

                              PORT(5)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'm'

                              PORT(11)

                              PORT(5)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'n'

                              PORT(11)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'o'

                              PORT(9)

                              PORT(11)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'p'

                              PORT(5)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'q'

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'r'

                              PORT(9)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 's'

                              PORT(10)

                              PORT(5)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 't'

                              PORT(10)

                              PORT(13)

                              time.sleep(1)

                        

                           elif seg == 'u'

                              PORT(9)

                              PORT(11)

                              PORT(5)

                              time.sleep(1)

                        

                           elif seg == 'v'

                              PORT(9)

                              PORT(5)

                              time.sleep(1)

                        

                           elif seg == 'w'

                              PORT(10)

                              PORT(6)

                              time.sleep(1)

                        

                           elif seg == 'x'

                              PORT(11)

                              PORT(5)                      

                              time.sleep(1)

                        

                           elif seg == 'y'

                              PORT(11)

                              time.sleep(1)

                        

                           elif seg == 'z'

                              PORT(9)

                              PORT(11)

                              time.sleep(1)

                        

                           elif seg == ' '

                              PORT(10)

                              PORT(9)

                              PORT(11)

                              PORT(5)

                              PORT(6)

                              PORT(13)

                              time.sleep(1)

                        

                           GPIO.output(10,0)

                           GPIO.output(9,0)

                           GPIO.output(11,0)

                           GPIO.output(5,0)

                           GPIO.output(6,0)

                           GPIO.output(13,0)

 

                           removeAllFile(r'mediapiSD_VOLDCIM100MEDIA')

 

 

 

 

 

                        

                        

                else

                        GPIO.output(LED, False)                        

                

except KeyboardInterrupt     

        GPIO.cleanup()
