import face_recognition
import numpy as np

from . import db


def find_faces(analised_frame):
    users = db.get_users()
    ids = []
    user_encodings = []
    for user in users:
        ids.append(user.get('id'))
        user_encodings.append(make_encoding_from_string(user.get('encoding')))

    for face_encoding in analised_frame:
        matches = face_recognition.compare_faces(user_encodings, face_encoding)
        face_distances = face_recognition.face_distance(user_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            found_id = ids[best_match_index]
            return found_id


def get_encoding_of_image(path):
    image = face_recognition.load_image_file(path)
    encoding = face_recognition.face_encodings(image)
    if encoding:
        encoding = encoding[0]
    return encoding


def collect_encodings(f_names):
    known_encodings = tuple(get_encoding_of_image(path) for path in f_names)
    return known_encodings


def make_encoding_from_string(string):
    return np.array(list(map(float, string.split())))


def make_string_of_encoding(encoding):
    return ' '.join(map(str, list(encoding)))


def encode_image(image_path):
    return make_string_of_encoding(get_encoding_of_image(image_path))


def recognise(path):
    face_encodings = face_recognition.face_encodings(face_recognition.load_image_file(path))
    return find_faces(face_encodings)

