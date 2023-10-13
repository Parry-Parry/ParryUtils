import os 
import pandas as pd 
from fire import Fire
from os.path import join
from tqdm import tqdm
from functools import partial

def compress(dir : str, out : str, dtype : str , index_col : bool = False, header : bool = False):
    os.makedirs(out, exist_ok=True)
    files = [f for f in os.listdir(dir) if f.endswith(f'.{dtype}')]

    if dtype == 'tsv':
        sep = '\t'
        open_func = partial(pd.read_csv, sep=sep, index_col=index_col, header=header)
    elif dtype == 'csv':
        sep = ','
        open_func = partial(pd.read_csv, sep=sep, index_col=index_col, header=header)
    elif dtype == 'json':
        open_func = partial(pd.read_json, index_col=index_col, header=header, orient='records', lines=True)
    else:
        raise ValueError(f'Unknown dtype: {dtype}')

    def process_file(file):
        name = file + '.gz'
        df = open_func(join(dir, file))
        if dtype == 'json':
            df.to_json(join(out, name), index=index_col, header=header, orient='records', lines=True)
        else:
            df.to_csv(join(out, name), sep=sep, index=index_col, header=header)
        os.remove(join(dir, file))
        return 1

    for file in tqdm(files):
        process_file(file)
    os.rmdir(dir)

    return 0
    
if __name__ == '__main__':
    Fire(compress)