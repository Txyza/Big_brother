from flask import Flask, request

app = Flask(__name__)

from flask import Flask, request, abort

import json
from datetime import datetime
from multiprocessing import Process
from server import db
from server.recogniser import recogniser

# {ip:status}

camers_ips = []


def findFace(file, status):  # returns : idOfHuman, idOfCamera
    id = recogniser.recognise(recogniser.get_encoding_of_image(file))
    if id != None:
        db.update(id, status)


# def changeStatus(file):
# 	fnd = findFace(file)
# 	return {fnd[0] : {place(fnd[1]):str(datetime.now())}}
@app.route('/register/<status>', methods=["GET"])
def register(status):
    camers_ips.update([{request.remote_addr: status}])


@app.route('/transport', methods=["GET", 'POST'])
def transport():
    try:
        Process(target=findFace, args=(request.files["photo"], camers_ips.get([request.remote_addr]))).start()
    except:
        return "", 413
    else:
        return "", 200


@app.route("/users", methods=['GET'])
def get_users():
    users = db.get_users()
    partuser = []


    for i in users:
        partuser.append({
            'photo':i.get("photo"),
            'id':i.get("id"),
            "name":i.get("name"),
            "surname":i.get("surname"),
            "status":i.get("status")

        })
    return json.dump((usersShort))


@app.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    users = db.get_users()
    for l in users:
        if user_id == l.get("id"):
            return json.dumps(l), 200
        else:
            abort(404)


@app.route("/add_user", methods=['POST'])
def add_user():
    if not request.json:
        return "", 400
    user = json.load(request.json)
    db.add_user(user)
    return "", 200


@app.route("/get_cameras_ip", methods=['GET'])
def get_cm_ips():
    return json.dumps(camers_ips), 200


if (__name__ == '__main__'):
    app.run()
