# Sep 21, 2014: Picamera motion detection

***

## Hardware: total cost: $114.44 as of Sep 21, 2014

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

***

# Installation Guide

### ensure Python is installed:
```
python --version
```

### install PIP:
```
sudo apt-get install python-dev
sudo apt-get install python-setuptools
sudo apt-get install python-pip
```

## on the Raspberry Pi

### install Numpy:
```
sudo pip install numpy
```

### install Picamera:
```
sudo rpi-update
sudo apt-get install python-picamera
```

## On another server
> Maybe, on the same Raspberry Pi (RPi). This was not tested, because if you're using
this setup to "catch a thief" or whatever then having the images on the RPi isn't 
going to help as they could just smash it or take it leaving you with no images.

### install Flask:
```
sudo pip install Flask
```

### on some server, start socket server:
```
git clone https://github.com/cleesmith/picamera_motion_socket_flask.git
cd picamera_motion_socket_flask/run_on_some_server
python server.py
```

### install motion detection socket send:
```
git clone https://github.com/cleesmith/picamera_motion_socket_flask.git
cd picamera_motion_socket_flask
... test it:
cd picamera_motion_socket_flask/run_on_raspberry_pi
python detect_motion_socket_send.py
```

### trigger motion detection by moving in front of camera:
```
ls -la run_on_some_server/images_web_app/static
... should list *.jpg files
```

### again, on some server, start flask web app to view images:
```
cd picamera_motion_socket_flask/run_on_some_server/images_web_app
python all_images.py
... browse to:
http://localhost:5000/
```

***
