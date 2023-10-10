from fire import Fire
from pyyaml import load
import json
import logging 

def train(config_path : str):
    runs = load(open(config_path, 'r'))

    for k, cfg in runs.items():
        logging.info(f'RUN NAME: {k} \n ARGS:\n', json.dumps(cfg['args'], indent=2))
        cmd = ['python', '-m', cfg['script']]
        for arg, val in cfg['args'].items():
            cmd.append(f'--{arg}')
            cmd.append(str(val))
    
    return f'Completed {len(runs)} runs.'

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Fire(train)