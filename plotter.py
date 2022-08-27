import os, sys
import math
from PySide6 import QtCore, QtGui, QtWidgets

f_path = "raw_values.csv"

y_axis_list = []

with open(f_path) as f:
    for line in f:
        line = line.strip("\n")
        y_axis_list.append(line.split(","))
        
x_lux_list = []


temp_list_2 = []
#rotate grid
for i in range(len(y_axis_list[0])):
    temp_list = []
    for j in range(len(y_axis_list)):
        temp_list.append(y_axis_list[j][i])
    temp_list_2.append(temp_list)
    
y_axis_list = temp_list_2

#settings
increments = 1
max_distance = 300 #max x distance
interval = 2 #x distance increment
candela_to_lux_modifier = 10.76391 #10.76391for feet only, not required for meters
tilt_adjust = 0

x_range = int(max_distance/increments)
#find angular_element
desired_angle = 0
starting_angle = -90
current_angle = -90

angular_element = 0
if desired_angle%2==0:
    while current_angle!=desired_angle:
        current_angle = starting_angle+angular_element*interval
        #print(current_angle)
        angular_element+=1
else:
    print("desired angle needs to be even number")
    
#print(angular_element-1)
angular_element = angular_element-1

#calculate lux at y for x distance for all vertical degrees (-88 to 88) by angular slice
# y_counter = 0
# x_lux_list = []
# for x in range(x_range):
#     x= x+1
#     x = x * increments
#     y_lux_list = []
#     for y_counter in range(len(y_axis_list)):
#         angle = -90+y_counter*interval+tilt_adjust
#         if angle >-90 and angle<90:
#             candela = y_axis_list[y_counter][angular_element]
#             y = math.tan(angle * math.pi / 180) * x
#             d = math.sqrt(x**2+y**2)
#             if angle==0:
#                 lux = (float(candela)*candela_to_lux_modifier)/(x**2)
#             else:
#                 lux = (float(candela)*candela_to_lux_modifier)/(d**2)
#             y_lux_list.append((y,lux))
#     x_lux_list.append(y_lux_list)

#calculate lux at y for x distance for all vertical degrees (-88 to 88) by flattening of values to 1 plane (averaged)
# y_counter = 0
# x_lux_list = []
# for x in range(x_range):
#     x= x+1
#     x = x * increments
#     y_lux_list = []
#     for y_counter in range(len(y_axis_list)):
#         angle = -90+y_counter*interval+tilt_adjust
#         if angle >-90 and angle<90:
#             #candela = y_axis_list[y_counter][angular_element]
#             candela = 0
#             for candela_element in y_axis_list[y_counter]:
#                 candela = candela + int(candela_element)
#             candela = candela/90
#             y = math.tan(angle * math.pi / 180) * x
#             d = math.sqrt(x**2+y**2)
#             if angle==0:
#                 lux = (float(candela)*candela_to_lux_modifier)/(x**2)
#             else:
#                 lux = (float(candela)*candela_to_lux_modifier)/(d**2)
#             y_lux_list.append((y,lux))
#     x_lux_list.append(y_lux_list)

#calculate lux at y for x distance for all horizontal degrees (-88 to 88) by angular slice
# y_counter = 0
# x_lux_list = []
# for x in range(x_range):
#     x= x+1
#     x = x * increments
#     y_lux_list = []
#     for y_counter in range(len(y_axis_list[angular_element])):
#         angle = -90+y_counter*interval+tilt_adjust
#         if angle >-90 and angle<90:
#             candela = y_axis_list[angular_element][y_counter]
#             y = math.tan(angle * math.pi / 180) * x
#             d = math.sqrt(x**2+y**2)
#             if angle==0:
#                 lux = (float(candela)*candela_to_lux_modifier)/(x**2)
#             else:
#                 lux = (float(candela)*candela_to_lux_modifier)/(d**2)
#             y_lux_list.append((y,lux))
#     x_lux_list.append(y_lux_list)

#calculate lux at y for x distance for all horizontal degrees (-88 to 88) by flattening values to 1 plane (averaged)
# y_counter = 0
# x_lux_list = []
# #flattening values to 1 array
# flatten_list = []
# for x in range(len(y_axis_list[0])):
#     sum = 0
#     for y_set in y_axis_list:
#         sum+=int(y_set[x])
#     flatten_list.append(sum)    
# for x in range(x_range):
#     x= x+1
#     x = x * increments
#     y_lux_list = []
#     for y_counter in range(len(flatten_list)):
#         angle = -90+y_counter*interval+tilt_adjust
#         if angle >-90 and angle<90:
#             candela = flatten_list[y_counter]/90
#             y = math.tan(angle * math.pi / 180) * x
#             d = math.sqrt(x**2+y**2)
#             if angle==0:
#                 lux = (float(candela)*candela_to_lux_modifier)/(x**2)
#             else:
#                 lux = (float(candela)*candela_to_lux_modifier)/(d**2)
#             y_lux_list.append((y,lux))
#     x_lux_list.append(y_lux_list)

