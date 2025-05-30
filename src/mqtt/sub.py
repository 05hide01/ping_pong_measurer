# python 3.11

import random

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
ping_topic = "python/mqtt/ping"
pong_topic = "python/mqtt/pong"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received from `{msg.topic}` topic")
        client.publish(pong_topic, msg.payload)
        print(f"Published to `pong` topic")

    client.subscribe(ping_topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever(timeout = 30000000)


if __name__ == '__main__':
    run()
