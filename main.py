#works on desktop...and works on pi
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import StringProperty


#matplotlib
import matplotlib.pyplot as plt

#image stuff
import smopy

#get serial data
#import serial.tools.list_ports

#mgrs stuff
import mgrs



#####################################################
## set some stuff beforehand
#####################################################
Window.fullscreen = 'auto' # default to fullscreen
font_size = 30 #font size
quantico = "quantico.regular.ttf" #set font
mgrs_mode = False # for switching inbetween modes



#####################################################
### how to make and add buttons - needed for AC later
#####################################################
buttons=[]
def make_button(command,func):
    """
    function for adding a lot of buttons
    """

    btn = Button(text=command)
    btn.bind(on_press = func)
    buttons.append(btn)
    return buttons

def B1(instance):
    print()
    #now=datetime.now()
    #string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Arm"
    #string = {string:'out'}
    #add_messages(string)
    #device.send_data_broadcast('arm')

def B2(instance):
    print()
    #now=datetime.now()
    #string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Disarm"
    #string = {string:'out'}
    #add_messages(string)
    #device.send_data_broadcast('disarm')

def B3(instance):
    print()#now=datetime.now()
    #string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Launch"
    #string = {string:'out'}
    #add_messages(string)
    #device.send_data_broadcast('relay_on')

def LatLon_MGRS(instance):
    """
    TOGGLE DISPLAYING LAT/LON VS MGRS
    """
    global mgrs_mode
    if mgrs_mode == False:
        mgrs_mode = True
        gps_handle.text = latlon_display_string

    else:
        mgrs_mode = False
        gps_handle.text = mgrs_display_string


a = 1
def update_gps(instance):
    """
    Update GPS info at regular intervals
    """

    ### get serial data
    global a
    a += 1
    b = str(a)

    if mgrs_mode == True:
        ## edit mgrs_mode string
        #parse string into mgrs_mode
        mgrs_display_string = " MGRS: " + b
        gps_handle.text = mgrs_display_string

    else:
        ### edit LatLon string
        latlon_display_string = " Lat/Lon: " + b
        gps_handle.text = latlon_display_string



##############################################################
#GPS stuff

##READ SERIAL DATA, UPDATE PLOT AND POSITION IN BACKGROUND
#create the plot, add it to the boxlayout

latlow = 30.358
lathigh = 30.363
lonlow = -97.790
lonhigh = -97.7793

fig, ax = plt.subplots()
fig.patch.set_facecolor('black')

lakewood_map = smopy.Map((latlow, lonlow, lathigh, lonhigh), z=17)
lakewood_map.show_mpl(ax=ax)

x, y = lakewood_map.to_pixels((latlow+lathigh)/2, (lonlow+lonhigh)/2)

plt.plot(x,y)


gps_map= BoxLayout(orientation='vertical')
gps_map.add_widget(FigureCanvasKivyAgg(plt.gcf()))

latlon_display_string = " "
mgrs_display_string = " "

gps_printout = Label(text=latlon_display_string, size_hint=(1, 0.15), font_name=quantico, font_size = font_size, valign='top')
gps_printout.bind(size=gps_printout.setter('text_size'))
gps_handle = gps_printout


############################################################
# ADD ALL BUTTONS, NEST BOXES, AND MAP TO FUNCTIONS
############################################################

btn1 = make_button('B1',B1)
btn2 = make_button('B2',B2)
btn3 = make_button('B3',B3)
btn4 = make_button('LatLon/MGRS',LatLon_MGRS)
btn_layout = BoxLayout(orientation='vertical',size_hint=(.15,1))
for button in buttons: 
    btn_layout.add_widget(button)

gps_layout = BoxLayout(orientation='vertical')
gps_layout.add_widget(gps_map)
gps_layout.add_widget(gps_printout)



class MyApp(App):
    def build(self):
        Clock.schedule_interval(update_gps, 1)
        total_layout = BoxLayout(orientation='horizontal')
        total_layout.add_widget(btn_layout)
        total_layout.add_widget(gps_layout)
        return total_layout



if __name__ == '__main__':
    MyApp().run()