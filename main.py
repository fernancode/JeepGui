#works on desktop...
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

#matplotlib
import matplotlib.pyplot as plt

#get serial data
#import serial.tools.list_ports

# time stuff?
from datetime import datetime
import time

Window.fullscreen = 'auto'

### how to make and add buttons - needed for AC later
def Arm(instance):
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Arm"
    string = {string:'out'}
    #add_messages(string)
    #device.send_data_broadcast('arm')

def Disarm(instance):
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Disarm"
    string = {string:'out'}
    #add_messages(string)
    #device.send_data_broadcast('disarm')

def Launch(instance):
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED:      Launch"
    string = {string:'out'}
    #add_messages(string)
    #device.send_data_broadcast('relay_on')

def Ping(instance):  
    now=datetime.now()
    string = now.strftime("%H:%M:%S")+ "    DELIVERED       Ping"
    string = {string:'out'}
    #add_messages(string)
    #device.send_data_broadcast('ping')


#add buttons and name them using make button function ^^
buttons=[]
def make_button(command,func):
    btn = Button(text=command)
    btn.bind(on_press = func)
    buttons.append(btn)
    return buttons

btn1 = make_button('B1',Arm)
btn2 = make_button('B2',Disarm)
btn3 = make_button('B3',Launch)
btn4 = make_button('B4',Ping)
btn_layout = BoxLayout(orientation='vertical',size_hint=(.15,1))
for button in buttons: 
    btn_layout.add_widget(button)

plt.plot([1,2,3,4])
gps_map= BoxLayout(orientation='vertical')
gps_map.add_widget(FigureCanvasKivyAgg(plt.gcf()))

gps_string = Label(text="Lat, lon, and other stuff", size_hint=(1, .15))
gps_string.bind(size=gps_string.setter('text_size'))

gps_layout = BoxLayout(orientation='vertical')
gps_layout.add_widget(gps_map)
gps_layout.add_widget(gps_string)


class MyApp(App):
    def build(self):
        total_layout = BoxLayout(orientation='horizontal')
        total_layout.add_widget(btn_layout)
        total_layout.add_widget(gps_layout)

        return total_layout


if __name__ == '__main__':
    MyApp().run()