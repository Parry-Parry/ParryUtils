import ir_measures
import numpy as np
import logging

# Adapted from https://gist.github.com/stefanonardo/693d96ceb2f531fa05db530f3e21517d

'''
Adapted for ir_measures so nice and fast. 
'''

class EarlyStopping(object):
    def __init__(self, val_topics, metric, qrels, mode='min', min_delta=0, patience=10, percentage=False):
        self.mode = mode
        self.min_delta = min_delta
        self.patience = patience
        self.best = None
        self.num_bad_epochs = 0
        self.is_better = None
        self._init_is_better(mode, min_delta, percentage)

        if patience == 0:
            self.is_better = lambda a, b: True
            self.step = lambda a: False

        self.val_topics = val_topics
        self.metric = ir_measures.parse_measure(metric)
        self.evaluator = ir_measures.evaluator([self.metric], qrels)

    def step(self, metrics):
        indicator = False
        if self.best is None:
            self.best = metrics
            indicator = True
            return False, indicator

        if np.isnan(metrics):
            return True, indicator

        if self.is_better(metrics, self.best):
            self.num_bad_epochs = 0
            self.best = metrics
        else:
            self.num_bad_epochs += 1

        if self.num_bad_epochs >= self.patience:
            return True, indicator

        return False, indicator

    def _init_is_better(self, mode, min_delta, percentage):
        if mode not in {'min', 'max'}:
            raise ValueError('mode ' + mode + ' is unknown!')
        if not percentage:
            if mode == 'min':
                self.is_better = lambda a, best: a < best - min_delta
            if mode == 'max':
                self.is_better = lambda a, best: a > best + min_delta
        else:
            if mode == 'min':
                self.is_better = lambda a, best: a < best - (
                            best * min_delta / 100)
            if mode == 'max':
                self.is_better = lambda a, best: a > best + (
                            best * min_delta / 100)
    
    def compute_metric(self, ranks):

        ranks = ranks.copy().rename(columns={'qid': 'query_id', 'docno': 'doc_id'})
        ranks['score'] = ranks['score'].astype(float)
        ranks['query_id'] = ranks['query_id'].astype(str)
        ranks['doc_id'] = ranks['doc_id'].astype(str)
        value = self.evaluator.calc_aggregate(ranks)
        logging.info(value)
        return list(value.values())[0]
                
    def __call__(self, model):
        ranks = model.transform(self.val_topics)
        value = self.compute_metric(ranks)
        return self.step(value)

