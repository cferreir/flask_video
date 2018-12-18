#!/usr/bin/env python
from importlib import import_module
import socket
import os
import sys
from flask import Flask, render_template, Response, request

# import camera driver
# if os.environ.get('CAMERA'):
#    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#    from camera import Camera

from camera_opencv import Camera  # Hard code using web cam

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/pic/<string:address>', methods= ["GET"])
def here(address=None):
    return send_from_directory(app.static_folder, 'images/123_Octavia_St.jpg', mimetype='image/jpg')

@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'POST':
            if request.form.get('up') == 'up':
                # pass
                # print("UP UP")
                return render_template('up.html')
            elif  request.form.get('down') == 'down':
                # pass # do something else
                # print("DOWN DOWN")
                return render_template('down.html')
            else:
                # pass # unknown
                return render_template('index.html')
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    my_ip = get_ip()
    sys.stderr.write(app.instance_path)
    app.run(host=my_ip, threaded=True, debug=True)
