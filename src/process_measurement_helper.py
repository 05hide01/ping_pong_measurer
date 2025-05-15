import argparse
import concurrent.futures
import datetime
import functools
import gc
import os
import sys
from time import perf_counter_ns as timer
from typing import Any, Iterator
import logging
import zenoh
import common
import random
import string
# from zenoh.session import Session, Sample

import ping_pong_measurer_zenoh_python as pzp
from ping import Ping
from measurer import Measurer, State


# ping pong using Zenoh-python in multithread

class PingThread():
    def __init__(self, ping_max: int, session: Any, messages: list[str], measurers: list[Measurer]):
        self._ping_max = ping_max
        self._session = session
        self._messages = messages
        self._measurers = measurers
    
    def start_ping_pong(self, node_id: int):
        measurer = self._measurers[node_id]
        ping_node = Ping(node_id, self._session, measurer, self._ping_max)

        measurer.start_measurement(timer()/1e6)
        # perf_counter_ns は nano second
        # 1 millisecond = 1000,000 nanosecond
        ping_node.start(self._messages[node_id])
        measurer.stop_measurement(timer()/1e6)
        result = max(measurer._state.measure_time[-1]) - min(measurer._state.measure_time[-1])
        print(result)
        return result
def generate_random_string(n,seed=None):
    if n<=0:
        return ""
    if seed is not None:
        random.seed(seed)
    #ASCII
    character_set = string.ascii_letters + string.digits + string.punctuation

    return ''.join(random.choice(character_set) for _ in range(n))

def get_now_string() -> str:
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    now_string = now.strftime('%Y%m%d%H%M%S')
    print(f"now_string: {now_string}")
    return now_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run pong process')
    parser.add_argument('--node', type=int, default=1, help='the number of Pong Node (default: 5)')
    parser.add_argument('--mt', type=int, default=100, help='the number of Measurement (default: 100)')
    parser.add_argument('--pb', type=int, required=True, help='the number of Measurement (default: 100)')
    parser.add_argument('--pt', type=int, required=True, help='the number of Measurement (default: 100)')
    parser.add_argument('--config', type=str, default=None, help='Path to the configuration file')
    parser.add_argument('--dn', type=str, default="default_name", help='the name of device node (default: default_name)')


    # parser.add_argument('--pb', type=int, default=100, help='the payload byte of pingpong message (default: 100)')
    # parser.add_argument('--pt', type=int, default=1, help='the number of pingpong (default: 1)')

    # pb_list = [1, 10, 100, 1000, 10000, 100000, 1000000]
    # pt_list = [0, 1, 10]

    # pb_list = [1000000]
    # pt_list = [10]

    # test_list = []

    # for pb in pb_list:
    #     for pt in pt_list:
    #         # if pb*pt > 1000000:
    #         #     continue
    #         test_list.append([pb, pt])
    
    # for pb, pt in test_list:
    #     gc.collect()
        
    args = parser.parse_args()
    node_num = args.node
    measurement_times = args.mt
    payload_bytes = args.pb
    pingpong_times = args.pt
    # message = 'a' * payload_bytes
    message = generate_random_string(payload_bytes, seed=42)
    # print(f'message:{message}')
    # messages = [message for _ in range(node_num)]
    messages = [message] 
    # conf = common.get_config_from_args(args)
    conf = zenoh.Config()
    # conf.insert("","")
    #print(f'config: {conf}')
    session = zenoh.open(conf)
    print(f'session: {session}')

    
    data_folder_path = os.path.join(f"./data/",f"{args.dn}")
    file_name = f"pb{payload_bytes}_mt{measurement_times}_pt{pingpong_times}"
    print(f"data_folder_path: {data_folder_path}")
    try:
        os.makedirs(data_folder_path)
    except FileExistsError:
        pass


    measurers = [Measurer(State(node_id = i),  data_directory_path = data_folder_path, file_name = file_name) for i in range(node_num)]
    start_pp = PingThread(pingpong_times, session, messages, measurers)
    
    results = []
    for m_time in range(measurement_times):
        print(f"start measurement time: {m_time} for {payload_bytes} bytes payload and {pingpong_times} pingpong times")
        
    # ThreadPoolExecutor の場合
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     # publish ping message concurrentlypc{node_num}_
        for i in range(node_num):
            results.append(start_pp.start_ping_pong(0))
            print(f'results: {results[i]}')
    
    print("ping pong results:", results)

    pzp.stop_ping_measurer(measurers) # measurer の測定開始はThreadPoolExecutorの中で（このオーバーヘッドが大きいと予想するので）
    pzp.stop_ping_processes()
    pzp.stop_os_info_measurement()
print("finish")
os._exit(0)
