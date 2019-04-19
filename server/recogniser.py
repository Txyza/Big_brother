import face_recognition
import numpy as np

import server.db as db


def find_faces(analised_frame):
    users = db.get_users()
    users = tuple((user.encoding, user.id) for user in users)

    for face_encoding in analised_frame:
        matches = face_recognition.compare_faces((u[0] for u in users), face_encoding)
        face_distances = face_recognition.face_distance((u[0] for u in users), face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            found_id = users[best_match_index][1]
            return found_id


def get_encoding_of_image(path):
    image = face_recognition.load_image_file(path)
    encoding = face_recognition.face_encodings(image)[0]
    return encoding


def collect_encodings(f_names):
    known_encodings = tuple(get_encoding_of_image(path) for path in f_names)
    return known_encodings


def make_encoding_from_string(string):
    return np.ndarray(map(float, string.split()))


def make_string_of_encoding(encoding):
    return ' '.join(encoding)


def encode_image(image_path):
    return make_string_of_encoding(get_encoding_of_image(image_path))


def recognise(frame):
    face_encodings = face_recognition.face_encodings(frame)
    return find_faces(face_encodings)

