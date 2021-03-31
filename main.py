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

import numpy as np
from six import BytesIO
from six.moves.urllib.request import urlopen, Request

##real poor resolution
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
Window.show_cursor = False # remove mouse
font_size = 20 #font size
quantico = "courier-prime-sans.ttf" #set font
mgrs_mode = False # for switching inbetween modes



#####################################################
### how to make and add buttons - needed for AC later
#####################################################
buttons=[]
def make_button(command,func):
    """
    function for adding a lot of buttons
    """

    btn = Button(text=command, font_size=30)
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
        latlon_display_string = "Lat: 30.123456\nLon: -97.123456\nAlt: 500\nSats: 8\n" + b
        gps_handle.text = latlon_display_string



##############################################################
#GPS stuff

##READ SERIAL DATA, UPDATE PLOT AND POSITION IN BACKGROUND
#create the plot, add it to the boxlayout

latlow = 30.358
lathigh = 30.363
lonlow = -97.790
lonhigh = -97.7793

def deg2num(latitude, longitude, zoom, do_round=True):
    """Convert from latitude and longitude to tile numbers.
    If do_round is True, return integers. Otherwise, return floating point
    values.
    Source: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
    """
    lat_rad = np.radians(latitude)
    n = 2.0 ** zoom
    if do_round:
        f = np.floor
    else:
        f = lambda x: x
    xtile = f((longitude + 180.) / 360. * n)
    ytile = f((1.0 - np.log(np.tan(lat_rad) + (1 / np.cos(lat_rad))) / np.pi) /
              2. * n)
    if do_round:
        if isinstance(xtile, np.ndarray):
            xtile = xtile.astype(np.int32)
        else:
            xtile = int(xtile)
        if isinstance(ytile, np.ndarray):
            ytile = ytile.astype(np.int32)
        else:
            ytile = int(ytile)
    return (xtile, ytile)


mymap = smopy.Map((latlow, lonlow, lathigh, lonhigh))

fig, ax = plt.subplots()
fig = plt.figure()
fig.set_size_inches([1,1])
fig.patch.set_facecolor('black')
ax = plt.Axes(fig, [0,0,1,1])
ax.set_axis_off()
fig.add_axes(ax) 
ax.imshow(mymap.img)



gps_map= BoxLayout(orientation='vertical')
gps_map.add_widget(FigureCanvasKivyAgg(plt.gcf()))

latlon_display_string = " "
mgrs_display_string = " "

gps_printout = Label(text=latlon_display_string, size_hint=(.4, 1), font_name=quantico, font_size = font_size, valign='top')
gps_printout.bind(size=gps_printout.setter('text_size'))
gps_handle = gps_printout


############################################################
# ADD ALL BUTTONS, NEST BOXES, AND MAP TO FUNCTIONS
############################################################

btn1 = make_button('B1',B1)
btn2 = make_button('B2',B2)
btn3 = make_button('B3',B3)
btn4 = make_button('Lat/Lon \n     \n MGRS',LatLon_MGRS)
btn_layout = BoxLayout(orientation='vertical',size_hint=(.15,1))
for button in buttons: 
    btn_layout.add_widget(button)

gps_layout = BoxLayout(orientation='horizontal')
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