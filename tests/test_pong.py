import sys
import os

src_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

sys.path.append(src_folder_path)


from src import pong
from pong import Pong

def test_pong():
    """
    basic test for pong
    """