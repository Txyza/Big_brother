import cv2
import os
import time


FRAME_RATE = 10
OFFSET = 5
CONST_TIME_DELAY = 0.2
CAMERAS_ID = [0]
FACE_RECOGNIZER_PATH = 'cascades/haarcascade_frontalface_default.xml'


def is_camera_exists(camera):
    return CAMERAS_ID.count(camera) > 0


def _append_faces(faces, new_faces):
    for f in new_faces:
        faces.put(f)


def _get_frame(cap):
    return cap.read()[1]


def _find_faces(frame, face_cascade):
    return face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.3, 5)


def _crop_faces(frame, faces, cameraID):
    list_of_faces = []
    for (x, y, w, h) in faces:
        y1, y2, x1, x2 = _size_crop(x, y, x + w, y + h, frame.shape[0], frame.shape[1])
        list_of_faces.append((cv2.imencode('.png', frame[y1:y2, x1:x2])[1].tostring(), cameraID))
    return list_of_faces


def _highlight_faces(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return frame


def _size_crop(x1, y1, x2, y2, frame_w, frame_h):
    if y1 - OFFSET >= 0:
        y1 -= OFFSET
    if y2 + OFFSET < frame_w:
        y2 += OFFSET
    if x1 - OFFSET >= 0:
        x1 -= OFFSET
    if x2 + OFFSET < frame_h:
        x2 += OFFSET
    return y1, y2, x1, x2


def start(frames, faces):
    face_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.abspath(__file__)) + '/' + FACE_RECOGNIZER_PATH)
    caps = [cv2.VideoCapture(i) for i in CAMERAS_ID]

    for cap in caps:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

    # Framerate stuff
    last_processed_frame = 0
    last_saved_frame = 0
    frame_delay = 1.0 / FRAME_RATE

    while True:
        processing_delay = faces.qsize() * CONST_TIME_DELAY
        processing = (time.time() - last_saved_frame) > processing_delay

        for cameraID in CAMERAS_ID:
            frame = _get_frame(caps[cameraID])
            faces_to_add = _find_faces(frame, face_cascade)
            if processing:
                croped_faces = _crop_faces(frame, faces_to_add, cameraID)
                _append_faces(faces, croped_faces)

            frame = _highlight_faces(frame, faces_to_add)
            frame_raw = cv2.imencode('.png', frame)[1].tostring()
            if frames.full():
                frames.get()
            frames.put((frame_raw, cameraID))

        now = time.time()
        if processing:
            last_saved_frame = now
        if now - last_processed_frame > frame_delay:
            last_processed_frame = now
        else:
            time.sleep(frame_delay - (now - last_processed_frame))
