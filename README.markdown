# Sep 2014: Raspberry Pi
# Picamera motion detection

***

> Ok, so I bought a Raspberry Pi.  It blinks. Got it.  Now what?
I decided keeping an eye on things around the house was a useful project.
Sure, I would have rather designed and built a robot that can self-balance,
recognize faces/objects, or retrieve beers from the fridge ... but what 
good is that. Ok, you're right, fridge retrieval would be cool.

## Hardware: total cost: $114.44

### Required:
1. Raspberry Pi Model B+ (B PLUS) 512MB Computer  $39.44
http://www.amazon.com/gp/product/B00LPESRUK/ref=wms_ohs_product?ie=UTF8&psc=1

2. USA Raspberry Pi Micro USB Power Supply Charger - 5v 1500ma  $6.81
http://www.amazon.com/gp/product/B00DZLSEVI/ref=wms_ohs_product?ie=UTF8&psc=1

3. Raspberry PI 5MP Camera Board  $24.99
http://www.amazon.com/gp/product/B00E1GGE40/ref=wms_ohs_product?ie=UTF8&psc=1

### Optional:
1. Addicore Raspberry Pi Heatsink Set $5.10
http://www.amazon.com/gp/product/B00HPQGTI4/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1

2. Edimax EW-7811Un 150M 11n Wi-Fi USB Adapter  $8.70
http://www.amazon.com/gp/product/B003MTTJOY/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1

3. Raspberry Pi Camera Case  $8.99
http://www.amazon.com/gp/product/B00IJZJKK4/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1

4. Monoprice 108431 Dummy Outdoor Brick Camera  $20.41
http://www.amazon.com/gp/product/B007VDTTTM/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1

> This dummy camera has plenty of room inside, waterproof, and it is mostly metal. But 
it's best feature is a real glass plate in front, so the captured images are clear.

***

> Note: many of the above items are less expensive from other sellers, such as Adafruit.

### Optional lighting:
1. Mr. Beams MB363 Wireless LED Spotlight with Motion Sensor and Photocell  $49.99
http://www.amazon.com/gp/product/B008X099PQ/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1

> These motion sensor lights work great and they usually detect motion before the Picamera
which means you get a well lit image.

***

# Installation Guide

## (1) on the Raspberry Pi and the other server

### ensure Python is installed:
```
python --version
```

### ensure PIP is installed:
```
pip --version ... if not do:
sudo apt-get install python-dev
sudo apt-get install python-setuptools
sudo apt-get install python-pip
```

***

## (2) on the Raspberry Pi

### install Numpy:
```
sudo pip install numpy
```
> Numpy is used by picamera.array.PiMotionAnalysis to detect motion.

### install Picamera:
```
sudo rpi-update
sudo apt-get install python-picamera
```

### install motion detection with socket send:
```
git clone https://github.com/cleesmith/picamera_motion_socket_flask.git
cd picamera_motion_socket_flask
... test it:
cd run_on_raspberry_pi
nano detect_motion_socket_send.py ... ensure folder and host/port settings are correct
python detect_motion_socket_send.py
```
> It's probably best to wait until the socket server is started before starting
the above ... see below.

***

## (3) On another server
> Maybe, on the same Raspberry Pi (RPi). This was not tested, because if you're using
this setup to "catch a thief" or whatever then having the images on the RPi isn't 
going to help as they could just smash it or take it ... leaving you with no images.
Of course, this all depends on your situation.

### start socket server:
```
git clone https://github.com/cleesmith/picamera_motion_socket_flask.git
cd picamera_motion_socket_flask/run_on_some_server
nano server.py ... ensure folder and host/port settings are correct
python server.py
```

### trigger motion detection by moving in front of camera:

> doing an Irish gig works but is not required

```
ls -la run_on_some_server/images_web_app/static
... should list *.jpg files
```

### again, on some server, install/start the flask web app:
```
sudo pip install Flask
cd picamera_motion_socket_flask/run_on_some_server/images_web_app
nano all_images.py ... ensure folder and host/port settings are correct
python all_images.py
... use web browser to view images:
http://localhost:5000/
```

## (4) More about picamera on the Raspberry Pi

### after testing, you can turn off the red LED on the camera:
```
sudo nano /boot/config.txt
... add this line:
disable_camera_led=1
sudo reboot
```
> Otherwise, the red LED causes a reflection in the glass pane at night.

### start picamera in the background:

> There following are possible ways to daemonize, i.e. start a program in the background:
* via nohup with ampersand ('&')
* via an Upstart script

via nohup with ampersand ('&'):
```
cd picamera_motion_socket_flask
nohup python detect_motion_socket_send.py &
... the logger output will be in the nohup.out file in this folder
... see if it's running and what the pid is:
ps aux | grep -i python
```
> A disadvantage to using nohup is that it doesn't restart when the pi is rebooted. But
it does allow you to exit out of the terminal while it continues to run in the background.

via an Upstart script:
```
sudo apt-get install upstart
sudo reboot
sudo cp picamera_motion_socket_flask/upstart/etc/init/picamera-motion-capture.conf /etc/init/
sudo service picamera-motion-capture start ... use stop to kill it
... see if it's running and what the pid is:
ps aux | grep -i python
```
> The advantage to installing and using Upstart to daemonize programs are:
* they will start up on reboot
* they can be set to respawn, in the case of the unforeseen this will restart the program
* in common use on linux deployments

***

## Observations
* the setup is senstive enough to detect cat movements, but it's not overly sensitive,
plus you get funny cat pics as they roll around on the porch and fall off the edge but
act as though they meant to do that (crazy cats)
* at night, there needs to be ample lighting ... tested with Mr. Beams MB363
* worked well sending images to a Mac and to a remote server at DigitalOcean, but
it is not a secure setup for a remote server ... as any open port is an invitation
to exploitation
* this setup works just as well if the camera is duct taped to the inside of a clean window,
and that's cheaper too

***

## Future enhancements
* perform image sends from the pi asynchronously
* use SCP batch to send images
* allow deletion of images via web app UI
* allow different sort order of images via web app UI
* at night have server.py play a sound when a new image arrives, which could 
wake you up so you can then scream "Annie get your gun!" ... of course, the
name of your heavily armed partner may vary ... in case you're without a
partner, maybe, create a RPi robot with an attached pistol using the
fictitious Pigun module (be sure to set trigger=hair), name it Annie or Wyatt, imagine 
the fun as you try to bring the groceries inside with your pigunbot on the prowl

***

> No cats were harmed, maybe embarassed a bit, during this setup.  There is no 
implied or expressed guarantee that this setup will deter thieves or mass murderers 
should such folk approach your home.
Otherwise, enjoy :-)

***
