from flask import Flask, request

app = Flask(__name__)

from flask import Flask, request, abort

import json
from multiprocessing import Process
from server_routes import db, recogniser

# {ip:status}

camers_ips = {}


def findFace(file, status):  # returns : idOfHuman, idOfCamera
    with open('temp.png', 'wb') as f:
        f.write(file.read())
    id = recogniser.recognise('temp.png')
    if id != None:
        db.update(id, status)


# def changeStatus(file):
# 	fnd = findFace(file)
# 	return {fnd[0] : {place(fnd[1]):str(datetime.now())}}
@app.route('/register/<status>', methods=["GET"])
def register(status):
    global camers_ips
    camers_ips.update({request.remote_addr: status})
    return '', 200


@app.route('/transport', methods=["GET", 'POST'])
def transport():
    try:
        global camers_ips
        Process(target=findFace, args=(request.files["photo"], camers_ips.get(request.remote_addr))).start()
    except Exception as e:
        return str(e), 413
    else:
        return "", 200


@app.route("/getusers", methods=['GET'])
def get_users():
    users = db.get_users()
    partuser = []
    for i in users:
        partuser.append({
            'photo': i.get("photo"),
            'id': i.get("id"),
            "name": i.get("name"),
            "surname": i.get("surname"),
            "status": i.get("status")
        })
    return json.dumps(partuser), 200, {'Access-Control-Allow-Origin': '*'}


@app.route("/users/<int:id_user>")
def get_user(id_user):
    users = db.get_users()
    for l in users:
        if id_user == l.get("id"):
            return json.dumps(l), 200, {'Access-Control-Allow-Origin': '*'}
    else:
        abort(404)


@app.route("/add_user", methods=['POST'])
def add_user():
    user = {'photo': request.files['photo'],
            'surname': request.files['surname'].read().decode(),
            'name': request.files['name'].read().decode()
            }
    db.add_user(user)
    return "", 200, {'Access-Control-Allow-Origin': '*'}


@app.route("/get_cameras_ip", methods=['GET'])
def get_cm_ips():
    return json.dumps(camers_ips), 200, {'Access-Control-Allow-Origin': '*'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
