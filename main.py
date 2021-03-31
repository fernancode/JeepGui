"""
Fernando de la Fuente
JEEPGPS Gui
"""

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
import matplotlib.pyplot as plt
import numpy as np
import smopy #map plotter library
import gpsd #gpsd library
import mgrs #mgrs library
import time

#####################################################
## set some stuff beforehand
#####################################################
Window.fullscreen = 'auto' # default to fullscreen
Window.show_cursor = False # remove mouse
font_size = 22.5 #font size
quantico = "courier-prime-sans.ttf" #set font
m = mgrs.MGRS()
mgrs_mode = False # for switching inbetween modes
#display strings for text
latlon_format_string = "\n    DecDeg\n  {date}\n   {time}\n\nLat: {latitude:.5f}\nLon: {longitude:.5f}\nAlt: {altitude:.1f} ft\nVel: {speed:.1f} mph\nDir: {direction:.1f} deg\nErr: {error:.1f} m\nSat: {satellites:.0f}"
mgrs_format_string = "\n     MGRS\n  {date}\n   {time}\n\nGZD: {GZD}\nSID: {SID}\nEWP: {EWP}\nNSP: {NSP}\nAlt: {altitude:.1f} ft\nVel: {speed:.1f} mph\nDir: {direction:.1f} deg\nErr: {error:.1f} m\nSat: {satellites:.0f}"

#initialize stuff
date = "0000-00-00"
time = "00:00:00"
GZD = "XXX"
SID = "XX"
EWP = "00000"
NSP = "00000"
latitude = 0.0
longitude = 0.0
altitude = 0.0
speed = 0.0
direction = 0.0
error = 0.0
satellites = 0.0
#startup display string
mgrs_display_string = mgrs_format_string.format(date=date, time=time, GZD=GZD, SID=SID, EWP=EWP, NSP=NSP, altitude=altitude, speed=speed, direction=direction, error=error, satellites=satellites)
latlon_display_string = latlon_format_string.format(date=date, time=time, latitude=latitude, longitude=longitude, altitude=altitude, speed=speed, direction=direction, error=error, satellites=satellites)



#####################################################
### how to make and add buttons - needed for AC later
#####################################################
buttons=[]
def make_button(command,func):
    """
    function for adding a lot of buttons
    """

    btn = Button(text=command, font_size=25)
    btn.bind(on_press = func)
    buttons.append(btn)
    return buttons

def QUIT(instance):
    App.get_running_app().stop()

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
        #gps_handle.text = latlon_display_string

    else:
        mgrs_mode = False
        #gps_handle.text = mgrs_display_string

def update_gps(instance):
    """
    Update GPS info at regular intervals
    """

    global latlon_format_string
    global mgrs_format_string
    global latlon_display_string
    global mgrs_display_string
    global map_url
    global mgrs_mode

    try:
        packet = gpsd.get_current()
    except:
        packet = 'not a packet'

    try:
        latitude, longitude = packet.position()
    except:
        latitude = 0
        longitude = 0
    
    try:
        altitude = packet.altitude()
        altitude *= 3.28084
    except: 
        altitude = 0

    try: 
        vector = packet.movement()
        speed = vector['speed']
        speed *= 2.23694
        direction = vector['track']
    except:
        speed = 0
        direction = 0

    try:
        error, errorz = packet.position_precision()
    except:
        error = 0
    try:
        satellites = packet.sats_valid
    except:
        satellites = 0
    try:
        time_object = packet.get_time(local_time=True)
        date = time_object.strftime("%Y-%m-%d")
        time = time_object.strftime("%H:%M:%S")
    except:
        date = "----------"
        time = "--------"
    try:
        map_url = packet.map_url()
    except:
        #TODO:
        map_url = "default openstreet map location"

    mgrs_string = m.toMGRS(latitude, longitude)
    GZD = mgrs_string[0:3]
    SID = mgrs_string[3:5]
    EWP = mgrs_string[5:10]
    NSP = mgrs_string[10:15]
    #format strings
    mgrs_display_string = mgrs_format_string.format(date=date, time=time, GZD=GZD, SID=SID, EWP=EWP, NSP=NSP, altitude=altitude, speed=speed, direction=direction, error=error, satellites=satellites)
    latlon_display_string = latlon_format_string.format(date=date, time=time, latitude=latitude, longitude=longitude, altitude=altitude, speed=speed, direction=direction, error=error, satellites=satellites)

    if mgrs_mode == True:
        gps_handle.text = mgrs_display_string
    else:
        gps_handle.text = latlon_display_string


##############################################################
#GPS plot stuff

latlow = 30.358
lathigh = 30.363
lonlow = -97.790
lonhigh = -97.7793

mymap = smopy.Map((latlow, lonlow, lathigh, lonhigh))
fig, ax = plt.subplots()
fig = plt.figure()
fig.set_size_inches([1,1])
fig.patch.set_facecolor('black')
ax = plt.Axes(fig, [0,0,1,1])
ax.set_axis_off()
fig.add_axes(ax) 
ax.imshow(mymap.img)



############################################################
# ADD ALL BUTTONS, NEST BOXES, AND MAP TO FUNCTIONS
############################################################

btn1 = make_button('  GPS\nMODE',LatLon_MGRS)
btn2 = make_button('B2',B2)
btn3 = make_button('B3',B3)
btn4 = make_button('QUIT',QUIT)
btn_layout = BoxLayout(orientation='vertical',size_hint=(.15,1))
for button in buttons: 
    btn_layout.add_widget(button)

gps_layout = BoxLayout(orientation='horizontal')
gps_map= BoxLayout(orientation='vertical')
gps_map.add_widget(FigureCanvasKivyAgg(plt.gcf()))
gps_printout = Label(text=latlon_display_string, size_hint=(.4, 1), font_name=quantico, font_size = font_size, valign='top')
gps_printout.bind(size=gps_printout.setter('text_size'))
gps_handle = gps_printout
gps_layout.add_widget(gps_map)
gps_layout.add_widget(gps_printout)



#############################################################
########### ACTUALLY START THE PROGRAM ######################
#############################################################

gpsd.connect()

class MyApp(App):
    def build(self):
        total_layout = BoxLayout(orientation='horizontal')
        total_layout.add_widget(btn_layout)
        total_layout.add_widget(gps_layout)

        start = time.time()
        Clock.schedule_interval(update_gps, 0.1)
        end = time.time()
        print(end-start)

        return total_layout

if __name__ == '__main__':
    MyApp().run()
