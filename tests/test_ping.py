import sys
import os

src_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

sys.path.append(src_folder_path)


from src import ping
from ping import Ping

def test_ping():
    """
    basic test for ping
    """
    