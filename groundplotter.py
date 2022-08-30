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



#rotate grid
# temp_list_2 = []
# for i in range(len(y_axis_list[0])):
#     temp_list = []
#     for j in range(len(y_axis_list)):
#         temp_list.append(y_axis_list[j][i])
#     temp_list_2.append(temp_list)
    
# y_axis_list = temp_list_2

#settings
candela_to_lux_modifier = 10.76391 #10.76391for feet only, not required for meters

#reverse ground project calculations
height = 8
y_tilt = 0
x_tilt = 0

increments = 1
x_distance = 100
x_range = int(x_distance/increments)
z_distance = 150
z_range = int(z_distance/increments)*2

starting_x_deg = -45
starting_y_deg = 45
ending_x_deg = 45
ending_y_deg = -45
degrees_increment = 1
# angle_increment = 1
element_count = len(y_axis_list)
projection_list = []

for x in range(1,x_range+1):
    x=x*increments
    for z in range(z_range):
        z=-z_distance+z*increments
        theta_x = math.degrees(math.atan(z/x))-x_tilt
        theta_y = -90+math.degrees(math.atan(x/height))-y_tilt
        x_th_1, x_th_2 = 0, 0
        y_th_1, y_th_2 = 0, 0
        if theta_y >= ending_y_deg and theta_x >= starting_x_deg and theta_x <= ending_x_deg:
            for xth in range(element_count):
                angle = starting_x_deg + xth*degrees_increment
                #print(angle)
                if theta_x==angle:
                    x_th_1 = xth
                    x_th_2 = xth
                    break
                if theta_x < 0:
                    if theta_x < angle and angle<=0:
                        x_th_1 = xth
                        x_th_2 = xth-1
                        #print("x - negative",angle,theta_x, -45+x_th_1*15,-45+x_th_2*15)
                        break
                else:
                    if theta_x <= angle and angle>=0:
                        x_th_1 = xth
                        x_th_2 = xth-1
                        #print("x - positive",angle,theta_x,-45+x_th_1*15,-45+x_th_2*15)
                        break
            for yth in range(element_count):
                angle = starting_y_deg - yth*degrees_increment
                #print(angle)
                if theta_y==angle:
                    y_th_1 = yth
                    y_th_2 = yth
                    break
                if theta_y < 0:
                    if theta_y > angle and angle<=0:
                        y_th_1 = yth
                        y_th_2 = yth-1
                        #print("y - negative",angle,theta_y, 45-y_th_1*15,45-y_th_2*15)
                        break
                else:
                    if theta_y >= angle and angle>=0:
                        y_th_1 = yth
                        y_th_2 = yth-1
                        #print("y - positive",angle,theta_y,-90+y_th*2)
                        break
            
            #averaged linear interpolation
            #interpolating by x axis
            interpolation_level = 1
            interpolation_steps = degrees_increment * interpolation_level
            c_x_increment_1 = float(y_axis_list[y_th_1][x_th_1])-float(y_axis_list[y_th_1][x_th_2])
            c_x_increment_2 = float(y_axis_list[y_th_2][x_th_1])-float(y_axis_list[y_th_2][x_th_2])
            c_x_increment_1 = c_x_increment_1 / interpolation_steps
            c_x_increment_2 = c_x_increment_2 / interpolation_steps
            
            x_dif = theta_x-(starting_x_deg+x_th_1*degrees_increment)
            if x_dif>0:
                c_x_1 = float(y_axis_list[y_th_1][x_th_2]) + (x_dif * c_x_increment_1)
                c_x_2 = float(y_axis_list[y_th_2][x_th_2]) + (x_dif * c_x_increment_2)
            else:
                c_x_1 = float(y_axis_list[y_th_1][x_th_1]) + (x_dif  * c_x_increment_1)
                c_x_2 = float(y_axis_list[y_th_2][x_th_1]) + (x_dif  * c_x_increment_2)
            
            c_y_increment = c_x_2 - c_x_1
            c_y_increment = c_y_increment / interpolation_steps
            
            y_dif = theta_y - (starting_y_deg-y_th_1*degrees_increment) 
            c_y = c_x_1 + (c_y_increment * interpolation_level * y_dif)
            candela = c_y
            #print("calc thetas",theta_x, theta_y,"list theta x,x2",(starting_x_deg+x_th_1*degrees_increment), (starting_x_deg+x_th_2*degrees_increment),"list theta y,y2",(starting_y_deg-y_th_1*degrees_increment), (starting_y_deg-y_th_2*degrees_increment),"dif data x,y",x_dif, y_dif, c_x_increment_1,c_x_increment_2,"x candela", c_x_1, c_x_2,"final candela",c_y,"set 1", y_axis_list[y_th_1][x_th_1], y_axis_list[y_th_1][x_th_2],"set 2", y_axis_list[y_th_2][x_th_1], y_axis_list[y_th_2][x_th_2])
            
            # candela = y_axis_list[y_th_1][x_th_1]
            d = math.sqrt((height**2)+(x**2)+(z**2))
            lux = (float(candela)*candela_to_lux_modifier)/(d**2)
            if z ==0 and x%2==0:
                print("calculated theta:",theta_x,theta_y,"list theta",starting_x_deg+x_th_1*degrees_increment,starting_y_deg-y_th_1*degrees_increment,"z,x",z,x,"interpolated candela",candela,c_x_1, c_x_2,"distance",d,"lux",lux,"original candelas",starting_x_deg+x_th_1*degrees_increment,starting_y_deg-y_th_1*degrees_increment, y_axis_list[y_th_1][x_th_1],starting_x_deg+x_th_2*degrees_increment,starting_y_deg-y_th_1*degrees_increment,y_axis_list[y_th_1][x_th_2],starting_x_deg+x_th_1*degrees_increment,starting_y_deg-y_th_2*degrees_increment,y_axis_list[y_th_2][x_th_1],starting_x_deg+x_th_2*degrees_increment,starting_y_deg-y_th_2*degrees_increment,y_axis_list[y_th_2][x_th_2])
            #print("calculated theta:",theta_x,theta_y,"list theta x",-90+x_th_1*2,-90+x_th_2*2,"list theta y",-90+y_th_1*2,-90+y_th_2*2,"z,x",z,x,"candela",candela,d,lux)
            projection_list.append((z,x,lux))
            
