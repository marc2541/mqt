from paho.mqtt import client as mqtt_client
import random

broker = "localhost"
port = 1883
topic = ["objM", "objG"]
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global mes1
        mes1 =" "
        global mes2
        mes2 =" "

        if str(msg.topic) == "ObjM":
            mes1 = msg.payload.decode()
            print(mes1)
        
        if str(msg.topic) == "ObjM":
            mes2 = msg.payload.decode()
            print(mes2)

    for i in topic:
        client.subscribe(i, qos = 2)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()