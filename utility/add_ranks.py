from fire import Fire

def ranks(file: str, out : str=None):
    import pyterrier as pt 
    if not pt.started():
        pt.init()
    
    if out is None: out = file
    res = pt.io.read_results(file)
    res = res.sort_values(by=["qid", "score"], ascending=[True, False])
    res = pt.model.add_ranks(res)
    pt.io.write_results(res, out)

    return "Done!"

if __name__ == "__main__":
    Fire(ranks)