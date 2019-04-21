import json

from flask import Flask
from flask import Response
from flask import request
from reader import cameras, server
from multiprocessing import Queue


def StartWebServer(frames, port=5000):
    app = Flask(__name__)

    def get_stream(camera):
        while True:
            frame = server.get_last_frame(camera, frames)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    @app.route("/getStream", methods=['GET', 'POST'])
    def video_feed():
        try:
            if request.method == 'GET':
                data = int(request.args.get('camera', 0))
            else:
                data = int(json.loads(request.data.decode('utf-8'))['idCam'])
            if not cameras.is_camera_exists(data):
                return Response(status=404),{'Access-Control-Allow-Origin': '*'}
        except:
            return Response(status=418), {'Access-Control-Allow-Origin': '*'}

        return Response(get_stream(data), mimetype='multipart/x-mixed-replace; boundary=frame',headers={'Access-Control-Allow-Origin': '*'})

    @app.route("/", methods=['GET', 'POST'])
    def index():
        return Response(status=200)

    app.run("0.0.0.0", port)
