from fire import Fire
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import json
import logging 
import subprocess as sp

def execute(config_path : str):
    executions = load(open(config_path, 'r'), Loader=Loader)

    for k, cfg in executions.items():
        logging.info('\n'.join([f'EXECUTION NAME: {k}', 'ARGS:', json.dumps(cfg['args'], indent=2)]))
        cmd = ['python', '-m', cfg['script']]
        for arg, val in cfg['args'].items():
            cmd.append(f'--{arg}')
            cmd.append(str(val))
        sp.run(cmd)
    
    return f'Completed {len(executions)} executions.'

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Fire(execute)