#wall projection calculation
# wall_distance = 30
# interval = 2
# y_counter = 0
# x_tilt = 0
# y_tilt = 0
# projection_list=[]
# for x_values in y_axis_list:
#     y_angle = -90 + y_counter*interval+x_tilt
#     x_counter=0
#     for candela in x_values:
#         x_angle = -90 + x_counter*interval+y_tilt
#         #print(y_angle, x_angle, candela)
#         y = math.tan(y_angle * math.pi / 180) * wall_distance
#         z = math.tan(x_angle * math.pi / 180) * wall_distance
#         d = math.sqrt(wall_distance**2+y**2+z**2)
#         lux = (float(candela)*candela_to_lux_modifier)/(d**2)
#         #print(z,y,lux)
#         projection_list.append((z,y,lux))
#         x_counter+=1
#     y_counter+=1

#ground projection calculations
# height = 8
# y_tilt =-0
# x_tilt = 0
# y_counter = 0
# projection_list = []
# y_angle_limit = math.degrees(math.atan(height/max_distance))
# print(y_angle_limit)
# for x_values in y_axis_list:
#     y_angle = -90 + y_counter*interval+y_tilt
#     if y_angle<=-y_angle_limit and y_angle>-90:
#         x_counter=0
#         for candela in x_values:
#             x_angle = -90 + x_counter*interval+x_tilt
#             if x_angle<90 and x_angle>-90:
#             #print(y_angle, x_angle, candela)
#                 x = math.tan(((90+y_angle) * math.pi) / 180) * height
#                 z = math.tan((x_angle * math.pi) / 180) * x
#                 d = math.sqrt(height**2+x**2+z**2)
#                 lux = (float(candela)*candela_to_lux_modifier)/(d**2)
#                 #print(y_angle,x_angle,candela,d,z,x,lux)
#                 projection_list.append((z,x,lux))
#             x_counter+=1
#     y_counter+=1
    
#reverse ground project calculations
height = 8
y_tilt = 0
x_tilt = 0

