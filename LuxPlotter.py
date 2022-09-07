import os, sys
import math, time
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
        height = 8
        x_tilt = 0
        y_tilt = 0
        x_distance = 800  #distance out
        z_distance = 300  #distance on the side
        increments = 1
        starting_x_deg=-90
        starting_y_deg=90
        ending_x_deg=90
        ending_y_deg=-90
        x_degrees_increment=2
        y_degrees_increment=2
        
        plot_title = f"Ground Plot at {height} ft. with x tilt: {x_tilt} deg., y tilt: {y_tilt} deg."
        
        self.offsetx =50
        self.offsety = 150
        self.xrange = z_distance*2
        self.yrange = x_distance
        self.plot_width = self.xrange*2+100
        self.plot_height = self.yrange*2+200
        #projection_list,max_lux = self.generateGroundPlot(height, y_tilt, x_tilt, increments, x_distance, z_distance, starting_x_deg, starting_y_deg, ending_x_deg, ending_y_deg, x_degrees_increment, y_degrees_increment)
        projection_list,max_lux = self.generatePlanePlot(0,"y",90, 2,z_distance,x_distance, 1)
        
        #wall plot
        # wall_distance = 100
        # x_tilt = 0
        # y_tilt = 0
        # x_distance = 300 #must be in increments of 25
        # y_distance = 300 #must be in increments of 25
        # increments = 1
        # starting_x_deg=-90
        # starting_y_deg=90
        # ending_x_deg=90
        # ending_y_deg=-90
        # x_degrees_increment=15
        # y_degrees_increment=18
        # self.offsetx = 50
        # self.offsety = y_distance+75
        # self.xrange = x_distance
        # self.yrange = y_distance
        # self.plot_width = self.xrange*4+100
        # self.plot_height = self.yrange*4+200
        # plot_title = f"Wall Plot at {wall_distance} from the source with x tilt: {x_tilt}, y tilt: {y_tilt}"
        # projection_list,max_lux = self.generateWallPlot(wall_distance, y_tilt, x_tilt, increments, x_distance, y_distance, starting_x_deg, starting_y_deg, ending_x_deg, ending_y_deg, x_degrees_increment, y_degrees_increment)
        
        
        
        self.scale_factor = 1
        print(self.plot_width,self.plot_height)
        canvas = QtGui.QPixmap(self.plot_width,self.plot_height)
        canvas.fill(QtCore.Qt.gray)
        self.label.setPixmap(canvas)
        
        #ratio'd step map
        # self.step_map = [.1,max_lux*.1**2,max_lux*.2**2,max_lux*.3**2,max_lux*.4**2,max_lux*.5**2,max_lux*.6**2,max_lux*.7**2,max_lux*.8**2,max_lux*.9**2,max_lux]
        
        #normalized step map
        self.step_map = [1,2,4,8,16,32,64,128,256,512,1024]
        #print(self.step_map)
        
        #self.GroundPlot(projection_list,increments,plot_title)
        # for i in range(90):
        #     canvas.fill(QtCore.Qt.gray)
        #     self.label.setPixmap(canvas)
        #     y_tilt = - i
        #     projection_list,max_lux = self.generateGroundPlot(height, y_tilt, x_tilt, increments, x_distance, z_distance, starting_x_deg, starting_y_deg, ending_x_deg, ending_y_deg, x_degrees_increment, y_degrees_increment)
        #     print("rendering")
        #     self.GroundPlot(projection_list,increments,plot_title)
        #     self.save(f"ground_plot_angle_{y_tilt}.png")
        #     print("saved")
        start = time.time()
        self.GroundPlot(projection_list,increments,plot_title)
        end = time.time()
        print(end-start)
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
        
    def getInterpolatedCandela1D(self,theta,starting_degree,degrees_increment,axis):
        if starting_degree<0:
            degrees_increment = -1*degrees_increment
        element_1 = math.ceil((starting_degree-theta)/degrees_increment)
        
        if theta % degrees_increment!=0:
            element_2 = element_1 -1
        else:
            element_2 = element_1
            
        theta_diff = theta- (starting_degree-element_1*degrees_increment) 
        if axis  =="y":
            origin = int((len(y_axis_list[0])-1)/2)
            c_diff = float(y_axis_list[element_1][origin])-float(y_axis_list[element_2][origin])
            c_increment = c_diff/abs(degrees_increment)
            candela = float(y_axis_list[element_1][origin]) - (c_increment * theta_diff)
            #print(theta,starting_degree-element_1*degrees_increment,"c1",y_axis_list[element_1][origin],starting_degree-element_2*degrees_increment,"c2",y_axis_list[element_2][origin],"theta diff",theta_diff,"c_diff",c_diff,"c_incre",c_increment,"c",candela)

        else:
            origin = int((len(y_axis_list)-1)/2)
            #print(origin,element_1,element_2)
            c_diff = float(y_axis_list[origin][element_1])-float(y_axis_list[origin][element_2])
            c_increment = c_diff/abs(degrees_increment)
            candela = float(y_axis_list[origin][element_1]) + (c_increment * theta_diff)
            #print(theta,starting_degree-element_1*degrees_increment,"c1",y_axis_list[origin][element_1],starting_degree-element_2*degrees_increment,"c2",y_axis_list[origin][element_2],"theta diff",theta_diff,"c_diff",c_diff,"c_incre",c_increment,"c",candela)
        return candela
    
    
    def getInterpolatedCandela2D(self,theta_x,starting_x_deg,x_degrees_increment,theta_y,starting_y_deg, y_degrees_increment):
        #bidirectional interpolation
        #finding x
        if starting_x_deg<0:
            x_degrees_increment = -1*x_degrees_increment
        if starting_y_deg<0:
            y_degrees_increment = -1*y_degrees_increment
        x_th_1 = math.ceil((starting_x_deg-theta_x)/x_degrees_increment)
        if theta_x%x_degrees_increment!=0:
            x_th_2 = x_th_1 -1
        else:
            x_th_2 = x_th_1
        
        y_th_1 = math.ceil((starting_y_deg-theta_y)/y_degrees_increment)
        y_th_2 = y_th_1 -1
        if theta_y%y_degrees_increment!=0:
            y_th_2 = y_th_1 -1
        else:
            y_th_2 = y_th_1
        
        #interpolating by x axis
        c_x_increment_1 = float(y_axis_list[y_th_1][x_th_1])-float(y_axis_list[y_th_1][x_th_2])
        c_x_increment_2 = float(y_axis_list[y_th_2][x_th_1])-float(y_axis_list[y_th_2][x_th_2])
        c_x_increment_1 = c_x_increment_1 / abs(x_degrees_increment)
        c_x_increment_2 = c_x_increment_2 / abs(x_degrees_increment)
        
        #x_dif = theta_x-(starting_x_deg+x_th_1*x_degrees_increment)
        x_dif = theta_x-(starting_x_deg-x_th_1*x_degrees_increment)
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
        
        # if theta_x ==0:
        #     print("calculated theta:",theta_x,theta_y,"list theta",starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment, y_axis_list[y_th_1][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,y_axis_list[y_th_1][x_th_2],starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_2])

        # if theta_x ==0:
        #     print(x_dif, y_dif, c_y,"calculated theta:",theta_x,theta_y,"list theta",starting_x_deg-x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,starting_x_deg-x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment, y_axis_list[y_th_1][x_th_1],starting_x_deg-x_th_2*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,y_axis_list[y_th_1][x_th_2],starting_x_deg-x_th_1*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_1],starting_x_deg-x_th_2*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_2])

        
                
        #print("calc thetas",theta_x, theta_y,"list theta x,x2",(starting_x_deg+x_th_1*degrees_increment), (starting_x_deg+x_th_2*degrees_increment),"list theta y,y2",(starting_y_deg-y_th_1*degrees_increment), (starting_y_deg-y_th_2*degrees_increment),"dif data x,y",x_dif, y_dif, c_x_increment_1,c_x_increment_2,"x candela", c_x_1, c_x_2,"final candela",c_y,"set 1", y_axis_list[y_th_1][x_th_1], y_axis_list[y_th_1][x_th_2],"set 2", y_axis_list[y_th_2][x_th_1], y_axis_list[y_th_2][x_th_2])
        return c_y
    
    def generatePlanePlot(self,slice_angle,plane_axis,starting_degree, degrees_increment,x_distance, y_distance, increments):
        x_range = int(x_distance/increments)*2
        y_range = int(y_distance/increments)
        projection_list = []
        max_lux = 0
        for y in range(1,y_range+1):
            y = y*increments
            for x in range (x_range):
                x = -x_distance+x*increments
                theta = math.degrees(math.atan(x/y))
                candela = self.getInterpolatedCandela1D(theta,starting_degree,degrees_increment,plane_axis)
                d = math.sqrt((x**2)+(y**2))
                lux = (float(candela)*candela_to_lux_modifier)/(d**2)
                if x == 0 and y%25==0:
                    print(candela,d,lux)
                if lux > max_lux:
                    max_lux = lux 
                projection_list.append((x,y,lux))
        print(max_lux)
        return projection_list,max_lux
    
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
                candela = self.getInterpolatedCandela2D(theta_x,starting_x_deg,x_degrees_increment,theta_y, starting_y_deg, y_degrees_increment)
                # candela = y_axis_list[y_th_1][x_th_1]
                d = math.sqrt((height**2)+(x**2)+(z**2))
                lux = (float(candela)*candela_to_lux_modifier)/(d**2)
                
                #adjusting for plane
                # angle_incident = math.acos(height/d)
                # lux = lux * math.cos(angle_incident)
                
                if lux > max_lux:
                    max_lux = lux 
                # if z ==0 and x%25==0:
                #     print("calculated theta:",theta_x,theta_y,"list theta",starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,"z,x",z,x,"interpolated candela",candela,"distance",d,"lux",lux,"original candelas",starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment, y_axis_list[y_th_1][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_1*y_degrees_increment,y_axis_list[y_th_1][x_th_2],starting_x_deg+x_th_1*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_1],starting_x_deg+x_th_2*x_degrees_increment,starting_y_deg-y_th_2*y_degrees_increment,y_axis_list[y_th_2][x_th_2])
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
                candela = self.getInterpolatedCandela2D(theta_x,starting_x_deg,x_degrees_increment,theta_y, starting_y_deg, y_degrees_increment)
                # candela = y_axis_list[y_th_1][x_th_1]
                d = math.sqrt((wall_distance**2)+(x**2)+(y**2))
                lux = (float(candela)*candela_to_lux_modifier)/(d**2)
                
                #adjusting for plane
                # angle_incident = math.acos(wall_distance/d)
                # lux = lux * math.cos(angle_incident)
                
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
        try:
            filename = QtWidgets.QFileDialog.getSaveFileName(self,("Save File"),"Plot_Output.png",".png")
            self.label.pixmap().save(filename[0],"PNG",100)
            self.dispMsg("Save!")
        except Exception as e:
            print(e)
            self.dispMsg(f"Error Occured while saving.\n Error: {e}")
            
    def save(self,filename):
        self.label.pixmap().save(filename,"PNG",100)
        
    
    def WallPlot(self,projection_list,increments,plot_title):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        #draw points
        self.drawBySolid(painter,"wall",projection_list,increments)

        #draw axis
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)

        #draw markers
        #-x axis
        for i in range(self.xrange*4+1):
            if i%(50)==0:
                #painter.drawLine(self.offsetx+i,self.plot_height-self.offsety*2+self.yrange*2,self.offsetx+i,self.plot_height-self.offsety*2+self.yrange*2+10)
                painter.drawText(QtCore.QPointF(self.offsetx+(i)-15, self.plot_height-self.offsety+self.yrange-50),str(-self.xrange+i/2))
        painter.drawText(QtCore.QPointF(self.plot_width/2-40, self.plot_height+self.yrange-5),"Distance (ft.)")
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                #painter.drawLine(self.offsetx-5,self.plot_height-self.offsety*2-i,self.offsetx,self.plot_height-self.offsety*2-i)
                painter.drawText(QtCore.QPointF(self.offsetx-40, self.plot_height-self.offsety*2-i+5),str(i/2))
                if i!=0:
                    painter.drawText(QtCore.QPointF(self.offsetx-40, self.plot_height-self.offsety*2+i+5),"-"+str(i/2))
        painter.drawText(QtCore.QPointF(5, 25),"Distance (ft.)")
        
        #draw grid
        pen = QtGui.QPen(QtCore.Qt.white,1)
        painter.setPen(pen)
        for i in range(self.xrange*4+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,50,self.offsetx+i,self.plot_height-self.offsety*2+self.yrange*2+10)
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.plot_width-self.offsetx,self.plot_height-self.offsety*2-i,self.offsetx,self.plot_height-self.offsety*2-i)
                painter.drawLine(self.plot_width-self.offsetx,self.plot_height-self.offsety*2+i,self.offsetx,self.plot_height-self.offsety*2+i)
        
        
        
        #draw title
        font_metric = QtGui.QFontMetrics(painter.font())
        font_offset = font_metric.boundingRect(plot_title).width()/2
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        painter.drawText(QtCore.QPointF(self.plot_width/2-font_offset, 20),plot_title)
        
        #draw legend
        s = "1 Lux = Intensity of the light of a full moon"
        font_offset = font_metric.boundingRect(s).width()/2
        painter.drawText(QtCore.QPointF(self.plot_width/2-font_offset, self.plot_height-25),s)
        legend_distance = self.plot_width - self.offsetx*2
        legend_section = legend_distance/10
        for i in range(len(self.color_map)):
            painter.setPen(self.color_map[i])
            painter.setBrush(self.color_map[i])
            painter.drawRect(self.plot_width/2 - legend_distance/2 +(i)*legend_section, self.plot_height-90,legend_section,20)
            painter.setPen(QtGui.Qt.white)
            painter.drawText(QtCore.QPointF(self.plot_width/2 -legend_distance/2 +(i)*legend_section-10,self.plot_height-50), f"{round(self.step_map[i],2)}")
        painter.drawText(QtCore.QPointF(self.plot_width/2 -legend_distance/2 +(10)*legend_section-10,self.plot_height-50), f"{round(self.step_map[10],2)}")
        
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
        pen = QtGui.QPen(QtCore.Qt.white,1)
        painter.setPen(pen)
        #x axis
        for i in range(self.xrange*2+1):
            if i%(50)==0:
                #painter.drawLine(self.offsetx+i,self.plot_height-self.offsety,self.offsetx+i,self.plot_height-self.offsety+10)
                painter.drawText(QtCore.QPointF(self.offsetx+(i)-15, self.plot_height-self.offsety+30),str(-self.xrange/2+i/2))
        painter.drawText(QtCore.QPointF(self.plot_width/2-40, self.plot_height-100),"Distance (ft.)")
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                #painter.drawLine(self.offsetx-5,self.plot_height-self.offsety-i,self.offsetx,self.plot_height-self.offsety-i)
                painter.drawText(QtCore.QPointF(self.offsetx-40, self.plot_height-self.offsety-i+5),str(i/2))
        painter.drawText(QtCore.QPointF(5, 25),"Distance (ft.)")
        
        #draw grid
        for i in range(self.xrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.offsetx+i,self.plot_height-self.offsety,self.offsetx+i,50)
        #yaxis
        for i in range(self.yrange*2+1):
            if i%(50)==0:
                painter.drawLine(self.plot_width-self.offsetx,self.plot_height-self.offsety-i,self.offsetx,self.plot_height-self.offsety-i)
                
        #football field overlay
        pen = QtGui.QPen(QtCore.Qt.green,5)
        painter.setPen(pen)
        #length wise field
        for i in range(self.xrange*2+1):
            if (i-self.xrange-160)%320==0:
                painter.drawLine(self.offsetx+i,self.plot_height-self.offsety,self.offsetx+i,50)
        for i in range(self.yrange*2+1):
            if i%(720)==0:
                painter.drawLine(self.plot_width-self.offsetx,self.plot_height-self.offsety-i,self.offsetx,self.plot_height-self.offsety-i)
        #width wise field
        # for i in range(self.xrange*2+1):
        #     if (i-self.xrange-360)%720==0:
        #         painter.drawLine(self.offsetx+i,self.plot_height-self.offsety,self.offsetx+i,50)
        # for i in range(self.yrange*2+1):
        #     if i%(320)==0:
        #         painter.drawLine(self.plot_width-self.offsetx,self.plot_height-self.offsety-i,self.offsetx,self.plot_height-self.offsety-i)

        #draw title
        font_metric = QtGui.QFontMetrics(painter.font())
        font_offset = font_metric.boundingRect(plot_title).width()/2
        pen = QtGui.QPen(QtCore.Qt.white,2)
        painter.setPen(pen)
        painter.drawText(QtCore.QPointF(self.plot_width/2-font_offset, 20),plot_title)
        
        #draw legend
        s = "1 Lux = Intensity of the light of a full moon"
        font_offset = font_metric.boundingRect(s).width()/2
        painter.drawText(QtCore.QPointF(self.plot_width/2-font_offset, self.plot_height-25),s)
        legend_distance = self.plot_width - self.offsetx*2
        legend_section = legend_distance/10
        for i in range(len(self.color_map)):
            painter.setPen(self.color_map[i])
            painter.setBrush(self.color_map[i])
            painter.drawRect(self.plot_width/2 - legend_distance/2 +(i)*legend_section, self.plot_height-90,legend_section,20)
            painter.setPen(QtGui.Qt.white)
            painter.drawText(QtCore.QPointF(self.plot_width/2 -legend_distance/2 +(i)*legend_section-10,self.plot_height-50), f"{round(self.step_map[i],2)}")
        painter.drawText(QtCore.QPointF(self.plot_width/2 -legend_distance/2 +(10)*legend_section-10,self.plot_height-50), f"{round(self.step_map[10],2)}")
            
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
                if lux_item[2]>=self.step_map[0]:
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
        
    def dispMsg(self,msg):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setText(msg+"        ")
        msgbox.exec()

        

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    w = LuxPlotter()
    w.show()
    app.exec()