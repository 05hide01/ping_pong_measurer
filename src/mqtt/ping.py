# ping.py
import argparse
import time
import os
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    # 最初の ping を送信し、開始時刻を記録
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
    client.subscribe('pong')
    userdata['start'] = time.time()
    client.publish('ping', os.urandom(userdata['size']))
    print('on_connect: subscribed to pong, sent ping')

def on_message(client, userdata, msg):
    # pong を受け取るたびに呼ばれる
    userdata['received'] += 1

    if userdata['received'] < userdata['count']:
        # 次の ping を送信
        client.publish('ping', os.urandom(userdata['size']))
    else:
        # count 回の往復が完了 → 合計時間を表示して終了
        elapsed = time.time() - userdata['start']
        print(f'Count: {userdata["count"]}, Payload size: {userdata["size"]} bytes, Total elapsed: {elapsed:.6f} sec')
        client.disconnect()
    
    print('on_message: received pong, sent ping')

def main():
    parser = argparse.ArgumentParser(
        description='Ping→Pong を count 回繰り返し、合計時間を測定 (payload はランダムな n バイト)'
    )
    parser.add_argument('--count', '-n', type=int, required=True, 
                        help='往復回数')
    parser.add_argument('--size', '-s', type=int, required=True, 
                        help='ペイロードサイズ (バイト数)')
    parser.add_argument('--host',  '-H', default='localhost',      
                        help='ブローカーのホスト名')
    parser.add_argument('--port',  '-P', type=int, default=1883,   
                        help='ブローカーのポート')
    args = parser.parse_args()

    userdata = {
        'count':    args.count,
        'size':     args.size,
        'received': 0,
        'start':    None
    }

    client = mqtt.Client()
    client.user_data_set(userdata)
    client.on_connect = on_connect
    client.on_message = on_message
    print('Before connect')

    client.connect(args.host, args.port)
    print('After connect')
    client.loop_forever()
    print('After loop_forever')

if __name__ == '__main__':
    main()


