import requests

def build_header() -> dict:
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

def response_byte(request_url:str) -> bytes:
    response = requests.get(request_url, headers=build_header())
    return response.content

def response_txt(request_url:str) -> str:
    response = requests.get(request_url, headers=build_header())
    return response.text