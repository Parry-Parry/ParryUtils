from fire import Fire
import json
import logging 
import subprocess as sp
from parryutil import load_yaml

def execute(config_path : str, default_path : str = None):
    executions = load_yaml(config_path)
    if default_path is not None: defaults = load_yaml(default_path)
    for k, cfg in executions.items():
        if default_path is not None: cfg['args'].update(defaults)  
        logging.info('\n'.join([f'EXECUTION NAME: {k}', 'ARGS:', json.dumps(cfg['args'], indent=2)]))
        cmd = ['python', '-m', cfg['script']]
        for arg, val in cfg['args'].items():
            cmd.append(f'--{arg}')
            if val is not None:
                if type(val) == list:
                    cmd.append(' '.join(val))
                    continue
                cmd.append(str(val))
        sp.run(cmd)
    
    return f'Completed {len(executions)} executions.'

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Fire(execute)