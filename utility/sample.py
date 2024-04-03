from fire import Fire
import logging

'''
Quick subsetting of any ir_datasets docpairs.
'''

def sample(dataset : str, out_file : str, subset : int = 100000):
    import pandas as pd
    import ir_datasets as irds
    dataset = irds.load(dataset)
    assert dataset.has_docpairs(), "Dataset must have docpairs! Make sure you're not using a test collection"
    df = pd.DataFrame(dataset.docpairs_iter())
    assert len(df) > subset, "Subset must be smaller than the dataset!"
    df = df.sample(n=subset) 
    df.to_csv(out_file, sep='\t', index=False)
    return f"Successfully took subset of {dataset} of size {subset} and saved to {out_file}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Fire(sample)