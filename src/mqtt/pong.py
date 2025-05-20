# pong.py
import argparse
import threading
import time
import asyncio
from hbmqtt.broker import Broker
import paho.mqtt.client as mqtt

def make_broker_config(host, port):
    return {
        'listeners': {
            'default': {
                'type': 'tcp',
                'bind': f'{host}:{port}'
            }
        },
        'sys_interval': 10,
        'auth': {
            'allow-anonymous': True
        },
        'topic-check': {
            'enabled': False,
        },
    }

async def broker_coro(config):
    broker = Broker(config)
    await broker.start()

def start_broker(config):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print('Starting broker...')
    loop.run_until_complete(broker_coro(config))

def on_connect(client, userdata, flags, rc):
    client.subscribe('ping')
    print('on_connect: subscribed to ping', flush=True)

def on_message(client, userdata, msg):
    client.publish('pong', msg.payload)
    print('on_message: received ping, reply pong', flush=True)

def main():
    parser = argparse.ArgumentParser(description='Pong client: start broker and reply to ping')
    parser.add_argument('--host',    '-H', default='localhost', help='Broker host (default: localhost)')
    parser.add_argument('--port',    '-P', type=int, default=1883, help='Broker port (default: 1883)')
    args = parser.parse_args()

    config = make_broker_config(args.host, args.port)
    th = threading.Thread(target=start_broker, args=(config,), daemon=True)
    th.start()

    time.sleep(1)  # ブローカー準備

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.host, args.port)
    client.loop_forever()

if __name__ == '__main__':
    main()