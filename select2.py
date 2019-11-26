# -*- coding: utf-8 -*-
import re
import sys
import cv2
import PIL
import pytesseract
import RPi.GPIO as GPIO
import time
import os


Button = 20			#동작 버튼
switch = 21			#한글/영어 스위치

#GPIO 사용 및 초기화
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Button, GPIO.IN)
GPIO.setup(switch, GPIO.IN)

GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

GPIO.output(2,0)
GPIO.output(3,0)
GPIO.output(4,0)
GPIO.output(14,0)
GPIO.output(15,0)
GPIO.output(18,0)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

GPIO.output(17,0)
GPIO.output(27,0)
GPIO.output(22,0)
GPIO.output(23,0)
GPIO.output(24,0)
GPIO.output(25,0)

GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)

GPIO.output(10,0)
GPIO.output(9,0)
GPIO.output(11,0)
GPIO.output(8,0)
GPIO.output(7,0)
GPIO.output(5,0)

GPIO.setup(6,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

GPIO.output(6,0)
GPIO.output(12,0)
GPIO.output(13,0)
GPIO.output(19,0)
GPIO.output(16,0)
GPIO.output(26,0)

#함수 선언
def PORT(pin):
    GPIO.output(pin,1)

# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

#함수 선언
def convert(txt):
    split_keyword_list = list(txt)
    #print(split_keyword_list)
    global result
    result = list()
    for keyword in split_keyword_list:
        # 한글 여부 check 후 분리
        if re.match('.*[ㄱ - ㅎ ㅏ - ㅣ 가 -힣]+.*', keyword) is not None:
            char_code = ord(keyword) - 44032
            char1 = int(char_code / 588)
            result.append(CHOSUNG_LIST[char1])
            #print('초성 : ()'.format(CHOSUNG_LIST[char1]))
            char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
            result.append(JUNGSUNG_LIST[char2])
            char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
            if char3==0:
                result.append('')
            else:
                result.append(JONGSUNG_LIST[char3])
            #print('종성' : {}' .format(JONGSUNG_LIST[char3]))
        else:
            result.append(keyword)

#사진 파일 전부 삭제 함수선언
def removeAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)




