sudo apt-get update
sudo apt-get install gpsd gpsd-clients python-gps
sudo apt install python3-setuptools git-core python3-dev
sudo apt install unclutter

pip install gpsd_py3 kivy mgrs screen_brightness_control
pip install cefpython3
#add to /etc/rc.local for gps to work
#/usr/sbin/gpsd /dev/ttyS0 -F /var/run/gpsd.sock

#add to /etc/xdg/lxsession/LXDE-pi/autostart
#@bash /home/pi/gui_startup.sh
#@unclutter -idle 0.01

#add to .bashrc in /home folder or add to gui_startup.sh script later
#/usr/bin/git -C JeepGui pull