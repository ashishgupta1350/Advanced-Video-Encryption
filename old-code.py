import sys
import cv2
import numpy as np
import os
from PyQt5 import Qt, uic
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPen, QPainter
from PyQt5.QtWidgets import QFileDialog, QApplication, QDialog, QMessageBox, QAction, QMainWindow
from PyQt5.uic import loadUi
from PyQt5 import QtCore
import binascii
from PyQt5.QtWidgets import QMenu
import webbrowser
import ChromeDinasourGame
import ChromeDinasourGamePakhi

class gui(QMainWindow):
    # init class
    def __init__(self):
        super(gui, self).__init__()
        print('The Application encrypts data using LSB encryption!')
        uic.loadUi(r'stegnographyUI.ui', self)
        self.initializePaint()
        self.cap = None
        self.globalDrawing = False
        self.displayImage(2)
        self.filterFlag = int(1)
        self.lastFilter = 'No Filter Used'
        self.initializeSlider()
        self.binaryData=''

    # helper functions for image stenography

    def getChar(self, binChar):
        binChar = reversed(binChar)
        mul = int(1)
        sum = int(0);
        for i in binChar:
            sum += (ord(i) - ord('0')) * mul
            mul *= int(2)
        return str(chr(sum))

    def getNumFromBin(self, binaryThing):
        binaryThing = reversed(binaryThing)
        mul = int(1)
        sum = int(0);
        for i in binaryThing:
            sum += (ord(i) - ord('0')) * mul
            mul *= int(2)
        return sum

    def binary2String(self, myBinString):
        i = 0
        #     myBinString='01100001'
        retString = ''
        l = len(myBinString)
        while i < l:
            binChar = myBinString[i:i + 8]
            ch = self.getChar(binChar)
            retString += ch
            i += 8;
        return retString

    def string2Binary(self, myString):
        # myString = 'This is me'
        binString = ''
        for i in myString:
            a = ord(i)
            bitstring = bin(a)
            bitstring = bitstring[2:]
            bitstring = -len(bitstring) % 8 * '0' + bitstring
            binString += bitstring
        return binString



    def convertData(self):
        pass # self.binaryData

    def readAndWriteVideo(self,videoName):
        cap=cv2.VideoCapture(videoName)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                # do some processing on the frame


                # processing the frame ends
                out.write(frame)

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()


    def encryptVideoHelper(self, data):
        # convert to binary
        # initialize capture
        # initialize out.
        # read data from frame and write to the frame and out the frame to the video
        # if the read data has ended then don't process the other frames and return
        writeFlag=True
        binaryData=self.string2Binary(data)
        cap = cv2.VideoCapture(videoName)
        if cap.isOpened()==False:
            print('Input Video is not loaded!')
            return
        ret,frame=cap.read()
        w,h=len(frame) # not sure if it is (h,w)
        outputVideo=cv2.VideoWriter()
        outputVideo.open("output.avi",-1,25,(w,h), True)
        # so we have the data as character string
        index=0 
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                # do some processing on the frame
                if writeFlag==True:
                    if len(frame.shape) == 2:
                        rows, cols = frame.shape
                    else:
                        rows, cols, channel = frame.shape

                    if len(frame.shape) == 2:
                        # index = 0
                        for row in range(rows):
                            for col in range(cols):

                                num = frame[row][col]
                                # convert the num to binary
                                bitstring = bin(num)
                                bitstring = bitstring[2:]
                                bitstring = -len(bitstring) % 8 * '0' + bitstring
                                # after converting it to binary change the last positions of the image number
                                temp = bitstring[0:6]
                                if index + 1 < len(binaryData):
                                    temp += binaryData[index:index + 2]
                                    index += 2
                                else:
                                    index = -1
                                    frame[row][col] = self.getNumFromBin(temp)
                                    myEndFlag = 1
                                    break

                                # index = index % len(binaryData) # we dont want to do that the index circles around the image. Instread we want to break it.
                                frame[row][col] = self.getNumFromBin(temp)
                            if myEndFlag == 1:
                                break
                        if index==-1:
                            writeFlag=False
                    elif len(frame.shape) >=3  :
                        for row in range(rows):
                            for col in range(cols):
                                num = frame[row][col][0]
                                # convert the num to binary
                                bitstring = bin(num)
                                bitstring = bitstring[2:]
                                bitstring = -len(bitstring) % 8 * '0' + bitstring
                                temp = ''
                                temp += bitstring[0:6]
                                # after converting it to binary change the last positions of the image number, the green channel has all the data
                                if index + 1 < len(binaryData):
                                    temp += binaryData[index]
                                    temp += binaryData[index + 1]
                                    index += 2
                                else:
                                    index = -1
                                    frame[row][col][0] = self.getNumFromBin(temp)
                                    myEndFlag = 1
                                    break
                                # index = index % len(binaryData)
                                frame[row][col][0] = self.getNumFromBin(temp)
                            if myEndFlag == 1:
                                break

                        if index == -1:
                            writeFlag=False

                # processing the frame ends
                outputVideo.write(frame)

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        outputVideo.release()
        cv2.destroyAllWindows()

    def bringEncryptedDataFromVideo(self,videoName):
        cap = cv2.VideoCapture(videoName)
        if(cap.isOpened() == False):
            print('Video not loaded!')
            return

        frame=cap.read()
        endChecker = ''
        dataFromImage = ''  # this will contain a binary string that will be read from the image
        rows,cols,channel = [0,0,0]
        dataFromImageReturn = ''
        if len(frame.shape) == 2:
            rows, cols = frame.shape
        else:
            rows, cols, channel = frame.shape
        while(cap.isOpened()):
            ret, frame = cap.read()
            cv2.imshow('Video Extractor', frame)
            if ret == True:
                # read frame into a string and return that string.
                if len(frame.shape) == 2:
                    for row in range(rows):
                        for col in range(cols):
                            num = frame[row][col]
                            # convert the num to binary
                            bitstring = bin(num)
                            bitstring = bitstring[2:]
                            bitstring = -len(bitstring) % 8 * '0' + bitstring
                            # after converting it to binary change the last positions of the image number
                            dataFromImage += bitstring[6:8]
                            dataFromImageReturn += bitstring[6:8]
                            if len(dataFromImage) >= 8:  # to check the end of the file statement from data flag
                                if len(endChecker) == 7:
                                    if endChecker == '!@#$%^&':
                                        timeToReturn = True
                                        break
                                    else:
                                        endChecker = endChecker[1:]
                                        endChecker += self.binary2String(dataFromImage)
                                elif len(endChecker) < 7:
                                    endChecker += self.binary2String(dataFromImage)
                                else:
                                    endChecker = ''
                                print(self.binary2String(dataFromImage), end='')
                                dataFromImage = ''
                        if timeToReturn:
                            break
                elif len(frame.shape) == 3:
                    for row in range(rows):
                        for col in range(cols):
                            num = frame[row][col][0]
                            # convert the num to binary
                            bitstring = bin(num)
                            bitstring = bitstring[2:]
                            bitstring = -len(bitstring) % 8 * '0' + bitstring
                            # after converting it to binary change the last positions of the image number
                            dataFromImage += bitstring[6:8]
                            dataFromImageReturn += bitstring[6:8]

                            if len(dataFromImage) >= 8:  # to check the end of the file statement from data flag
                                if len(endChecker) == 7:
                                    if endChecker == '!@#$%^&':
                                        timeToReturn = True
                                        break
                                    else:
                                        endChecker = endChecker[1:]
                                        endChecker += self.binary2String(dataFromImage)
                                elif len(endChecker) < 7:
                                    endChecker += self.binary2String(dataFromImage)
                                else:
                                    endChecker = ''
                                print(self.binary2String(dataFromImage), end='')
                                dataFromImage = ''
                        if timeToReturn:
                            break
            if timeToReturn:
                break
            # this is inside while loop

        cap.release()
        cv2.destroyAllWindows()

        return dataFromImageReturn   



    def readDataToVideo(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text File (*.txt)')
        data = None
        myfile = None
        if fname:
            with open(fname, 'r') as myfile:
                data = myfile.read()
            # self.waterMarkImageClicked(data)
            data+='!@#$%^&*!@#$%^&*' # the end of data sequence, for safety the data end seq has been added twice so that at the end of first frame and start of the second frame, the data can be easily read
            self.encryptVideoHelper(data)
            myfile.close()
        else:
            print('Please reselect a valid file!')

    def decryptDataFromVideo(self):
        print('Decrypting: ')
        fname, _ = QFileDialog.getOpenFileName(self, 'Open File to save', '', 'Text File (*.txt)')
        data = None
        myfile = None

        if fname:
            with open(fname, 'w') as myfile:
                # myfile.write(self.checkWatermark())
                myfile.write(self.bringEncryptedDataFromVideo())
            myfile.close()
        else:
            print('Please reselect a valid file!')


app = QApplication(sys.argv)
window = gui()
window.setWindowTitle('Mini Photoshop')
window.show()
sys.exit(app.exec_())
