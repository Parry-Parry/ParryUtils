from fire import Fire
import pandas as pd
import logging
import ir_datasets as irds

def sample(dataset : str, out_file : str, subset : int = 100000):
    dataset = irds.load(dataset)
    df = pd.DataFrame(dataset.docpairs_iter())
    df = df.sample(n=subset) 
    df.to_csv(out_file, sep='\t', index=False)
    return "Done!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Fire(sample)