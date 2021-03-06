import socket
from datetime import datetime
from pytz import timezone
import pytz

server_now = datetime.now() # should be UTC
utc = pytz.timezone('UTC')
dt_utc = utc.localize(server_now)
eastern = timezone('America/New_York')
dt_et = dt_utc.astimezone(eastern)

# change_me: to your host and port:
HOST = '192.168.0.2'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(ADDR)
serv.listen(5)
print('listening ...')
while True:
  conn, addr = serv.accept()
  print('client connected ... ', addr)
  # if you capture images as png then change the '.jpg' ...
  # change_me: ensure complete path to images folder is correct:
  filename = '/some/folder/picamera_motion_socket/images/static/' + \
    datetime.now().strftime('%Y-%m-%dT%H.%M.%S.%f') + '.jpg'
  # or datetime stamp in EDT/EST (for example):
  # server_now = datetime.now() # should be UTC
  # utc = pytz.timezone('UTC')
  # dt_utc = utc.localize(server_now)
  # eastern = timezone('America/New_York')
  # dt_et = dt_utc.astimezone(eastern)
  # filename = '/some/folder/picamera_motion_socket_flask/run_on_some_server/images_web_app/static/' + \
  #   dt_et.strftime('%Y-%m-%dT%H.%M.%S.%f') + '.jpg'
  # create and open file for writing:
  myfile = open(filename, 'w')

  while True:
    data = conn.recv(BUFSIZE)
    if not data: break
    myfile.write(data)

  myfile.close()
  print('finished writing file: ', filename)
  conn.close()
  print('client disconnected')
  # maybe play a warning when motion detected at night, for OS X do:
  # import subprocess
  # audio_file = "/full/path/to/audio.wav"
  # return_code = subprocess.call(["afplay", audio_file])
