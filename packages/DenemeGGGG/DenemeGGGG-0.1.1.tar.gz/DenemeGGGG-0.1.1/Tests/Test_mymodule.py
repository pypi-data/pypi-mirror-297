import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Packages.my_module import add, greet, subtract

def test_greet():
    assert greet("Göktuğ") == "Hello, Göktuğ!"
    assert greet("John") == "Hello, John!"

def test_add():
    assert add(3, 4) == 7
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(0, 0) == 0
