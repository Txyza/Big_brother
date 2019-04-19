from flask import Flask,request
app = Flask(__name__)
import json
from multiprocessing import Process
from http import asyncio

def findFace(file):
	pass

#enctype="multipart/form-data"
@app.route('/transport', methods=["GET",'POST'])
def transport():
	try:
		Procces(target = findFace,args = (request.files["photo"],)).start()
	except:
		return  json.dumps({})  , 401
	else:
   		return "", 200

if __name__ == '__main__':
	app.run()	 


