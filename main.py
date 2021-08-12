#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages

from flask import Flask, render_template, Response, request
from camera import VideoCamera
import click


pi_camera = None


@click.command()
@click.option(
    "--flip",
    is_flag=True,
    help="Whether or not to flip image."
)
@click.option(
    "--height",
    default=320,
    type=int,
    help="Height in pixels of video capture.",
)
@click.option(
    "--width",
    default=240,
    type=int,
    help="Width in pixels of video capture.",
)
@click.option(
    "--framerate",
    default=32,
    type=int,
    help="Frame rate.",
)
def init_camera(flip, height, width, framerate):
    global pi_camera
    pi_camera = VideoCamera(flip=flip, resolution=(height, width), framerate=framerate)


# App Globals (do not edit)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    init_camera()
    app.run(host='0.0.0.0', debug=False)
    


