from multiprocessing import Process, Queue
import argparse
from reader import cameras
from reader import server
from reader import _flask


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--server", required=True, help="main server ip")
    ap.add_argument("-n", "--name", required=True, help="place where camera belong")
    args = vars(ap.parse_args())

    frames = Queue(1)
    faces = Queue()

    cameras_process = Process(target=cameras.start, args=(frames, faces,))
    sender_process = Process(target=server.start, args=(faces, args['server'], args['name'],))

    cameras_process.start()
    sender_process.start()

    flask_process = Process(target=_flask.StartWebServer, args=(frames,))
    flask_process.start()
    flask_process.join()