try:
        while True:
                    if ((GPIO.input(Button)==1)and(GPIO.input(switch)==0)):
                        img_path = r'/media/pi/SD_VOL2/DCIM/100MEDIA/IMAG0001.JPG'
                        img = cv2.imread(img_path,cv2.IMREAD_COLOR)
                        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        img2 = PIL.Image.fromarray(img2)
                        txt = pytesseract.image_to_string(img2)
                        print(txt)

                        removeAllFile(r'/media/pi/SD_VOL2/DCIM/100MEDIA')		#사진 파일 전부 삭제

                        txtlower = txt.lower()						#영어대문자 소문자로 변환
                        TXT = ','.join(txtlower)
                        arr = TXT.split(',')
                        count=len(txt)

                        from gtts import gTTS						#TTS(Text-To-Speech)

                        tts = gTTS(text = txt , lang = 'en')
                        tts.save("speech.mp3")

                        from pygame import mixer

                        mixer.init()
                        mixer.music.load(r'/home/pi/speech.mp3')
                        mixer.music.play()


                        i=0                            
                        

                        for i in range(0,count):
                                            
                                            if (i%4)==0:
                                                seg1=arr[i]

                                                if seg1 == 'a':					#글자에 따른 점자출력 (반대로 출력)
                                                        PORT(3)
                                                        PORT(4)
                                                        PORT(14)
                                                        PORT(15)
                                                        PORT(18)
                                                        time.sleep(1)
                                                        
                                                elif seg1 == 'b':
                                                        PORT(3)
                                                        PORT(14)
                                                        PORT(15)
                                                        PORT(18)
                                                        time.sleep(1)
                                                        
                                                elif seg1 == 'c':
                                                        PORT(4)
                                                        PORT(14)
                                                        PORT(15)
                                                        PORT(18)
                                                        time.sleep(1)
                                                
                                                elif seg1 == 'd':
                                                       PORT(4)
                                                       PORT(15)
                                                       PORT(18)
                                                       time.sleep(1)
                                                
                                                elif seg1 == 'e':
                                                       PORT(3)
                                                       PORT(4)
                                                       PORT(15)
                                                       PORT(18)
                                                       time.sleep(1)
                                                
                                                elif seg1 == 'f':
                                                       PORT(14)
                                                       PORT(15)
                                                       PORT(18)
                                                       time.sleep(1)
                                                
                                                elif seg1 == 'g':
                                                       PORT(15)
                                                       PORT(18)
                                                       time.sleep(1)
                                                
                                                elif seg1 == 'h':
                                                       PORT(3)
                                                       PORT(15)
                                                       PORT(18)
                                                       time.sleep(1)
                                                
                                                elif seg1 == 'i':
                                                       PORT(2)
                                                       PORT(14)
                                                       PORT(15)
                                                       PORT(18)
                                                       time.sleep(1)
                                                
                                                elif seg1 == 'j':
                                                       PORT(2)
                                                       PORT(15)
                                                       PORT(18)
                                                       time.sleep(1)
                                                
                                                elif seg1 == 'k':
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'l':
                                                      PORT(3)
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'm':
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'n':
                                                      PORT(4)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'o':
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'p':
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'q':
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'r':
                                                      PORT(3)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 's':
                                                      PORT(2)
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 't':
                                                      PORT(2)
                                                      PORT(18)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'u':
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(14)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'v':
                                                      PORT(3)
                                                      PORT(14)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'w':
                                                      PORT(2)
                                                      PORT(15)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'x':
                                                      PORT(4)
                                                      PORT(14)                      
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'y':
                                                      PORT(4)
                                                      time.sleep(1)
                                                
                                                elif seg1 == 'z':
                                                      PORT(3)
                                                      PORT(4)
                                                      time.sleep(1)
                                                
                                                elif seg1 == ' ':
                                                      PORT(2)
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)





                                                      
                                                print(seg1)

                                                GPIO.output(2,0)
                                                GPIO.output(3,0)
                                                GPIO.output(4,0)
                                                GPIO.output(14,0)
                                                GPIO.output(15,0)
                                                GPIO.output(18,0)

                                            if (i%4)==1:
                                                seg2=arr[i]

                                                    
                                                if seg2 == 'a':
                                                       PORT(27)
                                                       PORT(22)
                                                       PORT(23)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                
                                                elif seg2 == 'b':
                                                       PORT(27)
                                                       PORT(23)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'c':
                                                       PORT(22)
                                                       PORT(23)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'd':
                                                       PORT(22)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'e':
                                                       PORT(27)
                                                       PORT(22)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'f':
                                                       PORT(23)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                              
                                                elif seg2 == 'g':
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'h':
                                                       PORT(27)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'i':
                                                       PORT(17)
                                                       PORT(23)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'j':
                                                       PORT(17)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'k':
                                                       PORT(27)
                                                       PORT(22)
                                                       PORT(23)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'l':
                                                       PORT(27)
                                                       PORT(23)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'm':
                                                       PORT(22)
                                                       PORT(23)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'n':
                                                       PORT(22)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'o':
                                                       PORT(27)
                                                       PORT(22)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'p':
                                                       PORT(23)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'q':
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'r':
                                                       PORT(27)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 's':
                                                       PORT(17)
                                                       PORT(23)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 't':
                                                       PORT(17)
                                                       PORT(25)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'u':
                                                       PORT(27)
                                                       PORT(22)
                                                       PORT(23)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'v':
                                                       PORT(27)
                                                       PORT(23)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'w':
                                                       PORT(17)
                                                       PORT(24)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'x':
                                                       PORT(22)
                                                       PORT(23)                      
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'y':
                                                       PORT(22)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == 'z':
                                                       PORT(27)
                                                       PORT(22)
                                                       time.sleep(1)
                                                 
                                                elif seg2 == ' ':
                                                       PORT(17)
                                                       PORT(27)
                                                       PORT(22)
                                                       PORT(23)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)

                                                       

                                                print(seg2)     
                                                GPIO.output(17,0)
                                                GPIO.output(27,0)
                                                GPIO.output(22,0)
                                                GPIO.output(23,0)
                                                GPIO.output(24,0)
                                                GPIO.output(25,0)

                                            if (i%4)==2:
                                                seg3=arr[i]

                                                     
                                                if seg3 == 'a':
                                                        PORT(9)
                                                        PORT(11)
                                                        PORT(8)
                                                        PORT(7)
                                                        PORT(5)
                                                        time.sleep(1)
                                                 
                                                elif seg3 == 'b':
                                                       PORT(9)
                                                       PORT(8)
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'c':
                                                       PORT(11)
                                                       PORT(8)
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'd':
                                                       PORT(11)
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'e':
                                                       PORT(9)
                                                       PORT(11)
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'f':
                                                       PORT(8)
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'g':
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'h':
                                                       PORT(9)
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'i':
                                                       PORT(10)
                                                       PORT(8)
                                                       PORT(7)
                                                       PORT(5)
                                                       time.sleep(1)
                                                 
                                                elif seg3 == 'j':
                                                      PORT(10)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'k':
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'l':
                                                      PORT(9)
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'm':
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'n':
                                                      PORT(11)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'o':
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'p':
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'q':
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'r':
                                                      PORT(9)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 's':
                                                      PORT(10)
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 't':
                                                      PORT(10)
                                                      PORT(5)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'u':
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(8)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'v':
                                                      PORT(9)
                                                      PORT(8)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'w':
                                                      PORT(10)
                                                      PORT(7)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'x':
                                                      PORT(11)
                                                      PORT(8)                      
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'y':
                                                      PORT(11)
                                                      time.sleep(1)
                                                
                                                elif seg3 == 'z':
                                                      PORT(9)
                                                      PORT(11)
                                                      time.sleep(1)
                                                
                                                elif seg3 == ' ':
                                                      PORT(10)
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)

                      

                                                print(seg3)

                                                GPIO.output(10,0)
                                                GPIO.output(9,0)
                                                GPIO.output(11,0)
                                                GPIO.output(8,0)
                                                GPIO.output(7,0)
                                                GPIO.output(5,0)

                                            if (i%4)==3:
                                                seg4=arr[i]


                                                
                                                if seg4 == 'a':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'b':
                                                      PORT(12)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'c':
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'd':
                                                      PORT(13)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'e':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'f':
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'g':
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'h':
                                                      PORT(12)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'i':
                                                      PORT(6)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'j':
                                                      PORT(6)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'k':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'l':
                                                      PORT(12)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'm':
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'n':
                                                      PORT(13)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'o':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'p':
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'q':
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'r':
                                                      PORT(12)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 's':
                                                      PORT(6)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 't':
                                                      PORT(6)
                                                      PORT(26)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'u':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'v':
                                                      PORT(12)
                                                      PORT(19)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'w':
                                                      PORT(6)
                                                      PORT(16)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'x':
                                                      PORT(13)
                                                      PORT(19)                      
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'y':
                                                      PORT(13)
                                                      time.sleep(1)
                                                
                                                elif seg4 == 'z':
                                                      PORT(12)
                                                      PORT(13)
                                                      time.sleep(1)
                                                
                                                elif seg4 == ' ':
                                                      PORT(6)
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)



                                                      

                                                print(seg4)

                                                GPIO.output(6,0)
                                                GPIO.output(12,0)
                                                GPIO.output(13,0)
                                                GPIO.output(19,0)
                                                GPIO.output(16,0)
                                                GPIO.output(26,0)


                    elif ((GPIO.input(Button)==0)and(GPIO.input(switch)==0)):
                        img_path = r'/media/pi/SD_VOL2/DCIM/100MEDIA/IMAG0001.JPG'
                        img = cv2.imread(img_path,cv2.IMREAD_COLOR)
                        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        img2 = PIL.Image.fromarray(img2)
                        txt = pytesseract.image_to_string(img2, lang = 'kor')
                        print(txt)

                        removeAllFile(r'/media/pi/SD_VOL2/DCIM/100MEDIA')

                    
                        convert(txt)						#한글 분리 함수
                        TXT = ','.join(result)
                        arr = TXT.split(',')
                        count=len(result)

                        from gtts import gTTS					#TTS(Text-To-Speech)

                        tts = gTTS(text = txt , lang = 'ko')
                        tts.save("speech.mp3")

                        from pygame import mixer

                        mixer.init()
                        mixer.music.load(r'/home/pi/speech.mp3')
                        mixer.music.play()


                        i=0                            
                        

                        for i in range(0,count):
                                            
                                            if (i%4)==0:
                                                seg1=arr[i]

 
                                                
                                                if seg1 == ' ':
                                                      PORT(2)
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)



                                                elif seg1 == 'ㄱ':
                                                        PORT(2)
                                                        PORT(4)
                                                        PORT(14)
                                                        PORT(15)
                                                        PORT(18)
                                                        time.sleep(1)

                                                elif seg1 == 'ㄴ':
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)

                                                elif seg1 == 'ㄷ':
                                                      PORT(2)
                                                      PORT(14)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㄹ':
                                                      PORT(2)
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅁ':
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅂ':
                                                      PORT(2)
                                                      PORT(4)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅅ':
                                                      PORT(2)
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(15)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅇ':
                                                      PORT(2)
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅈ':
                                                      PORT(2)
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(15)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅊ':
                                                      PORT(2)
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(15)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅋ':
                                                      PORT(14)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅌ':
                                                      PORT(3)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅍ':
                                                      PORT(4)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅎ':
                                                      PORT(2)
                                                      PORT(15)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅏ':
                                                      PORT(3)
                                                      PORT(14)
                                                      PORT(15)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅑ':
                                                      PORT(2)
                                                      PORT(4)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅓ':
                                                      PORT(2)
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅕ':
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(15)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅗ':
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(14)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅛ':
                                                      PORT(2)
                                                      PORT(4)
                                                      PORT(14)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅜ':
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅠ':
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(15)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅡ':
                                                      PORT(2)
                                                      PORT(14)
                                                      PORT(15)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅣ':
                                                      PORT(3)
                                                      PORT(4)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅐ':
                                                      PORT(3)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅔ':
                                                      PORT(4)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅖ':
                                                      PORT(2)
                                                      PORT(4)
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅘ':
                                                      PORT(3)
                                                      PORT(14)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅚ':
                                                      PORT(4)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅝ':
                                                      PORT(14)
                                                      PORT(18)
                                                      time.sleep(1)
                                                elif seg1 == 'ㅢ':
                                                      PORT(2)
                                                      PORT(15)
                                                      time.sleep(1)




                                                      
                                                print(seg1)

                                                GPIO.output(2,0)
                                                GPIO.output(3,0)
                                                GPIO.output(4,0)
                                                GPIO.output(14,0)
                                                GPIO.output(15,0)
                                                GPIO.output(18,0)

                                            if (i%4)==1:
                                                seg2=arr[i]

                                                    
                                                 
                                                if seg2 == ' ':
                                                       PORT(17)
                                                       PORT(27)
                                                       PORT(22)
                                                       PORT(23)
                                                       PORT(24)
                                                       PORT(25)
                                                       time.sleep(1)

                                                elif seg2 == 'ㄱ':
                                                        PORT(17)
                                                        PORT(22)
                                                        PORT(23)
                                                        PORT(24)
                                                        PORT(25)
                                                        time.sleep(1)

                                                elif seg2 == 'ㄴ':
                                                      PORT(22)
                                                      PORT(23)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)

                                                elif seg2 == 'ㄷ':
                                                      PORT(17)
                                                      PORT(23)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㄹ':
                                                      PORT(17)
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅁ':
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅂ':
                                                      PORT(17)
                                                      PORT(22)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅅ':
                                                      PORT(17)
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(23)
                                                      PORT(24)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅇ':
                                                      PORT(17)
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(23)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅈ':
                                                      PORT(17)
                                                      PORT(22)
                                                      PORT(23)
                                                      PORT(24)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅊ':
                                                      PORT(17)
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(24)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅋ':
                                                      PORT(23)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅌ':
                                                      PORT(27)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅍ':
                                                      PORT(22)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅎ':
                                                      PORT(17)
                                                      PORT(24)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅏ':
                                                      PORT(27)
                                                      PORT(23)
                                                      PORT(24)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅑ':
                                                      PORT(17)
                                                      PORT(22)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅓ':
                                                      PORT(17)
                                                      PORT(23)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅕ':
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(24)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅗ':
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(23)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅛ':
                                                      PORT(17)
                                                      PORT(22)
                                                      PORT(23)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅜ':
                                                      PORT(22)
                                                      PORT(23)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅠ':
                                                      PORT(22)
                                                      PORT(23)
                                                      PORT(24)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅡ':
                                                      PORT(17)
                                                      PORT(23)
                                                      PORT(24)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅣ':
                                                      PORT(27)
                                                      PORT(22)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅐ':
                                                      PORT(27)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅔ':
                                                      PORT(22)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅖ':
                                                      PORT(17)
                                                      PORT(22)
                                                      PORT(23)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅘ':
                                                      PORT(27)
                                                      PORT(23)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅚ':
                                                      PORT(22)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅝ':
                                                      PORT(23)
                                                      PORT(25)
                                                      time.sleep(1)
                                                elif seg2 == 'ㅢ':
                                                      PORT(17)
                                                      PORT(24)
                                                      time.sleep(1)

                                                       

                                                print(seg2)     
                                                GPIO.output(17,0)
                                                GPIO.output(27,0)
                                                GPIO.output(22,0)
                                                GPIO.output(23,0)
                                                GPIO.output(24,0)
                                                GPIO.output(25,0)

                                            if (i%4)==2:
                                                seg3=arr[i]

                                                     
                                                
                                                if seg3 == ' ':
                                                      PORT(10)
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)


                                                elif seg3 == 'ㄱ':
                                                        PORT(10)
                                                        PORT(11)
                                                        PORT(8)
                                                        PORT(7)
                                                        PORT(5)
                                                        time.sleep(1)

                                                elif seg3 == 'ㄴ':
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)

                                                elif seg3 == 'ㄷ':
                                                      PORT(10)
                                                      PORT(8)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㄹ':
                                                      PORT(10)
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅁ':
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅂ':
                                                      PORT(10)
                                                      PORT(11)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅅ':
                                                      PORT(10)
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(7)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅇ':
                                                      PORT(10)
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅈ':
                                                      PORT(10)
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(7)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅊ':
                                                      PORT(10)
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(7)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅋ':
                                                      PORT(8)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅌ':
                                                      PORT(9)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅍ':
                                                      PORT(11)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅎ':
                                                      PORT(10)
                                                      PORT(7)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅏ':
                                                      PORT(9)
                                                      PORT(8)
                                                      PORT(7)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅑ':
                                                      PORT(10)
                                                      PORT(11)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅓ':
                                                      PORT(10)
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅕ':
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(7)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅗ':
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(8)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅛ':
                                                      PORT(10)
                                                      PORT(11)
                                                      PORT(8)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅜ':
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅠ':
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(7)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅡ':
                                                      PORT(10)
                                                      PORT(8)
                                                      PORT(7)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅣ':
                                                      PORT(9)
                                                      PORT(11)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅐ':
                                                      PORT(9)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅔ':
                                                      PORT(11)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅖ':
                                                      PORT(10)
                                                      PORT(11)
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅘ':
                                                      PORT(9)
                                                      PORT(8)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅚ':
                                                      PORT(11)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅝ':
                                                      PORT(8)
                                                      PORT(5)
                                                      time.sleep(1)
                                                elif seg3 == 'ㅢ':
                                                      PORT(10)
                                                      PORT(7)
                                                      time.sleep(1)




                                                      

                                                print(seg3)

                                                GPIO.output(10,0)
                                                GPIO.output(9,0)
                                                GPIO.output(11,0)
                                                GPIO.output(8,0)
                                                GPIO.output(7,0)
                                                GPIO.output(5,0)

                                            if (i%4)==3:
                                                seg4=arr[i]


                                                
                                                
                                                if seg4 == ' ':
                                                      PORT(6)
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)


                                                elif seg4 == 'ㄱ':
                                                        PORT(6)
                                                        PORT(13)
                                                        PORT(19)
                                                        PORT(16)
                                                        PORT(26)
                                                        time.sleep(1)

                                                elif seg4 == 'ㄴ':
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)

                                                elif seg4 == 'ㄷ':
                                                      PORT(6)
                                                      PORT(9)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㄹ':
                                                      PORT(6)
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅁ':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅂ':
                                                      PORT(6)
                                                      PORT(13)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅅ':
                                                      PORT(6)
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅇ':
                                                      PORT(6)
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅈ':
                                                      PORT(6)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅊ':
                                                      PORT(6)
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(16)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅋ':
                                                      PORT(19)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅌ':
                                                      PORT(12)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅍ':
                                                      PORT(13)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅎ':
                                                      PORT(6)
                                                      PORT(16)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅏ':
                                                      PORT(12)
                                                      PORT(19)
                                                      PORT(16)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅑ':
                                                      PORT(6)
                                                      PORT(13)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅓ':
                                                      PORT(9)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅕ':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(16)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅗ':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(19)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅛ':
                                                      PORT(6)
                                                      PORT(13)
                                                      PORT(19)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅜ':
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅠ':
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(16)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅡ':
                                                      PORT(6)
                                                      PORT(19)
                                                      PORT(16)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅣ':
                                                      PORT(12)
                                                      PORT(13)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅐ':
                                                      PORT(12)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅔ':
                                                      PORT(13)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅖ':
                                                      PORT(6)
                                                      PORT(13)
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅘ':
                                                      PORT(12)
                                                      PORT(19)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅚ':
                                                      PORT(13)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅝ':
                                                      PORT(19)
                                                      PORT(26)
                                                      time.sleep(1)
                                                elif seg4 == 'ㅢ':
                                                      PORT(6)
                                                      PORT(16)
                                                      time.sleep(1)


                                                      

                                                print(seg4)

                                                GPIO.output(6,0)
                                                GPIO.output(12,0)
                                                GPIO.output(13,0)
                                                GPIO.output(19,0)
                                                GPIO.output(16,0)
                                                GPIO.output(26,0)
                                  
                                        
                                    

                     
                    
except KeyboardInterrupt:     
        GPIO.cleanup()
