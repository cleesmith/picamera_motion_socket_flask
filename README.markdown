# Oct 2014: Raspberry Pi
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
> Update:
> it seems the Edimax wifi adapter is not responding to the broadcast ARP request,
> i.e doing a ping after inactivity causes "**ping: sendto: Host is down**" messages.
> But the host is not down it's just napping, well, actually the edimax is napping.
>
> see: http://www.raspberrypi.org/forums/viewtopic.php?f=28&t=33369
>
> The solution:
> ```
> sudo nano /etc/modprobe.d/8192cu.conf
>     add these lines:
>     # disable power management:
>     options 8192cu rtw_power_mgnt=0
> sudo reboot
> ```

3. Raspberry Pi Camera Case  $8.99
http://www.amazon.com/gp/product/B00IJZJKK4/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1

4. Monoprice 108431 Dummy Outdoor Brick Camera  $20.41
http://www.amazon.com/gp/product/B007VDTTTM/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1

> This dummy camera has plenty of room inside, waterproof, and it is mostly metal. But 
it's best feature is a real glass plate in front, so the captured images are clear if 
kept clean.

***

> Note: many of the above items are less expensive from other sellers, such as Adafruit.

### Optional lighting:
1. Mr. Beams MB363 Wireless LED Spotlight with Motion Sensor and Photocell  $49.99
http://www.amazon.com/gp/product/B008X099PQ/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1

> These motion sensor lights work great and they usually detect motion before the Picamera
which means you get a well lit image. They do require 3 D size batteries, which makes 
them heavy like tiny boat anchors. By "well lit image" I mean within about 10-12 feet
from the camera, and anything past that distance is just dark.

***

# Installation Guide

## (1) On the Raspberry Pi and the other server

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

## (2) Just on the Raspberry Pi

### install Numpy:
```
sudo pip install numpy
```
> Numpy is used by picamera.array.PiMotionAnalysis to detect motion. Ok, the truth 
is that there really isn't any motion detection per se.  What the code does is 
explained here (see 10.5. PiMotionArray):
http://picamera.readthedocs.org/en/latest/array.html. 
If I just turn on/off the porch light this software captures an image of the porch,
and I highly doubt it can detect the motion of photons.  Instead the video "looks"
different than it did before, so it captures an image.

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
going to help as any ne'er–do–well could just smash it or take it ... leaving you with no images.

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

***

## (4) More about picamera on the Raspberry Pi

### after testing, you can turn off the red LED on the camera:
```
sudo nano /boot/config.txt
... add this line:
disable_camera_led=1
sudo reboot
```
> Otherwise, the red LED causes a reflection in the glass pane at night.

### start detect_motion_socket_send.py in the background:

> The following are possible ways to daemonize, i.e. start a program in the background:

> 1. via nohup with ampersand ('&')
> 2. via an Upstart script

#### 1. via nohup with ampersand ('&'):
```
cd picamera_motion_socket_flask
nohup python detect_motion_socket_send.py &
... the logger output will be in the nohup.out file in this folder
... see if it's running and what the pid is:
ps aux | grep -i python
```
> A disadvantage to using nohup is that it doesn't restart when the pi is rebooted. But
it does allow you to exit out of the terminal while it continues to run in the background.

#### 2. via an Upstart script:
```
sudo apt-get install upstart
sudo reboot
sudo cp picamera_motion_socket_flask/upstart/etc/init/picamera-motion-capture.conf /etc/init/
sudo service picamera-motion-capture start ... use stop to kill it
... see if it's running and what the pid is:
ps aux | grep -i python
```
> The advantages to installing and using Upstart to daemonize programs are:
* they will start up on reboot
* they can be set to respawn, in the case of the unforeseen this will restart the program
* they use a common deployment pattern as seen on many linux servers

***

## Observations
* the setup is senstive enough to detect cat movements, but it's not overly sensitive,
plus you get funny cat pics as they roll around on the porch and fall off the edge but
act as though they meant to do that (crazy cats)
* at night, there needs to be ample lighting ... tested with Mr. Beams MB363
* worked well sending images to a Mac and to a remote server at DigitalOcean, however
sending to a publically available sever is not secure ... as any open port is an invitation
to exploitation
* also, this setup works just as well if the camera is **duct taped** to the inside of a 
clean window ... plus that's less expensive

***

## Future enhancements
* perform image sends from the pi asynchronously
* use SCP batch to send images more securely, if to a remote server (non-home)
* allow deletion of images via web app UI, or auto-delete after a week
* allow different sort order of images via web app UI
* use machine learning and pattern image analysis to track/detect patterns and trends
within the captured images ... yeah right, not unless my brain becomes much larger
* attach this setup to my mailbox, so it can greet my mail carrier and snap a pic of
the mail, and if it's all junk mail I can ignore it ... or, even better, have the 
RPi flame throw the junk mail ... somehow
* at night you may want to have server.py play a sound when a new image arrives, which 
could wake you up screaming "Annie get your gun!" ... of course, the
name of your heavily armed partner may vary ... in case you're without a
partner, maybe, create a RPi robot with an attached pistol using the
soon-to-be-developed PiSlinger module (don't forget to set trigger=hair)
... imagine the fun as you try to bring the groceries indoors from your car with that 
robot on the prowl

***

> No cats were harmed during this setup, maybe embarassed a bit.  There is no 
implied or expressed guarantee that this setup will deter any ne'er–do–well;
should such folk approach your home.
Otherwise, enjoy :-)

***
