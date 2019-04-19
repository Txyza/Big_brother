import cv2 as cv
import os
import time


framerate = 10
offset = 50
face_recognizer_path = 'cascades/haarcascade_frontalface_default.xml'


def cutFace(image, x, y, w, h):
    """Cut face rectangle from image"""
    y1, y2, x1, x2 = y, y + h, x, x + w
    if y - offset >= 0:
        y1 = y - offset
    if y + h + offset < image.shape[1]:
        y2 = y + h + offset
    if x - offset >= 0:
        x1 = x - offset
    if x + w + offset < image.shape[0]:
        x2 = x + w + offset
    return image[y1:y2, x1:x2]


def sendFrame(frame):
    """Sends frame to server to recognize"""
    # TODO: transfer
    cv.imshow("Ya nashel tebya haha", frame)
    cv.waitKey(1)
    pass


if __name__ == "__main__":
    # Get main camera
    cap = cv.VideoCapture(0)
    # Initialize face recognizer
    face_cascade = cv.CascadeClassifier(os.path.dirname(os.path.abspath(__file__)) + '/' + face_recognizer_path)

    # Framerate stuff
    start = 0
    delay = 1.0 / framerate

    while (True):
        ret, image = cap.read()
        assert ret, 'Failed to get frame from capture'

        grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grayscale, 1.3, 5)
        for (x, y, w, h) in faces:
            face = image
            cv.rectangle(face, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = cutFace(face, x, y, w, h)
            sendFrame(face)

        # Sleep 'till the next frame
        now = time.time()
        if (now - start > delay):
            start = now
        else:
            time.sleep(delay - (now - start))

    cv.destroyAllWindows()