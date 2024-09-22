import sys
from cambridge.utils import response_txt

def test_path():
    print(sys.path)

def test_response_txt():
    text = response_txt('https://baidu.com')    
    assert len(text) > 0