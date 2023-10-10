from fire import Fire
import pandas as pd
import logging
import ir_datasets as irds

def sample(dataset : str, out_file : str, subset : int = 100000):
    dataset = irds.load(dataset)
    train = pd.DataFrame(dataset.docpairs_iter()).rename(columns={'query_id': 'qid',})
    train = train.sample(n=subset) 

    train.to_csv(out_file, sep='\t', index=False)

    return "Done!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Fire(sample)