increments = 1
x_distance = 300
x_range = int(x_distance/increments)
z_distance = 150
z_range = int(z_distance/increments)*2

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
        for xth in range(element_count):
            angle = -90 + xth*2
            #print(angle)
            if theta_x < 0:
                if theta_x < angle and angle<=0:
                    x_th_1 = xth
                    x_th_2 = xth-1
                    #print("x - negative",angle,theta_x, -90+x_th*2)
                    break
            else:
                if theta_x <= angle and angle>=0:
                    x_th_1 = xth
                    x_th_2 = xth-1
                    #print("x - positive",angle,theta_x,-90+x_th*2)
                    break
            for yth in range(element_count):
                angle = -90 + yth*2
                #print(angle)
                if theta_y < 0:
                    if theta_y < angle and angle<=0:
                        y_th_1 = yth
                        y_th_2 = yth-1
                        #print("y - negative",angle,theta_y, -90+y_th*2)
                        break
                else:
                    if theta_y < angle and angle>=0:
                        y_th_1 = yth
                        y_th_2 = yth-1
                        #print("y - positive",angle,theta_y,-90+y_th*2)
                        break
        
        #averaged linear interpolation
        #interpolating by x axis
        degree_increment = 2
        interpolation_level = 20
        interpolation_steps = degree_increment * interpolation_level
        c_x_increment_1 = int(y_axis_list[y_th_1][x_th_2])-int(y_axis_list[y_th_1][x_th_1])
        c_x_increment_2 = int(y_axis_list[y_th_2][x_th_2])-int(y_axis_list[y_th_2][x_th_1])
        c_x_increment_1 = c_x_increment_1 / interpolation_steps
        c_x_increment_2 = c_x_increment_2 / interpolation_steps
        
        x_dif = theta_x-(-90+x_th_1*2)
        c_x_1 = int(y_axis_list[y_th_1][x_th_2]) + (x_dif * interpolation_level * c_x_increment_1)
        c_x_2 = int(y_axis_list[y_th_2][x_th_2]) + (x_dif * interpolation_level * c_x_increment_2)
        
        c_y_increment = c_x_2 - c_x_1
        c_y_increment = c_y_increment / interpolation_steps
        
        y_dif = theta_y - (-90+y_th_1*2) 
        c_y = c_x_1 - (c_y_increment * interpolation_level * y_dif)
        candela = c_y
        #print(theta_x, theta_y,(-90+x_th_1*2), (-90+x_th_2*2),(-90+y_th_1*2), (-90+y_th_2*2),"dif data",x_dif, c_x_increment_1,c_x_increment_2,"x candela", c_x_1, c_x_2,"final candela",c_y,"set 1", y_axis_list[y_th_1][x_th_1], y_axis_list[y_th_1][x_th_2],"set 2", y_axis_list[y_th_2][x_th_1], y_axis_list[y_th_2][x_th_2])
        
        # candela = y_axis_list[y_th_1][x_th_1]
        d = math.sqrt((height**2)+(x**2)+(z**2))
        lux = (float(candela)*candela_to_lux_modifier)/(d**2)
        if z ==0 and x%25==0:
            print("calculated theta:",theta_x,theta_y,"list theta",-90+x_th_1*2,-90+y_th_1*2,"z,x",z,x,"interpolated candela",candela,c_x_1, c_x_2,"distance",d,"lux",lux,"original candelas",-90+x_th_1*2,-90+y_th_1*2, y_axis_list[y_th_1][x_th_1],-90+x_th_2*2,-90+y_th_1*2,y_axis_list[y_th_1][x_th_2],-90+x_th_1*2,-90+y_th_2*2,y_axis_list[y_th_2][x_th_1],-90+x_th_2*2,-90+y_th_2*2,y_axis_list[y_th_2][x_th_2])
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

    
class RenderPlane(QtWidgets.QWidget):
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
        x = 1
        pixel_size = 4
        for item in x_lux_list:
            # x = x * increments
            for lux_item in item: 
                y = lux_item[0]
                if y < self.yrange and y > -self.yrange :
                    if lux_item[1]>0 and lux_item[1] < 25:
                        pen = QtGui.QPen(QtGui.QColor(0,0,int((lux_item[1]/25)*255)),pixel_size)
                    elif lux_item[1] >25 and lux_item[1] < 50:
                        pen = QtGui.QPen(QtGui.QColor(0,int((lux_item[1]/50)*255),0),pixel_size)
                    elif lux_item[1] >50 and lux_item[1] < 100:
                        pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[1])/50)*10),0),pixel_size)
                    elif lux_item[1] >100 and lux_item[1] < 250:
                        pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[1])/250)*165),0),pixel_size)
                    elif lux_item[1] >250 and lux_item[1] < 1000:
                        pen = QtGui.QPen(QtGui.QColor(255,80-int(((lux_item[1])/1000)*80),0),pixel_size)
                    else:
                        pen = QtGui.QPen(QtCore.Qt.white,pixel_size)
                    painter.setPen(pen)
                    painter.drawPoint(x*2+self.offsetx, self.height-self.offsety-y*2)
            x +=1

        #draw axis
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        #+y
        point1 = QtCore.QPointF(self.offsetx, self.height-self.offsety-self.yrange*2)
        point2 = QtCore.QPointF(self.offsetx, self.height-self.offsety)
        line1 = QtCore.QLineF(point1, point2)
        painter.drawLine(line1)
        #-y
        point1 = QtCore.QPointF(self.offsetx, self.height-self.offsety+self.yrange*2)
        point2 = QtCore.QPointF(self.offsetx, self.height-self.offsety)
        line1 = QtCore.QLineF(point1, point2)
        painter.drawLine(line1)
        #x
        point1 = QtCore.QPointF(self.offsetx, self.height-self.offsety+self.yrange*2)
        point2 = QtCore.QPointF(self.width-self.offsetx, self.height-self.offsety+self.yrange*2)
        line1 = QtCore.QLineF(point1, point2)
        painter.drawLine(line1)


        #draw markers
        #x axis
        for i in range(self.xrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,self.height-self.offsety+self.yrange*2,self.offsetx+i,self.height-self.offsety+self.yrange*2+10)
                painter.drawText(QtCore.QPointF(self.offsetx+(i)-15, self.height-self.offsety+self.yrange*2+30),str(i/2))
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
        
        painter.end()
        
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
                if lux_item[2]>0 and lux_item[2] < 10:
                    pen = QtGui.QPen(QtGui.QColor(0,0,int((lux_item[2]/10)*255)),pixel_size)
                elif lux_item[2] >10 and lux_item[2] < 25:
                    pen = QtGui.QPen(QtGui.QColor(0,int((lux_item[2]/25)*255),0),pixel_size)
                elif lux_item[2] >25 and lux_item[2] < 50:
                    pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/50)*10),0),pixel_size)
                elif lux_item[2] >50 and lux_item[2] < 100:
                    pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/100)*165),0),pixel_size)
                elif lux_item[2] >100 and lux_item[2] < 150:
                    pen = QtGui.QPen(QtGui.QColor(255,80-int(((lux_item[2])/150)*80),0),pixel_size)
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
        -y
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
    app.exec_()