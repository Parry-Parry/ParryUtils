import pyterrier as pt
if not pt.started():
    pt.init()
from fire import Fire
import pandas as pd
import logging
import re
import ir_datasets as irds
from pyterrier_pisa import PisaIndex

clean = lambda x : re.sub(r"[^a-zA-Z0-9¿]+", " ", x)

def main(ir_dataset : str,
         index_path : str,
         out_path : str,
         num_threads : int = 8,
         budget : int = 100,
         subset : int = -1) -> str:
    
    dataset = irds.load(ir_dataset)
    queries = pd.DataFrame(dataset.queries_iter()).rename(columns={'query_id': 'qid', 'text': 'query'})
    if subset > 0: queries = queries.sample(n=subset)
    index = PisaIndex(index_path, threads=num_threads)
    bm25 = index.bm25(k1=1.2, b=0.75, num_results=budget, verbose=True)
    print(f'Running BM25 on {len(queries)} queries')

    result = bm25.transform(queries)
    pt.io.write_results(result, out_path)

    return "Done!" 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Fire(main)