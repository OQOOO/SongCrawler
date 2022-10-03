import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import webbrowser
from bs4 import BeautifulSoup
import requests
import random

import songListDC

def resSoup(url): # url -> html 전환 함수
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup

pvSongs = set()
form_class = uic.loadUiType("ui.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_searchSong.clicked.connect(self.searchSongDef)
        self.btn_YtbOpen.clicked.connect(self.YtbOpen)
        self.btn_RandYtbOpen.clicked.connect(self.RandOpen)
        self.btn_dcincide.clicked.connect(self.dcOpen)

    #-------------------------------------------------------
    def searchSongDef(self):
        first = self.spinBoxPage.value()
        last = self.spinBoxPage_2.value()

        self.textList, self.songList = songListDC.searchSongDC(first, last)
        self.textBrowser.clear()

        for i in self.textList:
            self.textBrowser.append(i)


    def YtbOpen(self):
        a = self.spinBoxYtbOpen.value()
        song = self.songList[a-1]

        webbrowser.open(song)
        self.label_Nowlisten.setText(str(self.songList.index(song)+1))


    def RandOpen(self):
        while 1:
            rand = random.randrange(0, len(self.songList))
            if rand not in pvSongs:
                song = self.songList[rand]
                pvSongs.add(rand)
                
                if len(pvSongs) == len(self.songList):
                    pvSongs.clear()
                break

        webbrowser.open(song)
        self.label_Nowlisten.setText(str(self.songList.index(song)+1))

    def dcOpen(self):
        webbrowser.open("https://search.dcinside.com/post/p/1%7Bi%7D/sort/latest/q/.EC.A7.80.EB.93.A3.EB.85.B8")

    #-------------------------------------------------------

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()