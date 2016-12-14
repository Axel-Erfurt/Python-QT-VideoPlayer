from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSizePolicy, QListWidget, QListWidgetItem, \
QMenu, QTableWidget, QFileDialog, QAction, QCursor
from PyQt4.phonon import Phonon
from PyQt4.Qt import QSize, QString, Qt, QStatusBar, QIcon, QImage, QGraphicsOpacityEffect, QMessageBox
from PyQt4.QtCore import QPoint

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.media = Phonon.MediaObject(self)
        ### video widget ####
        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(320,200)
        self.myfilename = ""
        self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), self), QtCore.SIGNAL('activated()'), self.handlePlayButton)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("o"), self), QtCore.SIGNAL('activated()'), self.handleButton)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("q"), self), QtCore.SIGNAL('activated()'), self.handleQuit)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("f"), self), QtCore.SIGNAL('activated()'), self.handleFullscreen)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("s"), self), QtCore.SIGNAL('activated()'), self.toggleSlider)
        self.connect(QtGui.QShortcut(QtGui.QKeySequence("i"), self), QtCore.SIGNAL('activated()'), self.handleInfo)
	
		### context menu ####
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popup2)
		
        ### seek slider ###
        self.slider = Phonon.SeekSlider(self.media)
        self.slider.setStyleSheet(stylesheet(self))
        isize = QSize(16,16)
        self.slider.setFixedHeight(8)
        self.slider.setIconSize(isize)
        self.slider.hide()

        ### connection position to label ###
        self.media.isSeekable()

        ### layout ###
        layout = QtGui.QGridLayout(self)
        layout.setMargin(1)
        layout.addWidget(self.video, 0, 0, 1, 1)
        layout.addWidget(self.slider, 0, 0, 1, 1)
        layout.setColumnStretch (0, 1)
        layout.setRowStretch (0, 0)
        layout.setHorizontalSpacing(6)
	
        #self.createPopup()
	
    def handleButton(self):
        if self.media.state() == Phonon.PlayingState:
	        self.media.stop()
	        self.loadFile()
        else:
	        self.loadFile()

    def handlePlayButton(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.pause()
        else:
            self.media.play()
	
    def handleQuit(self):
        app.quit()

    def handleFullscreen(self):
        if self.windowState() & QtCore.Qt.WindowFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
	
    def wheelEvent(self,event):
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mscale = event.delta() / 5
        self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.778) 
	
    def loadpopup(self, pos):
        lmenu = QMenu()
        loadAction = lmenu.addAction("Video laden")
        action = lmenu.exec_(self.mapToGlobal(pos))
        if action == loadAction:
            self.handleButton()

    def popup2(self, pos):	
        contextmenu = QMenu()
        contextmenu.addAction("Play / Pause (SPACE)", self.handlePlayButton)
        contextmenu.addSeparator()
        contextmenu.addAction("Load Video (o)", self.handleButton)
        contextmenu.addAction("Toggle Slider (s)", self.toggleSlider)
        contextmenu.addSeparator()
        contextmenu.addAction("Information (i)", self.handleInfo)
        contextmenu.addSeparator()
        contextmenu.addAction("Exit (q)", self.handleQuit)
        contextmenu.exec_(QCursor.pos())
	
    def toggleSlider(self):	
        if self.slider.isVisible():
            self.slider.hide()
        else:
            self.slider.show()
            self.slider.setGeometry(10, self.frameGeometry().height() - 20, self.frameGeometry().width() - 20, 14)
            self.slider.setFocus()
	
    def handleInfo(self):
            msg = QMessageBox()
            #msg.setFixedSize(500, 300)
            #msg.setGeometry(100,100, 400, 200)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Axel Schneider")
            msg.setInformativeText(unicode("2016"))
            msg.setWindowTitle("Phonon Player")
            msg.setDetailedText("use Mouse Wheel for Zoom")
            msg.setStandardButtons(QMessageBox.Ok)
	
            retval = msg.exec_()
            print "value of pressed message box button:", retval
	
    def loadFile(self):
            path = QtGui.QFileDialog.getOpenFileName(self, ("Video laden"),
                                                '/Axel_1/Filme',
                                                "Videos (*.mp4 *.ts *.avi *.mpeg *.mpg *.mkv)")
            if path:
	            	#self.myfilename = unicode(path)
                	self.media.setCurrentSource(Phonon.MediaSource(path))
                	self.video.setScaleMode(1)
                	self.video.setAspectRatio(1)
                	self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
                	Phonon.createPath(self.media, self.audio)
                	Phonon.createPath(self.media, self.video)
                	self.slider.hide()
                	self.media.play()

    def mouseMoveEvent(self, event):   
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() \
						- QPoint(self.frameGeometry().width() / 2, \
						self.frameGeometry().height() / 2))
            event.accept() 
	
def stylesheet(self):
        return """
	
Phonon--SeekSlider > QSlider::groove:horizontal 
{
	background: black;
	border: 1px solid #565656;
	height: 4px;
	border-radius: 0px;
}

Phonon--SeekSlider > QSlider::sub-page:horizontal 
{
	background: blue;
	border: 1px solid #565656;
	height: 2px;
	border-radius: 0px;
}
        """

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Phonon Player')
    window = Window()
    window.setGeometry(0,0,720,404)
    #window.setWindowFlags(Qt.WindowStaysOnTopHint)	
    window.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())