class LuxPlotter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.height=900
        self.width=900
        layout = QtWidgets.QVBoxLayout()
        #renderer = RenderPlane(self)
        #renderer = RenderWallProjection(self)
        renderer = RenderGroundProjection(self)
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
        
        
class RenderGroundProjection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.label = QtWidgets.QLabel()
        self.parent=parent
        #canvas = QtGui.QPixmap(400,300)
        #self.label.setPixmap(canvas)
        # self.width = parent.geometry().width()
        self.scale = 1.25
        self.offsetx =50
        self.offsety = 50
        self.xrange = 300
        self.yrange = 300
        self.width = self.xrange*2+100
        self.height = self.yrange*2+100
        
    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        
        #painter.begin(self)
        painter.scale(self.scale, self.scale)
        
        #draw points
        pixel_size = 2
        for lux_item in projection_list:
            # x = x * increments
            x = lux_item[0]
            y = lux_item[1]
            #lux = lux_item[2]
            if y < self.yrange and y > -self.yrange and x<self.xrange and x>-self.xrange:
                if lux_item[2]>0 and lux_item[2] <= 10:
                    pen = QtGui.QPen(QtGui.QColor(0,0,int((lux_item[2]/10)*255)),pixel_size)
                elif lux_item[2] >10 and lux_item[2] <= 25:
                    pen = QtGui.QPen(QtGui.QColor(0,int((lux_item[2]/25)*255),0),pixel_size)
                elif lux_item[2] >25 and lux_item[2] <= 50:
                    pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/50)*10),0),pixel_size)
                elif lux_item[2] >50 and lux_item[2] <= 100:
                    pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/100)*165),0),pixel_size)
                elif lux_item[2] >100 and lux_item[2] <= 200:
                    pen = QtGui.QPen(QtGui.QColor(255,150-int(((lux_item[2])/200)*150),0),pixel_size)
                else:
                    pen = QtGui.QPen(QtCore.Qt.white,pixel_size)
                painter.setPen(pen)
                painter.drawPoint(x*2+self.offsetx+self.xrange, self.height-self.offsety-y*2)

        #draw axis
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        #+y
        point1 = QtCore.QPointF(self.offsetx, self.height-self.offsety-self.yrange*2)
        point2 = QtCore.QPointF(self.offsetx, self.height-self.offsety)
        line1 = QtCore.QLineF(point1, point2)
        painter.drawLine(line1)
        #-y
        # point1 = QtCore.QPointF(self.offsetx+self.xrange, self.height-self.offsety+self.yrange*2)
        # point2 = QtCore.QPointF(self.offsetx+self.xrange, self.height-self.offsety)
        # line1 = QtCore.QLineF(point1, point2)
        # painter.drawLine(line1)
        #x
        point1 = QtCore.QPointF(self.offsetx, self.height-self.offsety)
        point2 = QtCore.QPointF(self.width-self.offsetx, self.height-self.offsety)
        line1 = QtCore.QLineF(point1, point2)
        painter.drawLine(line1)


        #draw markers
        #x axis
        for i in range(self.xrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,self.height-self.offsety,self.offsetx+i,self.height-self.offsety+10)
                painter.drawText(QtCore.QPointF(self.offsetx+(i)-15, self.height-self.offsety+30),str(-self.xrange/2+i/2))
        painter.drawText(QtCore.QPointF(self.width/2-40, self.height-5),"X Distance (ft.)")
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx-5,self.height-self.offsety-i,self.offsetx,self.height-self.offsety-i)
                painter.drawText(QtCore.QPointF(self.offsetx-40, self.height-self.offsety-i+5),str(i/2))
        painter.drawText(QtCore.QPointF(5, 25),"Y Distance (ft.)")
        
        #draw title
        painter.drawText(QtCore.QPointF(self.width/2-self.offsetx-25, 10),f"Ground Plot at {height} ft. from ground, tilted at {y_tilt} degs")
        painter.end()
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    w = LuxPlotter()
    w.show()
    app.exec()