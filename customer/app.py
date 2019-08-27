from flask import Flask
#from redis import Redis, RedisError
import os
import socket
import pandas as pd

app = Flask(__name__)

@app.route("/")
def hello():

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    #return html.format(name=os.getenv("NAME", "world"), #hostname=socket.gethostname(), visits=visits)
    #df=pd.read_csv("abc.csv")
    return "TEST"

@app.route("/api/csv/<string:a>")
def get_csv(a):
	try:
	#	#for i in category:		
		#df=pd.read_csv(filename,encoding="utf-8")
		return a
	except:
		return "ERROR"		
		


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

