#!/usr/bin/env python3
from PyQt5.QtGui import QPalette, QKeySequence
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QShortcut, QMessageBox)

class VideoPlayer(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVolume(80)
        videoWidget = QVideoWidget()
	
        openButton = QPushButton("Open...")
        openButton.clicked.connect(self.openFile)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedWidth(32)
        self.playButton.setStyleSheet("background-color: black")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setStyleSheet("background: transparent;")
        #self.positionSlider.setFixedHeight(10)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setAttribute(Qt.WA_TranslucentBackground, True)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(5, 0, 5, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)

        self.setLayout(layout)
		
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

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        print("QT5 Player started")

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                '/Axel_1/Filme', "Videos (*.mp4 *.ts *.avi *.mpeg *.mpg *.mkv)")

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
        action3 = menu.addSeparator() 
        actionURL = menu.addAction("URL from Clipboard (u)")
        action3 = menu.addSeparator() 
        actionToggle = menu.addAction("show / hide Slider (s)") 
        actionFull = menu.addAction("Fullscreen (f)")
        action8 = menu.addSeparator()
        actionInfo = menu.addAction("Info (i)")
        action5 = menu.addSeparator() 
        actionQuit = menu.addAction("Exit (q)") 
        actionFile.triggered.connect(self.openFile)
        actionQuit.triggered.connect(self.handleQuit)
        actionFull.triggered.connect(self.handleFullscreen)
        actionInfo.triggered.connect(self.handleInfo)
        actionToggle.triggered.connect(self.toggleSlider)
        actionURL.triggered.connect(self.playFromURL)
        menu.exec_(self.mapToGlobal(point))
	
    def wheelEvent(self,event):
        if self.positionSlider.isVisible():
            self.setGeometry(self.frameGeometry().left(), self.frameGeometry().top(), \
	        self.frameGeometry().width() \
	        + event.angleDelta().y()/10, self.frameGeometry().width()/1.55)
        else:
            self.setGeometry(self.frameGeometry().left(), self.frameGeometry().top(), \
	        self.frameGeometry().width() \
	        + event.angleDelta().y()/10, self.frameGeometry().width()/1.778)
	
    def handleFullscreen(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
            print("no Fullscreen")
        else:
            self.showFullScreen()
            print("Fullscreen entered")

    def handleInfo(self):
            msg = QMessageBox()
            msg.setStyleSheet('QMessageBox \
				{background-color: darkcyan; color: white;}\nQPushButton{color: lightgrey; font-size: 12px; background-color: #1d1d1d; border-radius: 5px; padding: 6px; text-align: center;}\n QPushButton:hover{color: darkcyan;}')
            msg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            msg.setGeometry(self.frameGeometry().left() + 30, self.frameGeometry().top() + 30, 300, 400)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Axel Schneider\t\n\nPython with Qt5")
            msg.setInformativeText("©2016")
            msg.setWindowTitle("Phonon Player")
            msg.setDetailedText("Mouse Wheel = Zoom\nUP = Volume Up\nDOWN = Volume Down\n" + \
				"LEFT = < 1 Minute\nRIGHT = > 1 Minute\n" + \
				"SHIFT+LEFT = < 10 Minutes\nSHIFT+RIGHT = > 10 Minutes")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec()
	
    def toggleSlider(self):	
        if self.positionSlider.isVisible():
            self.hideSlider()
        else:
            self.showSlider()
	
    def hideSlider(self):
            self.positionSlider.hide()
            self.playButton.hide()
            self.setGeometry(self.frameGeometry().left(), self.frameGeometry().top(), \
			self.frameGeometry().width(), self.frameGeometry().width()/1.778)
	
    def showSlider(self):	
            self.positionSlider.show()
            self.playButton.show()
            self.setGeometry(self.frameGeometry().left(), self.frameGeometry().top(), \
			self.frameGeometry().width(), self.frameGeometry().width()/1.55)
	
    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 100*60)
        print("Position: " + ("%.2f" % (self.mediaPlayer.position()/100/60)))

    def forwardSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)
        print("Position: " + ("%.2f" % (self.mediaPlayer.position()/1000/60)))
		
    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 100*60)
        print("Position: " + ("%.2f" % (self.mediaPlayer.position()/100/60)))

    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*60)
        print("Position: " + ("%.2f" % (self.mediaPlayer.position()/100/60)))
		
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
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
            self.playButton.setEnabled(True)
            self.mediaPlayer.play()
            self.hideSlider()
	  
    def openFileAtStart(self, filelist):
            matching = [s for s in filelist if ".myformat" in s]
            if len(matching) > 0:
                self.loadFilm(matching)

if __name__ == '__main__':
    '''
    try:
        main()
    except Exception as e:
        print(str(e))
    '''

    import sys
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.setAcceptDrops(True)
    player.setWindowTitle("QT5 Player")
    player.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    palette = QPalette()    
    palette.setColor(QPalette.Background,QtCore.Qt.black)    
    player.setPalette(palette)
    player.setGeometry(10, 40, 400, 290)
    player.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
    player.customContextMenuRequested[QtCore.QPoint].connect(player.contextMenuRequested)
    player.show()
    player.hideSlider()

    sys.exit(app.exec_())
