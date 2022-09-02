import os, sys
import math
from PySide6 import QtCore, QtGui, QtWidgets

f_path = "raw_values.csv"

y_axis_list = []

with open(f_path) as f:
    for line in f:
        if "ï»¿" in line:
            line = line.strip("ï»¿")
        line = line.strip("\n")
        y_axis_list.append(line.split(","))
        
#rotate grid
temp_list_2 = []
for i in range(len(y_axis_list[0])):
    temp_list = []
    for j in range(len(y_axis_list)):
        temp_list.append(y_axis_list[j][i])
    temp_list_2.append(temp_list)
    
y_axis_list = temp_list_2

candela_to_lux_modifier = 10.76391 #10.76391for feet only, not required for meters

class LuxPlotter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.color_map = [QtGui.QColor(45,49,139),QtGui.QColor(5,80,164),QtGui.QColor(11,111,186),QtGui.QColor(29,135,199),QtGui.QColor(37,159,218),QtGui.QColor(0,176,187),QtGui.QColor(105,191,100),QtGui.QColor(168,209,56),QtGui.QColor(246,130,33),QtGui.QColor(228,36,42)]
        self.window_height=900
        self.window_width=900
        self.setGeometry(0, 0, self.window_width, self.window_height)
        layout = QtWidgets.QVBoxLayout()
        self.scrollarea = QtWidgets.QScrollArea(self)
        self.scrollarea.setAlignment(QtCore.Qt.AlignCenter)
        layout_buttons = QtWidgets.QHBoxLayout()
        self.button_zoom_in = QtWidgets.QPushButton("Zoom In")
        self.button_zoom_in.clicked.connect(self.ZoomIn)
        self.button_fit = QtWidgets.QPushButton("Fit to Window")
        self.button_fit.clicked.connect(self.FitToWindow)
        self.button_zoom_out = QtWidgets.QPushButton("Zoom Out")
        self.button_zoom_out.clicked.connect(self.ZoomOut)
        self.button_save = QtWidgets.QPushButton("Save")
        self.button_save.clicked.connect(self.save)
        layout_buttons.addWidget(self.button_zoom_out)
        layout_buttons.addWidget(self.button_fit)
        layout_buttons.addWidget(self.button_zoom_in)
        layout_buttons.addWidget(self.button_save)
        #self.renderer = RenderGroundProjection(self)
        
        self.label = QtWidgets.QLabel()
        self.label.setScaledContents(True)
        
        #ground plot
        # height = 8
        # x_tilt = 0
        # y_tilt = 0
        # x_distance = 1000  #distance out
        # z_distance = 300  #distance on the side
        # increments = 1
        # starting_x_deg=-90
        # starting_y_deg=90
        # ending_x_deg=90
        # ending_y_deg=-90
        # x_degrees_increment=2
        # y_degrees_increment=2
        
        # plot_title = f"Ground Plot at {height} with x tilt: {x_tilt}, y tilt: {y_tilt}"
        
        # self.offsetx =50
        # self.offsety = 150
        # self.xrange = z_distance*2
        # self.yrange = x_distance
        # self.plot_width = self.xrange*2+100
        # self.plot_height = self.yrange*2+200
        # projection_list,max_lux = self.generateGroundPlot(height, y_tilt, x_tilt, increments, x_distance, z_distance, starting_x_deg, starting_y_deg, ending_x_deg, ending_y_deg, x_degrees_increment, y_degrees_increment)
        
        #wall plot
        wall_distance = 80
        x_tilt = 0
        y_tilt = 0
        x_distance = 300 #must be in increments of 25
        y_distance = 300 #must be in increments of 25
        increments = 1
        starting_x_deg=-90
        starting_y_deg=90
        ending_x_deg=90
        ending_y_deg=-90
        x_degrees_increment=2
        y_degrees_increment=2
        self.offsetx = 50
        self.offsety = y_distance+75
        self.xrange = x_distance
        self.yrange = y_distance
        self.plot_width = self.xrange*4+100
        self.plot_height = self.yrange*4+200
        plot_title = f"Wall Plot at {wall_distance} from the source with x tilt: {x_tilt}, y tilt: {y_tilt}"
        projection_list,max_lux = self.generateWallPlot(wall_distance, y_tilt, x_tilt, increments, x_distance, y_distance, starting_x_deg, starting_y_deg, ending_x_deg, ending_y_deg, x_degrees_increment, y_degrees_increment)
        
        
        
        self.scale_factor = 1
        print(self.plot_width,self.plot_height)
        canvas = QtGui.QPixmap(self.plot_width,self.plot_height)
        canvas.fill(QtCore.Qt.gray)
        self.label.setPixmap(canvas)
        
        self.step_map = [.4,max_lux*.1**2,max_lux*.2**2,max_lux*.3**2,max_lux*.4**2,max_lux*.5**2,max_lux*.6**2,max_lux*.7**2,max_lux*.8**2,max_lux*.9**2,max_lux]
        print(self.step_map)
        
        #self.GroundPlot(projection_list,increments,plot_title)
        self.WallPlot(projection_list,increments,plot_title)
        self.FitToWindow()
        
        #self.scrollarea.setWidget(self.renderer)
        self.scrollarea.setWidget(self.label)
        layout.addWidget(self.scrollarea)
        layout.addLayout(layout_buttons)
        self.setLayout(layout)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.setStyleSheet("background:black")
        self.center()
        self.setWindowTitle('Lux Plotter')
        self.show()
        
    def getInterpolatedCandela(self,theta_x,starting_x_deg,x_degrees_increment,theta_y,starting_y_deg, y_degrees_increment,x_element_count,y_element_count,increments):
        x_th_1, x_th_2 = 0, 0
        y_th_1, y_th_2 = 0, 0
        for xth in range(x_element_count):
            angle = starting_x_deg + xth*x_degrees_increment
            #print(angle)
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
        for yth in range(y_element_count):
            angle = starting_y_deg - yth*y_degrees_increment
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
        c_x_increment_1 = float(y_axis_list[y_th_1][x_th_1])-float(y_axis_list[y_th_1][x_th_2])
        c_x_increment_2 = float(y_axis_list[y_th_2][x_th_1])-float(y_axis_list[y_th_2][x_th_2])
        c_x_increment_1 = c_x_increment_1 / x_degrees_increment
        c_x_increment_2 = c_x_increment_2 / x_degrees_increment
        
        x_dif = theta_x-(starting_x_deg+x_th_1*x_degrees_increment)
        if x_dif>0:
            c_x_1 = float(y_axis_list[y_th_1][x_th_2]) + (x_dif * c_x_increment_1)
            c_x_2 = float(y_axis_list[y_th_2][x_th_2]) + (x_dif * c_x_increment_2)
        else:
            c_x_1 = float(y_axis_list[y_th_1][x_th_1]) + (x_dif  * c_x_increment_1)
            c_x_2 = float(y_axis_list[y_th_2][x_th_1]) + (x_dif  * c_x_increment_2)
        
        c_y_increment = c_x_2 - c_x_1
        c_y_increment = c_y_increment / y_degrees_increment
        
        y_dif = theta_y - (starting_y_deg-y_th_1*y_degrees_increment) 
        c_y = c_x_1 + (c_y_increment * y_dif) #final interpolated candela value
        #print("calc thetas",theta_x, theta_y,"list theta x,x2",(starting_x_deg+x_th_1*degrees_increment), (starting_x_deg+x_th_2*degrees_increment),"list theta y,y2",(starting_y_deg-y_th_1*degrees_increment), (starting_y_deg-y_th_2*degrees_increment),"dif data x,y",x_dif, y_dif, c_x_increment_1,c_x_increment_2,"x candela", c_x_1, c_x_2,"final candela",c_y,"set 1", y_axis_list[y_th_1][x_th_1], y_axis_list[y_th_1][x_th_2],"set 2", y_axis_list[y_th_2][x_th_1], y_axis_list[y_th_2][x_th_2])
        return c_y
    
    def generateGroundPlot(self,height,y_tilt,x_tilt,increments,x_distance,z_distance,starting_x_deg,starting_y_deg,ending_x_deg,ending_y_deg,x_degrees_increment,y_degrees_increment):
        x_range = int(x_distance/increments)
        z_range = int(z_distance/increments)*2
        y_element_count = len(y_axis_list)
        x_element_count = len(y_axis_list[0])
        projection_list = []
        max_lux = 0
        for x in range(1,x_range+1):
            x=x*increments
            for z in range(z_range):
                z=-z_distance+z*increments
                theta_x = math.degrees(math.atan(z/x))-x_tilt
                theta_y = -90+math.degrees(math.atan(x/height))-y_tilt
                # if theta_y >= ending_y_deg and theta_x >= starting_x_deg and theta_x <= ending_x_deg:
                candela = self.getInterpolatedCandela(theta_x,starting_x_deg,x_degrees_increment,theta_y, starting_y_deg, y_degrees_increment,x_element_count,y_element_count,increments)
                # candela = y_axis_list[y_th_1][x_th_1]
                d = math.sqrt((height**2)+(x**2)+(z**2))
                lux = (float(candela)*candela_to_lux_modifier)/(d**2)
                if lux > max_lux:
                    max_lux = lux 
                #if z ==0 and x%25==0:
                #    print("calculated theta:",theta_x,theta_y,"list theta",starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,"z,x",z,x,"interpolated candela",candela,c_x_1, c_x_2,"distance",d,"lux",lux,"original candelas",starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment, y_axis_list[y_th_1][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,y_axis_list[y_th_1][x_th_2],starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_2])
                #print("calculated theta:",theta_x,theta_y,"list theta x",-90+x_th_1*2,-90+x_th_2*2,"list theta y",-90+y_th_1*2,-90+y_th_2*2,"z,x",z,x,"candela",candela,d,lux)
                projection_list.append((z,x,lux))
        return projection_list,max_lux
    
    def generateWallPlot(self,wall_distance,y_tilt,x_tilt,increments,x_distance,y_distance,starting_x_deg,starting_y_deg,ending_x_deg,ending_y_deg,x_degrees_increment,y_degrees_increment):
        x_range = int(x_distance/increments)*2
        y_range = int(y_distance/increments)*2
        y_element_count = len(y_axis_list)
        x_element_count = len(y_axis_list[0])
        projection_list = []

        max_lux = 0
        for y in range(y_range+1):
            y=y_distance-y*increments
            for x in range(x_range+1):
                x=-x_distance+x*increments
                theta_x = math.degrees(math.atan(x/wall_distance))-x_tilt
                theta_y = math.degrees(math.atan(y/wall_distance))-y_tilt
                
                # if theta_y<= starting_y_deg and theta_y >= ending_y_deg and theta_x >= starting_x_deg and theta_x <= ending_x_deg:
                candela = self.getInterpolatedCandela(theta_x,starting_x_deg,x_degrees_increment,theta_y, starting_y_deg, y_degrees_increment,x_element_count,y_element_count,increments)
                # candela = y_axis_list[y_th_1][x_th_1]
                d = math.sqrt((wall_distance**2)+(x**2)+(y**2))
                lux = (float(candela)*candela_to_lux_modifier)/(d**2)
                if lux > max_lux:
                    max_lux = lux 
                #if x ==0 and y%10==0:
                #    print("calculated theta:",theta_x,theta_y,"list theta",starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,"x,y",x,y,"interpolated candela",candela,c_x_1, c_x_2,"distance",d,"lux",lux,"original candelas",starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment, y_axis_list[y_th_1][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,y_axis_list[y_th_1][x_th_2],starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_2])
                #print("calculated theta:",theta_x,theta_y,"list theta x",-90+x_th_1*2,-90+x_th_2*2,"list theta y",-90+y_th_1*2,-90+y_th_2*2,"z,x",z,x,"candela",candela,d,lux)
                projection_list.append((x,y,lux))
        return projection_list,max_lux
        
        
    def FitToWindow(self):
        self.scale_factor = (self.height()-75)/self.plot_height
        self.label.resize((self.scale_factor)*self.label.pixmap().size())
        
    def ZoomIn(self):
        self.scale_factor+=.1
        self.label.resize((self.scale_factor)*self.label.pixmap().size())
        
    def ZoomOut(self):
        self.scale_factor-=.1
        self.label.resize((self.scale_factor)*self.label.pixmap().size())
        
    def save(self):
        self.label.pixmap().save("testing.png","PNG",100)
        
    
    def WallPlot(self,projection_list,increments,plot_title):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        #draw points
        self.drawBySolid(painter,"wall",projection_list,increments)

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
        #-x axis
        for i in range(self.xrange*4+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,self.plot_height-self.offsety*2+self.yrange*2,self.offsetx+i,self.plot_height-self.offsety*2+self.yrange*2+10)
                painter.drawText(QtCore.QPointF(self.offsetx+(i)-15, self.plot_height-self.offsety+self.yrange-50),str(-self.xrange+i/2))
        painter.drawText(QtCore.QPointF(self.plot_width/2-40, self.plot_height+self.yrange-5),"X Distance (ft.)")
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx-5,self.plot_height-self.offsety*2-i,self.offsetx,self.plot_height-self.offsety*2-i)
                painter.drawText(QtCore.QPointF(self.offsetx-40, self.plot_height-self.offsety*2-i+5),str(i/2))
        #-yaxis
        for i in range(self.yrange*2+1):
            if i !=0:
                if i%(50)==0:
                    painter.drawLine(self.offsetx-5,self.plot_height-self.offsety*2+i,self.offsetx,self.plot_height-self.offsety*2+i)
                    painter.drawText(QtCore.QPointF(self.offsetx-40, self.plot_height-self.offsety*2+i+5),"-"+str(i/2))
        painter.drawText(QtCore.QPointF(5, 25),"Y Distance (ft.)")
        
        #draw grid
        pen = QtGui.QPen(QtCore.Qt.gray,1)
        painter.setPen(pen)
        for i in range(self.xrange*4+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,0,self.offsetx+i,self.plot_height-self.offsety*2+self.yrange*2+10)
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.plot_width,self.plot_height-self.offsety*2-i,self.offsetx,self.plot_height-self.offsety*2-i)
                painter.drawLine(self.plot_width,self.plot_height-self.offsety*2+i,self.offsetx,self.plot_height-self.offsety*2+i)
        
        
        #draw title
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        painter.drawText(QtCore.QPointF(self.plot_width/2-self.offsetx*2, 20),plot_title)
        
        #draw legend
        painter.drawText(QtCore.QPointF(self.plot_width/2-self.offsetx-50, self.plot_height-25),f"1 Lux = Intensity of the light of a full moon")
        legend_distance = self.plot_width - self.offsetx*4
        legend_section = legend_distance/10
        for i in range(len(self.color_map)):
            painter.setPen(self.color_map[i])
            painter.setBrush(self.color_map[i])
            painter.drawRect(self.plot_width/2 - legend_distance/2 - self.offsetx +(i+1)*legend_section - legend_section/2, self.plot_height-90,legend_section,20)
            painter.setPen(QtGui.Qt.white)
            painter.drawText(QtCore.QPointF(self.plot_width/2 - legend_distance/2 - self.offsetx +(i+1)*legend_section+legend_section/2-10,self.plot_height-50), f"{round(self.step_map[i+1],2)}")
        
        painter.end()
        self.label.setPixmap(canvas)
            
        
    def GroundPlot(self,projection_list,increments,plot_title):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        #painter.scale(self.scale, self.scale)
        self.drawBySolid(painter,"ground",projection_list,increments)
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        #+y
        point1 = QtCore.QPointF(self.offsetx, self.plot_height-self.offsety-self.yrange*2)
        point2 = QtCore.QPointF(self.offsetx, self.plot_height-self.offsety)
        line1 = QtCore.QLineF(point1, point2)
        painter.drawLine(line1)
        #x
        point1 = QtCore.QPointF(self.offsetx, self.plot_height-self.offsety)
        point2 = QtCore.QPointF(self.plot_width-self.offsetx, self.plot_height-self.offsety)
        line1 = QtCore.QLineF(point1, point2)
        painter.drawLine(line1)


        #draw markers
        #x axis
        for i in range(self.xrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,self.plot_height-self.offsety,self.offsetx+i,self.plot_height-self.offsety+10)
                painter.drawText(QtCore.QPointF(self.offsetx+(i)-15, self.plot_height-self.offsety+30),str(-self.xrange/2+i/2))
        painter.drawText(QtCore.QPointF(self.plot_width/2-40, self.plot_height-100),"X Distance (ft.)")
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx-5,self.plot_height-self.offsety-i,self.offsetx,self.plot_height-self.offsety-i)
                painter.drawText(QtCore.QPointF(self.offsetx-40, self.plot_height-self.offsety-i+5),str(i/2))
        painter.drawText(QtCore.QPointF(5, 25),"Y Distance (ft.)")
        
        #draw grid
        pen = QtGui.QPen(QtCore.Qt.gray,1)
        painter.setPen(pen)
        for i in range(self.xrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,self.plot_height-self.offsety,self.offsetx+i,0)
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.plot_width,self.plot_height-self.offsety-i,self.offsetx,self.plot_height-self.offsety-i)

        #draw title
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        painter.drawText(QtCore.QPointF(self.plot_width/2-self.offsetx-75, 20),plot_title)
        
        #draw legend
        painter.drawText(QtCore.QPointF(self.plot_width/2-self.offsetx-50, self.plot_height-25),f"1 Lux = Intensity of the light of a full moon")
        for i in range(len(self.color_map)):
            painter.setPen(self.color_map[i])
            painter.setBrush(self.color_map[i])
            painter.drawRect(self.plot_width/2 - self.xrange/2 - self.offsetx*2 +(i+1)*self.xrange/10, self.plot_height-90,self.xrange/10,20)
            painter.setPen(QtGui.Qt.white)
            painter.drawText(QtCore.QPointF(self.plot_width/2 - self.xrange/2 - self.offsetx*2 +(i+1)*self.xrange/10+self.xrange/10-10,self.plot_height-50), f"{round(self.step_map[i+1],2)}")
            
        painter.end()
        self.label.setPixmap(canvas)
        
    def drawBySolid(self,painter,plot_type,projection_list,increments):
        pixel_size = increments * 2
        for lux_item in projection_list:
            # x = x * increments
            x = lux_item[0]
            y = lux_item[1]
            #lux = lux_item[2]
            if y < self.yrange and y > -self.yrange and x<self.xrange and x>-self.xrange:
                if lux_item[2]>self.step_map[0] and lux_item[2] <= self.step_map[1]:
                    pen = QtGui.QPen(self.color_map[0],pixel_size)
                elif lux_item[2] >self.step_map[1] and lux_item[2] <= self.step_map[2]:
                    pen = QtGui.QPen(self.color_map[1],pixel_size)
                elif lux_item[2] >self.step_map[2] and lux_item[2] <= self.step_map[3]:
                    pen = QtGui.QPen(self.color_map[2],pixel_size)
                elif lux_item[2] >self.step_map[3] and lux_item[2] <= self.step_map[4]:
                    pen = QtGui.QPen(self.color_map[3],pixel_size)
                elif lux_item[2] >self.step_map[4] and lux_item[2] <= self.step_map[5]:
                    pen = QtGui.QPen(self.color_map[4],pixel_size)
                elif lux_item[2] >self.step_map[5] and lux_item[2] <= self.step_map[6]:
                    pen = QtGui.QPen(self.color_map[5],pixel_size)
                elif lux_item[2] >self.step_map[6] and lux_item[2] <= self.step_map[7]:
                    pen = QtGui.QPen(self.color_map[6],pixel_size)
                elif lux_item[2] >self.step_map[7] and lux_item[2] <= self.step_map[8]:
                    pen = QtGui.QPen(self.color_map[7],pixel_size)
                elif lux_item[2] >self.step_map[8] and lux_item[2] <= self.step_map[9]:
                    pen = QtGui.QPen(self.color_map[8],pixel_size)
                elif lux_item[2] >self.step_map[9] and lux_item[2] <= self.step_map[10]:
                    pen = QtGui.QPen(self.color_map[9],pixel_size)
                else:
                    pen = QtGui.QPen(QtCore.Qt.white,pixel_size)
                painter.setPen(pen)
                if plot_type =="wall":
                    painter.drawPoint(x*2+self.offsetx+self.xrange*2, self.plot_height-self.offsety*2-y*2)
                else:
                    painter.drawPoint(x*2+self.offsetx+self.xrange, self.plot_height-self.offsety-y*2)
                
    # def drawByGradient(self,painter):
    #     pixel_size = increments * 2
    #     for lux_item in projection_list:
    #         # x = x * increments
    #         x = lux_item[0]
    #         y = lux_item[1]
    #         #lux = lux_item[2]
    #         if y < self.yrange and y > -self.yrange and x<self.xrange and x>-self.xrange:
    #             if lux_item[2]>self.step_0 and lux_item[2] <= self.step_1:
    #                 pen = QtGui.QPen(QtGui.QColor(0,0,int((lux_item[2]/10)*255)),pixel_size)
    #             elif lux_item[2] >self.step_1 and lux_item[2] <= self.step_2:
    #                 pen = QtGui.QPen(QtGui.QColor(0,int((lux_item[2]/25)*255),0),pixel_size)
    #             elif lux_item[2] >self.step_2 and lux_item[2] <= self.step_3:
    #                 pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/50)*10),0),pixel_size)
    #             elif lux_item[2] >self.step_3 and lux_item[2] <= self.step_4:
    #                 pen = QtGui.QPen(QtGui.QColor(255,255-int(((lux_item[2])/100)*165),0),pixel_size)
    #             elif lux_item[2] >self.step_4 and lux_item[2] <= self.step_5:
    #                 pen = QtGui.QPen(QtGui.QColor(255,150-int(((lux_item[2])/200)*150),0),pixel_size)
    #             else:
    #                 pen = QtGui.QPen(QtCore.Qt.white,pixel_size)
    #             painter.setPen(pen)
    #             painter.drawPoint(x*2+self.offsetx+self.xrange, self.plot_height-self.offsety-y*2)
        
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

        

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    w = LuxPlotter()
    w.show()
    app.exec()