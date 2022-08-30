import os, sys
import math
from PySide6 import QtCore, QtGui, QtWidgets

f_path = "flood_values.csv"

y_axis_list = []

with open(f_path) as f:
    for line in f:
        line = line.strip("\n")
        y_axis_list.append(line.split(","))
        
x_lux_list = []


# temp_list_2 = []
# #rotate grid
# for i in range(len(y_axis_list[0])):
#     temp_list = []
#     for j in range(len(y_axis_list)):
#         temp_list.append(y_axis_list[j][i])
#     temp_list_2.append(temp_list)
    
# y_axis_list = temp_list_2

#settings
increments = 1
#max_distance = 300 #max x distance
interval = 2 #x distance increment
candela_to_lux_modifier = 10.76391 #10.76391for feet only, not required for meters
#tilt_adjust = 0

# x_range = int(max_distance/increments)

#wall projection calculation
wall_distance = 30
interval = 2
y_counter = 0
x_tilt = 0
y_tilt = 0
projection_list=[]
for x_values in y_axis_list:
    y_angle = -90 + y_counter*interval+y_tilt
    x_counter=0
    for candela in x_values:
        x_angle = -90 + x_counter*interval+x_tilt
        #print(y_angle, x_angle, candela)
        y = math.tan(y_angle * math.pi / 180) * wall_distance
        z = math.tan(x_angle * math.pi / 180) * wall_distance
        d = math.sqrt(wall_distance**2+y**2+z**2)
        lux = (float(candela)*candela_to_lux_modifier)/(d**2)
        #print(z,y,lux)
        projection_list.append((z,y,lux))
        x_counter+=1
    y_counter+=1


class LuxPlotter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.height=900
        self.width=900
        layout = QtWidgets.QVBoxLayout()
        #renderer = RenderPlane(self)
        renderer = RenderWallProjection(self)
        #renderer = RenderGroundProjection(self)
        layout.addWidget(renderer)
        self.setLayout(layout)
        self.setGeometry(0, 0, self.width, self.height)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setStyleSheet("background:black")
        self.center()
        self.setWindowTitle('IES to Lux Plotter')
        self.show()
        
    def center(self):
        window = self.window()
        window.setGeometry(
            QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight,
            QtCore.Qt.AlignCenter,
            window.size(),
            QtGui.QGuiApplication.primaryScreen().availableGeometry(),
        ),
    )

        
class RenderWallProjection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.label = QtWidgets.QLabel()
        self.parent=parent
        #canvas = QtGui.QPixmap(400,300)
        #self.label.setPixmap(canvas)
        # self.width = parent.geometry().width()
        self.scale =1.25
        self.offsetx =50
        self.offsety = 50
        self.xrange = 300
        self.yrange = 150
        self.width = self.xrange*2+100
        self.height = self.yrange*2+100
        
    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        
        #painter.begin(self)
        painter.scale(self.scale, self.scale)
        
        #draw points
        pixel_size = 4
        for lux_item in projection_list:
            # x = x * increments
            x = lux_item[0]
            y = lux_item[1]
            #lux = lux_item[2]
            if y < self.yrange and y > -self.yrange and x<self.xrange and x>-self.xrange:
                if lux_item[2]>0 and lux_item[2] < 25:
                    pen = QtGui.QPen(QtGui.QColor(0,0,int((lux_item[2]/25)*255)),pixel_size)
                elif lux_item[2] >25 and lux_item[2] < 50:
                    pen = QtGui.QPen(QtGui.QColor(0,int((lux_item[2]/50)*255),0),pixel_size)
                elif lux_item[2] >50 and lux_item[2] < 100:
                    pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/50)*10),0),pixel_size)
                elif lux_item[2] >100 and lux_item[2] < 250:
                    pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/250)*165),0),pixel_size)
                elif lux_item[2] >250 and lux_item[2] < 1000:
                    pen = QtGui.QPen(QtGui.QColor(255,80-int(((lux_item[2])/1000)*80),0),pixel_size)
                else:
                    pen = QtGui.QPen(QtCore.Qt.white,pixel_size)
                painter.setPen(pen)
                painter.drawPoint(x*2+self.offsetx+self.xrange, self.height-self.offsety-y*2)

        #draw axis
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        #+y
        # point1 = QtCore.QPointF(self.offsetx+self.xrange, self.height-self.offsety-self.yrange*2)
        # point2 = QtCore.QPointF(self.offsetx+self.xrange, self.height-self.offsety)
        # line1 = QtCore.QLineF(point1, point2)
        # painter.drawLine(line1)
        # #-y
        # point1 = QtCore.QPointF(self.offsetx+self.xrange, self.height-self.offsety+self.yrange*2)
        # point2 = QtCore.QPointF(self.offsetx+self.xrange, self.height-self.offsety)
        # line1 = QtCore.QLineF(point1, point2)
        # painter.drawLine(line1)
        #x
        # point1 = QtCore.QPointF(self.offsetx, self.height-self.offsety)
        # point2 = QtCore.QPointF(self.width-self.offsetx, self.height-self.offsety)
        # line1 = QtCore.QLineF(point1, point2)
        # painter.drawLine(line1)


        #draw markers
        #x axis
        for i in range(self.xrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,self.height-self.offsety+self.yrange*2,self.offsetx+i,self.height-self.offsety+self.yrange*2+10)
                painter.drawText(QtCore.QPointF(self.offsetx+(i)-15, self.height-self.offsety+self.yrange*2+30),str(-self.xrange/2+i/2))
        painter.drawText(QtCore.QPointF(self.width/2-40, self.height+self.yrange*2-5),"X Distance (ft.)")
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx-5,self.height-self.offsety-i,self.offsetx,self.height-self.offsety-i)
                painter.drawText(QtCore.QPointF(self.offsetx-40, self.height-self.offsety-i+5),str(i/2))
        #-yaxis
        for i in range(self.yrange*2+1):
            if i !=0:
                if i%(50)==0:
                    painter.drawLine(self.offsetx-5,self.height-self.offsety+i,self.offsetx,self.height-self.offsety+i)
                    painter.drawText(QtCore.QPointF(self.offsetx-40, self.height-self.offsety+i+5),"-"+str(i/2))
        painter.drawText(QtCore.QPointF(5, 25),"Y Distance (ft.)")
        
        #draw title
        painter.drawText(QtCore.QPointF(self.width/2-self.offsetx-25, 10),f"wall Plot at {wall_distance} ft. from source, tilted at {y_tilt} degs")
        
        painter.end()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    w = LuxPlotter()
    w.show()
    app.exec_()