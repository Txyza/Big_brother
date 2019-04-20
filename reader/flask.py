from flask import Flask, Response
from flask import request
from reader import cameras, server
from multiprocessing import Queue


def StartWebServer(FRAMES, port = 5000):

    app = Flask(__name__)

    def frames(camera):
        while True:
            frame = server.get_last_frame(camera, FRAMES)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


    @app.route("/getStream", methods=['GET'])
    def video_feed():
        try:
            data = int(request.args.get('camera', 0))
            if not cameras.is_camera_exists(data):
                return Response(status=404)
        except:
            return Response(status=418)

        return Response(frames(data), mimetype='multipart/x-mixed-replace; boundary=frame')


    app.run("", port)
