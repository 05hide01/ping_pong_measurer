import concurrent.futures
from typing import List, Iterator
import logging
import zenoh
# from zenoh.session import Session

import ping
import pong
from ping import Ping
from pong import Pong
from measurer import Measurer

def start_ping_processes(
        conf,
        num_nodes: int, 
        ping_max: int = 10
        ) -> Iterator[Ping]:
    conf = zenoh.Config()
    session = zenoh.open(conf)
    print(f'ping_session: {session}')
    ping_iter = (ping.Ping(i, session, ping_max) 
                 for i in range(num_nodes))
    return ping_iter


def start_ping_measurer() -> None:
    pass

def start_ping_pong(node_id: int, message: str) -> None:
    # TODO: ping_max を引数に取る（Pingに与える）
    # session をノードごとにつくるバージョン　(cf. start_ping_pong_session)
    session = zenoh.open()
    ping_node = Ping(node_id, session)
    ping_node.start(message)

def start_ping_pong_session(node_id: int, session, message: str) -> None:
    # TODO: ping_max を引数に取る（Pingに与える）
    # session を全ノードで共有するバージョン　(cf. start_ping_pong)
    ping_node = Ping(node_id, session)
    ping_node.start(message)

def stop_ping_measurer(measurers: list[Measurer]) -> None:

    for measurer in measurers:
        with open(f"{measurer._data_directory_path}/{measurer._file_name}.csv", mode='w') as file:
            file.write("send time[microsecond],recv time[microsecond],took time[ms]\n")
            for start_time, end_time in measurer._state.measure_time:
                file.write(f"{start_time}, {end_time}, {end_time - start_time}\n")
                # utc の行はとりあえずなしにしておく



def stop_ping_processes() -> None:
    pass

def stop_os_info_measurement() -> None:
    pass

