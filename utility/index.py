import ir_datasets as irds
import pandas as pd
import os 
import shutil
from fire import Fire

def bm25(index_dir : str, k1 : float = 1.2, b : float = 0.75, threads : int = 1, pisa=True, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    if pisa:
        from pyterrier_pisa import PisaIndex
        return PisaIndex(index_dir, threads=threads, **kwargs).bm25(k1=k1, b=b)
    else:
        index = pt.IndexFactory.of(index_dir, memory=True)
        return pt.BatchRetrieve(index, wmodel="BM25", controls={"wmodel": "BM25", "k1": k1, "b": b}, **kwargs)

def bm25_text_scorer(index_dir : str, k1 : float = 1.2, b : float = 0.75, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    index = pt.IndexFactory.of(index_dir, memory=True)
    return pt.text.scorer(body_attr="text", wmodel="BM25", background_index=index)

def pt_index(index : str, meta_docno_len : int = 20, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    return pt.IterDictIndexer(index, meta={'docno': meta_docno_len, 'text': 4096}, **kwargs)

def pisa_index(index : str, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyterrier_pisa import PisaIndex
    return PisaIndex(index, text_field='text', **kwargs)

def load_dot_rerank(checkpoint : str ='sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco', batch_size : int = 64, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from transformers import AutoModel, AutoTokenizer
    from pyterrier_dr import HgfBiEncoder

    model = AutoModel.from_pretrained(checkpoint).cuda().eval()
    is_mlm = model.config.model_type == "bert" and hasattr(model.config, "mask_token_id") and model.config.mask_token_id is not None

    if is_mlm:
        print("The model is set up for Masked Language Modeling (MLM).")
    else:
        print("The model is not set up for Masked Language Modeling (MLM).")

    model.max_seq_length = 512
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    tokenizer.model_max_length = 512
    backbone = HgfBiEncoder(model, tokenizer, {}, device=model.device, batch_size=batch_size)
    return backbone

def load_dot_dense(index_path : str, checkpoint : str ='sebastian-hofstaetter/distilbert-dot-tas_b-b256-msmarco', batch_size : int = 64, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyterrier_dr import NumpyIndex

    backbone = load_dot_rerank(checkpoint, batch_size)
    index = NumpyIndex(index_path)
    return backbone >> index

def load_electra(checkpoint : str ='crystina-z/monoELECTRA_LCE_nneg31', batch_size : int = 64, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyterrier_dr import ElectraScorer
    return ElectraScorer(model_name=checkpoint, batch_size=batch_size)

def load_splade(index_path : str, checkpoint : str = 'naver/splade-cocondenser-ensembledistil', batch_size : int = 128, index : str = 'msmarco_passage', **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyt_splade import SpladeFactory
    from pyterrier_pisa import PisaIndex

    index = PisaIndex(index_path, **kwargs).quantized()
    splade = SpladeFactory(model=checkpoint)
    return splade.query_encoder(batch_size=batch_size) >> index

def load_splade_indexer(index_path : str, checkpoint : str = 'naver/splade-cocondenser-ensembledistil', batch_size : int = 128, **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyt_splade import SpladeFactory
    from pyterrier_pisa import PisaIndex

    index = PisaIndex(index_path, stemmer='none', **kwargs).toks_indexer()
    splade = SpladeFactory(model=checkpoint)    
    return splade.doc_encoder(batch_size=batch_size) >> index

def load_rankgpt(dataset : str, **model_kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyterrier_llm import RankGPT
    return pt.text.get_text(dataset, "text") >> RankGPT(**model_kwargs)

def load_rankzephyr(dataset : str, **model_kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyterrier_llm import FastChatListwise
    model_name = "castorini/rank_zephyr_7b_v1_full"
    return pt.text.get_text(dataset, "text") >> FastChatListwise(model_name, mode='sliding', **model_kwargs)

def load_lit5(dataset : str, **model_kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyterrier_llm import LiT5
    model_name = "castorini/LiT5-Distill-large"
    return pt.text.get_text(dataset, "text") >> LiT5(model_name, mode='sliding', **model_kwargs)


def index_docs(dataset : str, index_dir : str, model_name_or_path : str = None, type : str = 'dot', batch_size : int = 128, overwrite : bool = False, threads : int = 4, meta_docno_len : int = 20):
    if os.path.exists(index_dir):
        if not overwrite: return "Index already exists"
        else: shutil.rmtree(index_dir)
    
    if type == 'dot':
        index = load_dot_dense(index_dir, model_name_or_path, batch_size=batch_size)
    elif type == 'splade':
        index = load_splade_indexer(index_dir, model_name_or_path, batch_size=batch_size, threads=threads)
    elif type == 'pt':
        index = pt_index(index_dir, threads=threads, meta_docno_len=meta_docno_len)
    elif type == 'pisa':
        index = pisa_index(index_dir, threads=threads)
    else:
        raise ValueError(f"Unknown type {type}")

    dataset = irds.load(dataset)
    assert dataset.has_docs(), "Dataset does not have docs"
    docs = pd.DataFrame(dataset.docs_iter()).rename(columns={'doc_id':'docno'})[['docno', 'text']]
    index.index(docs.to_dict('records'))
    return "Done!"

if __name__ == '__main__':
    Fire(index_docs)