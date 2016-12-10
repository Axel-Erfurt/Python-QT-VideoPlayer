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

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget)

        self.setLayout(layout)
        
        self.myinfo = "TV-Livestream\n©2016\nAxel Schneider\n\nMouse Wheel = Zoom\nUP = Volume Up\nDOWN = Volume Down\n"

        self.widescreen = True
		
		#### shortcuts ####
        self.shortcut = QShortcut(QKeySequence("q"), self)
        self.shortcut.activated.connect(self.handleQuit)
        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.play)
        self.shortcut = QShortcut(QKeySequence("f"), self)
        self.shortcut.activated.connect(self.handleFullscreen)
        self.shortcut = QShortcut(QKeySequence("i"), self)
        self.shortcut.activated.connect(self.handleInfo)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.shortcut.activated.connect(self.volumeUp)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.shortcut.activated.connect(self.volumeDown)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.error.connect(self.handleError)

        print("QT5 Player started")

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)


    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        print("Error: " + self.mediaPlayer.errorString())

    def handleQuit(self):
        self.mediaPlayer.stop()
        print("Goodbye ...")
        app.quit()
	
    def contextMenuRequested(self,point):
        menu = QtWidgets.QMenu()
        actionARD = menu.addAction("ARD")
        actionZDF = menu.addAction("ZDF")
        actionMDR = menu.addAction("MDR")
        actionHR = menu.addAction("HR")
        actionRBB = menu.addAction("RBB")
        actionBR = menu.addAction("BR")
        actionSR = menu.addAction("SR")
        actionNDR = menu.addAction("NDR")
        actionWDR = menu.addAction("WDR")
        actionARTE = menu.addAction("ARTE")
        actionNeo = menu.addAction("ZDF Neo")
        actionZDFInfo = menu.addAction("ZDF Info")
        actionAlpha = menu.addAction("alpha")
        actionMDRPlus = menu.addAction("MDR +")
        actionSep = menu.addSeparator()
        actionORF1 = menu.addAction("ORF 1")
        actionORF2 = menu.addAction("ORF 2")
        actionORF3 = menu.addAction("ORF 3")

        actionsep2 = menu.addSeparator() 
        actionFull = menu.addAction("Fullscreen (f)")
        actionSep = menu.addSeparator()
        actionInfo = menu.addAction("Info (i)")
        action5 = menu.addSeparator() 
        actionQuit = menu.addAction("Exit (q)") 

        actionQuit.triggered.connect(self.handleQuit)
        actionFull.triggered.connect(self.handleFullscreen)
        actionInfo.triggered.connect(self.handleInfo)

        actionARD.triggered.connect(self.handleARD)
        actionZDF.triggered.connect(self.handleZDF)
        actionMDR.triggered.connect(self.handleMDR)
        actionZDFInfo.triggered.connect(self.handleZDFInfo)
        actionHR.triggered.connect(self.handleHR)
        actionARTE.triggered.connect(self.handleARTE)
        actionRBB.triggered.connect(self.handleRBB)
        actionBR.triggered.connect(self.handleBR)
        actionSR.triggered.connect(self.handleSR)
        actionAlpha.triggered.connect(self.handleAlpha)
        actionNDR.triggered.connect(self.handleNDR)
        actionWDR.triggered.connect(self.handleWDR)
        actionNeo.triggered.connect(self.handleNeo)
        actionMDRPlus.triggered.connect(self.handleMDRPlus)
        actionORF1.triggered.connect(self.handleORF1)
        actionORF2.triggered.connect(self.handleORF2)
        actionORF3.triggered.connect(self.handleORF3)

        menu.exec_(self.mapToGlobal(point))

    def wheelEvent(self,event):
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mscale = event.angleDelta().y() / 5
        self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.778)         

    def handleFullscreen(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
            print("no Fullscreen")
        else:
            self.showFullScreen()
            print("Fullscreen entered")

    def handleInfo(self):
            msg = QMessageBox()
            msg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)
            msg.setGeometry(self.frameGeometry().left() + 30, self.frameGeometry().top() + 30, 300, 400)
            msg.setIcon(QMessageBox.Information)
            msg.setText("QT5 Player")
            msg.setInformativeText(self.myinfo)
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec()
            		
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
############################### TV ################################
    def handleARD(self):
        myurl = "http://daserste_live-lh.akamaihd.net/i/daserste_de@91204/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleZDF(self):
        myurl = "http://zdf1314-lh.akamaihd.net/i/de14_v1@392878/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleMDR(self):
        myurl = "http://mdr_th_hls-lh.akamaihd.net/i/livetvmdrthueringen_de@106903/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleRBB(self):
        myurl = "http://rbb_live-lh.akamaihd.net/i/rbb_brandenburg@107638/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleHR(self):
        myurl = "http://live1_hr-lh.akamaihd.net/i/hr_fernsehen@75910/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleBR(self):
        myurl = "http://livestreams.br.de/i/bfsnord_germany@119898/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleSR(self):
        myurl = "http://livestream.sr-online.de/live.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleNDR(self):
        myurl = "http://ndr_fs-lh.akamaihd.net/i/ndrfs_nds@119224/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleWDR(self):
        myurl = "http://wdr_fs_geo-lh.akamaihd.net/i/wdrfs_geogeblockt@112044/index_2692_av-b.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleZDFInfo(self):
        myurl = "http://zdf1112-lh.akamaihd.net/i/de12_v1@392882/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleNeo(self):
        myurl = "http://zdf1314-lh.akamaihd.net/i/de13_v1@392877/master.m3u8"
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleMDRPlus(self):
        myurl = "http://liveevent1.mdr.de/i/livetvmdrevent1_ww@106904/index_1106_av-b.m3u8" #?sd=10&rebase=on
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleAlpha(self):
        myurl = "http://livestreams.br.de/i/bralpha_germany@119899/master.m3u8" 
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleARTE(self):
        myurl = "http://artelive-lh.akamaihd.net/i/artelive_de@393591/master.m3u8" 
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleORF1(self):
        myurl = "http://apasfiisl.apa.at/ipad/orf1_q4a/orf.sdp/playlist.m3u8" 
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleORF2(self):
        myurl = "http://apasfiisl.apa.at/ipad/orf2_q4a/orf.sdp/playlist.m3u8" 
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

    def handleORF3(self):
        myurl = "http://apasfiisl.apa.at/ipad/orf3_q4a/orf.sdp/playlist.m3u8" 
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.mediaPlayer.play()

############################### Ende TV ################################

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)

    player = VideoPlayer()
    player.setAcceptDrops(True)
    player.setWindowTitle("QT5 Player")
    player.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    player.setGeometry(700, 400, 400, 400/1.778)
    player.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
    player.customContextMenuRequested[QtCore.QPoint].connect(player.contextMenuRequested)
    player.show()
sys.exit(app.exec_())