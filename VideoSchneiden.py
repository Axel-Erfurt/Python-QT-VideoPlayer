# -- coding: utf-8 --
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSizePolicy, QListWidget, QListWidgetItem, QMenu, QTableWidget, QFileDialog
from PyQt4.phonon import Phonon
from PyQt4.Qt import QSize, QString, Qt, QStatusBar, QIcon, QImage
from time import time
import os, subprocess
#from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
import numpy as np

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.media = Phonon.MediaObject(self)
        ### video widget ####
        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(320,200)
        self.videoCuts = []
        self.myfilename = ""
        self.extension = ""
        self.t1 = ""
        self.t2 = ""
        self.t3 = ""
        self.t4 = ""
        self.t5 = ""
        self.t6 = ""
	
        ### open button ###
        self.button = QtGui.QPushButton('Choose Video', self)
        self.button.setFixedWidth(90)
        self.button.clicked.connect(self.handleButton)
        self.button.setStyleSheet(stylesheet(self))

        ### play / pause button ###
        self.playbutton = QtGui.QPushButton('Play', self)
        self.playbutton.setFixedWidth(80)
        self.playbutton.clicked.connect(self.handlePlayButton)
        self.playbutton.setStyleSheet(stylesheet(self))
	
	        ### save button ###
        self.savebutton = QtGui.QPushButton('Save', self)
        self.savebutton.setFixedWidth(80)
        self.savebutton.clicked.connect(self.handleSaveVideo)
        self.savebutton.setStyleSheet(stylesheet(self))

        ### seek slider ###
        self.slider = Phonon.SeekSlider(self.media)
        self.slider.setStyleSheet(stylesheet(self))
        isize = QSize(16,16)
        self.slider.setIconSize(isize)
        self.slider.setFocus()
       # self.slider.connect(self.handleLabel)

        ### connection position to label ###
        self.media.isSeekable()
        self.media.tick.connect(self.handleLabel)
        self.media.seekableChanged.connect(self.handleLabel)
        #self.slider.wheel.connect(self.handleLabel)

        ### table view ###
        self.iconList = QListWidget()
        self.iconList.setAlternatingRowColors(True)
        self.iconList.setFixedWidth(200)
        self.iconList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.iconList.setStyleSheet("QListWidget::item:selected:active { background: #7D8ED9; color:#FFFFFF; } ")
        self.iconList.setViewMode(0)
        self.iconList.setSelectionBehavior(1)
        self.iconList.setIconSize(QSize(80, 80/1.78))
        self._hookListActions()
        self.iconList.customContextMenuRequested.connect(self._openListMenu)

		### set start button ###
        self.startbutton = QtGui.QPushButton('set Start', self)
        self.startbutton.setFixedWidth(80)
        self.startbutton.clicked.connect(self.handleStartButton)
        self.startbutton.setStyleSheet(stylesheet(self))

		### set end button ###
        self.endbutton = QtGui.QPushButton('set End', self)
        self.endbutton.setFixedWidth(80)
        self.endbutton.clicked.connect(self.handleEndButton)
        self.endbutton.setStyleSheet(stylesheet(self))

		### label ###
        self.mlabel = QtGui.QLabel('Frame', self)
        #self.mlabel.setFixedWidth(80)

        ### layout ###
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.iconList, 0, 0, 1, 1)
        layout.addWidget(self.video, 0, 1, 1, 6)
        layout.addWidget(self.slider, 1, 1, 1, 6)
        layout.addWidget(self.button, 2, 0, 1, 1)
        layout.addWidget(self.savebutton, 2, 1, 1, 1)
        layout.addWidget(self.playbutton, 2, 3, 1, 1)
        layout.addWidget(self.startbutton, 2, 5, 1, 1)
        layout.addWidget(self.endbutton, 2, 6, 1, 1)
        layout.addWidget(self.mlabel, 2, 4, 1, 1)

    def handleButton(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self, ("Video laden"),
                                                '/Axel_1/Filme',
                                                "Videos (*.ts *.mp4)")
            if path:
                self.myfilename = unicode(path) #.encode("utf-8")
                window.setWindowTitle(self.myfilename)
                self.extension = path.split(".")[1]
                print(self.extension)
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.video.setScaleMode(1)
                self.video.setAspectRatio(1)
                self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
                Phonon.createPath(self.media, self.audio)
                Phonon.createPath(self.media, self.video)
                self.media.play()
                self.playbutton.setText('Pause')
	
    def handleSaveVideo(self):
	                result = QFileDialog.getSaveFileName(self, ("Video speichern"),
                                                '/tmp/film.' + str(self.extension),
                                                "Videos (*.ts *.mp4)")
		    	if result:
	                    target = unicode(result)
	            	self.t1 = float(self.videoCuts[0])
	            	self.t2 = float(self.videoCuts[1])
		    	ffmpeg_extract_subclip(self.myfilename, self.t1, self.t2, targetname=target)	
		    	window.setWindowTitle("Film gespeichert")
	                self.purgeMarker()

    def handlePlayButton(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.pause()
            self.playbutton.setText('Play')

        else:
            #print(self.iconList.count())
            self.media.play()
            self.playbutton.setText('Pause')

    def handleStartButton(self):
            rm = str(self.media.currentTime() / 100.00 / 10.00)
            item = QListWidgetItem()
            img = QImage(self.video.snapshot())
            pix = QtGui.QPixmap.fromImage(img)
            item.setIcon(QIcon(pix))
            item.setText("Start: " + rm)
            self.iconList.addItem(item)
            self.videoCuts.append(rm)

    def handleEndButton(self):
            rm = str(self.media.currentTime() / 100.00 / 10.00)
            item = QListWidgetItem()
            #item.setSizeHint(QSize(150, 40))
            img = QImage(self.video.snapshot())
            pix = QtGui.QPixmap.fromImage(img)
            item.setIcon(QIcon(pix))
            item.setText("End: " + rm)
            self.iconList.addItem(item)
            self.videoCuts.append(rm)
            self.t3 = float(str(self.media.remainingTime()))
            print(self.t3)
            self.media.stop()
            self.playbutton.setText('Play')

    def handleLabel(self):
            self.mlabel.setText(str(self.media.currentTime() / 100.00 / 10.00))
            #self.mlabel.setText(str(self.media.currentTime() / 1000 / 60 / 60) \
			#+ ":" + str(self.media.currentTime() / 1000 / 60) \
			#+ ":" + str(self.media.currentTime() / 1000%60))

    def _hookListActions(self):
        #TOO bad-the list model -should be here... 
        rmAction = QtGui.QAction(QtGui.QIcon('icons/close-x.png'), 'entfernen', self)
        rmAction.triggered.connect(self._removeMarker)
        rmAllAction = QtGui.QAction(QtGui.QIcon('icons/clear-all.png'), 'alle entfernen', self)
        rmAllAction.triggered.connect(self.purgeMarker)
        self.gotoAction = QtGui.QAction(QtGui.QIcon('icons/go-next.png'), 'zu dieser Position springen', self)
        self.gotoAction.triggered.connect(self._gotoFromMarker)
  
        #menus      
        self._listMenu = QMenu()
        self._listMenu.addAction(self.gotoAction)
        self._listMenu.addSeparator()
        self._listMenu.addAction(rmAction)
        self._listMenu.addAction(rmAllAction)

    #---List widget context menu
    def _removeMarker(self,whatis):
        selectionList = self.iconList.selectedIndexes()
        if len(selectionList)==0:
            return
        item = selectionList[0]
        self.iconList.takeItem(item.row())
        #self.videoCuts.remove[1])
  
    def clearMarkerList(self):
        self.iconList.clear()

    #remove contents, remove file 
    def purgeMarker(self):
        self.iconList.clear()
        self.videoCuts = []
        
    def _gotoFromMarker(self,whatis):
        selectionList = self.iconList.selectedIndexes()
        if len(selectionList)==0:
            return
        item = selectionList[0]
        pos = item.data().toString().replace("Start: ", "").replace("End: ", "")
        #frame = pos.ToInt()
        #self.video.currentTime = 1589
        self.setWindowTitle(pos)

    def _openListMenu(self,position):
        selectionList = self.iconList.selectedIndexes()
        if len(selectionList)==0:
            return
        self._listMenu.exec_(self.iconList.viewport().mapToGlobal(position)) 

def stylesheet(self):
        return """
Phonon--SeekSlider > QSlider::groove:horizontal 
{
	border: 1px solid #bbb;
	background: white;
	height: 6px;
	border-radius: 4px;
}

Phonon--SeekSlider > QSlider::sub-page:horizontal 
{
	background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
    stop: 0 #66e, stop: 1 #bbf);
	background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
    stop: 0 #bbf, stop: 1 #55f);
	border: 1px solid #777;
	height: 6px;
	border-radius: 4px;
}

Phonon--SeekSlider > QSlider::add-page:horizontal 
{
	background: #fff;
	border: 1px solid #777;
	height: 6px;
	border-radius: 4px;
}

Phonon--SeekSlider > QSlider::handle:horizontal 
{
	background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #eee, stop:1 #ccc);
	border: 1px solid #777;
	width: 15px;
	margin-top: -2px;
	margin-bottom: -2px;
	border-radius: 4px;
}

Phonon--SeekSlider > QSlider::handle:horizontal:hover 
{
	background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #fff, stop:1 #ddd);
	border: 1px solid #444;
	border-radius: 4px;
}

Phonon--SeekSlider > QSlider::sub-page:horizontal:disabled 
{
	background: #bbb;
	border-color: #999;
}

Phonon--SeekSlider > QSlider::add-page:horizontal:disabled 
{
	background: #eee;
	border-color: #999;
}

Phonon--SeekSlider > QSlider::handle:horizontal:disabled 
{
	background: #eee;
	border: 1px solid #aaa;
	border-radius: 4px;
}

Phonon--SeekSlider > QSlider::hover
{
    border-width: 2px;
    border-style: solid;
    border-color: blue;
	background: gold;
	border-radius: 8px;
}

QPushButton
{	
	font-size: 11px;
	border: 3px outset grey;
	border-radius: 4px;
	height: 24px;
	color: black;
	background-color: lightgrey;
	background-position: bottom-left;
} 

QPushButton::hover
{
	font-weight: bold;
	color: white;
	background-color: green;
} 

        """
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Cut_TS')
    window = Window()
    window.setWindowTitle('Cut TS Video')
    window.setGeometry(100,250,720,450)
    window.show()
    sys.exit(app.exec_())