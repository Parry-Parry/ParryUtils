import re 
import itertools
import os
import shutil
from functools import wraps
from time import time

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

clean = lambda x : re.sub(r"[^a-zA-Z0-9¿]+", " ", x)

def refresh():
    os.system('git pull')
    os.system('pip install -e .')


def load_json(file : str):
    import json
    if file.endswith(".json"):
        return json.load(open(file, 'r'))
    elif file.endswith("jsonl"):
        return [json.loads(line) for line in open(file, 'r')]
    elif file.endswith("jsonl.gz"):
        import gzip
        return [json.loads(line) for line in gzip.open(file, 'rt')]
    elif file.endswith("json.gz"):
        import gzip
        return json.load(gzip.open(file, 'rt'))
    else:
        raise ValueError(f"Unknown file type for {file}")

def save_json(data, file : str):
    import json
    if file.endswith(".json"):
        json.dump(data, open(file, 'w'))
    elif file.endswith("jsonl"):
        with open(file, 'w') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
    elif file.endswith("jsonl.gz"):
        import gzip
        with gzip.open(file, 'wt') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
    elif file.endswith("json.gz"):
        import gzip
        json.dump(data, gzip.open(file, 'wt'))
    else:
        raise ValueError(f"Unknown file type for {file}")


def cut_prompt(output : str, input : str) -> str:
    return output[len(input):]

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def concatenate(*lists) -> list:
    return itertools.chain.from_iterable(lists)

def copy_path(path : str, root : str = '/tmp') -> str:
    base = os.path.basename(path)
    new_dir = os.path.join(root, base)
    if not os.path.isdir(new_dir):
        new_dir = shutil.copytree(path, os.path.join(root, base))
    return new_dir

def load_yaml(path : str) -> dict:
    return load(open(path), Loader=Loader)

def timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap