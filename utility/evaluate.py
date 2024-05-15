from fire import Fire 
import os 
from os.path import join
from ir_measures import evaluator, read_trec_run, parse_measure
from ir_measures import *
import ir_datasets as irds
import pandas as pd

def main(eval :str, run_dir : str, out_dir : str, rel : int = 1, iter=False, metric : str = None):
    parent = os.path.dirname(out_dir)
    os.makedirs(parent, exist_ok=True)
    files = [f for f in os.listdir(run_dir) if os.path.isfile(join(run_dir, f))]
    ds = irds.load(eval)
    qrels = ds.qrels_iter()
    if metric is not None: metrics = [parse_measure(metric)]
    else: metrics = [AP(rel=rel), NDCG(cutoff=10), NDCG(cutoff=5), NDCG(cutoff=1), R(rel=rel)@100, R(rel=rel)@1000, P(rel=rel, cutoff=10), RR(rel=rel), RR(rel=rel, cutoff=10)]
    evaluate = evaluator(metrics, qrels)
    df = []
    for file in files:
        if file.endswith(".gz"):
            name = file.strip('.gz')
            run = read_trec_run(join(run_dir, file))
            if iter:
                res = {}
                for elt in evaluate.iter_calc(run):
                    df.append(
                        {
                            'name' : name,
                            'query_id' : elt.query_id,
                            'metric' : str(elt.measure),
                            'value' : elt.value,
                        }
                    )
            else:
                res = evaluate.calc_aggregate(run)
                res = {str(k) : v for k, v in res.items()}
                res['name'] = name 
                df.append(res)
    
    df = pd.DataFrame.from_records(df)
    df.to_csv(out_dir, sep='\t', index=False)

    return "Success!"

if __name__ == '__main__':
    Fire(main)