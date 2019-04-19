from flask import Flask, Response
from flask import request
from threading import Thread
import json
from .cameras import Cameras
from .server import Server

app = Flask(__name__)


cameras = Cameras()
server = Server()


def frames(camera):
    while True:
        frame = server.get_last_frame(camera)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route("/getStream", methods=['POST'])
def video_feed():
    try:
        data = int(json.loads(request.data.decode('utf-8'))['idCam'])
        if not cameras.is_camera_exists(data):
            return Response(status=404)
        return Response(frames(data),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    except:
        return Response(status=418)


if __name__ == "__main__":
    cameras.register_callback(lambda camera, frame: server.new_frame(camera, frame))

    cameras_thread = Thread(target=cameras.start)
    cameras_thread.start()

    app.run()
