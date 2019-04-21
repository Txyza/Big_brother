from flask import Flask, request

app = Flask(__name__)
from werkzeug import abort
from flask import Flask, request
import urllib.request
import json
from multiprocessing import Process
from server_routes import db, recogniser
import os
import random
import string
from datetime import datetime
from time import sleep

# {ip:status}

camers_ips = {}
countUnknowns = 0


def check_camers():
    global camers_ips
    while True:
        for i in camers_ips.keys():
            if urllib.request.urlopen('https://' + i).getcode() != 200:
                camers_ips.pop(i, None)
        sleep(10)


Process(target=check_camers)


def findFace(file, status):
    global countUnknowns
    # returns : idOfHuman, idOfCamera
    filename = str(datetime.now()) + '.png'
    with open(filename, 'wb') as f:
        f.write(file.read())
    id = recogniser.recognise(filename)

    if id != None:
        db.update(id, status)

    os.remove(filename)


# def changeStatus(file):
# 	fnd = findFace(file)
# 	return {fnd[0] : {place(fnd[1]):str(datetime.now())}}
@app.route('/getInfo/<status>', methods=["GET"])
def getInfo(status):
    try:
        return json.dumps(db.get_info(status)), 200, {'Access-Control-Allow-Origin': '*'}
    except:
        abort(404)


@app.route('/register/<status>', methods=["GET"])
def register(status):
    global camers_ips
    if status == "@cleaner":
        status = status + "  "
    camers_ips.update({request.remote_addr: status})
    return '', 200


@app.route('/transport', methods=["GET", 'POST'])
def transport():
    try:
        global camers_ips
        Process(target=findFace, args=(request.files["photo"], camers_ips.get(request.remote_addr))).start()
    except Exception as e:
        abort(413)
    else:
        return "", 200


@app.route("/getusers/<search>",methods = ["GET"])
def get_users(search):

    if search == "0":
        name,surname = None, None
        splitted=""
    else:
        splitted = search.split()
        if len(splitted) >= 2:
            name, surname = splitted[0], splitted[1]
        else:
            name = splitted[0]
            surname = '*'
    if not name and not surname:
        users = db.get_users()
    else:
        users = db.get_find_users(name, surname)

    partuser = []
    for i in users:
        # if  (name in i.get("surname") and surname in i.get("name")) or (surname in i.get("surname") and name in i.get("name")):
        partuser.append({
            'photo': i.get("photo"),
            'id': i.get("id"),
            "name": i.get("name"),
            "surname": i.get("surname"),
            "status": i.get("status"),
            "date": i.get("date")
        })
    return json.dumps(partuser), 200, {'Access-Control-Allow-Origin': '*'}


@app.route("/users/<int:id_user>")
def get_user(id_user):
    users = db.get_user(id_user)

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


# from ip:status make {ip:ip status:status}
def getFrontCameraIps(cameraIp):
    ip = tuple(camers_ips.keys())[0]
    print(ip)
    print(cameraIp.get(ip))
    return {'ip': ip, 'status': cameraIp.get(ip)}


@app.route("/get_camers_ip", methods=['GET'])
def get_cm_ips():
    global camers_ips
    front_camers_ips = []
    for ip in camers_ips:
        front_camers_ips.append({'ip': ip, 'status': camers_ips.get(ip)})
    return json.dumps(front_camers_ips), 200, {'Access-Control-Allow-Origin': '*'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
