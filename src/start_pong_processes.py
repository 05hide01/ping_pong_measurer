import argparse
import concurrent.futures
import functools
from typing import List, Iterator,Any
import logging
import zenoh
# from zenoh.session import Session

import ping
import pong
from ping import Ping
from pong import Pong

def start_pong_processes(
        num_nodes: int
        ) -> None:
    session = zenoh.open()
    print(f'pong_process_session: {session}')
    print("session opened")
    pong_iter = (pong.Pong(i, session) 
                 for i in range(num_nodes))
    print("start pong processes")
    return None

def start_pong_serving(node_id: int)-> None:
    # session を各pongノードで作成する (cf. start_pong_serving_session)
    conf = zenoh.Config()
    session = zenoh.open(config=conf)
    print(f'pong_session: {session}')   
    pong_node = Pong(node_id, session)
    pong_node.start()

def start_pong_serving_session(node_id: int, session: Any)-> None:
    pong_node = Pong(node_id, session)
    pong_node.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run pong process')
    parser.add_argument('--node', type=int, default=5, help='the number of Pong Node (default: 5)')


    args = parser.parse_args()
    node_num = args.node
    print(f"node_num: {node_num}")


    # with concurrent.futures.ProcessPoolExecutor() as executor:        
    #     results = executor.map(start_pong_serving, list(range(node_num)))
    results=[]
    for i in range(node_num):
        print(f"start pong serving: {i}")
        results.append(start_pong_serving(i))
        print(f'results: {results[i]}')
    

    