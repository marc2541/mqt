from flask import Flask, render_template, request
from paho.mqtt import client as mqtt_client
import random

topic = ["python/mqtt", "objM", "Otemp", "Ohum"]
app = Flask(__name__)
broker = '172.16.10.42'
port = 1883
client_id1 = f'python-mqtt-{random.randint(0, 1000)}'

global lumet
lumet = "OFF"
global test1
test1 = "Empty"
global test2
test2= "Empty"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id1)
   # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if str(msg.topic) == "Otemp":
            global test1
            tempO = msg.payload.decode()
            test1 = tempO
        if str(msg.topic) == "Ohum":
            global test2
            humO = msg.payload.decode()
            test2 = humO
        if str(msg.topic) == "ObjM":
            global lumet
            if msg.payload.decode() == "ON":
                lumet = "ON"
            if msg.payload.decode() == "OFF":
                lumet = "OFF"
        


    for i in topic:
        client.subscribe(i, qos = 2)
    client.on_message = on_message


def runit():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", vartemp = test1, varhum = test2, varlumet = lumet)


if __name__ == "__main__":
    runit()
    try:
        app.run (host='172.16.10.42', port=8080, debug=True)
    except KeyboardInterrupt:
        print("...stopped...")