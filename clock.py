# -*- coding : utf-8-*-

import sys
from PyQt5 import  QtGui, QtWidgets, QtCore
from random import *
from datetime import *
from time import sleep
from threading import Thread

onColor = QtGui.QColor(205, 213, 229)
offColor = QtGui.QColor(69, 76, 90)

threadOn = True

class noBorder(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.border_width = 8
        self.roundAngle = 15
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window | QtCore.Qt.SplashScreen)
    
    def mousePressEvent(self, e):
        if e.button()==QtCore.Qt.LeftButton:
            self.dragging = True
            self.dragPos = e.globalPos() - self.pos()
            e.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
    
    def mouseReleaseEvent(self, e):
        if e.button()==QtCore.Qt.LeftButton:
            self.dragging = False
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    
    def mouseMoveEvent(self, e):
        if self.dragging and QtCore.Qt.LeftButton:
            self.move(e.globalPos()-self.dragPos)
            e.accept()
    
    def keyPressEvent(self, e):
        global threadOn
        if e.key()==QtCore.Qt.Key_Escape:
            threadOn = False
            sys.exit(app.exec_())
    
    def paintEvent(self, e):
        path = QtGui.QPainterPath()
        path.setFillRule(QtCore.Qt.WindingFill)
        
        shadow = QtGui.QColor(20, 20, 20, 50)
        inner = QtGui.QColor(40, 44, 52, 230)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        painter.fillPath(path, QtGui.QBrush(inner))

        for i in range(10):
            i_path = QtGui.QPainterPath()
            i_path.setFillRule(QtCore.Qt.WindingFill)
            ref = QtCore.QRectF(10-i, 10-i, self.width()-2*(10-i), self.height()-2*(10-i))
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            shadow.setAlpha(int(150-i**0.5*50))
            painter.setPen(shadow)
            painter.drawPath(i_path)
        
        painter2 = QtGui.QPainter(self)
        painter2.setRenderHint(painter.Antialiasing)
        painter2.setBrush(inner)
        painter2.setPen(QtCore.Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width()-9)
        rect.setHeight(rect.height()-9)
        painter2.drawRoundedRect(rect, self.roundAngle, self.roundAngle)

class noBorderWin(noBorder, QtWidgets.QWidget):
    def __init__(self):
        super(noBorderWin, self).__init__()

class clockText(QtWidgets.QWidget):
    def __init__(self, parent, char):
        self.char = char
        self.state = True
        super().__init__(parent)

    def on(self):
        self.state = True
        self.repaint()

    def off(self):
        self.state = False
        self.repaint()
    
    def paintEvent(self, e): 
        painter = QtGui.QPainter(self)

        pen = QtGui.QPen()
        pen.setWidth(1)
        if self.state:
            pen.setColor(onColor)
        else:
            pen.setColor(offColor)
        painter.setPen(pen)

        font = QtGui.QFont()
        font.setFamily('Cascadia Code')
        font.setPointSize(11)
        painter.setFont(font)
        
        painter.drawText(100, 100, self.char)

        painter.end() 


app = QtWidgets.QApplication(sys.argv)

window = noBorderWin()
window.resize(500, 500)
window.move(1220, 50)


series = []
for i in range(91-65):
    addChar = chr(i + 65)
    series.append(addChar)
shuffle(series)

clockFace = '''t w e n t y - - i t - i s - - -
- - - f i f t e e n h a p p y -
- t w o e i g h t e e n - o n e
- t - u - v s i x t e e n - - -
t h i r t e e n t - - h a l f -
- r - t w e l v e - - - l o v e
s e v e n t e e n p h y s i c s
- e l e v e n q u a r t e r - -
- n i n e t e e n - m a r r y -
- e - y e a r m i n u t e s - -
- w - p a s t o - - - - s i x -
e l e v e n o n e t h r e e m -
f o u r e i g h t w e l v e a -
- - - y i c h i - o - t e n s -
f i v e o ' c l o c k - n i n e'''.split( )

#16 columns and 15 rows

