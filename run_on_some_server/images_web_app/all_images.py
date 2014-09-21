import os
import sys
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')  
def home():
  # get the names of all files in ~/Sites/picamera_motion_socket/images/static,
  # then sort them in descending order by last modified time, then
  # generate the url for each pic, then render templates/index.html:
  path_to_watch = '/some/folder/run_on_some_server/images_web_app/static'
  pics = os.listdir(path_to_watch)
  pics.sort(key=lambda x: os.stat(os.path.join(path_to_watch, x)).st_mtime, reverse=True)
  pic_urls = []
  for pic in pics:
    try:
      pic_urls.append(url_for('static', filename=pic))
    except Exception:
      # note exception, but keep on truckin':
      print(sys.exc_info())

  return render_template("index.html", pics=pic_urls)

if __name__ == "__main__":
  app.run()

