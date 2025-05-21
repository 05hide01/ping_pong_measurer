# python 3.11
import argparse
import os
import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
ping_topic = "python/mqtt/ping"
pong_topic = "python/mqtt/pong"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
results = [['took time[ms]']]

def connect_mqtt():
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

def subscribe(client: mqtt_client, file_name):
    def on_message(client, userdata, msg):
        print('on_message: received pong, sent ping')
        userdata['received'] += 1
        if userdata['received'] < userdata['count']:
            print(f"Received from `{msg.topic}` topic")
            client.publish(ping_topic, msg.payload)
            print(f"Published to `pong` topic")
        else:
            # count 回の往復が完了 → 合計時間を表示して終了
            elapsed = time.time() - userdata['start']
            print(f'Count: {userdata["count"]}, Payload size: {userdata["size"]} bytes, Total elapsed: {elapsed:.6f} sec')
            client.disconnect()
            results.append([f'{elapsed:.6f}'])
            
    client.subscribe(pong_topic)
    client.on_message = on_message


def publish(client, msg):
    result = client.publish(ping_topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send to topic `{ping_topic}`")
    else:
        print(f"Failed to send message to topic {ping_topic}")


def run(pingpong_times, measurement_times, message, size, file_name):
    for i in range(measurement_times):
        userdata = {
            'count':    pingpong_times,
            'size':     size,
            'received': 0,
            'start':    time.time(),
        }
        client = connect_mqtt()
        client.user_data_set(userdata)
        subscribe(client, file_name)
        publish(client, message)
        client.loop_forever(timeout=30000000)
    with open(file_name, 'w') as f:
        for result in results:
            f.write(','.join(map(str, result)) + '\n')
    print("finish")


if __name__ == '__main__':
    dev_list = ['orin', 'rasp5', 'kakip', 'rdkx3', 'rb3g2', 'banana', 'orange']
    parser = argparse.ArgumentParser(description='Ping→Pong を count 回繰り返し、合計時間を測定 (payload はランダムな n バイト)')
    parser.add_argument('--node', type=int, default=1, help='the number of Pong Node (default: 5)')
    parser.add_argument('--mt', type=int, default=100, help='the number of Measurement (default: 100)')
    parser.add_argument('--pb', type=int, default=100, help='the number of Measurement (default: 100)')
    parser.add_argument('--pt', type=int, default=10, help='the number of Measurement (default: 10)')
    parser.add_argument('--config', type=str, default=None, help='Path to the configuration file')
    parser.add_argument('--ping_dev', type=str, required=True, choices= dev_list, help='the name of device')
    parser.add_argument('--pong_dev', type=str, required=True, choices= dev_list, help='the name of device')
    parser.add_argument('--inter_dev', type=str, required=True, choices= dev_list, help='the name of device')
    parser.add_argument('--struct', type=str, required=True, choices=['single', 'multi'], help='the type of structure')
    args = parser.parse_args()
    node_num = args.node
    measurement_times = args.mt
    payload_bytes = args.pb
    pingpong_times = args.pt
    # message = os.urandom(payload_bytes).decode('latin-1')
    message = "a"*payload_bytes
    ping_dev = args.ping_dev
    pong_dev = args.pong_dev
    inter_dev = args.inter_dev
    struct = args.struct

    protocol = "mqtt"

    dir_path = os.path.join(f"../../data/", f"{protocol}", f"{struct}", f"{ping_dev}_{inter_dev}_{pong_dev}")
    os.makedirs(dir_path, exist_ok=True)

    os.mkdir(dir_path) if not os.path.exists(dir_path) else None
    file_name = os.path.join(dir_path, f"pb{payload_bytes}_mt{measurement_times}_pt{pingpong_times}.csv")
    run(pingpong_times, measurement_times, message, payload_bytes, file_name)
