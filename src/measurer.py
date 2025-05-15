from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterator, List
import logging

import zenoh
# from zenoh.session import Session, Sample

@dataclass
class Measurement():
    measurement_time: datetime
    send_time: int
    recv_time: int

@dataclass
class State():
    node_id: int = 0
    ping_counts: int =  0
    start_time: int = 0 # in mili second
    measure_time: list[list[int]] = field(default_factory=list) # [[start_time, end_time], [start_time, end_time], ...]

    # measurements: Measurement = Measurement() Stateを先に定義してからMeasurerを作るように変更
    

class Measurer():
    node_id_prefix = 'ping_node'
    def __init__(self, state: State, data_directory_path: str, file_name:str) -> None:
        self._state = state
        self._data_directory_path = data_directory_path
        self._file_name = file_name
        

    def get_ping_counts(self) -> int:
        return self._state.ping_counts

    def increment_ping_counts(self) -> int:
        self._state.ping_counts += 1

    def reset_ping_counts(self) -> None:
        self._state.ping_counts = 0
    
    def start_measurement(self, start_time: int) -> None:
        self._state.start_time = start_time

    def stop_measurement(self, end_time: int) -> None:
        self._state.measure_time.append([self._state.start_time, end_time])

    def get_measurement_time(self) -> None:
        return self._state.measurements

    def terminate(self) -> None:
        pass


