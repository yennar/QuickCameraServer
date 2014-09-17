from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import sys

class ServerConfigWin(QDialog):
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        
        self.initUI()
        self.initCamera()
        
        self.initTimer = QTimer()
        self.initTimer.timeout.connect(self.onDoPreview)
        self.initTimer.setInterval(1000)
        self.initTimer.setSingleShot(True)
        self.initTimer.start()
    
    def initUI(self):
        
        layMain = QFormLayout()
        
        self.cbxCamera = QComboBox()
        layMain.addRow('Camera',self.cbxCamera)

        self.vdoMain = QCameraViewfinder()
        layMain.addRow('Preview',self.vdoMain)
        
        self.btnText = QPushButton('Test')
        layMain.addRow('Preview',self.btnText)
        self.btnText.clicked.connect(self.onText)
        
        self.setLayout(layMain)
        
    def initCamera(self):
        cameras = QCameraInfo.availableCameras()
        for camera in cameras:
            self.cbxCamera.addItem(camera.description(),camera.deviceName())
        self.mainCamera = None
            
    def onDoPreview(self):
        if self.cbxCamera.currentData() is None:
            self.vdoMain.deleteLater()
            self.vdoMain = QLabel('No camera')
            return            
        
        self.mainCamera = QCamera(self.cbxCamera.currentData())
        self.mainImageCapture = QCameraImageCapture(self.mainCamera)
        self.mainImageCapture.setCaptureDestination(QCameraImageCapture.CaptureToBuffer)
        self.mainImageCapture.setBufferFormat(QVideoFrame.Format_Jpeg)
        self.mainImageCapture.imageAvailable.connect(self.onImageAvailable)
        self.mainImageCapture.imageSaved.connect(self.onImageSaved)
        self.mainCamera.setViewfinder(self.vdoMain)
        self.mainCamera.setCaptureMode(QCamera.CaptureStillImage)
        self.mainCamera.start()
        self.resize(640,480)
        
    def onText(self):
        if self.mainCamera is None:
            return
        
        self.mainCamera.searchAndLock()
        self.mainImageCapture.capture()
        self.mainCamera.unlock()

    def onImageSaved(self,image_id,image_name):
        print image_id,image_name
    
    def onImageAvailable(self,image_id,image_buffer):
        print image_id
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ServerConfigWin()
    w.show()
    app.exec_()