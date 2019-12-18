#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPalette, QKeySequence, QIcon
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint, QTime, QMimeData, QProcess, QEvent
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLineEdit,
                            QPushButton, QSizePolicy, QSlider, QMessageBox, QStyle, QVBoxLayout,  
                            QWidget, QShortcut, QMenu)
import sys
import os
import subprocess
#QT_DEBUG_PLUGINS

class VideoPlayer(QWidget):

    def __init__(self, aPath, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.setAttribute( Qt.WA_NoSystemBackground, True )
        self.setAcceptDrops(True)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.mediaStatusChanged.connect(self.printMediaData)
        self.mediaPlayer.setVolume(80)
        self.videoWidget = QVideoWidget(self)
        
        self.lbl = QLineEdit('00:00:00')
        self.lbl.setReadOnly(True)
        self.lbl.setFixedWidth(70)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.setStyleSheet(stylesheet(self))
        
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setReadOnly(True)
        self.elbl.setFixedWidth(70)
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

        self.clip = QApplication.clipboard()
        self.process = QProcess(self)
        self.process.readyRead.connect(self.dataReady)
#        self.process.started.connect(lambda: print("grabbing YouTube URL"))
        self.process.finished.connect(self.playFromURL)

        self.myurl = ""
        
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

        self.widescreen = True
        
        #### shortcuts ####
        self.shortcut = QShortcut(QKeySequence("q"), self)
        self.shortcut.activated.connect(self.handleQuit)
        self.shortcut = QShortcut(QKeySequence("u"), self)
        self.shortcut.activated.connect(self.playFromURL)

        self.shortcut = QShortcut(QKeySequence("y"), self)
        self.shortcut.activated.connect(self.getYTUrl)

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
        self.setToolTip("press 'o' to open file (see context menu for more)")

        print("QT5 Player started")
        print("press 'o' to open file (see context menu for more)")
        self.suspend_screensaver()

    def playFromURL(self):
        self.mediaPlayer.pause()
        self.myurl = self.clip.text()
        self.mediaPlayer.setMedia(QMediaContent(QUrl(self.myurl)))
        self.playButton.setEnabled(True)
        self.mediaPlayer.play()
        self.hideSlider()
        print(self.myurl)

    def getYTUrl(self):
        cmd = "youtube-dl -g -f best " + self.clip.text()
        print("grabbing YouTube URL")
        self.process.start(cmd)

    def dataReady(self):
        self.myurl = str(self.process.readAll(), encoding = 'utf8').rstrip() ###
        self.myurl = self.myurl.partition("\n")[0]
        print(self.myurl)
        self.clip.setText(self.myurl)
        self.playFromURL()

    def suspend_screensaver(self):
        'suspend linux screensaver'
        proc = subprocess.Popen('gsettings set org.gnome.desktop.screensaver idle-activation-enabled false', shell=True)
        proc.wait()

    def resume_screensaver(self):
        'resume linux screensaver'
        proc = subprocess.Popen('gsettings set org.gnome.desktop.screensaver idle-activation-enabled true', shell=True)
        proc.wait()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")

        if fileName != '':
            self.loadFilm(fileName)
            print("File loaded")

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
        print("Error: ", self.mediaPlayer.errorString())

    def handleQuit(self):
        self.mediaPlayer.stop()
        self.resume_screensaver()
        print("Goodbye ...")
        app.quit()
    
    def contextMenuRequested(self,point):
        menu = QMenu()
        actionFile = menu.addAction(QIcon.fromTheme("video-x-generic"),"open File (o)")
        actionclipboard = menu.addSeparator() 
        actionURL = menu.addAction(QIcon.fromTheme("browser"),"URL from Clipboard (u)")
        actionclipboard = menu.addSeparator() 
        actionYTurl = menu.addAction(QIcon.fromTheme("youtube"), "URL from YouTube (y)")
        actionclipboard = menu.addSeparator() 
        actionToggle = menu.addAction(QIcon.fromTheme("next"),"show / hide Slider (s)") 
        actionFull = menu.addAction(QIcon.fromTheme("view-fullscreen"),"Fullscreen (f)")
        action169 = menu.addAction(QIcon.fromTheme("tv-symbolic"),"16 : 9")
        action43 = menu.addAction(QIcon.fromTheme("tv-symbolic"),"4 : 3")
        actionSep = menu.addSeparator()
        actionInfo = menu.addAction(QIcon.fromTheme("help-about"),"Info (i)")
        action5 = menu.addSeparator() 
        actionQuit = menu.addAction(QIcon.fromTheme("application-exit"),"Exit (q)")

        actionFile.triggered.connect(self.openFile)
        actionQuit.triggered.connect(self.handleQuit)
        actionFull.triggered.connect(self.handleFullscreen)
        actionInfo.triggered.connect(self.handleInfo)
        actionToggle.triggered.connect(self.toggleSlider)
        actionURL.triggered.connect(self.playFromURL)
        actionYTurl.triggered.connect(self.getYTUrl)
        action169.triggered.connect(self.screen169)
        action43.triggered.connect(self.screen43)
        menu.exec_(self.mapToGlobal(point))

    def wheelEvent(self,event):
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mscale = event.angleDelta().y() / 5
        if self.widescreen == True:
            self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.778) 
        else:
            self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.33)            

    def screen169(self):
        self.widescreen = True
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.778
        self.setGeometry(mleft, mtop, mwidth, mwidth / mratio)

    def screen43(self):
        self.widescreen = False
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.33
        self.setGeometry(mleft, mtop, mwidth, mwidth / mratio)

    def handleFullscreen(self):
        if self.windowState() & Qt.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.showNormal()
            print("no Fullscreen")
        else:
            self.showFullScreen()
            QApplication.setOverrideCursor(Qt.BlankCursor)
            print("Fullscreen entered")

    def handleInfo(self):
        msg = QMessageBox.about(self, "QT5 Player", self.myinfo)
            
    def toggleSlider(self):    
        if self.positionSlider.isVisible():
            self.hideSlider()
        else:
            self.showSlider()
    
    def hideSlider(self):
            self.playButton.hide()
            self.lbl.hide()
            self.positionSlider.hide()
            self.elbl.hide()
            mwidth = self.frameGeometry().width()
            mheight = self.frameGeometry().height()
            mleft = self.frameGeometry().left()
            mtop = self.frameGeometry().top()
            if self.widescreen == True:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.778) 
            else:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.33)
    
    def showSlider(self):
            self.playButton.show()
            self.lbl.show()
            self.positionSlider.show()
            self.elbl.show()
            mwidth = self.frameGeometry().width()
            mheight = self.frameGeometry().height()
            mleft = self.frameGeometry().left()
            mtop = self.frameGeometry().top()
            if self.widescreen == True:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.55) 
            else:
                self.setGeometry(mleft, mtop, mwidth, mwidth / 1.33)
    
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
        elif event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("drop")
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toString()
            print("url = ", url)
            self.mediaPlayer.stop()
            self.mediaPlayer.setMedia(QMediaContent(QUrl(url)))
            self.playButton.setEnabled(True)
            self.mediaPlayer.play()
        elif event.mimeData().hasText():
            mydrop =  event.mimeData().text()
            ### YouTube url
            if "youtube" in mydrop:
                print("is YouTube", mydrop)
                self.clip.setText(mydrop)
                self.getYTUrl()
            else:
                ### normal url
                print("generic url = ", mydrop)
                self.mediaPlayer.setMedia(QMediaContent(QUrl(mydrop)))
                self.playButton.setEnabled(True)
                self.mediaPlayer.play()
                self.hideSlider()
    
    def loadFilm(self, f):
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
            self.playButton.setEnabled(True)
            self.mediaPlayer.play()

    def printMediaData(self):
        if self.mediaPlayer.mediaStatus() == 6:
            if self.mediaPlayer.isMetaDataAvailable():
                res = str(self.mediaPlayer.metaData("Resolution")).partition("PyQt5.QtCore.QSize(")[2].replace(", ", " x ").replace(")", "")
                print("%s%s" % ("Video Resolution = ",res))
            else:
                print("no metaData available")
      
    def openFileAtStart(self, filelist):
            matching = [s for s in filelist if ".myformat" in s]
            if len(matching) > 0:
                self.loadFilm(matching)

