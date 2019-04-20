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
    try:
        result = requests.post(server_ip + '/transport', files=data)
        if result.status_code == 413:
            time.sleep(5)
        # print(result)
    except Exception as e:
        print(str(e))


def send_hello(name):
    requests.get(server_ip + '/register/' + name)


def start(faces, ip, name):
    global server_ip
    server_ip = ip

    send_hello(name)

    while True:
        send_frame_to_server(faces.get())
        time.sleep(0.2)
