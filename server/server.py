from flask import Flask, request, abort
import json
import server.db as db
from datetime import datetime
from multiprocessing import Process


app = Flask(__name__)

camers_ips = []

def findFace(file): #returns : idOfHuman, idOfCamera
	pass

def place(idOfCamera): #cases idofCamera <=> place
	pass

def changeStatus(file):
	fnd = findFace(file)
	return {fnd[0] : {place(fnd[1]):str(datetime.now())}}


@app.route('/transport', methods=["GET",'POST'])
def transport():
	try:
		Process(target = findFace, args = (request.files["photo"],)).start()
	except:
		return "", 413
	else:
		return "", 200


@app.route("/users", methods=['GET'])
def get_users():
	users = db.get_users()
	usersShort = {'users':[users[0], users[1], users[2], users[3]]}
	return json.dump((usersShort))

@app.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
	users = db.get_users()
	for l in users:
		if user_id == l.get("id"):
			return json.dumps(l), 200
		else: abort(404)

@app.route("/add_user", methods=['POST'])
def add_user():
	if not request.json:
		abort(400)
	user = json.load(request.json)
	db.add_user(user)
	return "", 200

@app.route("/get_cameras_ip", methods=['GET'])
def get_cm_ips():
	return json.dumps(camers_ips), 200

if(__name__ == '__main__'):
	app.run()
