from flask import Flask
import requests
from datetime import datetime, timezone
import itertools

APP_VERSION = "v0.0.2"
senseBox_list = ["5eba5fbad46fb8001b799786","5c21ff8f919bf8001adf2488","5ade1acf223bd80019a1011c"]

app = Flask(__name__)

@app.route('/')
def index() -> dict[str]:
    return {"body" : "Welcome to HiveBox!"}

@app.route('/version')
def version() -> dict[str, str]:
    return {"api" : "version", "body" : APP_VERSION}

@app.route('/temperature')
def temperature():
    temperature_list = []
    for senseBox_id in senseBox_list:
        response = requests.get("https://api.opensensemap.org/boxes/" + senseBox_id, timeout=30).json()
        temperature_list.append(list(filter(lambda x: (x["title"]=="Temperatur" or x["title"]=="temperature") and (datetime.strptime(response["sensors"][2]["lastMeasurement"]["createdAt"], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc).timestamp() > datetime.now().timestamp() - 3600),response["sensors"])))
    temperature_list = list(map(lambda x: float(x["lastMeasurement"]["value"]), list(itertools.chain.from_iterable(temperature_list))))
    return {"senseBox_ids" : senseBox_list, "type" : "avg", "measurement" : "Temperature", "value" : sum(temperature_list) / len(temperature_list)}

if __name__ ==  '__main__':
      app.run(host="0.0.0.0", port=8000)