#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPalette, QKeySequence, QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLineEdit,
        					QPushButton, QSizePolicy, QSlider, QMessageBox, QStyle, QVBoxLayout,  
							QWidget, QShortcut)
import os

class VideoPlayer(QWidget):

    def __init__(self):
        super(VideoPlayer, self).__init__()

        self.setAttribute( Qt.WA_NoSystemBackground, True )

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVolume(80)
        self.videoWidget = QVideoWidget(self)
        
        self.lbl = QLineEdit('00:00:00')
        self.lbl.setFixedWidth(60)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.setStyleSheet(stylesheet(self))
        
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setFixedWidth(60)
        self.elbl.setUpdatesEnabled(True)
        self.elbl.setStyleSheet(stylesheet(self))

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedWidth(32)
        self.playButton.setStyleSheet("background-color: black")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setStyleSheet (stylesheet(self)) 
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.sliderMoved.connect(self.handleLabel)
        self.positionSlider.setSingleStep(2)
        self.positionSlider.setPageStep(20)
        self.positionSlider.setAttribute(Qt.WA_TranslucentBackground, True)
        
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(5, 0, 5, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.lbl)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.elbl)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)

        self.setLayout(layout)
        
        self.myinfo = "©2016\nAxel Schneider\n\nMouse Wheel = Zoom\nUP = Volume Up\nDOWN = Volume Down\n" + \
				"LEFT = < 1 Minute\nRIGHT = > 1 Minute\n" + \
				"SHIFT+LEFT = < 10 Minutes\nSHIFT+RIGHT = > 10 Minutes"
		
		#### shortcuts ####
        self.shortcut = QShortcut(QKeySequence("q"), self)
        self.shortcut.activated.connect(self.handleQuit)
        self.shortcut = QShortcut(QKeySequence("o"), self)
        self.shortcut.activated.connect(self.openFile)
        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.play)
        self.shortcut = QShortcut(QKeySequence("f"), self)
        self.shortcut.activated.connect(self.handleFullscreen)
        self.shortcut = QShortcut(QKeySequence("i"), self)
        self.shortcut.activated.connect(self.handleInfo)
        self.shortcut = QShortcut(QKeySequence("s"), self)
        self.shortcut.activated.connect(self.toggleSlider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.shortcut.activated.connect(self.volumeUp)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.shortcut.activated.connect(self.volumeDown)	
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Right) , self)
        self.shortcut.activated.connect(self.forwardSlider10)
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Left) , self)
        self.shortcut.activated.connect(self.backSlider10)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.positionChanged.connect(self.handleLabel)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        print("QT5 Player started")

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath(), "Videos (*.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v)")

        if fileName != '':
            self.loadFilm(fileName)
            print("File loaded")

    def playFromURL(self):
        self.mediaPlayer.pause()
        clip = QApplication.clipboard()
        myurl = clip.text()
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.playButton.setEnabled(True)
        self.mediaPlayer.play()
        self.hideSlider()
        print(myurl)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        print("Error: " + self.mediaPlayer.errorString())

    def handleQuit(self):
        self.mediaPlayer.stop()
        print("Goodbye ...")
        app.quit()
	
    def contextMenuRequested(self,point):
        menu = QtWidgets.QMenu()
        actionFile = menu.addAction("open File (o)")
        actionclipboard = menu.addSeparator() 
        actionURL = menu.addAction("URL from Clipboard (u)")
        actionclipboard = menu.addSeparator() 
        actionToggle = menu.addAction("show / hide Slider (s)") 
        actionFull = menu.addAction("Fullscreen (f)")
        action169 = menu.addAction("16 : 9")
        action43 = menu.addAction("4 : 3")
        actionSep = menu.addSeparator()
        actionInfo = menu.addAction("Info (i)")
        action5 = menu.addSeparator() 
        actionQuit = menu.addAction("Exit (q)") 

        actionFile.triggered.connect(self.openFile)
        actionQuit.triggered.connect(self.handleQuit)
        actionFull.triggered.connect(self.handleFullscreen)
        actionInfo.triggered.connect(self.handleInfo)
        actionToggle.triggered.connect(self.toggleSlider)
        actionURL.triggered.connect(self.playFromURL)
        action169.triggered.connect(self.screen169)
        action43.triggered.connect(self.screen43)
        menu.exec_(self.mapToGlobal(point))

    def wheelEvent(self,event):
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mscale = event.angleDelta().y() / 5
        if mwidth / mheight > 1.7:
            self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.778) 
        else:
            self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.33)            

    def screen169(self):
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.778
        self.setGeometry(mleft, mtop, mwidth, mwidth / mratio)

    def screen43(self):
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.33
        self.setGeometry(mleft, mtop, mwidth, mwidth / mratio)

    def handleFullscreen(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
            print("no Fullscreen")
        else:
            self.showFullScreen()
            print("Fullscreen entered")

    def handleInfo(self):
            msg = QMessageBox()
            msg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            msg.setGeometry(self.frameGeometry().left() + 30, self.frameGeometry().top() + 30, 300, 400)
            msg.setIcon(QMessageBox.Information)
            msg.setText("QT5 Player")
            msg.setInformativeText(self.myinfo)
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec()
            
    def toggleSlider(self):	
        if self.positionSlider.isVisible():
            self.hideSlider()
        else:
            self.showSlider()
	
    def hideSlider(self):
            self.lbl.hide()
            self.elbl.hide()
            self.positionSlider.hide()
            self.playButton.hide()
            mwidth = self.frameGeometry().width()
            mheight = self.frameGeometry().height()
            mleft = self.frameGeometry().left()
            mtop = self.frameGeometry().top()
            if mwidth / mheight < 1.7:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.778) 
            else:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.55)
	
    def showSlider(self):
            self.lbl.show()
            self.elbl.show()
            self.lbl.update()
            self.positionSlider.show()
            self.playButton.show()
            mwidth = self.frameGeometry().width()
            mheight = self.frameGeometry().height()
            mleft = self.frameGeometry().left()
            mtop = self.frameGeometry().top()
            if mwidth / mheight < 1.7:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.33) 
            else:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.55)
	
    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)

    def forwardSlider10(self):
            self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000*60)

    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*60)

    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000*60)
		
    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
        print("Volume: " + str(self.mediaPlayer.volume()))
	
    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
        print("Volume: " + str(self.mediaPlayer.volume()))
		
    def mouseMoveEvent(self, event):   
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() \
						- QPoint(self.frameGeometry().width() / 2, \
						self.frameGeometry().height() / 2))
            event.accept() 
		
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        f = str(event.mimeData().urls()[0].toLocalFile())
        self.loadFilm(f)
	
    def loadFilm(self, f):
            self.hideSlider()
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
            self.playButton.setEnabled(True)
            self.mediaPlayer.play()
            print(self.mediaPlayer.media().canonicalResource().resolution())
            print(self.mediaPlayer.metaData("Resolution"))
	  
    def openFileAtStart(self, filelist):
            matching = [s for s in filelist if ".myformat" in s]
            if len(matching) > 0:
                self.loadFilm(matching)

###################################################################
    def handleLabel(self):
            self.lbl.clear()
            mtime = QTime(0,0,0,0)
            self.time = mtime.addMSecs(self.mediaPlayer.position())
            self.lbl.setText(self.time.toString())
            print(str(self.mediaPlayer.position()) \
            + " - " + self.time.toString())
            app.processEvents()

###################################################################

def stylesheet(self):
    return """

QSlider::handle:horizontal 
{
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #333, stop:1 #555555);
width: 14px;
border-radius: 0px;
}

QSlider::groove:horizontal {
border: 1px solid #444;
height: 10px;
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000, stop:1 #222222);
}

QLineEdit
{
background: black;
color: #585858;
border: 0px solid #076100;
font-size: 12px;
font-weight: bold;
}
    """

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)

    player = VideoPlayer()
    player.setAcceptDrops(True)
    player.setWindowTitle("QT5 Player")
    player.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    player.setGeometry(100, 300, 400, 290)
    player.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
    player.customContextMenuRequested[QtCore.QPoint].connect(player.contextMenuRequested)
    player.show()
sys.exit(app.exec_())
