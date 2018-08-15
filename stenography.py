import sys
import time
try:
    import cv2
except:
    print('Install OpenCV first!')
    print('pip install opencv-python')
    time.sleep(3)
    exit()
import os
try:
    from PyQt5 import Qt, uic
    from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QPoint
    from PyQt5.QtGui import QImage, QPixmap, QIcon, QPen, QPainter
    from PyQt5.QtWidgets import QFileDialog, QApplication, QDialog, QMessageBox, QAction, QMainWindow
except:
    print('Install PyQt5 first!')
    print('pip3 install pyqt5')
    time.sleep(3)
    exit()

class gui(QMainWindow):
    # init class
    def __init__(self):
        super(gui, self).__init__()
        print('The Application encrypts data using LSB encryption!')
        uic.loadUi(r'stegnographyUI.ui', self)
        # self.initializePaint()
        self.videoData = None
        self.videoName = None
        self.imageFolder = '/EncryptedImages'
        self.myImage=QPixmap("stenographyImage.jpg")
        self.imageLabel.setPixmap(self.myImage)
        try:
            self.videoName = 'input.avi'
        except:
            self.videoName = None
        self.encryptButton.clicked.connect(self.readDataToVideo)
        self.decryptButton.clicked.connect(self.decryptDataFromVideo)
        self.actionEncrypt_Image.triggered.connect(self.readDataToVideo)
        self.actionDecrypt_Image.triggered.connect(self.decryptDataFromVideo)
        self.actionExit2.triggered.connect(self.close)

    # helper functions for image stenography
    def close(self):
        sys.exit(app.exec_())

    def getChar(self, binChar):
        binChar = reversed(binChar)
        mul = int(1)
        sum = int(0)
        for i in binChar:
            sum += (ord(i) - ord('0')) * mul
            mul *= int(2)
        return str(chr(sum))

    def getNumFromBin(self, binaryThing):
        binaryThing = reversed(binaryThing)
        mul = int(1)
        sum = int(0)
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
            i += 8
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
        pass  # self.binaryData

    def encryptVideoHelper(self, data):

        # Creates set of images taken from the video that is loaded. This way a huge amount of data can be loaded
        # into the images and processed.
        # FOLLOWING PROCESS IS FOLLOWED:
        # convert to binary
        # initialize capture
        # initialize out.
        # read data from frame and write to the frame and out the frame to the video
        # if the read data has ended then don't process the other frames and return
        data += '\n\n!@#$%^&*'  # stopper so that the image doesnot read garbage. This stopper is read bt python easily
        frameCount = 0
        writeFlag = True
        binaryData = self.string2Binary(data)
        cap = cv2.VideoCapture(self.videoName)
        if cap.isOpened() == False:
            print('Input Video is not loaded!')
            return
        ret, frame = cap.read()
        w = None
        h = None
        myEndFlag = False
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        outputVideo = cv2.VideoWriter('output.avi', -1, 100.0, (int(cap.get(3)), int(cap.get(4))), True)
        # so we have the data as character string
        index = 0
        frameCount = int(0)
        while cap.isOpened():
            # print("Here")
            frameCount += 1
            ret, frame = cap.read()
            if ret == False:
                break
            if ret:
                # do some processing on the frame
                if writeFlag:
                    print('Loading:', writeFlag, 'Processing frame: ', frameCount)
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
                                    temp += binaryData[index]
                                    temp += binaryData[index + 1]
                                    index += 2
                                else:
                                    index = -1
                                    frame[row][col] = self.getNumFromBin(temp)
                                    myEndFlag = True
                                    break

                                # index = index % len(binaryData) # we dont want to do that the index circles around the image. Instread we want to break it.
                                frame[row][col] = self.getNumFromBin(temp)
                            if myEndFlag:
                                break
                        if index == -1:
                            print('Loading Complete')
                            writeFlag = False
                            # break

                    elif len(frame.shape) >= 3:
                        for row in range(rows):
                            for col in range(cols):
                                if index == -1:
                                    myEndFlag = True
                                    break
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
                                    myEndFlag = True
                                    break
                                # index = index % len(binaryData)
                                frame[row][col][0] = self.getNumFromBin(temp)
                            if myEndFlag:
                                break
                        print('Current index: ', index)
                        if index == -1:
                            print('Loading Complete')
                            writeFlag = False
                            outputVideo.write(frame)
                            # break

                            # break

                # processing the frame ends

                # instead of writing a frame, we can just save the frame as an image and then
                # some library to compile those images as a video without using compression
                # FFMPEG does that, though I am not in favour of using an external library, I have to

                # WRITE CODE FOR DISPLAYING IMAGE IN QLABEL VIA QPIXMAP
                try:
                    myPath = 'EncryptedImages/' + str(frameCount) + '.png'
                    imagePath = os.path.abspath(myPath)
                    print(imagePath)
                    cv2.imwrite(imagePath, frame)
                    outputVideo.write(frame)
                except:
                    print('Cant write to image, sorry!')
                if index == -1:
                    break

                # print(frameCount,end==' ')
                # print('Here')
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Release everything if job is finished
        print('Job Finished')
        cap.release()
        outputVideo.release()
        cv2.destroyAllWindows()

    def bringEncryptedDataFromVideo(self):
        cap = cv2.VideoCapture(self.videoName)
        # cv2.imshow('Some Frame',cap.read()[1])
        if (cap.isOpened() == False):
            print('Video not loaded!')
            return
        print('Video Loaded Successfully')
        # ret, frame = cap.read()
        endChecker = ''
        dataFromImage = ''  # this will contain a binary string that will be read from the image
        dataFromImageReturn = ''

        rows = 0
        cols = 0
        channel = 0
        # -- Debug --
        # print(len(frame))
        # print(type(frame))
        # try:
        #     print(frame.shape)
        # except:
        #     print('Shape of frame is not defined')
        timeToReturn = False

        rows=int(cap.get(4))
        cols=int(cap.get(3))
        # else:
        #     rows, cols, _ = [cap.get(3), cap.get(4), 3]
        print('Calling the loop')
        while (cap.isOpened() and not timeToReturn):
            ret, frame = cap.read()
            if ret and not timeToReturn:
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
                            print('\nEnd Found')
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
                            print('\nEnd Found')
                            break
            if timeToReturn:
                break
            # this is inside while loop

        cap.release()
        cv2.destroyAllWindows()

        return self.binary2String(dataFromImageReturn)

    def readDataToVideo(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open Text File to load text from!', '', 'Text File (*.txt)')
        # fname='2mb.txt'
        data = None

        myfile = None
        if fname:
            with open(fname, 'r') as myfile:
                data = myfile.read()
            # self.waterMarkImageClicked(data)

            self.encryptVideoHelper(data)
            myfile.close()
        else:
            print('Please reselect a valid file!')

    def decryptDataFromVideo(self):
        print('Decrypting: ')
        print('Input text file to load the data to -- ')
        fname, _ = QFileDialog.getOpenFileName(self, 'Open File to save text from video!', '', 'Text File (*.txt)')
        # fname = 'decryptData.txt'
        data = None
        myfile = None
        self.videoName = 'output.avi'
        if fname:
            with open(fname, 'w') as myfile:
                self.videoData = self.bringEncryptedDataFromVideo()
                myfile.write(self.videoData)
            myfile.close()
        else:
            print('Please reselect a valid file!')


app = QApplication(sys.argv)
window = gui()
window.setWindowTitle('Video Stegnography')
window.show()
sys.exit(app.exec_())
