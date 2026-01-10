from flask import Flask

APP_VERSION = "v0.0.1"

app = Flask(__name__)

@app.route('/')
def index():
    return {"body" : "Welcome to HiveBox!"}

@app.route('/version')
def version():
    return {"api" : "version", "body" : APP_VERSION}

if __name__ ==  '__main__':
      app.run(host="0.0.0.0", port=8000)