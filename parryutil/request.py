from fire import Fire
import json
from typing import Iterable, List
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import requests

### HELPER FUNCTIONS ###

def clear_line(n: int = 1) -> None:
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for _ in range(n):
        print(LINE_UP, end=LINE_CLEAR, flush=True)

def get_streaming_response(response: requests.Response) -> Iterable[List[str]]:
    for chunk in response.iter_lines(chunk_size=8192,
                                     decode_unicode=False,
                                     delimiter=b"\0"):
        if chunk:
            data = json.loads(chunk.decode("utf-8"))
            output = data["text"]
            yield output


def get_response(response: requests.Response) -> List[str]:
    data = json.loads(response.content)
    output = data["text"]
    return output

### MAIN FUNCTIONS ###

def post_http_request(prompt: str,
                      api_url: str,
                      stream: bool = False,
                      generation_kwargs : dict = {}) -> requests.Response:
    pload = {
        "prompt": prompt, "stream": stream, **generation_kwargs
    }
    response = requests.post(api_url, json=pload)
    return response

def request(api_url : str, prompt : str, params : dict, config_file : str = None):
    if config_file:
        params = load(open(config_file, 'r'), Loader=Loader)
    stream = params.pop('stream', False)
    response = post_http_request(prompt, api_url, stream, params)
    
    return get_streaming_response(response) if stream else get_response(response)

if __name__ == "__main__":
    Fire(request)