import json
from multiprocessing import Lock, Condition
import requests
import time

def get_last_frame(camera, frames):
    ans = b''
    try:
        frame, curr_cam = frames.get()
        if curr_cam == camera:
            ans = frame
    finally:
        pass

    return ans


def send_frame_to_server(frame):
        data = {'photo': frame[0]}
        result = requests.post('http://192.168.1.50:8080' + '/transport', files=data)
        if result.status_code == 413:
            time.sleep(5)
        print(result)
        pass

def send_hello():
    requests.get('http://192.168.1.50:8080' + '/register/peregovorka')

def parse_faces(faces):
    while True:
        send_frame_to_server(faces.get())
        time.sleep(0.2)
