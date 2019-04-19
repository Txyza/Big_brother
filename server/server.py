from flask import Flask, request

app = Flask(__name__)
import json
from multiprocessing import Process
import server.db as db
import server.recogniser as recogniser


def findFace(file, status):
    id = recogniser.recognise(file)
    db.update(id, status)


# enctype="multipart/form-data"
@app.route('/transport', methods=["GET", 'POST'])
def transport():
    print(request.remote_addr)
    try:
        Procces(target=findFace, args=(request.files["photo"],)).start()
    except:
        return json.dumps({}), 401
    else:
        return "", 200


# @app.route('/')

if __name__ == '__main__':
    app.run()


def add(user):
    pass