i = 0
clock = []
for n, c in enumerate(clockFace):
    if c == '-':
        currentChar = series[i%(91-65)]
        i += 1
        s = False
    else:
        currentChar = c.upper()
        s = True
    clock.append(clockText(window, currentChar))
    clock[n].state = False
    clock[n].move(29*(n%16)-73, 31*(n//16)-60)
    clock[n].resize(500, 500)

#test = clockText(window, 'A')
#test.move(0, -50)
#test.resize(500, 500)

#my = MyWidget(window)
#my.move(0,0)
#my.resize(500,500)

lightList = []
oldLightList = []

def lightUp(l):
    global lightList
    lightList.extend(l)

def clockMove():
    global lightList, oldLightList, threadOn
    #countdown = 0
    t = datetime.today()
    oldM = t.minute - 1
    while threadOn:
        t = datetime.today()
        m = t.minute
        h = t.hour % 12
        #print(m, h, oldM)
        '''countdown += 1
        countdown %= 12
        m = countdown%60
        h = countdown'''
        if m==oldM:
            sleep(1)
            continue
        oldM = m
        if m>30:
            h+=1
            h%=12
        if (m>=20 and m<=40 and m!=30):
            lightUp(range(6))
        else:
            lightUp([8, 9, 11, 12])
        if (m==15 and h%2==0) or (m==45 and h%2==1): #fifteen
            lightUp(range(19, 26))
        if m in [2, 22, 38, 58]:
            lightUp(range(33, 36))
        if m in [8, 28, 32, 52]:
            lightUp(range(36, 41))
        if m in [18, 42]:
            lightUp(range(36, 44))
        if m in [1, 21, 39, 59]:
            lightUp(range(45, 48))
        if m in [6, 26, 34, 54]:
            lightUp(range(54, 57))
        if m in [16, 44]:
            lightUp(range(54, 61))
        if m in [4, 24, 36, 56]:
            lightUp([19, 35, 51, 67])
        if m in [14, 46]:
            lightUp([19, 35, 51, 67, 83, 99, 115, 131])
        if m in [5, 25, 35, 55]:
            lightUp([21, 37, 53, 69])
        if m in [3, 23, 37, 57]:
            lightUp([49, 65, 81, 97, 113])
        if m in [13, 47]:
            lightUp(range(64, 72))
        if m in [10, 50]:
            lightUp([72, 88, 104])
        if m==30:
            lightUp(range(75, 79))
        if m in [12, 48]:
            lightUp(range(83, 89))
        if m in [7, 27, 33, 53]:
            lightUp(range(96, 101))
        if m in [17, 43]:
            lightUp(range(96, 105))
        if m in [11, 49]:
            lightUp(range(113, 119))
        if (m==15 and h%2==1) or (m==45 and h%2==0): #quarter
            lightUp(range(119, 126))
            lightUp([76])
        if m in [9, 29, 31, 51]:
            lightUp(range(129, 133))
        if m in [19, 41]:
            lightUp(range(129, 137))
        if m!=0:
            if (not (m in [15, 30, 45])) or (m==15 and h%2==0) or (m==45 and h%2==1):
                lightUp(range(151, 157))
                if m!=1 and m!=59:
                    lightUp([157])
            if m<=30:
                lightUp(range(163, 167))
            else:
                lightUp([166, 167])
        if h==6:
            lightUp(range(172, 175))
        if h==7:
            lightUp([172, 188, 204, 220, 236])
        if h==11:
            lightUp(range(176, 182))
        if h==1:
            lightUp(range(182, 185))
        if h==3:
            lightUp(range(185, 190))
        if h==2:
            lightUp([185, 201, 217])
        if h==4:
            lightUp(range(192, 196))
        if h==8:
            lightUp(range(196, 201))
        if h==0:
            lightUp(range(200, 206))
        if h==10:
            lightUp(range(219, 222))
        if h==5:
            lightUp(range(224, 228))
        if h==9:
            lightUp(range(236, 240))
        if (h!=9 and m==0):
            lightUp(range(228, 235))
        for i in range(len(clock)):
            if (i in oldLightList) and not (i in lightList):
                clock[i].off()
            if not (i in oldLightList) and (i in lightList):
                clock[i].on()
        oldLightList = lightList
        lightList = []
        sleep(1)

t = Thread(target=clockMove)
t.start()
window.show()
sys.exit(app.exec_())