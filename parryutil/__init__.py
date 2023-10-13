from typing import Union
from .funcs import clean, cut_prompt, batch, concatenate, copy_path
from .execute import execute
from .compress import compress
from .sample import sample

COMMANDS = {
    'compress' : compress,
    'execute' : execute,
    'sample' : sample
}

def parse_bool(arg : str) -> Union[bool, str]:
    if arg.lower() == 'true': return True
    if arg.lower() == 'false': return False
    return arg

def main(args):
    if len(args) == 1: 
        execute(args[0])
    else: 
        COMMANDS[args[0]](*map(parse_bool, args[1:]))

def main_cli():
    import sys
    main(sys.argv[1:])

__version__ = '0.0.3'