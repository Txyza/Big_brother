import copy

import cv2
import os
import time


framerate = 10
offset = 5
const_time_delay = 0.2
camerasID = [0]
face_recognizer_path = 'cascades/haarcascade_frontalface_default.xml'


class Cameras:
    def __init__(self):
        self._face_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.abspath(__file__)) + '/' + face_recognizer_path)
        self._caps = [cv2.VideoCapture(i) for i in camerasID]
        self._queue = []
        self._callbacks = []

    def register_callback(self, cb):
        self._callbacks.append(cb)

    def next_face(self):
        if len(self._queue) == 0:
            return None
        buf = self._queue.pop(0)
        return buf

    def is_camera_exists(self, camera):
        return camerasID.count(camera) > 0

    def _append_faces(self, faces):
        for face in faces:
            self._queue.append(face)

    def _get_frame(self, cameraID):
        return self._caps[cameraID].read()[1]

    def _find_faces(self, frame):
        return self._face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.3, 5)

    def _crop_faces(self, frame, faces, cameraID):
        list_of_faces = []
        for (x, y, w, h) in faces:
            y1, y2, x1, x2 = self._size_crop(x, y, x + w, y + h, frame.shape[0], frame.shape[1])
            list_of_faces.append((frame[y1:y2, x1:x2], cameraID))
        return list_of_faces

    @staticmethod
    def _highlight_faces(frame, faces):
        # new_frame = copy.deepcopy(frame)
        new_frame = frame
        for (x, y, w, h) in faces:
            cv2.rectangle(new_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return new_frame

    @staticmethod
    def _size_crop(x1, y1, x2, y2, frame_w, frame_h):
        if y1 - offset >= 0:
            y1 -= offset
        if y2 + offset < frame_w:
            y2 += offset
        if x1 - offset >= 0:
            x1 -= offset
        if x2 + offset < frame_h:
            x2 += offset
        return y1, y2, x1, x2

    def start(self):
        # Framerate stuff
        last_processed_frame = 0
        last_saved_frame = 0
        frame_delay = 1.0 / framerate

        while True:
            processing_delay = len(self._queue) * const_time_delay
            processing = (time.time() - last_saved_frame) > processing_delay

            for cameraID in camerasID:
                frame = self._get_frame(cameraID)
                faces = self._find_faces(frame)
                if processing:
                    croped_faces = self._crop_faces(frame, faces, cameraID)
                    self._append_faces(croped_faces)

                frame = self._highlight_faces(frame, faces)
                frame_raw = cv2.imencode('.png', frame)[1].tostring()
                for cb in self._callbacks:
                    cb(cameraID, frame_raw)

            now = time.time()
            if processing:
                last_saved_frame = now
            if now - last_processed_frame > frame_delay:
                last_processed_frame = now
            else:
                time.sleep(frame_delay - (now - last_processed_frame))