##################### update Label ##################################
    def handleLabel(self):
            self.lbl.clear()
            mtime = QTime(0,0,0,0)
            self.time = mtime.addMSecs(self.mediaPlayer.position())
            self.lbl.setText(self.time.toString())
###################################################################

def stylesheet(self):
    return """

QSlider::handle:horizontal 
{
background: transparent;
width: 8px;
}

QSlider::groove:horizontal {
border: 1px solid #444444;
height: 8px;
     background: qlineargradient(y1: 0, y2: 1,
                                 stop: 0 #2e3436, stop: 1.0 #000000);
}

QSlider::sub-page:horizontal {
background: qlineargradient( y1: 0, y2: 1,
    stop: 0 #729fcf, stop: 1 #2a82da);
border: 1px solid #777;
height: 8px;
}

QSlider::handle:horizontal:hover {
background: #2a82da;
height: 8px;
width: 8px;
border: 1px solid #2e3436;
}

QSlider::sub-page:horizontal:disabled {
background: #bbbbbb;
border-color: #999999;
}

QSlider::add-page:horizontal:disabled {
background: #2a82da;
border-color: #999999;
}

QSlider::handle:horizontal:disabled {
background: #2a82da;
}

QLineEdit
{
background: black;
color: #585858;
border: 0px solid #076100;
font-size: 8pt;
font-weight: bold;
}
    """

if __name__ == '__main__':

    app = QApplication(sys.argv)
    player = VideoPlayer('')
    player.setAcceptDrops(True)
    player.setWindowTitle("QT5 Player")
    player.setWindowIcon(QIcon.fromTheme("multimedia-video-player"))
    player.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    player.setGeometry(100, 300, 600, 380)
    player.setContextMenuPolicy(Qt.CustomContextMenu);
    player.customContextMenuRequested[QPoint].connect(player.contextMenuRequested)
    player.hideSlider()
    player.show()
    player.widescreen = True
    if len(sys.argv) > 1:
        print(sys.argv[1])
        if sys.argv[1].startswith("http"):
            player.myurl = sys.argv[1]
            player.playFromURL()
        else:
            player.loadFilm(sys.argv[1])
sys.exit(app.exec_())
