import time
import copy
import cv2
import os

size = 5
const_time_delay = 0.2
debug = False
queue = []
camerasID = [0]
caps = []
face_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.abspath(__file__)) + '/cascades/haarcascade_frontalface_default.xml')


def get_face_frame():
    buf = queue[0]
    queue.remove(queue[0])
    return buf


def append_faces(faces):
    for face in faces:
        queue.append(face)


def get_frame(cameraID):
    return caps[cameraID].read()[1]


def get_highlighted_frame(cameraID):
    frame = get_frame(cameraID)
    return highlight_faces(frame, find_faces(frame))


def find_faces(frame):
    return face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.3, 5)


def crop_faces(frame, faces):
    list_of_faces = []
    for (x, y, w, h) in faces:
        y1, y2, x1, x2 = size_crop(x, y, x + w, y + h, frame.shape[0], frame.shape[1])
        list_of_faces.append((frame[y1:y2, x1:x2], cameraID))
    return list_of_faces


def highlight_faces(frame, faces):
    new_frame = copy.deepcopy(frame)
    for (x, y, w, h) in faces:
        cv2.rectangle(new_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return new_frame


def size_crop(x1, y1, x2, y2, frame_w, frame_h):
    if y1 - size >= 0:
        y1 -= size
    if y2 + size <= frame_w:
        y2 += size
    if x1 - size >= 0:
        x1 -= size
    if x2 + size <= frame_h:
        x2 += size
    return y1, y2, x1, x2


def create_caps():
    for cameraID in camerasID:
        caps.append(cv2.VideoCapture(cameraID))


def start():
    create_caps()
    while(True):
        delay = len(queue) * const_time_delay
        time.sleep(delay)
        for cameraID in camerasID:
            frame = get_frame(cameraID)
            faces = find_faces(frame)
            croped_faces = crop_faces(frame, faces)
            append_faces(croped_faces)


if debug:
    create_caps()
    for cameraID in camerasID:
        frame = get_frame(cameraID)
        faces = find_faces(frame)
        croped_faces = crop_faces(frame, faces)
        highlighted_frame = highlight_faces(frame, faces)
        count = 0
        for face_to_save in croped_faces:
            cv2.imwrite(os.path.dirname(os.path.abspath(__file__)) + '/' + str(count) + '.png', face_to_save[0])
            count += 1
        cv2.imshow('img', highlighted_frame)
        cv2.waitKey(0)

cv2.destroyAllWindows()
